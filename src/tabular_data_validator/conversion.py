import pandas as pd
from datetime import datetime

def can_convert(value, data_type: type) -> bool:
    converters = {
        int: _can_convert_to_int,
        float: _can_convert_to_float,
        datetime: _can_convert_to_datetime,
    }

    if data_type not in converters:
        supported_types = ", ".join(
            supported_type.__name__ for supported_type in converters.keys()
        )
        raise ValueError(f"Unsupported data type: {data_type}. Please choose from {supported_types} or write new converter function.")

    return converters[data_type](value)


def _can_convert_to_int(value):
    if isinstance(value, bool):
        return False
    try:
        converted = float(value)
        if converted.is_integer():
            return True
        return False
    except (ValueError, TypeError):
        return False

def _can_convert_to_float(value):
    if isinstance(value, bool):
        return False
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False

def _can_convert_to_datetime(value):
    if pd.isna(value):
        return False
    if isinstance(value, bool):
        return False
    if _can_convert_to_float(value):
        return False
    try:
        pd.to_datetime(value, errors="raise")
        return True
    except (ValueError, TypeError):
        return False