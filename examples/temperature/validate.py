import pandas as pd

from contract import temperature_contract
from tabular_data_validator import validate

# Load the dataset from a CSV file.
temperature_dataset = pd.read_csv("temperature.csv", sep=";", decimal=",")

# CSV files do not preserve Python/pandas data types.
# The timestamp column is loaded as text, so it needs to be converted
# to datetime before date-related validation, such as sort order checks.
temperature_dataset["timestamp"] = pd.to_datetime(
    temperature_dataset["timestamp"],
    dayfirst=True
)

# Validate the prepared dataset against the rules defined in temperature_contract.
# * The validator does not modify the dataset.
# * It only checks the data and returns all detected validation issues.
issues = validate(temperature_dataset, temperature_contract)

# Display all validation issues found in the dataset.
if not issues:
    print("No validation issues found.")
else:
    for issue in issues:
        print(issue.message)