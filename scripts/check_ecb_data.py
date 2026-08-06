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

empty_columns_mask = df.isna().all()
print("\nEmpty columns:\n", empty_columns_mask[empty_columns_mask].index.tolist())

duplicate_time_period = df["TIME_PERIOD"].duplicated()
print("\nNumber of duplicated dates: ", duplicate_time_period.sum())
print("TIME_PERIOD contain duplicates: ", duplicate_time_period.any())

converted_time_period = pd.to_datetime(df["TIME_PERIOD"], errors="coerce")
print("\nInvalid TIME_PERIOD values after conversion: ", converted_time_period.isna().sum())
print("TIME_PERIOD is in chronological order: ", converted_time_period.is_monotonic_increasing)

print("\nThe earliest date: ", converted_time_period.min())
print("The latest date: ", converted_time_period.max())

print("\nThe minimum OBS_VALUE: ", df["OBS_VALUE"].min())
print("The maximum OBS_VALUE: ", df["OBS_VALUE"].max())

print("\nNumber of unique FREQ values: ", df["FREQ"].nunique())
print("FREQ values: ", df["FREQ"].unique())
print("Number of unique CURRENCY values: ", df["CURRENCY"].nunique())
print("CURRENCY values: ", df["CURRENCY"].unique())
print("Number of unique CURRENCY_DENOM values: ", df["CURRENCY_DENOM"].nunique())
print("CURRENCY_DENOM values: ", df["CURRENCY_DENOM"].unique())

print("\nMissing values in critical columns:\n", df[["TIME_PERIOD","OBS_VALUE","CURRENCY","CURRENCY_DENOM","FREQ"]].isna().sum())