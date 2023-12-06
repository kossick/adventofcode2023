import sys
import pathlib
import argparse

CURRENT_PATH = pathlib.Path.cwd()
_WinningNumbers = list[list[int]]
_TicketNumbers = list[list[int]]


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


def _extract_numbers(numbers: str) -> list[int]:
    return [int(n) for n in numbers.split(" ") if n.isdigit()]


def split_tickets(raw: list[str]) -> tuple[_WinningNumbers, _TicketNumbers]:
    winnings = list()
    tickets = list()
    for row in raw:
        winning_str, ticket_str = row.split(": ")[1].split(" | ")
        winnings.append(_extract_numbers(winning_str))
        tickets.append(_extract_numbers(ticket_str))
    return (winnings, tickets)


def winning_numbers(winning: list[int], ticket: list[int]) -> int:
    return len(list(set(winning).intersection(set(ticket))))


def calculate_points(total_matching: int) -> int:
    return 2 ** (total_matching - 1) if total_matching > 0 else 0


def won_scratchcards(matching: list[int]) -> dict[int, int]:
    scratchcards = {n + 1: 1 for n in range(len(matching))}
    for id, count in enumerate(matching, start=1):
        for _ in range(scratchcards[id]):
            for x in range(count):
                scratchcards[id + 1 + x] += 1
    return scratchcards


def main() -> None:
    parser = generate_arg_parser()
    args = parser.parse_args()
    file_name = args.filename if ".txt" in args.filename else f"{args.filename}.txt"
    try:
        raw_data = read_file(CURRENT_PATH / file_name)
    except FileNotFoundError:
        print(f"Unable to find the file '{file_name}', check that it exists and that you spelt it correctly!")
        sys.exit(1)

    winnings, tickets = split_tickets(raw_data)
    matching = [winning_numbers(w, t) for w, t in zip(winnings, tickets)]
    print(f"Total number of points is {sum([calculate_points(m) for m in matching])}")
    print(f"The total number of won scratchcards is {sum(won_scratchcards(matching).values())}")


if __name__ == "__main__":
    main()
