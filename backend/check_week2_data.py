from pathlib import Path
import pandas as pd


DATA_FOLDER = Path("data")

csv_files = list(DATA_FOLDER.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        "No CSV dataset found in backend/data/"
    )

DATA_FILE = csv_files[0]

print("=" * 60)
print("ECONOCAUSAL WEEK 2 - DATA CHECK")
print("=" * 60)

print("\nDataset:")
print(DATA_FILE)

print("\nReading treatment/outcome columns...")

df = pd.read_csv(
    DATA_FILE,
    usecols=["treatment", "conversion"]
)

print("\nRows:")
print(len(df))

print("\nTreatment distribution:")
print(df["treatment"].value_counts().sort_index())

print("\nTreatment proportions:")
print(
    df["treatment"]
    .value_counts(normalize=True)
    .sort_index()
)

print("\nConversion distribution:")
print(df["conversion"].value_counts().sort_index())

print("\nConversion rate by treatment:")
print(
    df.groupby("treatment")["conversion"]
    .mean()
)

print("\nMissing values:")
print(df.isnull().sum())

print("\n" + "=" * 60)
print("WEEK 2 DATA CHECK COMPLETE")
print("=" * 60)