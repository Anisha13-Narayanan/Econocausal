from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import numpy as np
import pandas as pd

from scipy.optimize import minimize
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split


# ============================================================
# OPTIONAL ML / CAUSAL LIBRARIES
# ============================================================

try:
    from econml.dml import CausalForestDML
    ECONML_AVAILABLE = True
except Exception:
    ECONML_AVAILABLE = False


try:
    from dowhy import CausalModel
    DOWHY_AVAILABLE = True
except Exception:
    DOWHY_AVAILABLE = False


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="EconoCausal API",
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# FILE UPLOAD CONFIGURATION
# ============================================================

UPLOAD_FOLDER = Path("data/uploads")
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


# ============================================================
# DEMO DATA FEATURES
# ============================================================

FEATURES = [
    "age",
    "income",
    "tenure_months",
    "past_orders",
    "avg_order_value",
    "site_visits_30d",
    "email_opens_30d"
]


# ============================================================
# DEMO DATA GENERATION
# ============================================================

def make_demo_data(n=2500, seed=42):

    rng = np.random.default_rng(seed)

    age = rng.integers(18, 70, n)

    income = np.clip(
        rng.normal(65000, 22000, n),
        18000,
        160000
    )

    tenure = rng.integers(1, 72, n)

    orders = rng.poisson(5, n)

    aov = np.clip(
        rng.normal(65, 18, n),
        15,
        180
    )

    visits = rng.poisson(8, n)

    opens = np.clip(
        rng.poisson(4, n),
        0,
        15
    )

    # Treatment assignment deliberately depends on
    # customer characteristics, creating confounding.

    logit = (
        -1.0
        + 0.000012 * (income - 60000)
        + 0.07 * visits
        - 0.018 * age
        + 0.08 * orders
    )

    p20 = 1 / (1 + np.exp(-logit))

    p20 = np.clip(
        p20,
        0.05,
        0.90
    )

    treatment = rng.binomial(
        1,
        p20
    )

    # Heterogeneous treatment effect.

    uplift = (
        0.05
        + 0.018 * (visits >= 8)
        + 0.025 * (income < 50000)
        - 0.015 * (age > 55)
    )

    baseline = (
        0.10
        + 0.015 * orders
        + 0.012 * visits
        + 0.000001 * income
        - 0.0015 * age
    )

    noise = rng.normal(
        0,
        0.04,
        n
    )

    purchase_probability = np.clip(
        baseline
        + treatment * uplift
        + noise,
        0.01,
        0.95
    )

    purchased = rng.binomial(
        1,
        purchase_probability
    )

    df = pd.DataFrame({

        "customer_id": np.arange(
            1,
            n + 1
        ),

        "age": age,

        "income": income.round(2),

        "tenure_months": tenure,

        "past_orders": orders,

        "avg_order_value": aov.round(2),

        "site_visits_30d": visits,

        "email_opens_30d": opens,

        "treatment": treatment,

        "purchased": purchased,

        "discount": treatment * 20
    })

    return df


# Create demo dataset.

DATA = make_demo_data()


# ============================================================
# REQUEST MODELS
# ============================================================

class TrainRequest(BaseModel):

    n_estimators: int = 200


class OptimizeRequest(BaseModel):

    budget: float = 5000.0

    max_discount: float = 20.0

    discount_options: list[float] = [
        0.0,
        10.0,
        20.0
    ]


class AuditRequest(BaseModel):

    n_samples: int = 1000


# ============================================================
# ITE ESTIMATION
# ============================================================

