import pandas as pd
from .issues import ValidationIssue, ValidationCode, Severity
from timeseries_validator.conversion import can_convert

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

def validate_data_type(data: pd.DataFrame, column: str, data_type: type) -> list[ValidationIssue]:
    issues = []

    # Skip missing values - they are validated in 'validate_missing_values'
    missing = data[column].isna()
    # Check if value has the correct type
    correct_type = data[column].apply(
        lambda value: isinstance(value, data_type)
    )
    to_check = ~missing & ~correct_type
    # Check if the value can be converted to the expected type
    convertible = pd.Series(False, index=data.index)
    convertible.loc[to_check] = data.loc[to_check, column].apply(
        lambda value: can_convert(value, data_type)
    )

    # Wrong type, but conversion is possible
    warning_mask = convertible & to_check
    warning = data[column][warning_mask]
    if not warning.empty:
        found_warning_types = warning.apply(lambda value: type(value).__name__).unique().tolist()
        message_warning = f"Column '{column}' for rows: {warning.index.tolist()} has incorrect data type. Expected: '{data_type.__name__}', Found: {found_warning_types}, but it can be converted to '{data_type.__name__}'"

        issues.append(ValidationIssue(ValidationCode.WRONG_DATA_TYPE, Severity.WARNING, message_warning))

    # Wrong type, and conversion is not possible
    error_mask = ~convertible & to_check
    wrong = data[column][error_mask]
    if wrong.empty:
        return issues

    found_error_types = wrong.apply(lambda value: type(value).__name__).unique().tolist()
    message = f"Column '{column}' for rows: {wrong.index.tolist()} has incorrect data type and they cannot be converted. Expected data type: '{data_type.__name__}', Found data type: {found_error_types}"

    issues.append(ValidationIssue(ValidationCode.WRONG_DATA_TYPE, Severity.ERROR, message))

    return issues