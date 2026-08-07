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