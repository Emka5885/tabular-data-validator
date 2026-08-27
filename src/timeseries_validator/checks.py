import pandas as pd
from .issues import ValidationIssue, ValidationCode, Severity
from timeseries_validator.conversion import can_convert

from .validation_options import SortOrder

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

# Missing values can cause pandas to change the type of other values in a column.
# For example, integer values may be converted to floats when the column contains None.
# This function validates the types after pandas has created the DataFrame.
def validate_data_type(data: pd.DataFrame, column: str, data_type: type) -> list[ValidationIssue]:
    issues = []

    # Skip missing values - they are validated in 'validate_missing_values'
    missing = data[column].isna()

    # Check if value has the correct type
    correct_type = data[column].apply(
        lambda value: isinstance(value, data_type)
    )

    to_check = ~missing & ~correct_type
    if not to_check.any():
        return issues

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

def validate_unique_values(data: pd.DataFrame, column: str) -> list[ValidationIssue]:
    # Skip missing values - they are validated in 'validate_missing_values'
    values = data[column].dropna()

    duplicated = values[values.duplicated(keep=False)]
    duplicated_values = duplicated.unique()

    if duplicated.empty:
        return []

    message = f"Duplicated values in column '{column}':\n"
    for value in duplicated_values:
        indexes = data.index[data[column] == value].tolist()
        message += f"Duplicated value {value} found at indices: {indexes}\n"
    return [ValidationIssue(ValidationCode.DUPLICATE_VALUES, Severity.ERROR, message)]

def validate_allowed_values(data: pd.DataFrame, column: str, allowed_values: list) -> list[ValidationIssue]:
    # Skip missing values - they are validated in 'validate_missing_values'
    values = data[column].dropna()

    # Keep only values that are not in the allowed values list
    incorrect_values = values[~values.isin(allowed_values)]

    message = f"Values not allowed in column '{column}':\n"

    for value in incorrect_values.unique():
        message += f"found {value} at indices: {incorrect_values.index[incorrect_values == value].tolist()}\n"

    issues = []
    if not incorrect_values.empty:
        message += f"Allowed values: {allowed_values}"
        issues = [ValidationIssue(ValidationCode.NOT_ALLOWED_VALUES, Severity.ERROR, message)]

    return issues

def validate_sort_order(data: pd.DataFrame, column: str, sort_order: SortOrder) -> list[ValidationIssue]:
    issues = []
    # Skip missing values - they are validated in 'validate_missing_values'
    values = data[column].dropna()
    if values.empty:
        return issues

    is_valid = True
    match sort_order:
        case SortOrder.DECREASING:
            is_valid = values.is_monotonic_decreasing and values.is_unique
        case SortOrder.INCREASING:
            is_valid = values.is_monotonic_increasing and values.is_unique
        case SortOrder.NON_DECREASING:
            is_valid = values.is_monotonic_increasing
        case SortOrder.NON_INCREASING:
            is_valid = values.is_monotonic_decreasing
        case SortOrder.CONSTANT:
            if values.nunique() != 1:
                is_valid = False
        case _:
            raise ValueError(f"Unsupported sort order: {sort_order}.")

    if not is_valid:
        message = f"Column '{column}' does not have {sort_order.value} sort order"
        return [ValidationIssue(ValidationCode.SORT_ORDER, Severity.ERROR, message)]

    return issues

def validate_value_range(data: pd.DataFrame, column: str, minimum, maximum) -> list[ValidationIssue]:
    issues = []
    # Skip missing values - they are validated in 'validate_missing_values'
    values = data[column].dropna()

    if minimum is not None and maximum is not None:
        if minimum > maximum:
            raise ValueError("Minimum value cannot be greater than maximum value.")

    less_than_minimum = values[values < minimum]
    if not less_than_minimum.empty:
        message = f"Values below the minimum '{minimum}' in column '{column}':\n"
        for value in less_than_minimum.unique():
            indexes = less_than_minimum.index[less_than_minimum == value].tolist()
            message += f"found {value} at indices: {indexes}\n"
        issues.append(ValidationIssue(ValidationCode.BELOW_MINIMUM, Severity.ERROR, message))

    greater_than_maximum = values[values > maximum]
    if not greater_than_maximum.empty:
        message = f"Values above the maximum '{maximum}' in column '{column}':\n"
        for value in greater_than_maximum.unique():
            indexes = greater_than_maximum.index[greater_than_maximum == value].tolist()
            message += f"found {value} at indices: {indexes}\n"
        issues.append(ValidationIssue(ValidationCode.ABOVE_MAXIMUM, Severity.ERROR, message))

    return issues