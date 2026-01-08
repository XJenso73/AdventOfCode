# Advent of Code 2024 - Day 06
from dataclasses import dataclass, field
from functools import cached_property

from src.utils import calculate_duration, import_data

FILE = "./datas/day06_debug.txt"
FILE = "./datas/day06.txt"
# Directions: Up, Right, Down, Left (90 degrees clockwise)
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
STARTPOINT = "^"
WAYPOINT = "#"


@dataclass
class Grid:
    grid: list[str]
    visited: set[tuple[int, int]] = field(init=False, default_factory=set)
    states: set[tuple[int, int, int], int] = field(init=False, default_factory=set)

    def __post_init__(self):
        self.rows: int = len(self.grid)
        self.cols: int = len(self.grid[0]) if self.rows > 0 else 0

    @cached_property
    def start_pos(self) -> tuple[int, int]:
        for row, line in enumerate(self.grid):
            if (col := line.find(STARTPOINT)) != -1:
                return (row, col)
        raise ValueError("Starting point not found")

    def is_valid(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def is_obstacle(self, row: int, col: int, block: tuple[int, int] | None = None) -> bool:
        return self.grid[row][col] == WAYPOINT or (row, col) == block

    def is_valid_and_waypoint(self, row: int, col: int, extra: tuple[int, int] | None = None) -> bool:
        if self.is_valid(row, col) is False:
            return False
        return self.grid[row][col] == WAYPOINT

    def simulate(self) -> tuple[bool, set[tuple[int, int]], set[tuple[int, int, int], int]]:
        row, col = self.start_pos
        dir_idx = 0
        visited = set()
        states = {}
        step = 0

        while self.is_valid(row, col):
            state = (row, col, dir_idx)
            if state in states:
                return True, visited, states

            states[state] = step
            visited.add((row, col))

            dir_row, dir_col = DIRECTIONS[dir_idx]
            next_row, next_col = row + dir_row, col + dir_col

            if self.is_valid_and_waypoint(next_row, next_col):
                dir_idx = (dir_idx + 1) % 4
            else:
                row, col = next_row, next_col

            step += 1
        return False, visited, states

    def obstacle_loop(self, block: tuple[int, int]) -> bool:
        row, col = self.start_pos
        dir_idx = 0
        current_path_states = set()

        while True:
            state = (row, col, dir_idx)
            if state in current_path_states:
                return True

            current_path_states.add(state)

            dir_row, dir_col = DIRECTIONS[dir_idx]
            next_row, next_col = row + dir_row, col + dir_col

            if self.is_valid(next_row, next_col) is False:
                return False

            if self.is_obstacle(next_row, next_col, block):
                dir_idx = (dir_idx + 1) % 4
            else:
                row, col = next_row, next_col


def solve_part_one(grid: Grid) -> None:
    result = len(grid.visited)
    # 41 / 5177
    print(f"Result part 1: {result}")


def solve_part_two(grid: Grid) -> None:
    result = 0
    # need to check positions that the guard actually visits
    for row, col in grid.visited:
        if (row, col) == grid.start_pos:
            continue

        is_loop = grid.obstacle_loop(block=(row, col))
        if is_loop:
            result += 1
    # 6 / 1686
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines: list[str] = import_data(FILE)
    grid = Grid(lines)
    _, grid.visited, grid.states = grid.simulate()
    solve_part_one(grid)
    solve_part_two(grid)
    calculate_duration()
