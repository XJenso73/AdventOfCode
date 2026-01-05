# Advent of Code 2024 - Day 02
from src.utils import calculate_duration, import_data

FILE = "./datas/day02_debug.txt"
# FILE = "./datas/day02.txt"
ALLOWED_DIFFS = [1, 2, 3]


def _parse(lines: list[str]) -> list[list[int]]:
    parsed_lines = []
    for line in lines:
        numbers = list(map(int, line.strip().split()))
        if numbers[0] > numbers[-1]:
            numbers.reverse()
        parsed_lines.append(numbers)

    return parsed_lines


def _is_consistent(line: list[int]) -> bool:
    all_increasing = all(value - line[idx] in ALLOWED_DIFFS for idx, value in enumerate(line[1:]))
    return all_increasing


def solve_part_one(lines: list[list[int]]) -> None:
    result = 0
    for numbers in lines:
        is_consistent = _is_consistent(numbers)
        if is_consistent:
            result += 1
    # 2 / 486
    print(f"Result part 1: {result}")


def solve_part_two(lines: list[str]) -> None:
    result = 0
    for line in lines:
        if _is_consistent(line):
            result += 1
        else:
            can_be_fixed = any(_is_consistent(line[:i] + line[i + 1 :]) for i in range(len(line)))
            if can_be_fixed:
                result += 1
    # 4 / 540
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    lines = _parse(lines)
    solve_part_one(lines)
    solve_part_two(lines)
    calculate_duration()
