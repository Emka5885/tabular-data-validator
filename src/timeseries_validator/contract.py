from .validation_options import SortOrder

class ColumnRules:
    def __init__(self, required: bool = False, no_missing_values: bool = False, data_type: type| None = None,
                 only_unique_values: bool=False, allowed_values: list | None = None, specific_sort_order: SortOrder | None = None,
                 minimum_value = None, maximum_value = None):
        self.required = required
        self.no_missing_values = no_missing_values
        self.data_type = data_type
        self.only_unique_values = only_unique_values
        self.allowed_values = allowed_values
        self.specific_sort_order = specific_sort_order
        self.minimum_value = minimum_value
        self.maximum_value = maximum_value

class ValidationContract:
    def __init__(self, require_non_empty: bool = True, columns: dict[str, ColumnRules] | None = None):
        self.require_non_empty = require_non_empty
        self.columns = columns if columns is not None else {}
