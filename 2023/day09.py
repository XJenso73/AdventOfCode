# Advent of Code 2023 - Day 09
from itertools import pairwise

from src.utils import calculate_duration, import_data

FILE = "./datas/day09_debug.txt"
FILE = "./datas/day09.txt"


def _parse_lines(lines: list[str]) -> list[list[int]]:
    return [[int(elem) for elem in line.split()] for line in lines if line.strip()]


def _calculate(lines: list[list[int]]):
    return sum(_get_next_new_value(line) for line in lines)


def _get_next_new_value(sequence: list[int]) -> int:
    layers = [sequence]
    while any(x != 0 for x in layers[-1]):
        current = layers[-1]
        diffs = [b - a for a, b in pairwise(current)]
        layers.append(diffs)

    return sum(layer[-1] for layer in layers)


def solve_mystery_one(lines: list[str]) -> None:
    lines = _parse_lines(lines)
    result = _calculate(lines)
    # 114 / 1938731307
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    lines = _parse_lines(lines)
    # Content drehen
    lines = [line[::-1] for line in lines]
    result = _calculate(lines)
    # 2 / 948
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)
    calculate_duration()
