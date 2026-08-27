import pandas as pd

from timeseries_validator.validator import validate
from timeseries_validator.contract import ValidationContract, ColumnRules
from timeseries_validator.issues import ValidationCode, Severity
from timeseries_validator.validation_options import SortOrder

def test_validate_empty_dataset():
    test_df = pd.DataFrame()
    validation_contract = ValidationContract(require_non_empty=True, columns=None)

    # Validate the empty DataFrame
    issues = validate(test_df, validation_contract)

    # Check that the correct issue is returned
    assert len(issues) == 1
    assert issues[0].code == ValidationCode.EMPTY_DATASET

def test_validate_required_columns():
    test_df = pd.DataFrame({"test1": [0]})
    validation_contract = ValidationContract(require_non_empty=True, columns={
        "test1" : ColumnRules(required=True),
        "test2": ColumnRules(required=True)
    })

    # Validate the DataFrame without required column
    issues = validate(test_df, validation_contract)

    # Check that the correct issue is returned
    assert len(issues) == 1
    assert issues[0].code == ValidationCode.MISSING_REQUIRED_COLUMNS
    assert "test2" in issues[0].message

def test_validate_missing_values():
    test_df = pd.DataFrame({"test1": [None, 1], "test2": [2, None]})
    validation_contract = ValidationContract(require_non_empty=False, columns={
        "test1" : ColumnRules(no_missing_values=False),
        "test2": ColumnRules(no_missing_values=True)
    })

    # Validate the DataFrame with missing values
    issues = validate(test_df, validation_contract)

    # Check that the correct issue is returned
    assert len(issues) == 1
    assert issues[0].code == ValidationCode.MISSING_VALUES
    assert "test2" in issues[0].message

def test_validate_data_types():
    test_df = pd.DataFrame({"test1": [0.1, 1.5, None], "test2": [2.1, 3.7, "abc"], "test3": [0.1, 9, True]})
    validation_contract = ValidationContract(require_non_empty=True, columns={
        "test1" : ColumnRules(data_type=float),
        "test2": ColumnRules(data_type=float),
        "test3": ColumnRules(data_type=float)
    })

    # Validate the DataFrame with wrong data types
    issues = validate(test_df, validation_contract)

    # Should skip missing values
    # Check that the correct issues are returned
    assert len(issues) == 3

    # "abc" cannot be converted from str to float - so error
    assert any(
        issue.code == ValidationCode.WRONG_DATA_TYPE
        and "test2" in issue.message
        and "for rows: [2]" in issue.message
        and issue.severity == Severity.ERROR
        for issue in issues
    )

    # 9 can be converted from int to float - so warning
    assert any(
        issue.code == ValidationCode.WRONG_DATA_TYPE
        and "test3" in issue.message
        and "for rows: [1]" in issue.message
        and issue.severity == Severity.WARNING
        for issue in issues
    )

    # True cannot be converted from bool to float - so error
    assert any(
        issue.code == ValidationCode.WRONG_DATA_TYPE
        and "test3" in issue.message
        and "for rows: [2]" in issue.message
        and issue.severity == Severity.ERROR
        for issue in issues
    )

def test_validate_unique_values():
    test_df = pd.DataFrame({"test1": [None, 1, None], "test2": [2, 2, 3], "test3": [2, 2, 3]})
    validation_contract = ValidationContract(require_non_empty=True, columns={
        "test1" : ColumnRules(only_unique_values=True),
        "test2": ColumnRules(only_unique_values=True),
        "test3": ColumnRules(only_unique_values=False)
    })

    # Validate the DataFrame
    issues = validate(test_df, validation_contract)

    # Should skip missing values
    # Check that the correct issue is returned
    assert len(issues) == 1
    assert any(
        issue.code == ValidationCode.DUPLICATE_VALUES
        and "test2" in issue.message
        and "value 2" in issue.message
        and "indices: [0, 1]" in issue.message
        for issue in issues
    )

def test_validate_allowed_values():
    test_df = pd.DataFrame({"test1": [None, 1, 0], "test2": [2, 2, 3]})
    validation_contract = ValidationContract(require_non_empty=False, columns={
        "test1" : ColumnRules(allowed_values=[0,1]),
        "test2": ColumnRules(allowed_values=[2])
    })

    # Validate the DataFrame
    issues = validate(test_df, validation_contract)

    # Should skip missing values
    # Check that the correct issue is returned
    assert len(issues) == 1
    assert any(
        issue.code == ValidationCode.NOT_ALLOWED_VALUES
        and "test2" in issue.message
        and "found 3" in issue.message
        and "indices: [2]" in issue.message
        for issue in issues
    )

def test_validate_sort_order():
    test_df = pd.DataFrame({"test1": [None, 1, 0, None, -1], "test2": [2, 2, 3, 2, 3]})
    validation_contract = ValidationContract(require_non_empty=True, columns={
        "test1" : ColumnRules(specific_sort_order=SortOrder.DECREASING),
        "test2": ColumnRules(specific_sort_order=SortOrder.INCREASING)
    })

    # Validate the DataFrame
    issues = validate(test_df, validation_contract)

    # Should skip missing values
    # Check that the correct issue is returned
    assert len(issues) == 1
    assert any(
        issue.code == ValidationCode.SORT_ORDER
        and "test2" in issue.message
        and "increasing" in issue.message
        for issue in issues
    )

def test_validate_value_range():
    test_df = pd.DataFrame({"test1": [None, 1, 0, None, -1], "test2": [2, 2, 4, 2, 3]})
    validation_contract = ValidationContract(require_non_empty=False, columns={
        "test1" : ColumnRules(minimum_value=-1, maximum_value=1),
        "test2": ColumnRules(maximum_value=3)
    })

    # Validate the DataFrame
    issues = validate(test_df, validation_contract)

    # Should skip missing values
    # Check that the correct issue is returned
    assert len(issues) == 1
    assert any(
        issue.code == ValidationCode.ABOVE_MAXIMUM
        and "test2" in issue.message
        and "found 4" in issue.message
        and "indices: [2]" in issue.message
        for issue in issues
    )

