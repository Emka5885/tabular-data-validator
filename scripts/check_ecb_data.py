import pandas as pd
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
csv_path = project_root / "data" / "raw" / "data.csv"
df = pd.read_csv(csv_path, sep=",")

print("Number of rows: ", len(df))
print("Number of columns: ", len(df.columns))
print("\nColumns: ", df.columns.tolist())
print("\nFirst 5 rows:\n", df.head(5))
print("\nColumns data types:\n", df.dtypes)

missing_values = df.isna().sum()
missing_values = missing_values[missing_values > 0]
print("\nColumns containing missing values:\n", missing_values)