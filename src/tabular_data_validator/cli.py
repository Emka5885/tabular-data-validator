import argparse
from .validation_files_generator import generate

parser = argparse.ArgumentParser()
parser.add_argument("dataset_path")
parser.add_argument("--delimiter")
parser.add_argument("--decimal")

def main():
    args = parser.parse_args()
    generate(args.dataset_path, args.delimiter, args.decimal)

if __name__ == "__main__":
    main()