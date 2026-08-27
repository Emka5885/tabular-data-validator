import pandas as pd

from .contract import ValidationContract
from .issues import ValidationIssue
from .checks import (validate_empty_dataset, validate_required_columns, validate_missing_values, validate_data_type,
                     validate_unique_values, validate_allowed_values)

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

    # Data types
    data_types = {column_name : rule.data_type
                      for column_name, rule in contract.columns.items()
                      if rule.data_type is not None and column_name in dataset.columns}
    for column_name, data_type in data_types.items():
        issues.extend(validate_data_type(dataset, column_name, data_type))

    # Unique values
    unique_values = [column_name
                      for column_name, rule in contract.columns.items()
                      if rule.only_unique_values and column_name in dataset.columns]
    for column_name in unique_values:
        issues.extend(validate_unique_values(dataset, column_name))

    # Allowed values
    allowed_values = {column_name: rule.allowed_values
                  for column_name, rule in contract.columns.items()
                  if rule.allowed_values is not None and column_name in dataset.columns}
    for column_name, allowed in allowed_values.items():
        issues.extend(validate_allowed_values(dataset, column_name, allowed))

    return issues