def estimate_ite(df):

    X = df[FEATURES]

    T = df["treatment"].astype(int)

    Y = df["purchased"].astype(float)


    # --------------------------------------------------------
    # EconML CausalForestDML
    # --------------------------------------------------------

    if ECONML_AVAILABLE:

        model_y = RandomForestRegressor(
            n_estimators=150,
            min_samples_leaf=8,
            random_state=42,
            n_jobs=-1
        )

        model_t = RandomForestClassifier(
            n_estimators=150,
            min_samples_leaf=8,
            random_state=42,
            n_jobs=-1
        )

        est = CausalForestDML(
            model_y=model_y,
            model_t=model_t,
            n_estimators=200,
            discrete_treatment=True,
            random_state=42,
            n_jobs=-1
        )

        est.fit(
            Y,
            T,
            X=X
        )

        ite = est.effect(X)

        return (
            np.asarray(ite),
            "EconML CausalForestDML"
        )


    # --------------------------------------------------------
    # Fallback T-Learner
    # --------------------------------------------------------

    treated = df[T == 1]

    control = df[T == 0]


    mt = RandomForestRegressor(
        n_estimators=150,
        random_state=42
    )

    mc = RandomForestRegressor(
        n_estimators=150,
        random_state=42
    )


    mt.fit(
        treated[FEATURES],
        treated["purchased"]
    )

    mc.fit(
        control[FEATURES],
        control["purchased"]
    )


    ite = (
        mt.predict(X)
        -
        mc.predict(X)
    )


    return (
        np.asarray(ite),
        "Random-forest T-learner fallback"
    )


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health():

    return {

        "status": "ok",

        "econml_available":
            ECONML_AVAILABLE,

        "dowhy_available":
            DOWHY_AVAILABLE
    }


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {

        "project": "EconoCausal",

        "status": "running",

        "version": "1.0.0"
    }


# ============================================================
# DATASET UPLOAD
# ============================================================

@app.post("/upload")
async def upload_dataset(
    file: UploadFile = File(...)
):

    # Check whether a file was selected.

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )


    # Only CSV files are accepted.

    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported."
        )


    # Create destination path.

    destination = (
        UPLOAD_FOLDER
        /
        Path(file.filename).name
    )


    # Read uploaded file.

    contents = await file.read()


    # Save file.

    with open(
        destination,
        "wb"
    ) as output:

        output.write(contents)


    return {

        "message":
            "Dataset uploaded successfully.",

        "filename":
            file.filename,

        "size_bytes":
            len(contents),

        "saved_to":
            str(destination)
    }


# ============================================================
# DEMO DATA
# ============================================================

@app.get("/demo-data")
def demo_data(
    limit: int = 100
):

    return (
        DATA
        .head(
            min(
                limit,
                len(DATA)
            )
        )
        .to_dict(
            orient="records"
        )
    )


# ============================================================
# TRAIN DML MODEL
# ============================================================

@app.post("/train")
def train(
    req: TrainRequest
):

    df = DATA.copy()


    ite, method = estimate_ite(df)


    result = df[
        [
            "customer_id",
            "income",
            "age",
            "past_orders",
            "site_visits_30d",
            "treatment",
            "discount"
        ]
    ].copy()


    result["ite"] = ite


    result["predicted_uplift_pct"] = (
        ite * 100
    ).round(3)


    result["segment"] = np.select(

        [
            result["ite"] > 0.08,

            result["ite"] > 0.03
        ],

        [
            "Persuadable",

            "Moderate responder"
        ],

        default="Low responder"
    )


    return {

        "method":
            method,

        "rows":
            len(result),

        "mean_ite":
            float(
                np.mean(ite)
            ),

        "qini_proxy":
            float(
                np.sum(
                    np.sort(ite)[::-1][
                        :max(
                            1,
                            len(ite) // 10
                        )
                    ]
                )
            ),

        "customers":
            result
            .sort_values(
                "ite",
                ascending=False
            )
            .head(500)
            .to_dict(
                orient="records"
            )
    }


# ============================================================
# BUDGET OPTIMIZATION
# ============================================================

