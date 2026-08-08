import pandas as pd
from .issues import ValidationIssue, ValidationCode, Severity

def validate_empty_dataset(data: pd.DataFrame) -> list[ValidationIssue]:
    if data.empty:
        return [ValidationIssue(ValidationCode.EMPTY_DATASET, Severity.ERROR, "Dataset is empty")]
    return []

def validate_required_columns(data: pd.DataFrame, required_columns: list[str]) -> list[ValidationIssue]:
    missing_columns = []
    for column in required_columns:
        if column not in data.columns:
            missing_columns.append(column)

    if not missing_columns:
        return []

    message = "Missing required columns: " + ", ".join(missing_columns)
    return [ValidationIssue(ValidationCode.MISSING_REQUIRED_COLUMNS, Severity.ERROR, message)]

def validate_missing_values(data: pd.DataFrame, columns: list[str]) -> list[ValidationIssue]:
    missing = {}
    for column in columns:
        missing_values = data[column].isna()
        if missing_values.any():
            missing.update({column: data[missing_values].index.tolist()})

    errors = []
    for m in missing:
        message = f"Column '{m}' has missing values in rows: {missing[m]}"
        errors.append(ValidationIssue(ValidationCode.MISSING_VALUES, Severity.ERROR, message))

    return errors
