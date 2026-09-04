import pandas as pd
from pathlib import Path

from contract import ecb_contract
from tabular_data_validator import validate

project_root = Path(__file__).resolve().parent.parent.parent
csv_path = project_root / "data" / "raw" / "data.csv"
ecb_dataset = pd.read_csv(csv_path, sep=",")

issues = validate(ecb_dataset, ecb_contract)
for issue in issues:
    print(issue.message)