import json
import re
import time
from pathlib import Path

import pandas as pd
from dowhy import CausalModel


# ============================================================
# EconoCausal - Mid-Project Causal Refutation Audit
# ============================================================

DATA_FILE = Path("data/criteo-uplift-v2.1.csv")
OUTPUT_DIR = Path("data/mid_review")

TREATMENT = "treatment"
OUTCOME = "conversion"

COVARIATES = [
    "f0",
    "f1",
    "f2",
    "f3",
    "f4",
    "f5",
    "f6",
    "f7",
    "f8",
    "f9",
    "f10",
    "f11",
]

# Keep the refutation audit computationally manageable.
SAMPLE_SIZE = 100_000
RANDOM_STATE = 42


def load_data():
    print("=" * 70)
    print("Loading Criteo dataset")
    print("=" * 70)

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_FILE.resolve()}"
        )

    columns = COVARIATES + [TREATMENT, OUTCOME]

    df = pd.read_csv(
        DATA_FILE,
        usecols=columns
    )

    print(f"Full dataset rows: {len(df):,}")

    if len(df) > SAMPLE_SIZE:
        df = df.sample(
            n=SAMPLE_SIZE,
            random_state=RANDOM_STATE
        )

    df = df.dropna().reset_index(drop=True)

    print(f"Audit sample rows: {len(df):,}")
    print(f"Treatment column: {TREATMENT}")
    print(f"Outcome column: {OUTCOME}")
    print(f"Covariates: {COVARIATES}")

    return df


def parse_refutation_result(refutation, estimated_effect):
    """
    Extract the numerical values printed by DoWhy's refutation result.

    Expected format:

    Estimated effect:<value>
    New effect:<value>
    p value:<value>
    """

    text = str(refutation)

    estimated_match = re.search(
        r"Estimated effect:\s*([-+0-9.eE]+)",
        text
    )

    new_effect_match = re.search(
        r"New effect:\s*([-+0-9.eE]+)",
        text
    )

    p_value_match = re.search(
        r"p value:\s*([-+0-9.eE]+)",
        text
    )

    parsed_estimated_effect = (
        float(estimated_match.group(1))
        if estimated_match
        else float(estimated_effect)
    )

    parsed_new_effect = (
        float(new_effect_match.group(1))
        if new_effect_match
        else None
    )

    parsed_p_value = (
        float(p_value_match.group(1))
        if p_value_match
        else None
    )

    return {
        "estimated_effect": parsed_estimated_effect,
        "new_effect": parsed_new_effect,
        "p_value": parsed_p_value,
        "result": text,
    }


def run_refutation():
    df = load_data()

    print()
    print("=" * 70)
    print("Building DoWhy causal model")
    print("=" * 70)

    model = CausalModel(
        data=df,
        treatment=TREATMENT,
        outcome=OUTCOME,
        common_causes=COVARIATES,
    )

    identified_estimand = model.identify_effect(
        proceed_when_unidentifiable=True
    )

    print("\nIdentified estimand:")
    print(identified_estimand)

    print()
    print("=" * 70)
    print("Estimating causal effect")
    print("=" * 70)

    start_time = time.time()

    estimate = model.estimate_effect(
        identified_estimand,
        method_name="backdoor.linear_regression",
        test_significance=True,
    )

    estimation_time = time.time() - start_time

    estimated_ate = float(estimate.value)

    print(f"\nEstimated ATE: {estimated_ate}")
    print(f"Estimation time: {estimation_time:.2f} seconds")

    results = {
        "dataset": str(DATA_FILE),
        "sample_size": int(len(df)),
        "treatment": TREATMENT,
        "outcome": OUTCOME,
        "covariates": COVARIATES,
        "estimated_ate": estimated_ate,
        "estimation_time_seconds": round(estimation_time, 2),
        "refutation_tests": {},
    }

    # ========================================================
    # 1. Random Common Cause Refuter
    # ========================================================

    print()
    print("=" * 70)
    print("REFUTATION 1: Random Common Cause")
    print("=" * 70)

    start_time = time.time()

    random_common_cause = model.refute_estimate(
        identified_estimand,
        estimate,
        method_name="random_common_cause",
        random_state=RANDOM_STATE,
    )

    elapsed = time.time() - start_time

    print(random_common_cause)
    print(f"\nRuntime: {elapsed:.2f} seconds")

    random_result = parse_refutation_result(
        random_common_cause,
        estimated_ate
    )

    random_result["runtime_seconds"] = round(elapsed, 2)

    results["refutation_tests"]["random_common_cause"] = random_result

    # ========================================================
    # 2. Placebo Treatment Refuter
    # ========================================================

    print()
    print("=" * 70)
    print("REFUTATION 2: Placebo Treatment")
    print("=" * 70)

    start_time = time.time()

    placebo_refuter = model.refute_estimate(
        identified_estimand,
        estimate,
        method_name="placebo_treatment_refuter",
        placebo_type="permute",
        random_state=RANDOM_STATE,
    )

    elapsed = time.time() - start_time

    print(placebo_refuter)
    print(f"\nRuntime: {elapsed:.2f} seconds")

    placebo_result = parse_refutation_result(
        placebo_refuter,
        estimated_ate
    )

    placebo_result["runtime_seconds"] = round(elapsed, 2)

    results["refutation_tests"]["placebo_treatment"] = placebo_result

    # ========================================================
    # 3. Data Subset Refuter
    # ========================================================

    print()
    print("=" * 70)
    print("REFUTATION 3: Data Subset")
    print("=" * 70)

    start_time = time.time()

    subset_refuter = model.refute_estimate(
        identified_estimand,
        estimate,
        method_name="data_subset_refuter",
        subset_fraction=0.8,
        random_state=RANDOM_STATE,
    )

    elapsed = time.time() - start_time

    print(subset_refuter)
    print(f"\nRuntime: {elapsed:.2f} seconds")

    subset_result = parse_refutation_result(
        subset_refuter,
        estimated_ate
    )

    subset_result["runtime_seconds"] = round(elapsed, 2)

    results["refutation_tests"]["data_subset"] = subset_result

    # ========================================================
    # Save results
    # ========================================================

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / "causal_refutation_results.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print()
    print("=" * 70)
    print("CAUSAL AUDIT COMPLETE")
    print("=" * 70)

    print("Results saved to:")
    print(output_file.resolve())


if __name__ == "__main__":
    run_refutation()