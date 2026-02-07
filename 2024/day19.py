# Advent of Code 2024 - Day 19
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from functools import cache

from src.utils import calculate_duration, import_data

FILE = Path("datas/day19_debug.txt")
# FILE = Path("datas/day19.txt")


def _parse_input(lines: list[str]) -> tuple[tuple[str], list[str]]:
    split_index = lines.index("")
    towels = set(lines[0].split(", "))
    towels = tuple(towels)
    designs = lines[split_index + 1 :]
    return towels, designs


@cache
def ways(design: str, towels: tuple[str, ...]) -> int:
    # Basisfall: leerer String = 1 (gültige Zerlegung)
    if not design:
        return 1

    total = 0
    for t in towels:
        if design.startswith(t):
            # Rekursiv den Rest ermitteln
            total += ways(design[len(t) :], towels)
    return total


def solve_part_one(towels: tuple[str]) -> None:
    result = sum(1 for d in designs if ways(d, towels) > 0)
    # 6 / 258
    print(f"Result part 1: {result}")


def solve_part_two(towels: tuple[str], designs: list[str]) -> None:
    result = sum(ways(d, towels) for d in designs)
    # 16 / 632423618484345
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    towels, designs = _parse_input(lines)
    solve_part_one(towels)
    solve_part_two(towels, designs)
    calculate_duration()
