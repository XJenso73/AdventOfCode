# Advent of Code 2023 - Day 01

import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration, import_data

# FILE = "./datas/day01_debug.txt"
# FILE = "./datas/day01_debug_2.txt"
FILE = "./datas/day01.txt"

WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def solve_mystery_one(lines: list[str]) -> None:
    result = _calculate_result(lines)
    # 54708
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    lines = _append_digits_if_digits_as_word(lines)
    result = _calculate_result(lines)
    # 54087
    print(f"Result mystery 2: {result}")


def _calculate_result(lines: list[str]):
    result = 0
    for line in lines:
        digits = [int(char) for char in line if char.isdigit()]
        line_result = int(f"{digits[0]}{digits[-1]}")
        result += line_result
    return result


def _append_digits_if_digits_as_word(lines: list[str]) -> list[str]:
    for idx, word in enumerate(WORDS):
        lines = [line.replace(word, f"{word}{idx + 1}{word}") for line in lines]
    return lines


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)

    calculate_duration()
