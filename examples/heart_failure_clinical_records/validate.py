import pandas as pd

from contract import heart_failure_contract
from timeseries_validator.validator import validate

heart_failure_dataset = pd.read_csv("heart_failure_clinical_records_dataset.csv", sep=",")

issues = validate(heart_failure_dataset, heart_failure_contract)
for issue in issues:
    print(issue.message)