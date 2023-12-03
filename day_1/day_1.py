import sys
import pathlib
import argparse
import re

CURRENT_PATH = pathlib.Path.cwd()
DIGIT_STRINGS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}


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


def _contained_digit(substr: str) -> int:
    for string, digit in DIGIT_STRINGS.items():
        pattern = rf"{string}.*"
        if re.match(pattern, substr):
            return digit
    return 0


def _get_digits(line: str) -> list[int]:
    """
    Collects all digits in a given line.

    If it finds a digit then it immediately collects it. If it finds a letter then it checks to see if it matches
    the first letter of a digit written as a word; in this case if a full digit is found then it is converted to its
    numerical form and added to the returned digits.
    """
    digits = list()
    for idx, char in enumerate(line):
        if char.isdigit():
            digits.append(int(char))
        elif char in ("e", "f", "n", "o", "s", "t"):
            # any digit, written as a word, is at most 5 characters long
            substr = line[idx : idx + 5]
            contained = _contained_digit(substr)
            if contained > 0:
                digits.append(contained)
        else:
            continue
    # print(f"{digits=}")
    return digits


def add_calibration_values(raw_data: list[str]) -> int:
    total = 0
    for line in raw_data:
        digits = _get_digits(line)
        # Combine first and last digt so, e.g. 1 and 2 becomes 12
        total += (digits[0] * 10) + digits[-1]
    return total


def main() -> None:
    parser = generate_arg_parser()
    args = parser.parse_args()
    file_name = args.filename if ".txt" in args.filename else f"{args.filename}.txt"
    try:
        raw_data = read_file(CURRENT_PATH / file_name)
    except FileNotFoundError:
        print(f"Unable to find the file '{file_name}', check that it exists and that you spelt it correctly!")
        sys.exit(1)
    print(f"calibration total = {add_calibration_values(raw_data)}")


if __name__ == "__main__":
    main()