@app.post("/optimize")
def optimize(
    req: OptimizeRequest
):

    df = DATA.copy()


    ite20, method = estimate_ite(df)


    # Approximate $10 effect as half
    # of the $20 treatment effect.

    discounts = np.array(
        req.discount_options,
        dtype=float
    )

    n = len(df)


    # Expected incremental revenue.

    revenue = (
        df["avg_order_value"]
        .to_numpy()
    )

    effect20 = np.maximum(
        ite20,
        0
    )


    effects = np.outer(
        effect20,
        discounts / 20.0
    )


    incremental_revenue = (
        effects
        *
        revenue[:, None]
    )


    incremental_cost = (
        discounts[None, :]
    )


    # --------------------------------------------------------
    # Greedy budget assignment
    # --------------------------------------------------------

    candidates = []


    for i in range(n):

        for j, d in enumerate(discounts):

            if d <= 0:
                continue


            net_gain = (
                incremental_revenue[i, j]
                -
                d
            )


            ratio = (
                net_gain / d
                if d > 0
                else -np.inf
            )


            candidates.append(
                (
                    ratio,
                    net_gain,
                    i,
                    j,
                    d
                )
            )


    candidates.sort(
        reverse=True
    )


    selected = {}

    spent = 0.0


    for (
        ratio,
        net_gain,
        i,
        j,
        d
    ) in candidates:

        if i in selected:
            continue


        if (
            spent + d
            <= req.budget
            and
            net_gain > 0
        ):

            selected[i] = (
                d,
                net_gain
            )

            spent += d


    allocation = []


    for i, (
        d,
        gain
    ) in selected.items():

        allocation.append({

            "customer_id":
                int(
                    df.iloc[i][
                        "customer_id"
                    ]
                ),

            "discount":
                float(d),

            "expected_incremental_revenue":
                float(
                    gain + d
                ),

            "expected_net_gain":
                float(gain),

            "ite_20":
                float(
                    effect20[i]
                )
        })


    allocation_df = pd.DataFrame(
        allocation
    )


    # --------------------------------------------------------
    # Optimization summary
    # --------------------------------------------------------

    if allocation_df.empty:

        summary = {

            "budget":
                req.budget,

            "spent":
                0.0,

            "expected_incremental_revenue":
                0.0,

            "expected_net_gain":
                0.0,

            "customers_targeted":
                0
        }

    else:

        summary = {

            "budget":
                req.budget,

            "spent":
                float(
                    allocation_df[
                        "discount"
                    ].sum()
                ),

            "expected_incremental_revenue":
                float(
                    allocation_df[
                        "expected_incremental_revenue"
                    ].sum()
                ),

            "expected_net_gain":
                float(
                    allocation_df[
                        "expected_net_gain"
                    ].sum()
                ),

            "customers_targeted":
                int(
                    len(allocation_df)
                )
        }


    return {

        "method":
            method,

        "summary":
            summary,

        "allocation":
            allocation[:500]
    }


# ============================================================
# DOWHY CAUSAL AUDIT
# ============================================================

@app.post("/causal-audit")
def causal_audit(
    req: AuditRequest
):

    if not DOWHY_AVAILABLE:

        return {

            "status":
                "skipped",

            "message":
                "DoWhy is not installed in the current environment."
        }


    df = (
        DATA
        .head(
            min(
                req.n_samples,
                len(DATA)
            )
        )
        .copy()
    )


    model = CausalModel(

        data=df,

        treatment="treatment",

        outcome="purchased",

        common_causes=FEATURES
    )


    identified_estimand = (
        model.identify_effect()
    )


    estimate = model.estimate_effect(

        identified_estimand,

        method_name=
            "backdoor.linear_regression"
    )


    try:

        refutation = model.refute_estimate(

            identified_estimand,

            estimate,

            method_name=
                "random_common_cause"
        )

        refutation_text = str(
            refutation
        )

    except Exception as exc:

        refutation_text = (
            f"Refutation test failed: {exc}"
        )


    return {

        "identified_estimand":
            str(
                identified_estimand
            ),

        "estimate":
            str(
                estimate
            ),

        "refutation":
            refutation_text
    }