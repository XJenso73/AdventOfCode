# Advent of Code 2023 - Day 03
import math
import re
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.utils import calculate_duration, import_data

FILE = "./datas/day03_debug.txt"
# FILE = "./datas/day03.txt"
PATTERN = re.compile(r"\d+")


def solve_mystery_one(lines: list[str]) -> None:
    result = _process_grid_data_mystery_one(lines)
    # 4361 / 536202
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    result = _process_grid_data_mystery_two(lines)
    # 467835 / 78272573
    print(f"Result mystery 2: {result}")


def _process_grid_data_mystery_one(grid: list[str]) -> int:
    total_sum = 0
    for grid_idx, line in enumerate(grid):
        for match in PATTERN.finditer(line):
            num = int(match.group())
            start_col = match.start()
            end_col = match.end()
            if _is_adjacent_to_symbol(grid, grid_idx, start_col, end_col):
                total_sum += num
    return total_sum


def _is_adjacent_to_symbol(grid: list[str], idx: int, start: int, end: int):
    for y in range(idx - 1, idx + 2):
        for x in range(start - 1, end + 1):
            if 0 <= y < len(grid) and 0 <= x < len(grid[0]):
                char = grid[y][x]
                if not char.isdigit() and char != ".":
                    return True
    return False


def _process_grid_data_mystery_two(grid: list[str]) -> int:
    total_sum = 0
    all_rows = len(grid)
    for idx, line in enumerate(grid):
        star_indices = [i for i, char in enumerate(line) if char == "*"]
        for col in star_indices:
            star_matches = []
            star_range = range(col - 1, col + 2)
            for row in range(idx - 1, idx + 2):
                if 0 <= row < all_rows:
                    for match in PATTERN.finditer(grid[row]):
                        number_range = range(match.start(), match.end())
                        if set(star_range) & set(number_range):
                            star_matches.append(int(match.group()))

            if len(star_matches) == 2:
                total_sum += math.prod(star_matches)

    return total_sum


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)
    calculate_duration()
