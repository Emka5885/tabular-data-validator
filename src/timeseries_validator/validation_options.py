from enum import Enum

class SortOrder(Enum):
    DECREASING = "decreasing"
    INCREASING = "increasing"
    NON_DECREASING = "non_decreasing"
    NON_INCREASING = "non_increasing"
    CONSTANT = "constant"