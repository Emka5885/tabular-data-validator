import pandas as pd
from timeseries_validator.issues import ValidationCode, Severity
from timeseries_validator.checks import validate_empty_dataset

def test_empty_dataset():
    # Create an empty DataFrame
    empty_df = pd.DataFrame()

    # Validate the empty DataFrame
    issues = validate_empty_dataset(empty_df)

    # Check that the correct issue is returned
    assert len(issues) == 1
    assert issues[0].code == ValidationCode.EMPTY_DATASET
    assert issues[0].severity == Severity.ERROR

def test_nonempty_dataset():
    # Create a nonempty DataFrame
    nonempty_df = pd.DataFrame({"test": [1]})

    # Validate the nonempty DataFrame
    issues = validate_empty_dataset(nonempty_df)

    # Check that the emtpy list is returned
    assert issues == []