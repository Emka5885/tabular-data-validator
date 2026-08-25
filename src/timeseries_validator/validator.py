import pandas as pd

from .contract import ValidationContract
from .issues import ValidationIssue
from .checks import validate_empty_dataset, validate_required_columns, validate_missing_values, validate_data_type

def validate(dataset: pd.DataFrame, contract: ValidationContract) -> list[ValidationIssue]:
    """
    Validate a dataset against a validation contract.

    :param dataset: The dataset to validate.
    :param contract: The validation contract to use.
    :return: A list of validation issues found in the dataset.
    """
    issues = []

    # Empty dataset
    if contract.require_non_empty:
        issues.extend(validate_empty_dataset(dataset))

    # Missing required columns
    required_columns = [column_name
                        for column_name, rule in contract.columns.items()
                        if rule.required]
    issues.extend(validate_required_columns(dataset, required_columns))

    # Missing values
    missing_values = [column_name
                      for column_name, rule in contract.columns.items()
                      if rule.no_missing_values and column_name in dataset.columns]
    issues.extend(validate_missing_values(dataset, missing_values))

    return issues
