# Advent of Code 2023 - Day 16
import sys
from collections import deque
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.utils import calculate_duration, import_data

FILE = "./datas/day16_debug.txt"
# FILE = "./datas/day16.txt"

DIRECTIONS = {
    ".": lambda dx, dy: [(dx, dy)],
    "/": lambda dx, dy: [(-dy, -dx)],
    "\\": lambda dx, dy: [(dy, dx)],
    "-": lambda dx, dy: [(dx, dy)] if dy == 0 else [(1, 0), (-1, 0)],
    "|": lambda dx, dy: [(dx, dy)] if dx == 0 else [(0, 1), (0, -1)],
}


def _calculate_mystery_one(grid: list[str], start_config=(0, 0, 1, 0)) -> int:
    # start_beam = (x, y, dx, dy)
    queue = deque([start_config])
    # visited speichert (x, y, dx, dy), um Endlosschleifen zu vermeiden
    visited = set()
    # energized speichert nur (x, y), das ist unser Endergebnis
    energized = set()

    width = len(grid[0])
    height = len(grid)
    while queue:
        x, y, dx, dy = queue.popleft()

        if not (0 <= x < width and 0 <= y < height):
            continue
        if (x, y, dx, dy) in visited:
            continue

        visited.add((x, y, dx, dy))
        energized.add((x, y))

        for ndx, ndy in _next_direction(grid[y][x], dx, dy):
            queue.append((x + ndx, y + ndy, ndx, ndy))

    return len(energized)


def _next_direction(char: str, dx: int, dy: int) -> list[tuple[int, int]]:
    logic = DIRECTIONS.get(char)
    if logic:
        return logic(dx, dy)
    return []


def _calculate_mystery_two(lines):
    starts = _get_start_configuration(lines)
    return max(_calculate_mystery_one(lines, start_config) for start_config in starts)


def _get_start_configuration(lines):
    width = len(lines[0])
    height = len(lines)

    starts = []

    # oben nach unten, unten nach oben
    for x in range(width):
        starts.append((x, 0, 0, 1))
        starts.append((x, height - 1, 0, -1))

    # links nach rechts, rechts nach links
    for y in range(height):
        starts.append((0, y, 1, 0))
        starts.append((width - 1, y, -1, 0))
    return starts


def solve_mystery_one(lines: list[str]) -> None:
    result = _calculate_mystery_one(lines)
    # 46 / 6978
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    result = _calculate_mystery_two(lines)
    # 51 / 7315
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)
    calculate_duration()
