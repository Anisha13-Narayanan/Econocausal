from pathlib import Path
import time

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from econml.dml import CausalForestDML


# ============================================================
# CONFIGURATION
# ============================================================

DATA_FILE = Path("data/criteo-uplift-v2.1.csv")

FEATURES = [
    "f0", "f1", "f2", "f3",
    "f4", "f5", "f6", "f7",
    "f8", "f9", "f10", "f11"
]

TREATMENT = "treatment"
OUTCOME = "conversion"

# Start with a manageable development sample.
# Change to None later when scaling up.
SAMPLE_SIZE = 500_000

RANDOM_STATE = 42


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("ECONOCAUSAL WEEK 2 - DOUBLE MACHINE LEARNING")
print("=" * 70)

print("\nDataset:")
print(DATA_FILE)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_FILE}"
    )


print("\nLoading Criteo data...")

usecols = FEATURES + [
    TREATMENT,
    OUTCOME
]

start = time.time()

df = pd.read_csv(
    DATA_FILE,
    usecols=usecols
)

print(
    f"Full dataset loaded in "
    f"{time.time() - start:.2f} seconds."
)

print(f"Full rows: {len(df):,}")


# ============================================================
# SAMPLE DATA FOR DEVELOPMENT
# ============================================================

if SAMPLE_SIZE is not None and len(df) > SAMPLE_SIZE:

    print(
        f"\nSampling {SAMPLE_SIZE:,} rows "
        "for DML development..."
    )

    df = df.sample(
        n=SAMPLE_SIZE,
        random_state=RANDOM_STATE
    ).reset_index(drop=True)


print(f"DML rows: {len(df):,}")


# ============================================================
# DATA VALIDATION
# ============================================================

required_columns = (
    FEATURES
    + [TREATMENT, OUTCOME]
)

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing columns: {missing_columns}"
    )


df = df.dropna(
    subset=required_columns
).reset_index(drop=True)


# ============================================================
# DEFINE X, T, Y
# ============================================================

X = df[FEATURES].copy()

T = df[TREATMENT].astype(int)

Y = df[OUTCOME].astype(float)


print("\nTreatment distribution:")
print(T.value_counts())

print("\nTreatment proportions:")
print(
    T.value_counts(
        normalize=True
    )
)

print("\nOutcome distribution:")
print(Y.value_counts())


# ============================================================
# BASE MODELS
# ============================================================

print("\nCreating nuisance models...")

model_y = RandomForestRegressor(
    n_estimators=100,
    min_samples_leaf=20,
    max_features="sqrt",
    random_state=RANDOM_STATE,
    n_jobs=-1
)

model_t = RandomForestClassifier(
    n_estimators=100,
    min_samples_leaf=20,
    max_features="sqrt",
    random_state=RANDOM_STATE,
    n_jobs=-1
)


# ============================================================
# CAUSAL FOREST DML
# ============================================================

print("\nCreating CausalForestDML...")

estimator = CausalForestDML(
    model_y=model_y,
    model_t=model_t,

    n_estimators=200,

    discrete_treatment=True,

    min_samples_leaf=20,

    max_samples=0.5,

    random_state=RANDOM_STATE,

    n_jobs=-1
)


# ============================================================
# FIT MODEL
# ============================================================

print("\nTraining DML model...")
print("This may take some time.")

start = time.time()

estimator.fit(
    Y,
    T,
    X=X
)

training_time = time.time() - start

print(
    f"\nTraining completed in "
    f"{training_time:.2f} seconds."
)


# ============================================================
# ESTIMATE INDIVIDUAL TREATMENT EFFECT
# ============================================================

print("\nEstimating ITE...")

start = time.time()

ite = estimator.effect(X)

ite = np.asarray(ite)

print(
    f"ITE estimation completed in "
    f"{time.time() - start:.2f} seconds."
)


# ============================================================
# CREATE RESULT TABLE
# ============================================================

results = df.copy()

results["ite"] = ite

results["ite_percentage_points"] = (
    ite * 100
)


# ============================================================
# UPLIFT SEGMENTS
# ============================================================

results["segment"] = np.select(

    [
        results["ite"] >= 0.01,
        results["ite"] >= 0.005,
        results["ite"] >= 0
    ],

    [
        "High positive uplift",
        "Moderate positive uplift",
        "Low positive uplift"
    ],

    default="Negative uplift"
)


# ============================================================
# ITE SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("ITE SUMMARY")
print("=" * 70)

print(
    f"\nMean ITE: "
    f"{np.mean(ite):.6f}"
)

print(
    f"Median ITE: "
    f"{np.median(ite):.6f}"
)

print(
    f"Minimum ITE: "
    f"{np.min(ite):.6f}"
)

print(
    f"Maximum ITE: "
    f"{np.max(ite):.6f}"
)

print(
    f"Standard deviation: "
    f"{np.std(ite):.6f}"
)


# ============================================================
# TOP UPLIFT CUSTOMERS
# ============================================================

print("\nTop 20 estimated uplift observations:")

top_results = (
    results
    .sort_values(
        "ite",
        ascending=False
    )
    .head(20)
)

print(
    top_results[
        FEATURES
        + [
            TREATMENT,
            OUTCOME,
            "ite",
            "ite_percentage_points",
            "segment"
        ]
    ].to_string(
        index=False
    )
)


# ============================================================
# SEGMENT SUMMARY
# ============================================================

print("\nUplift segments:")

print(
    results["segment"]
    .value_counts()
)


# ============================================================
# SAVE RESULTS
# ============================================================

output_folder = Path(
    "data/week2"
)

output_folder.mkdir(
    parents=True,
    exist_ok=True
)


output_file = (
    output_folder
    / "criteo_ite_results.csv"
)

results.to_csv(
    output_file,
    index=False
)


# ============================================================
# SAVE MODEL
# ============================================================

import joblib

model_file = (
    output_folder
    / "causal_forest_dml.joblib"
)

joblib.dump(
    estimator,
    model_file
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("WEEK 2 TASK 1 COMPLETE")
print("=" * 70)

print(
    f"\nModel: CausalForestDML"
)

print(
    f"Base models: Random Forest"
)

print(
    f"Training rows: {len(df):,}"
)

print(
    f"Mean ITE: {np.mean(ite):.6f}"
)

print(
    f"\nITE results saved to:"
)

print(output_file)

print(
    f"\nModel saved to:"
)

print(model_file)