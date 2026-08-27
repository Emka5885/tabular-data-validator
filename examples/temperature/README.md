# Temperature dataset example

This is a synthetic dataset created to demonstrate the main features of `timeseries-validator`.

The example includes:
- a custom CSV dataset,
- a validation contract,
- validation of required columns, missing values, data types, unique values, allowed values, value ranges, and sort order.

The `timestamp` column is converted to `datetime` before validation because CSV files do not store pandas data type information.

The validator does not modify or convert the dataset. It only checks the prepared data against the rules defined in the contract and returns detected validation issues.