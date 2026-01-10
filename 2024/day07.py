# Advent of Code 2024 - Day 07
import sys
from dataclasses import dataclass
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration, import_data

FILE = "./datas/day07_debug.txt"
# FILE = "./datas/day07.txt"


@dataclass
class Grid:
    operations: list[tuple[int, list[int]]]


def _parse(lines: list[str]) -> Grid:
    data: list[tuple[int, list[int]]] = []
    for line in lines:
        if not line.strip():
            continue
        line = line.replace("  ", " ")
        result, parts = line.split(":")
        ziffern = list(map(int, parts.split()))
        data.append((int(result), ziffern))
    return Grid(data)


def is_valid(target: int, current: int, nums: list[int]) -> bool:
    if not nums:
        return current == target

    number, *rest = nums
    return is_valid(target, current + number, rest) or is_valid(target, current * number, rest)


def is_valid_with_concat(target: int, current: int, nums: list[int], include_concat: bool) -> bool:
    if not nums:
        return current == target
    if current > target:  # pruning
        return False

    number, *rest = nums

    # Addition, Multiplikation, ggf. Concatenation
    return (
        is_valid_with_concat(target, current + number, rest, include_concat)
        or is_valid_with_concat(target, current * number, rest, include_concat)
        or (include_concat and is_valid_with_concat(target, int(f"{current}{number}"), rest, include_concat))
    )


def solve_part_one(grid: Grid) -> None:
    result = 0
    for target, nums in grid.operations:
        if is_valid(target, nums[0], nums[1:]):
            result += target

    # result = "xy"
    # 3749 / 1545311493300
    print(f"Result part 1: {result}")


def solve_part_two(lines: list[str]) -> None:
    result = 0
    for target, nums in grid.operations:
        if is_valid_with_concat(target, nums[0], nums[1:], True):
            result += target

    #  11387 / 169122112716571
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines: list[str] = import_data(FILE)
    grid: Grid = _parse(lines)
    # print(grid)
    solve_part_one(grid)
    solve_part_two(grid)
    calculate_duration()
