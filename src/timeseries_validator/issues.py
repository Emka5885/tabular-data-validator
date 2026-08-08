from enum import Enum

class ValidationCode(Enum):
    EMPTY_DATASET = "empty_dataset"
    MISSING_REQUIRED_COLUMNS = "missing_required_columns"
    MISSING_VALUES = "missing_values"

class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"

class ValidationIssue:
    def __init__(self, code: ValidationCode, severity: Severity, message: str):
        self.code = code
        self.severity = severity
        self.message = message