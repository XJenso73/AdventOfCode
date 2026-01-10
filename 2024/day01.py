# Advent of Code 2024 - Day 01
import re
import sys
from collections import Counter
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration, import_data

FILE = "./datas/day01_debug.txt"
FILE = "./datas/day01.txt"
PATTERN = re.compile(r"(\d+)\D+(\d+)")


def _parse(lines: list[str]) -> tuple[list[int], list[int]]:
    historians_a = []
    historians_b = []
    for line in lines:
        if not line.strip():
            continue
        match = PATTERN.search(line)
        if match:
            group_a, group_b = map(int, match.groups())
            historians_a.append(group_a)
            historians_b.append(group_b)

    return historians_a, historians_b


def solve_part_one(historians_a: list[int], historians_b: list[int]) -> None:
    historians_a.sort()
    historians_b.sort()
    diff = [abs(x - y) for x, y in zip(historians_a, historians_b, strict=False)]
    result = sum(diff)
    print(f"Result mystery 1: {result}")


def solve_part_two(historians_a: list[int], historians_b: list[int]) -> None:
    freq = Counter(historians_b)
    result = sum(x * freq[x] for x in historians_a)
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    historians_a, historians_b = _parse(lines)
    solve_part_one(historians_a, historians_b)
    solve_part_two(historians_a, historians_b)
    calculate_duration()
