from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# ECONOCAUSAL - WEEK 2 TASK 2
# UPLIFT CURVE + QINI ANALYSIS
# ============================================================

DATA_FILE = Path("data/week2/criteo_ite_results.csv")
OUTPUT_DIR = Path("data/week2")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 1. Load ITE results
# ------------------------------------------------------------

print("=" * 60)
print("ECONOCAUSAL WEEK 2 - UPLIFT / QINI ANALYSIS")
print("=" * 60)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"ITE results not found: {DATA_FILE}\n"
        "Run dml_model.py first."
    )

print(f"\nLoading:\n{DATA_FILE}")

df = pd.read_csv(DATA_FILE)

print(f"Rows loaded: {len(df):,}")
print(f"Columns: {list(df.columns)}")


# ------------------------------------------------------------
# 2. Validate required columns
# ------------------------------------------------------------

required_columns = [
    "treatment",
    "conversion",
    "ite",
]

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )


# ------------------------------------------------------------
# 3. Clean data
# ------------------------------------------------------------

df = df[
    required_columns
].dropna()

df["treatment"] = df["treatment"].astype(int)
df["conversion"] = df["conversion"].astype(int)
df["ite"] = df["ite"].astype(float)


# ------------------------------------------------------------
# 4. Estimate treatment probability
# ------------------------------------------------------------

treatment_probability = df["treatment"].mean()
control_probability = 1.0 - treatment_probability

print("\nTreatment probability:")
print(f"  Treatment: {treatment_probability:.6f}")
print(f"  Control:   {control_probability:.6f}")

if treatment_probability <= 0 or control_probability <= 0:
    raise ValueError(
        "Both treatment and control groups must contain observations."
    )


# ------------------------------------------------------------
# 5. Rank customers by predicted ITE
# ------------------------------------------------------------

df = df.sort_values(
    "ite",
    ascending=False
).reset_index(drop=True)

df["rank"] = np.arange(1, len(df) + 1)

df["population_fraction"] = (
    df["rank"] / len(df)
)


# ------------------------------------------------------------
# 6. Calculate inverse-propensity weighted outcomes
# ------------------------------------------------------------

# Contribution from treated observations
df["treated_contribution"] = np.where(
    df["treatment"] == 1,
    df["conversion"] / treatment_probability,
    0.0,
)

# Contribution from control observations
df["control_contribution"] = np.where(
    df["treatment"] == 0,
    df["conversion"] / control_probability,
    0.0,
)


# ------------------------------------------------------------
# 7. Calculate cumulative incremental conversions
# ------------------------------------------------------------

df["cumulative_treated"] = (
    df["treated_contribution"].cumsum()
)

df["cumulative_control"] = (
    df["control_contribution"].cumsum()
)

df["cumulative_uplift"] = (
    df["cumulative_treated"]
    - df["cumulative_control"]
)


# ------------------------------------------------------------
# 8. Create Uplift Curve
# ------------------------------------------------------------

uplift_curve_file = (
    OUTPUT_DIR / "uplift_curve.png"
)

plt.figure(figsize=(10, 6))

plt.plot(
    df["population_fraction"],
    df["cumulative_uplift"],
    label="DML Predicted Uplift Ranking",
)

plt.axhline(
    y=0,
    linestyle="--",
    label="Zero Incremental Gain",
)

plt.xlabel("Fraction of Customers Targeted")
plt.ylabel("Cumulative Incremental Conversions")
plt.title("EconoCausal - Uplift Curve")

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    uplift_curve_file,
    dpi=150,
)

plt.close()


# ------------------------------------------------------------
# 9. Calculate Qini curve
# ------------------------------------------------------------

# Qini curve is represented here by cumulative incremental
# conversions obtained by targeting customers in descending
# predicted-ITE order.

qini_curve = df["cumulative_uplift"].to_numpy()

x = df["population_fraction"].to_numpy()


# ------------------------------------------------------------
# 10. Random targeting baseline
# ------------------------------------------------------------

final_uplift = qini_curve[-1]

random_baseline = (
    x * final_uplift
)


# ------------------------------------------------------------
# 11. Qini coefficient
# ------------------------------------------------------------

qini_coefficient = np.trapezoid(
    qini_curve - random_baseline,
    x,
)


# ------------------------------------------------------------
# 12. Save Qini Curve
# ------------------------------------------------------------

qini_curve_file = (
    OUTPUT_DIR / "qini_curve.png"
)

plt.figure(figsize=(10, 6))

plt.plot(
    x,
    qini_curve,
    label="DML Qini Curve",
)

plt.plot(
    x,
    random_baseline,
    linestyle="--",
    label="Random Targeting Baseline",
)

plt.xlabel("Fraction of Customers Targeted")
plt.ylabel("Cumulative Incremental Conversions")
plt.title("EconoCausal - Qini Curve")

plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    qini_curve_file,
    dpi=150,
)

plt.close()


# ------------------------------------------------------------
# 13. Identify best targeting fraction
# ------------------------------------------------------------

best_index = int(
    np.argmax(qini_curve)
)

best_target_fraction = (
    x[best_index]
)

best_cumulative_uplift = (
    qini_curve[best_index]
)


# ------------------------------------------------------------
# 14. Print results
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("UPLIFT / QINI RESULTS")
print("=" * 60)

print(
    f"\nMean predicted ITE: "
    f"{df['ite'].mean():.6f}"
)

print(
    f"Median predicted ITE: "
    f"{df['ite'].median():.6f}"
)

print(
    f"Maximum predicted ITE: "
    f"{df['ite'].max():.6f}"
)

print(
    f"Minimum predicted ITE: "
    f"{df['ite'].min():.6f}"
)

print(
    f"\nQini coefficient: "
    f"{qini_coefficient:.6f}"
)

print(
    f"Best targeting fraction: "
    f"{best_target_fraction:.2%}"
)

print(
    f"Cumulative uplift at best point: "
    f"{best_cumulative_uplift:.2f}"
)

print("\nGenerated files:")

print(
    f"  {uplift_curve_file}"
)

print(
    f"  {qini_curve_file}"
)

print("\n" + "=" * 60)
print("WEEK 2 TASK 2 COMPLETE")
print("=" * 60)