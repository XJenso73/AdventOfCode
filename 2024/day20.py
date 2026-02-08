# Advent of Code 2024 - Day 20
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from collections import deque

from src.utils import calculate_duration, import_data

DIRS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
FILE = Path("datas/day20_debug.txt")
FILE = Path("datas/day20.txt")


def solve(lines: list[str], max_cheat: int) -> int:
    h, w = len(lines), len(lines[0])

    def neighbors(r, c):
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < h and 0 <= nc < w:
                yield nr, nc

    # Start und Ende finden
    for r in range(h):
        for c in range(w):
            if lines[r][c] == "S":
                start = (r, c)
            elif lines[r][c] == "E":
                end = (r, c)

    # BFS vom Start
    dist_start = {start: 0}
    q = deque([start])
    while q:
        r, c = q.popleft()
        for nr, nc in neighbors(r, c):
            if lines[nr][nc] != "#" and (nr, nc) not in dist_start:
                dist_start[(nr, nc)] = dist_start[(r, c)] + 1
                q.append((nr, nc))

    # BFS vom Ende
    dist_end = {end: 0}
    q = deque([end])
    while q:
        r, c = q.popleft()
        for nr, nc in neighbors(r, c):
            if lines[nr][nc] != "#" and (nr, nc) not in dist_end:
                dist_end[(nr, nc)] = dist_end[(r, c)] + 1
                q.append((nr, nc))

    normal_dist = dist_start[end]
    count = 0

    # Alle Cheat-Paare prüfen
    for (r1, c1), d1 in dist_start.items():
        for dr in range(-max_cheat, max_cheat + 1):
            for dc in range(-max_cheat + abs(dr), max_cheat - abs(dr) + 1):
                r2, c2 = r1 + dr, c1 + dc
                if (r2, c2) in dist_end:
                    cheat_len = abs(dr) + abs(dc)
                    new_dist = d1 + cheat_len + dist_end[(r2, c2)]
                    if normal_dist - new_dist >= 100:
                        count += 1

    return count


def solve_part_one(lines: list[str]) -> None:
    result = solve(lines, max_cheat=2)
    # 1490
    print(f"Result part 1: {result}")


def solve_part_two(lines: list[str]) -> None:
    result = solve(lines, max_cheat=20)
    # 1011325
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_part_one(lines)
    solve_part_two(lines)
    calculate_duration()
