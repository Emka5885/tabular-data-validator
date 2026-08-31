from numpy.ma.core import minimum

from timeseries_validator.contract import ValidationContract, ColumnRules

heart_failure_contract = ValidationContract(
    require_non_empty=True,
    columns={
        "age": ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=int
        ),

        "anaemia": ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=int,
            allowed_values=[0, 1]
        ),

        "creatinine_phosphokinase": ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=int
        ),

        "diabetes": ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=int,
            allowed_values=[0, 1]
        ),

        "ejection_fraction": ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=int,
            minimum_value=0,
            maximum_value=100
        ),

        "high_blood_pressure": ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=int,
            allowed_values=[0, 1]
        ),

        "platelets": ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=float
        ),

        "serum_creatinine": ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=float
        ),

        "serum_sodium": ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=int
        ),

        "sex": ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=int,
            allowed_values=[0, 1]
        ),

        "smoking": ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=int,
            allowed_values=[0, 1]
        ),

        "time": ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=int
        ),

        "DEATH_EVENT": ColumnRules(
            required=True,
            no_missing_values=True,
            data_type=int,
            allowed_values=[0, 1]
        )
    }
)