import sys
import pathlib
import argparse
from collections import Counter
from dataclasses import dataclass
from functools import cmp_to_key
import re

CURRENT_PATH = pathlib.Path.cwd()
PATTERN = r"(?P<hand>\w{5})\s+(?P<bid>\d+)"
# Part 1 order
# CARD_ORDER = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
# Part 2 order
CARD_ORDER = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]
BASE_PATTERNS = [
    [1, 1, 1, 1, 1],  # High card
    [2, 1, 1, 1],  # One pair
    [2, 2, 1],  # Two pair
    [3, 1, 1],  # Three of a kind
    [3, 2],  # Full house
    [4, 1],  # Four of a kind
    [5],  # Five of a kind
]


@dataclass
class Hand:
    cards: str
    bid: int


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


def parse(raw: list[str]) -> list[Hand]:
    hands = list()
    for row in raw:
        m = re.search(PATTERN, row)
        if m:
            hands.append(Hand(cards=m.group("hand"), bid=int(m.group("bid"))))
    return hands


def _get_base_value(cards: str) -> int:
    counter = Counter(cards)
    if "J" in counter.keys() and counter["J"] < 5:
        others = {key: val for key, val in counter.items() if key != "J"}
        largest_key = sorted(others.keys(), key=lambda y: others[y], reverse=True)[0]
        counter[largest_key] += counter["J"]
        counter.pop("J", None)
    counts = sorted(list(counter.values()), reverse=True)
    return BASE_PATTERNS.index(counts)


def sort_by_rank(a: Hand, b: Hand) -> int:
    a_base = _get_base_value(a.cards)
    b_base = _get_base_value(b.cards)
    if a_base > b_base:
        return 1
    elif a_base < b_base:
        return -1
    else:
        for a_card, b_card in zip(a.cards, b.cards):
            a_order = CARD_ORDER.index(a_card)
            b_order = CARD_ORDER.index(b_card)
            if a_order > b_order:
                return 1
            elif a_order < b_order:
                return -1
    return 0


def calculate_winnings(sorted: list[Hand]) -> int:
    products = [idx * hand.bid for idx, hand in enumerate(sorted, start=1)]
    return sum(products)


def main() -> None:
    parser = generate_arg_parser()
    args = parser.parse_args()
    file_name = args.filename if ".txt" in args.filename else f"{args.filename}.txt"
    try:
        raw_data = read_file(CURRENT_PATH / file_name)
    except FileNotFoundError:
        print(f"Unable to find the file '{file_name}', check that it exists and that you spelt it correctly!")
        sys.exit(1)
    hands = parse(raw_data)
    sorted_hands = sorted(hands, key=cmp_to_key(sort_by_rank))
    print(f"Total winnings = {calculate_winnings(sorted_hands)}")


if __name__ == "__main__":
    main()
