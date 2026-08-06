import pandas as pd
from .issues import ValidationIssue, ValidationCode, Severity

def validate_empty_dataset(data: pd.DataFrame) -> list[ValidationIssue]:
    if data.empty:
        return [ValidationIssue(ValidationCode.EMPTY_DATASET, Severity.ERROR, "Dataset is empty")]
    return []