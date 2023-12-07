import sys
import pathlib
import argparse
from math import sqrt
from functools import reduce
import re

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


def _convert_value(x: float) -> int:
    """Handle upper limit: if already an int then it needs to be a smaller one, otherwise it must be floor"""
    if (y := int(x)) == x:
        return y - 1
    return y


def _calculate_winning_window(t_limit: int, w_dist: int) -> tuple[int, int]:
    """Calculate the minimum and maximum time `t` where `t(t_limit - t) >= w_dist`"""
    det = sqrt(t_limit**2 - (4 * w_dist))
    t_max = _convert_value((t_limit + det) / 2)
    return (int((t_limit - det) / 2) + 1, t_max)


def number_of_ways_of_winning(times: list[int], distances: list[int]) -> int:
    leeway = list()
    for t, d in zip(times, distances):
        min_t, max_t = _calculate_winning_window(t, d)
        leeway.append(max_t - min_t + 1)
    return reduce(lambda x, y: x * y, leeway)


def main() -> None:
    parser = generate_arg_parser()
    args = parser.parse_args()
    file_name = args.filename if ".txt" in args.filename else f"{args.filename}.txt"
    try:
        raw_data = read_file(CURRENT_PATH / file_name)
    except FileNotFoundError:
        print(f"Unable to find the file '{file_name}', check that it exists and that you spelt it correctly!")
        sys.exit(1)
    # Part 1
    times = [int(n) for n in re.findall(r"\d+", raw_data[0])]
    distances = [int(n) for n in re.findall(r"\d+", raw_data[1])]
    print(f"There are {number_of_ways_of_winning(times, distances)} ways of winning.")
    # Part 2, because I'm too lazy to change things
    times = [int(reduce(lambda x, y: x + y, re.findall(r"\d+", raw_data[0])))]
    distances = [int(reduce(lambda x, y: x + y, re.findall(r"\d+", raw_data[1])))]
    print(f"There are {number_of_ways_of_winning(times, distances)} ways of winning (big boy).")


if __name__ == "__main__":
    main()
