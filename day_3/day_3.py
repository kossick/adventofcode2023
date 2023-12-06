from collections.abc import Callable
import sys
import pathlib
import argparse
from dataclasses import dataclass
from functools import reduce
import re

CURRENT_PATH = pathlib.Path.cwd()
_Row = int
_Column = int
_Indices = tuple[_Row, _Column]


@dataclass
class Number:
    value: int
    row: _Row
    col_span: tuple[int, int]


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


def _find_symbols(grid: list[str], criteria: Callable[[str], bool]) -> list[_Indices]:
    return [(idy, idx) for idy, row in enumerate(grid) for idx, char in enumerate(row) if criteria(char)]


def _find_all_numbers(grid: list[str]) -> list[Number]:
    """Collect every number in the grid"""
    numbers = list()
    for idy, row in enumerate(grid):
        idx_skip = 0  # used to save scanning indices knowns to be part of the current number
        for idx, char in enumerate(row):
            if idx < idx_skip:
                continue
            if char.isnumeric():
                m = re.search(r"(?P<value>\d+)\D*", row[idx:])
                if m is not None:
                    value = m.group("value")
                    idx_skip = idx + len(value)
                    numbers.append(Number(value=int(value), row=idy, col_span=(idx, idx_skip)))
    return numbers


def find_gear_ratio(grid: list[str]) -> int:
    gear_ratios = list()

    def _touching_numbers(symbol: tuple[int, int]) -> list[int]:
        """Find all numbers touching the gear symbol and return their values"""
        min_row = max(0, symbol[0] - 1)
        max_row = min(len(grid), symbol[0] + 2)
        correct_rows = filter(lambda s: s.row in range(min_row, max_row), numbers)
        min_col = max(0, symbol[1] - 1)
        max_col = min(len(grid), symbol[1] + 2)
        touching = filter(
            lambda s: any((col in range(min_col, max_col) for col in range(s.col_span[0], s.col_span[1]))), correct_rows
        )
        return [n.value for n in list(touching)]

    gear_symbols = _find_symbols(grid, lambda x: x == "*")
    numbers = _find_all_numbers(grid)
    for symbol in gear_symbols:
        if len(touching := _touching_numbers(symbol)) == 2:
            gear_ratios.append(reduce(lambda x, y: x * y, touching))
    return sum(gear_ratios)


def find_part_numbers(grid: list[str]) -> list[int]:
    part_numbers = list()

    def _touching_symbol(number: Number) -> bool:
        """
        Check to see if a number is a neighbour of a symbol

        Checks based on row (restricting to symbols in the same row, or ±1, of the number),
        then checks column in the range `[min(number.col_span) - 1, max(number.col_span) + 1]`
        """
        min_row = max(0, number.row - 1)
        max_row = min(len(grid), number.row + 2)
        correct_rows = filter(lambda s: s[0] in range(min_row, max_row), symbols)
        min_col = max(0, number.col_span[0] - 1)
        max_col = min(len(grid[0]), number.col_span[1] + 1)
        touching = filter(lambda s: s[1] in range(min_col, max_col), correct_rows)
        return len(list(touching)) > 0

    symbols = _find_symbols(grid, lambda x: bool(re.match(r"[^\w\s.]", x)))
    numbers = _find_all_numbers(grid)
    for number in numbers:
        if _touching_symbol(number):
            part_numbers.append(number.value)
    return part_numbers


def main() -> None:
    parser = generate_arg_parser()
    args = parser.parse_args()
    file_name = args.filename if ".txt" in args.filename else f"{args.filename}.txt"
    try:
        raw_data = read_file(CURRENT_PATH / file_name)
    except FileNotFoundError:
        print(f"Unable to find the file '{file_name}', check that it exists and that you spelt it correctly!")
        sys.exit(1)
    part_numbers = find_part_numbers(raw_data)
    print(f"The sum of the part numbers is {sum(part_numbers)}")
    print(f"The total gear ratio is {find_gear_ratio(raw_data)}")


if __name__ == "__main__":
    main()
