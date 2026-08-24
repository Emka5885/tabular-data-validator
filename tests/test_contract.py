from timeseries_validator.contract import ValidationContract, ColumnRules

def test_validation_contract_defaults():
    contract = ValidationContract()

    assert contract.require_non_empty is True
    assert contract.columns == {}

def test_column_rules_defaults():
    column_rules = ColumnRules()

    assert column_rules.required is False
    assert column_rules.no_missing_values is False
    assert column_rules.data_type is None
    assert column_rules.only_unique_values is False
    assert column_rules.allowed_values is None
    assert column_rules.specific_sort_order is None
    assert column_rules.minimum_value is None
    assert column_rules.maximum_value is None

def test_validation_contract_with_column_rules():
    test_column_rules = ColumnRules(required=True, data_type=float, no_missing_values=True)
    test2_column_rules = ColumnRules(data_type=str, allowed_values=["PLN", "EUR"])
    contract = ValidationContract(require_non_empty=True,
                                  columns={"TEST_COLUMN": test_column_rules, "TEST2_COLUMN": test2_column_rules})

    assert contract.require_non_empty is True
    assert "TEST_COLUMN" in contract.columns
    assert contract.columns["TEST_COLUMN"].required is True
    assert contract.columns["TEST_COLUMN"].data_type is float
    assert contract.columns["TEST_COLUMN"].no_missing_values is True

    assert contract.columns["TEST2_COLUMN"].data_type is str
    assert contract.columns["TEST2_COLUMN"].no_missing_values is False
    assert contract.columns["TEST2_COLUMN"].allowed_values == ["PLN", "EUR"]

