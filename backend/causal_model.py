from pathlib import Path
import pandas as pd
from dowhy import CausalModel

# --------------------------------------------------
# Load real Criteo CSV
# --------------------------------------------------

DATA_FOLDER = Path("data")
csv_files = list(DATA_FOLDER.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        "Put your Criteo CSV inside backend/data/"
    )

DATA_FILE = csv_files[0]

df = pd.read_csv(DATA_FILE)

print("Dataset:", DATA_FILE.name)
print("Rows:", len(df))


# --------------------------------------------------
# Causal variables
# --------------------------------------------------

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
    "f11"
]


# --------------------------------------------------
# Validate dataset
# --------------------------------------------------

required_columns = COVARIATES + [
    TREATMENT,
    OUTCOME
]

missing = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing:
    raise ValueError(
        f"Missing columns: {missing}"
    )


# --------------------------------------------------
# Build causal DAG
# --------------------------------------------------

edges = []

for feature in COVARIATES:

    edges.append(
        f"{feature} -> {TREATMENT}"
    )

    edges.append(
        f"{feature} -> {OUTCOME}"
    )


edges.append(
    f"{TREATMENT} -> {OUTCOME}"
)


graph = """
digraph {
    %s
}
""" % "; ".join(edges)


# --------------------------------------------------
# Create DoWhy model
# --------------------------------------------------

model = CausalModel(
    data=df,
    treatment=TREATMENT,
    outcome=OUTCOME,
    graph=graph
)


# --------------------------------------------------
# Display information
# --------------------------------------------------

print("\n==============================")
print("ECONOCAUSAL WEEK 1")
print("==============================")

print("\nTreatment:")
print(TREATMENT)

print("\nOutcome:")
print(OUTCOME)

print("\nCovariates:")
print(COVARIATES)


# --------------------------------------------------
# Identify causal effect
# --------------------------------------------------

print("\nIdentifying causal effect...")

identified_estimand = model.identify_effect()

print("\n==============================")
print("IDENTIFIED ESTIMAND")
print("==============================")

print(identified_estimand)


# --------------------------------------------------
# Save DAG
# --------------------------------------------------

try:

    model.view_model(
        layout="dot",
        file_name="data/week1_causal_dag.png"
    )

    print(
        "\nDAG saved to:"
        " data/week1_causal_dag.png"
    )

except Exception as error:

    print(
        "\nDAG image could not be generated:"
    )

    print(error)


print("\nWEEK 1 CAUSAL MODEL COMPLETE")