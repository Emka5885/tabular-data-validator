import pandas as pd

from scripts.validation_generator import generate
from pathlib import Path

def test_validation_generator(tmp_path):
    test_csv = Path(__file__).parent / "data" / "test.csv"

    generate(test_csv, output_folder=tmp_path)

    dataset_name = test_csv.stem
    folder_path = tmp_path / dataset_name
    assert folder_path.is_dir()

    dataset_path = folder_path / test_csv.name
    assert dataset_path.is_file()
    assert dataset_path.read_bytes() == test_csv.read_bytes()

    # Contract
    contract_path = folder_path / "contract.py"
    assert contract_path.is_file()

    dataset = pd.read_csv(test_csv, sep=';', nrows=0)  # Read only the header to get column names
    columns = dataset.columns

    contract_content = contract_path.read_text(encoding="utf-8")

    for column in columns:
        assert column in contract_content

    # Validate
    validate_path = folder_path / "validate.py"
    assert validate_path.is_file()
