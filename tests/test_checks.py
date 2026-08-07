import pandas as pd
from timeseries_validator.issues import ValidationCode, Severity
from timeseries_validator.checks import validate_empty_dataset, validate_required_columns

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

    # Check that the emtpy list is returned
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

    # Check that the emtpy list is returned
    assert issues == []