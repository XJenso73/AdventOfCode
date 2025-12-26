from collections import deque
from functools import cache

from src.utils import calculate_duration, import_data

# FILE = "./datas/day07_debug.txt"
FILE = "./datas/day07.txt"


def solve_mystery_one(lines: list[str]) -> int:
    rows = len(lines)
    colums = len(lines[0])

    # Startpunkt suchen
    start_point_colum, start_point_line = _extract_start_point(lines)

    splits = 0
    queue = deque([(start_point_colum, start_point_line + 1)])
    visited_splits = set()  # Positionen der Strahlteiler, die schon gesplittet haben

    while queue:
        col, row = queue.popleft()
        if row >= rows or col < 0 or col >= colums:
            continue

        cell = lines[row][col]

        if cell == ".":
            queue.append((col, row + 1))
        elif cell == "^" and (col, row) not in visited_splits:
            splits += 1
            visited_splits.add((col, row))
            # Strahl links und rechts nach unten
            queue.append((col - 1, row + 1))
            queue.append((col + 1, row + 1))

    # 1490
    print(f"Result mystery 1: {splits}")


def solve_mystery_two(lines: list[str]) -> int:
    rows = len(lines)
    colums = len(lines[0])

    # Startpunkt
    start_point_colum, start_point_line = _extract_start_point(lines)

    @cache
    def dfs(col: int, row: int) -> int:
        # Algorithmusname (Depth-First Search)
        if row >= rows or col < 0 or col >= colums:
            return 1  # Endpunkt
        cell = lines[row][col]
        if cell == ".":
            return dfs(col, row + 1)
        elif cell == "^":
            return dfs(col - 1, row + 1) + dfs(col + 1, row + 1)
        else:
            # andere Zellen ignorieren
            return dfs(col, row + 1)

    result = dfs(start_point_colum, start_point_line + 1)
    print(f"Result mystery 2: {result}")


def _extract_start_point(lines: list[str]) -> tuple[int, int]:
    for index, line in enumerate(lines):
        if "S" in line:
            return line.index("S"), index
    raise ValueError("Startpunkt 'S' nicht gefunden")


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)

    calculate_duration()
