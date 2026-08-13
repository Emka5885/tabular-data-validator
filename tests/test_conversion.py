import pytest

from timeseries_validator.conversion import can_convert
from datetime import datetime

def test_conversion_with_unsupported_data_type():
    with pytest.raises(ValueError):
        can_convert("value", str)

def test_convert_to_integer():
    test_cases = ["1",2,"3.0",4.4,"5.5","6.000",None,"abc",' ',True]
    results = [can_convert(value, int) for value in test_cases]

    assert results == [True, True, True, False, False, True, False, False, False, False]

def test_convert_to_float():
    test_cases = ["1",2,"3.0",4.4,"5.5","6.000",None,"abc",' ',True]
    results = [can_convert(value, float) for value in test_cases]

    assert results == [True, True, True, True, True, True, False, False, False, False]

def test_convert_to_datetime():
    test_cases = [2.5,"6.50",None,"abc",' ',True, "2023-01-01", "2023/01/01", "01-01-2023", "2023.01.01", "2023-13-01", datetime(2020,1,2,00,00,00)]
    results = [can_convert(value, datetime) for value in test_cases]

    assert results == [False, False, False, False, False, False, True, True, True, True, False, True]