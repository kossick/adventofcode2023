import sys
import pathlib
import argparse

CURRENT_PATH = pathlib.Path.cwd()


def generate_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", default="test.txt")
    return parser


def read_file(file: pathlib.Path) -> list[str]:
    if not file.exists():
        raise FileNotFoundError
    with file.open() as in_file:
        source_data = in_file.readlines()
    return [data.rstrip("\n") for data in source_data]


def main() -> None:
    parser = generate_arg_parser()
    args = parser.parse_args()
    file_name = args.filename if ".txt" in args.filename else f"{args.filename}.txt"
    try:
        raw_data = read_file(CURRENT_PATH / file_name)
    except FileNotFoundError:
        print(f"Unable to find the file '{file_name}', check that it exists and that you spelt it correctly!")
        sys.exit(1)


if __name__ == "__main__":
    main()
