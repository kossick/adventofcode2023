import sys
import pathlib
import argparse
from functools import reduce
import re

CURRENT_PATH = pathlib.Path.cwd()
TOTAL_CUBES = {"red": 12, "green": 13, "blue": 14}
PATTERN = r"(?P<count>\d+) (?P<colour>\w+)"


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


def split_rounds(game: str) -> list[str]:
    return [round.strip() for round in game.split(";")]


def all_possible(rounds: list[str]) -> bool:
    for round in rounds:
        for cubes in round.split(","):
            m = re.search(PATTERN, cubes)
            if m and int(m.group("count")) > TOTAL_CUBES[m.group("colour")]:
                return False
    return True


def find_power(rounds: list[str]) -> int:
    max_cubes = {"red": 0, "green": 0, "blue": 0}
    for round in rounds:
        for cubes in round.split(","):
            m = re.search(PATTERN, cubes)
            if m:
                max_cubes[m.group("colour")] = max(int(m.group("count")), max_cubes[m.group("colour")])
    return reduce(lambda a, b: a * b, max_cubes.values())


def main() -> None:
    parser = generate_arg_parser()
    args = parser.parse_args()
    file_name = args.filename if ".txt" in args.filename else f"{args.filename}.txt"
    try:
        raw_data = read_file(CURRENT_PATH / file_name)
    except FileNotFoundError:
        print(f"Unable to find the file '{file_name}', check that it exists and that you spelt it correctly!")
        sys.exit(1)
    id_sum = 0
    power_sum = 0
    for idx, game in enumerate(raw_data, start=1):
        rounds = split_rounds(game.split(":")[1])
        if all_possible(rounds):
            id_sum += idx
        power_sum += find_power(rounds)
    print(f"Total sum of possible ids is {id_sum}")
    print(f"The sum of powers is {power_sum}")


if __name__ == "__main__":
    main()
