import pandas as pd
from timeseries_validator.validator import validate
from timeseries_validator.contract import ValidationContract, ColumnRules
from timeseries_validator.issues import ValidationCode

def test_validate_empty_dataset():
    test_df = pd.DataFrame()
    validation_contract = ValidationContract(require_non_empty=True, columns=None)

    # Validate the empty DataFrame
    issues = validate(test_df, validation_contract)

    # Check that the correct issue is returned
    assert len(issues) == 1
    assert issues[0].code == ValidationCode.EMPTY_DATASET

def test_validate_required_columns():
    test_df = pd.DataFrame({"test": [0]})
    validation_contract = ValidationContract(require_non_empty=True, columns={
        "test" : ColumnRules(required=True),
        "test2": ColumnRules(required=True)
    })

    # Validate the DataFrame without required column
    issues = validate(test_df, validation_contract)

    # Check that the correct issue is returned
    assert len(issues) == 1
    assert issues[0].code == ValidationCode.MISSING_REQUIRED_COLUMNS
    assert "test2" in issues[0].message

def test_validate_missing_values():
    test_df = pd.DataFrame({"test": [None, 1], "test2": [2, None]})
    validation_contract = ValidationContract(require_non_empty=False, columns={
        "test" : ColumnRules(no_missing_values=False),
        "test2": ColumnRules(no_missing_values=True)
    })

    # Validate the DataFrame with missing values
    issues = validate(test_df, validation_contract)

    # Check that the correct issue is returned
    assert len(issues) == 1
    assert issues[0].code == ValidationCode.MISSING_VALUES
    assert "test2" in issues[0].message

