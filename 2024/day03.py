# Advent of Code 2024 - Day 03
import re

from src.utils import calculate_duration, import_data

FILE = "./datas/day03_debug.txt"
FILE = "./datas/day03.txt"
PATTERN_1 = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
PATTERN_2A = re.compile(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)")
PATTERN_2B = re.compile(r"\d{1,3}")


def _calculate_part_two(text: str) -> int:
    tokens = PATTERN_2A.findall(text)
    enabled = True
    result = 0

    for token in tokens:
        match token:
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case mul if enabled and (nums := PATTERN_2B.findall(mul)):
                result += _calculate_result(map(int, nums))

    return result


def _calculate_result(result: tuple[int, int]) -> int:
    a, b = result
    return a * b


def solve_part_one(lines: list[str]) -> None:
    result = sum(_calculate_result(map(int, elem)) for elem in PATTERN_1.findall("".join(lines)))
    # 161 / 185797128
    print(f"Result part 1: {result}")


def solve_part_two(lines: list[str]) -> None:
    result = _calculate_part_two("".join(lines))
    # 48 / 89798695
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_part_one(lines)
    solve_part_two(lines)
    calculate_duration()
