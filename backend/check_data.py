from pathlib import Path
import pandas as pd

data_folder = Path("data")

csv_files = list(data_folder.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError("No CSV found in backend/data")

file = csv_files[0]

print("Dataset:", file.name)

df = pd.read_csv(file)

print("\nRows:", len(df))
print("Columns:", len(df.columns))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nTreatment distribution:")
print(df["treatment"].value_counts())

print("\nConversion distribution:")
print(df["conversion"].value_counts())