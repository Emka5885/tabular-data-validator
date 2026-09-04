# Tabular Data Validator

This is a Python library that allows you to validate tabular datasets based on specific rules defined in a Validation Contract.

When you have a dataset with a large number of rows, checking manually if all records are correct is not practical. This validator allows you to check them automatically. You only need to define which rules each column should follow.

## Installation

```bash
pip install tabular-data-validator
```

## Features

- empty dataset validation
- required columns validation
- missing values validation
- expected data type validation
- unique values validation
- allowed values validation
- sort order validation
- value range validation
- validation issues reported as errors and warnings
- Validation Contract for defining dataset rules
- CLI generator for creating `contract.py` and `validate.py`

## Getting started

Create validation files for your CSV dataset by providing the path to the file:

```bash
tabular-data-validator path/to/dataset.csv
```

The generator creates a new folder named after the dataset and copies the original CSV file into it. The original dataset remains unchanged in its current location.

```text
dataset/
├── dataset.csv
├── contract.py
└── validate.py
```

All column names from the dataset are automatically added to `contract.py`.

Open the generated folder and define the validation rules for each column in `contract.py`. Then run:

```bash
python validate.py
```

The validator will display all errors and warnings found in the dataset.

If needed, the CSV delimiter and decimal separator can be provided manually:

```bash
tabular-data-validator dataset.csv --delimiter ";" --decimal ","
```

## Validation Contract

Validation rules are defined in `contract.py` using `ValidationContract` and `ColumnRules`.

Dataset-level rules are defined in `ValidationContract`.

Currently available:

- `require_non_empty`

Available column rules:

| Rule | Description |
| --- | --- |
| `required` | Requires the column to exist |
| `no_missing_values` | Does not allow missing values |
| `data_type` | Defines the expected data type |
| `only_unique_values` | Requires values to be unique |
| `allowed_values` | Defines allowed values |
| `specific_sort_order` | Defines the expected sort order |
| `minimum_value` | Defines the minimum allowed value |
| `maximum_value` | Defines the maximum allowed value |

Conversion checks are currently supported for:

- `int`
- `float`
- `datetime`

If a value has a different type, the validator checks whether it can be safely converted to the expected type. The validator does not modify the original dataset.

For complete usage examples, see the `examples` directory.

## Examples

The repository contains examples using different types of datasets:

- ECB exchange rate data - real financial time-series data
- Temperature data - synthetic data used to demonstrate validation rules
- Heart Failure Clinical Records - external medical data from the UCI Machine Learning Repository

These examples show how the same validation system can be used with different types of tabular datasets.

## License

This project is licensed under the MIT License.
