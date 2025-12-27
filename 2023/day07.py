# Advent of Code 2023 - Day 07
from src.utils import calculate_duration, import_data

FILE = "./datas/day07_debug.txt"
# FILE = "./datas/day07.txt"


def solve_mystery_one(lines: list[str]) -> None:
    result = "xy"
    # 6440 / 252656917
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    result = "xy"
    # 5905 / 253499763
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)
    calculate_duration()
