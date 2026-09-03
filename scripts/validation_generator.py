import argparse
import csv
import shutil
import pandas as pd
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("dataset_path")
parser.add_argument("--delimiter")
parser.add_argument("--decimal")

def delete_dataset_folder(dataset_folder):
    shutil.rmtree(dataset_folder)

def generate(dataset_path, delimiter = None, decimal = None, output_folder=None):
    dataset_path = Path(dataset_path)
    if not dataset_path.is_file():
        raise FileNotFoundError(f"Incorrect path '{dataset_path}' - it is not a file.")
    dataset_name = dataset_path.stem

    if output_folder is None:
        output_folder = Path(__file__).resolve().parent
    target_folder = Path(output_folder) / dataset_name

    if delimiter is None:
        with open(dataset_path, "r", encoding="utf-8") as csvfile:
            try:
                sample = csvfile.read(4096)
                delimiter = csv.Sniffer().sniff(sample).delimiter
            except csv.Error:
                raise ValueError("Could not detect CSV delimiter. Use --delimiter to specify it manually.")

    dataset = pd.read_csv(dataset_path, sep=delimiter, nrows=0)  # Read only the header to get column names
    columns = dataset.columns

    # Folder
    try:
        target_folder.mkdir()
    except FileExistsError:
        raise FileExistsError(
            f"Folder with name '{dataset_name}' already exists. Delete or rename the existing folder and try again.")

    try:
        # Dataset.csv
        shutil.copy2(dataset_path, target_folder)

        # Contract.py
        columns_code = ""
        for column in columns:
            columns_code += f"{repr(column)}: ColumnRules(),\n\t\t"

        contract_content = f"""from timeseries_validator.contract import ValidationContract, ColumnRules

validation_contract = ValidationContract(
    require_non_empty=True,
    columns={{
        {columns_code}
    }}
)
"""

        contract_path = target_folder / "contract.py"
        contract_path.write_text(contract_content, encoding="utf-8")

        # Validate.py
        decimal = decimal if decimal is not None else "."

        validate_content = f"""import pandas as pd
from pathlib import Path

from contract import validation_contract
from timeseries_validator.validator import validate

dataset_folder = Path(__file__).resolve().parent
csv_path = dataset_folder / {dataset_path.name!r}
dataset = pd.read_csv(csv_path, sep={delimiter!r}, decimal={decimal!r})

issues = validate(dataset, validation_contract)
if not issues:
    print("No validation issues found.")
for issue in issues:
    print(f"[{{issue.severity.name}}] {{issue.message}}")
"""

        validate_path = target_folder / "validate.py"
        validate_path.write_text(validate_content, encoding="utf-8")

    except Exception:
        delete_dataset_folder(target_folder)
        raise


def main():
    args = parser.parse_args()
    generate(args.dataset_path, args.delimiter, args.decimal)


if __name__ == "__main__":
    main()