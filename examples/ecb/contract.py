from tabular_data_validator import ValidationContract, ColumnRules, SortOrder
from datetime import datetime

ecb_contract = ValidationContract(
    require_non_empty=True,
    columns = {
        "TIME_PERIOD" : ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=datetime,
            only_unique_values=True,
            specific_sort_order=SortOrder.INCREASING
        ),
        "OBS_VALUE" : ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=float,
            minimum_value=0.0001
        ),
        "CURRENCY" : ColumnRules(
            required=True,
            no_missing_values=True,
            allowed_values=["PLN"],
        ),
    }
)