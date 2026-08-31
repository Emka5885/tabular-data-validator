# Heart Failure Clinical Records Example

This example shows that `timeseries-validator` is a generic validator and can be used with different types of datasets.

## Validation contract

The validation contract is based on the official documentation provided by UCI.

It checks:

- required columns
- missing values
- expected data types
- allowed values for binary columns

The validation can reveal differences between the official dataset description and the actual data. This shows how a validator can help detect unexpected data before further processing.

## Dataset

The dataset is not included in this repository.

Download `heart_failure_clinical_records_dataset.csv` from the official UCI Machine Learning.

Repository page: [Heart Failure Clinical Records](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records)

## Source

Heart Failure Clinical Records  
UCI Machine Learning Repository  
DOI: 10.24432/C5Z89R

License: CC BY 4.0