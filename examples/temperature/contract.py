from timeseries_validator.contract import ValidationContract, ColumnRules
from datetime import datetime

from timeseries_validator.validation_options import SortOrder

# Define validation rules for the temperature dataset.
# ValidationContract contains dataset-level settings and rules for individual columns.
temperature_contract = ValidationContract(
    require_non_empty=True,
    columns = {
        "id" : ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=int,
            only_unique_values=True
        ),
        "timestamp" : ColumnRules(
            required=True,
            data_type=datetime,
            specific_sort_order=SortOrder.INCREASING,
            no_missing_values=True,
        ),
        "sensor" : ColumnRules(
            required=True,
            data_type=str,
            allowed_values=["A", "B", "C"],
        ),
        "temperature" : ColumnRules(
            required=True,
            data_type=float,
            minimum_value=-40,
            maximum_value=40,
        ),
        "status" : ColumnRules(
            required=True,
            data_type=str,
            allowed_values=["OK", "WARNING", "ERROR"],
        ),
    }
)