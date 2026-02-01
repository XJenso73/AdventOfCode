# Advent of Code 2024 - Day 18
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from collections import deque

from src.utils import calculate_duration, import_data

FILE = Path("datas/day18_debug.txt")
FILE = Path("datas/day18.txt")
SIZE = 71
START = (0, 0)
END = (70, 70)
DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def shortest_path(byte_positions: list[tuple[int, int]]) -> int | None:
    byte_positions = set(byte_positions)
    q = deque([(0, START)])
    seen = {START}

    while q:
        dist, pos = q.popleft()

        if pos == END:
            return dist

        x, y = pos
        for dir_x, dir_y in DIRECTIONS:
            next_x, next_y = x + dir_x, y + dir_y
            next_pos = (next_x, next_y)

            if 0 <= next_x < SIZE and 0 <= next_y < SIZE and next_pos not in byte_positions and next_pos not in seen:
                seen.add(next_pos)
                q.append((dist + 1, next_pos))

    return None


def first_blocking_byte(byte_positions: list[tuple[int, int]]) -> tuple[int, int]:
    low, hight = 0, len(byte_positions)

    while low < hight:
        mid = (low + hight) // 2
        if shortest_path(byte_positions[:mid]) is None:
            hight = mid
        else:
            low = mid + 1

    return byte_positions[low - 1]


def solve_part_one(byte_positions: list[tuple[int, int]]) -> None:
    result = shortest_path(byte_positions[:1024])
    # 324
    print(f"Result part 1: {result}")


def solve_part_two(byte_positions: list[tuple[int, int]]) -> None:
    result = first_blocking_byte(byte_positions)
    # 46,23
    print(f"Result part 2: {','.join(map(str, result))}")


if __name__ == "__main__":
    lines = import_data(FILE)
    byte_positions = [tuple(map(int, x.split(","))) for x in lines]
    solve_part_one(byte_positions)
    solve_part_two(byte_positions)
    calculate_duration()
