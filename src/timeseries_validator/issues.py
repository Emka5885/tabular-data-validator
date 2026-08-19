from enum import Enum

class ValidationCode(Enum):
    EMPTY_DATASET = "empty_dataset"
    MISSING_REQUIRED_COLUMNS = "missing_required_columns"
    MISSING_VALUES = "missing_values"
    WRONG_DATA_TYPE = "wrong_data_type"
    DUPLICATE_VALUES = "duplicate_values"
    NOT_ALLOWED_VALUES = "not_allowed_values"
    BELOW_MINIMUM = "below_minimum"
    ABOVE_MAXIMUM = "above_maximum"

class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"

class ValidationIssue:
    def __init__(self, code: ValidationCode, severity: Severity, message: str):
        self.code = code
        self.severity = severity
        self.message = message