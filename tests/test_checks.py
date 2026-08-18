import pandas as pd
from timeseries_validator.issues import ValidationCode, Severity
from timeseries_validator.checks import (validate_empty_dataset, validate_required_columns, validate_missing_values,
                                         validate_data_type, validate_unique_values, validate_allowed_values)

# ------------------------------
# Empty dataset
# ------------------------------
def test_empty_dataset():
    empty_df = pd.DataFrame()

    # Validate the empty DataFrame
    issues = validate_empty_dataset(empty_df)

    # Check that the correct issue is returned
    assert len(issues) == 1
    assert issues[0].code == ValidationCode.EMPTY_DATASET
    assert issues[0].severity == Severity.ERROR

def test_nonempty_dataset():
    nonempty_df = pd.DataFrame({"test": [1]})

    # Validate the nonempty DataFrame
    issues = validate_empty_dataset(nonempty_df)

    # Check that the empty list is returned
    assert issues == []

# ------------------------------
# Missing required columns
# ------------------------------
def test_missing_required_columns():
    test_df = pd.DataFrame({"test": [0], "test2": [2], "test3": [3]})

    # Validate the DataFrame without required columns
    issues = validate_required_columns(test_df, ["test1", "test4"])

    # Check that the correct issue is returned
    assert len(issues) == 1
    assert issues[0].code == ValidationCode.MISSING_REQUIRED_COLUMNS
    assert issues[0].severity == Severity.ERROR
    assert "test1" in issues[0].message
    assert "test4" in issues[0].message

def test_required_columns_exist():
    test_df = pd.DataFrame({"test": [0], "test2": [2], "test3": [3]})

    # Validate the DataFrame with required columns
    issues = validate_required_columns(test_df, ["test2", "test3"])

    # Check that the empty list is returned
    assert issues == []


# ------------------------------
# Missing values
# ------------------------------
def test_missing_values_in_specific_columns():
    test_df = pd.DataFrame({"test": [0,2,3,None], "test2": [None,1,2,3]})

    # Validate selected columns
    issues = validate_missing_values(test_df, ["test", "test2"])

    # Check that the correct issues are returned
    assert len(issues) == 2

    assert issues[1].code == ValidationCode.MISSING_VALUES
    assert issues[1].severity == Severity.ERROR
    assert "test2" in issues[1].message
    assert "0" in issues[1].message

    assert issues[0].code == ValidationCode.MISSING_VALUES
    assert issues[0].severity == Severity.ERROR
    assert "test" in issues[0].message
    assert "3" in issues[0].message

def test_specific_column_has_all_values():
    test_df = pd.DataFrame({"test": [0,1,2,3]})

    # Validate selected columns
    issues = validate_missing_values(test_df, ["test"])

    # Check that the empty list is returned
    assert issues == []

def test_specific_column_has_all_values_but_the_other_column_has_missing_values():
    test_df = pd.DataFrame({"test": [0, 2, 3, 4], "test2": [None, 1, 2, 3]})

    # Validate selected columns
    issues = validate_missing_values(test_df, ["test"])

    # Check that the empty list is returned
    assert issues == []


# ------------------------------
# Data types
# ------------------------------
def test_all_values_have_expected_data_type():
    test_df = pd.DataFrame({"test": [6,7,2,3]})

    # Validate data types
    issues = validate_data_type(test_df, "test", int)

    # Check that the emtpy list is returned
    assert issues == []

def test_wrong_data_types_can_be_converted_to_expected_data_type():
    test_df = pd.DataFrame({"test1": [0,"1",2,'3']})

    # Validate data types
    issues = validate_data_type(test_df, "test1", int)

    # Check that the correct issues are returned
    assert len(issues) == 1
    assert issues[0].code == ValidationCode.WRONG_DATA_TYPE
    assert issues[0].severity == Severity.WARNING
    assert "test1" in issues[0].message
    assert "1" in issues[0].message
    assert "3" in issues[0].message
    assert "str" in issues[0].message

def test_some_values_cannot_be_converted_to_expected_data_type():
    test_df = pd.DataFrame({"test2": [0,1,"abc",3]})

    # Validate data types
    issues = validate_data_type(test_df, "test2", int)

    # Check that the correct issues are returned
    assert len(issues) == 1
    assert issues[0].code == ValidationCode.WRONG_DATA_TYPE
    assert issues[0].severity == Severity.ERROR
    assert "test2" in issues[0].message
    assert "2" in issues[0].message
    assert "str" in issues[0].message

def test_some_values_can_be_converted_and_some_cannot():
    test_df = pd.DataFrame({"test3": [0,"1","abc",'3']})

    # Validate data types
    issues = validate_data_type(test_df, "test3", int)

    # Check that the correct issues are returned
    assert len(issues) == 2

    assert issues[0].code == ValidationCode.WRONG_DATA_TYPE
    assert issues[0].severity == Severity.WARNING
    assert "test3" in issues[0].message
    assert "1" in issues[0].message
    assert "3" in issues[0].message
    assert "str" in issues[0].message

    assert issues[1].code == ValidationCode.WRONG_DATA_TYPE
    assert issues[1].severity == Severity.ERROR
    assert "test3" in issues[1].message
    assert "2" in issues[1].message
    assert "str" in issues[1].message

def test_none_values_do_not_return_issues_during_data_type_validation():
    test_df = pd.DataFrame({"test4": pd.Series([6,None,2, 3], dtype=object)})

    # Validate data types
    issues = validate_data_type(test_df, "test4", int)

    # Check that the empty list is returned
    assert issues == []


# ------------------------------
# Unique values
# ------------------------------
def test_duplicated_values():
    test_df = pd.DataFrame({"test": [0,0,1,2,2]})

    # Validate the DataFrame with duplicated values
    issues = validate_unique_values(test_df, "test")

    # Check that the correct issue is returned
    assert len(issues) == 1
    assert issues[0].code == ValidationCode.DUPLICATE_VALUES
    assert issues[0].severity == Severity.ERROR
    assert "test" in issues[0].message
    assert "value 0" in issues[0].message
    assert "[0, 1]" in issues[0].message
    assert "value 2" in issues[0].message
    assert "[3, 4]" in issues[0].message

def test_only_unique_values():
    test_df = pd.DataFrame({"test": [0, 1, None, None]})

    # Validate the DataFrame with unique values
    issues = validate_unique_values(test_df, "test")

    # Check that the empty list is returned
    assert issues == []


# ------------------------------
# Allowed values
# ------------------------------
def test_only_allowed_values():
    test_df = pd.DataFrame({"test": [0, 1, None, None, 1]})

    # Validate the DataFrame with allowed values
    issues = validate_allowed_values(test_df, "test", [0,1])

    # Check that the empty list is returned
    assert issues == []

def test_not_allowed_values():
    test_df = pd.DataFrame({"test": [0, 8, 0, 1, 9, 9]})

    # Validate the DataFrame with not allowed values
    issues = validate_allowed_values(test_df, "test", [0,1])

    # Check that the correct issue is returned
    assert len(issues) == 1
    assert issues[0].code == ValidationCode.NOT_ALLOWED_VALUES
    assert issues[0].severity == Severity.ERROR
    assert "test" in issues[0].message
    assert "Allowed values: [0, 1]" in issues[0].message

    assert "found 8" in issues[0].message
    assert "[1]" in issues[0].message

    assert "found 9" in issues[0].message
    assert "[4, 5]" in issues[0].message