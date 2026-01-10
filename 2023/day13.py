# Advent of Code 2023 - Day 13
import sys
from itertools import groupby
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.utils import calculate_duration, import_data

FILE = "./datas/day13_debug.txt"
# FILE = "./datas/day13.txt"
type Grid = list[str]


def _parse(lines: list[str]) -> list[Grid]:
    return [list(group) for empty_row, group in groupby(map(str.strip, lines), bool) if empty_row]


def _calculate(grids: list[Grid], target_diffs: int) -> int:
    result = 0
    for grid in grids:
        # search horizontally
        row_count = _find_mirror(grid, target_diffs)
        if row_count > 0:
            result += row_count * 100
        else:
            # search verticaly
            transposed = ["".join(col) for col in zip(*grid, strict=False)]
            col_count = _find_mirror(transposed, target_diffs)
            result += col_count
    return result


def _find_mirror(grid: Grid, target_diffs: int) -> int:
    # pass through every possible horizontal axis
    for idx, _ in enumerate(grid[1:], start=1):
        # for idx in range(1, len(grid)):
        upper = grid[:idx][::-1]
        lower = grid[idx:]

        # Count all chars differences across the entire mirror area
        diffs = 0
        for up_row, low_row in zip(upper, lower, strict=False):
            # count diffs in the row
            diffs += sum(1 for a, b in zip(up_row, low_row, strict=False) if a != b)

        if diffs == target_diffs:
            return idx
    return 0


def solve_mystery_one(grids: list[Grid]) -> None:
    result = _calculate(grids, 0)
    # 405 / 34889
    print(f"Result mystery 1: {result}")


def solve_mystery_two(grids: list[Grid]) -> None:
    result = _calculate(grids, 1)
    # 400 / 34224
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    grids = _parse(lines)
    solve_mystery_one(grids)
    solve_mystery_two(grids)
    calculate_duration()
