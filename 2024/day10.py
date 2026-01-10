# Advent of Code 2024 - Day 10
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.utils import calculate_duration, import_data

FILE = "./datas/day10_debug.txt"
# FILE = "./datas/day10.txt"
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
MAX_ELEVATION = 9


@dataclass
class Grid:
    grid: list[list[int]]
    rows: int
    cols: int
    _cache: dict[tuple[int, int], tuple[tuple[int, int], ...]] = None

    def __post_init__(self):
        self._cache = {}

    def get(self, row, col):
        return self.grid[row][col] or 0

    def get_neighbors(self, row: int, col: int) -> Iterator[tuple[int, int]]:
        return (
            (next_row, next_col)
            for dir_row, dir_col in DIRECTIONS
            if 0 <= (next_row := row + dir_row) < self.rows and 0 <= (next_col := col + dir_col) < self.cols
        )

    def walk(self, row: int, col: int) -> tuple[tuple[int, int], ...]:
        if (row, col) in self._cache:
            return self._cache[(row, col)]

        if self.get(row, col) == MAX_ELEVATION:
            result = ((row, col),)
        else:
            current = self.get(row, col)
            result = tuple(peak for nr, nc in self.get_neighbors(row, col) if self.get(nr, nc) == current + 1 for peak in self.walk(nr, nc))

        self._cache[(row, col)] = result
        return result


def _parse(lines: list[str]) -> Grid:
    grid = [[int(char) for char in line] for line in lines if line.strip()]
    return Grid(grid, len(grid), len(grid[0]))


def _calculate(grid: Grid) -> tuple[int, int]:
    trailheads: list[tuple[int, int]] = _get_trailheads(grid)

    result_p1, result_p2 = 0, 0

    for start_row, start_col in trailheads:
        peaks = grid.walk(start_row, start_col)
        result_p1 += len(set(peaks))
        result_p2 += len(peaks)
    return result_p1, result_p2


def _get_trailheads(grid) -> list[tuple[int, int]]:
    return [(row, col) for row in range(grid.rows) for col in range(grid.cols) if grid.grid[row][col] == 0]


def solve_part_one(result: int) -> None:
    # 36 / 816
    print(f"Result part 1: {result}")


def solve_part_two(result: int) -> None:
    # 81 / 1960
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    grid: Grid = _parse(lines)
    result_part_one, result_part_two = _calculate(grid)
    solve_part_one(result_part_one)
    solve_part_two(result_part_two)
    calculate_duration()
