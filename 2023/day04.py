# Advent of Code 2023 - Day 04
from src.utils import calculate_duration, import_data

FILE = "./datas/day04_debug.txt"
FILE = "./datas/day04.txt"


def solve_mystery_one(lines: list[str]) -> None:
    result = _calculate_mystery_one(lines)
    # result = 3
    # 13 / 23750
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    result = _calculate_mystery_two(lines)
    # 30 / 13261850
    print(f"Result mystery 2: {result}")


def _calculate_mystery_one(lines):
    total_points = 0
    for line in lines:
        count_matches = _prepaire_datas(line)
        if count_matches > 0:
            points = 2 ** (count_matches - 1)
            total_points += points
    return total_points


def _prepaire_datas(line: str) -> int:
    line = line.replace("  ", " ")
    _, values = line.split(":")
    my_numbers, win_numbers = values.strip().split("|")
    my_number_set = _get_as_set(my_numbers)
    win_number_set = _get_as_set(win_numbers)
    matched_numbers = my_number_set.intersection(win_number_set)
    count_matches = len(matched_numbers)
    return count_matches


def _get_as_set(number: str) -> set[int]:
    return set(map(int, number.strip().split(" ")))


def _calculate_mystery_two(lines):
    counts = dict.fromkeys(range(len(lines)), 1)

    for idx, line in enumerate(lines):
        count_matches = _prepaire_datas(line)

        if count_matches > 0:
            current_card_copies = counts[idx]

            for i in range(1, count_matches + 1):
                next_card_idx = idx + i
                if next_card_idx in counts:
                    counts[next_card_idx] += current_card_copies

    return sum(counts.values())


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)
    calculate_duration()
