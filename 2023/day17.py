# Advent of Code 2023 - Day 17
import heapq
import sys
from dataclasses import dataclass
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.utils import calculate_duration, import_data


@dataclass(frozen=True, slots=True)
class State:
    pos_x: int
    pos_y: int
    dir_x: int
    dir_y: int
    steps: int


@dataclass(frozen=True, slots=True)
class GridConfig:
    height: int
    width: int


@dataclass(frozen=True, slots=True)
class StepConfig:
    min_steps: int = 1
    max_steps: int = 3


FILE = "./datas/day17_debug.txt"
# FILE = "./datas/day17.txt"
DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]


def _parse(lines: list[str]) -> list[list[int]]:
    return [list(map(int, line)) for line in lines]


def _calculate(grid: list[list[int]], step_config: StepConfig) -> int:
    grid_config = GridConfig(len(grid), len(grid[0]))

    priority_queue = [
        (0, 0, 0, 1, 0, 0),  # Osten
        (0, 0, 0, 0, 1, 0),  # Süden
    ]

    visited: set[tuple[int, int, int, int, int]] = set()

    while priority_queue:
        loss, pos_x, pos_y, dir_x, dir_y, steps = heapq.heappop(priority_queue)
        state = State(pos_x, pos_y, dir_x, dir_y, steps)

        if state in visited:
            continue
        visited.add(state)

        if (pos_x, pos_y) == (grid_config.width - 1, grid_config.height - 1) and steps >= step_config.min_steps:
            return loss

        for next_pos_x, next_pos_y, next_dir_x, next_dir_y, next_steps in _neighbors(state, grid_config, step_config):
            heapq.heappush(
                priority_queue, (loss + grid[next_pos_y][next_pos_x], next_pos_x, next_pos_y, next_dir_x, next_dir_y, next_steps)
            )


def _neighbors(state: State, grid_config: GridConfig, step_config: StepConfig):
    for n_dir_x, n_dir_y in DIRS:
        if (n_dir_x, n_dir_y) == (-state.dir_x, -state.dir_y):
            continue

        straight = (n_dir_x, n_dir_y) == (state.dir_x, state.dir_y)
        if not straight and state.steps < step_config.min_steps:
            continue

        if straight and state.steps >= step_config.max_steps:
            continue

        n_steps = state.steps + 1 if straight else 1
        n_pos_x, n_pos_y = state.pos_x + n_dir_x, state.pos_y + n_dir_y
        if 0 <= n_pos_x < grid_config.width and 0 <= n_pos_y < grid_config.height:
            yield n_pos_x, n_pos_y, n_dir_x, n_dir_y, n_steps


def solve_mystery_one(lines: list[str]) -> None:
    result = _calculate(lines, StepConfig())
    # 102 / 698
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    result = _calculate(lines, StepConfig(4, 10))
    # 94 / 825
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    lines = _parse(lines)
    solve_mystery_one(lines)
    solve_mystery_two(lines)
    calculate_duration()
