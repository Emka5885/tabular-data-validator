from enum import Enum

class ValidationCode(Enum):
    EMPTY_DATASET = "empty_dataset"

class Severity(Enum):
    ERROR = "error"

class ValidationIssue:
    def __init__(self, code: ValidationCode, severity: Severity, message: str):
        self.code = code
        self.severity = severity
        self.message = message