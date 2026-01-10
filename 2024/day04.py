# Advent of Code 2024 - Day 04
import sys
from dataclasses import dataclass
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration, import_data

FILE = "./datas/day04_debug.txt"
FILE = "./datas/day04.txt"

# Part 1
WORD = "XMAS"
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

# Part 2
CENTER_CHAR = "A"
NEEDED_CHARS = {"M", "S"}


@dataclass
class Position:
    row: int
    col: int
    drow: int = 0
    dcol: int = 0


@dataclass
class Grid:
    lines: list[str]
    height: int
    width: int

    @classmethod
    def from_lines(cls, lines: list[str]) -> "Grid":
        return cls(lines, len(lines), len(lines[0]))

    def is_valid(self, row: int, col: int) -> bool:
        return 0 <= row < self.height and 0 <= col < self.width

    def get(self, row: int, col: int) -> str:
        return self.lines[row][col]


def _calculate_part_one(grid: Grid) -> int:

    result = 0
    for row in range(grid.height):
        for col in range(grid.width):
            for dir_row, dir_col in DIRECTIONS:
                if _is_word_found(grid, Position(row, col, dir_row, dir_col)):
                    result += 1

    return result


def _is_word_found(grid: Grid, pos: Position) -> bool:
    return all(
        grid.is_valid(pos.row + pos.drow * i, pos.col + pos.dcol * i)
        and grid.get(pos.row + pos.drow * i, pos.col + pos.dcol * i) == WORD[i]
        for i in range(len(WORD))
    )


def _calculate_part_two(grid: Grid) -> int:
    return sum(
        1
        for row in range(1, grid.height - 1)
        for col in range(1, grid.width - 1)
        if grid.get(row, col) == CENTER_CHAR and _is_x_word_found(grid, Position(row, col))
    )


def _is_x_word_found(grid: Grid, pos: Position) -> bool:
    d1 = {grid.get(pos.row - 1, pos.col - 1), grid.get(pos.row + 1, pos.col + 1)}
    d2 = {grid.get(pos.row - 1, pos.col + 1), grid.get(pos.row + 1, pos.col - 1)}

    return d1 == NEEDED_CHARS and d2 == NEEDED_CHARS


def solve_part_one(grid: Grid) -> None:
    result = _calculate_part_one(grid)
    # 18 / 2297
    print(f"Result part 1: {result}")


def solve_part_two(grid: Grid) -> None:
    result = _calculate_part_two(grid)
    # 9 / 1745
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    grid = Grid.from_lines(lines)
    solve_part_one(grid)
    solve_part_two(grid)
    calculate_duration()
