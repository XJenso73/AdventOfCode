# Advent of Code 2024 - Day 05
from collections import defaultdict
from dataclasses import dataclass
from functools import cached_property, cmp_to_key

from src.utils import calculate_duration, import_data

FILE = "./datas/day05_debug.txt"
FILE = "./datas/day05.txt"


@dataclass
class Grid:
    rules: dict[int, set[int]]
    updates: list[list[int]]

    @cached_property
    def valid_updates(self) -> list[list[int]]:
        return [u for u in self.updates if self.is_valid_update(u)]

    @property
    def invalid_updates(self) -> list[list[int]]:
        return [u for u in self.updates if not self.is_valid_update(u)]

    def is_valid_update(self, update: list[int]) -> bool:
        position = {value: idx for idx, value in enumerate(update)}
        return all(position[a] <= position[b] for a, after in self.rules.items() if a in position for b in after if b in position)

    def sort_update(self, update: list[int]) -> list[int]:
        def compare(a: int, b: int) -> int:
            return -1 if b in self.rules.get(a, ()) else 1 if a in self.rules.get(b, ()) else 0

        return sorted(update, key=cmp_to_key(compare))

    @staticmethod
    def middle_value(update: list[int]) -> int:
        return update[len(update) // 2]


def _parse(lines: list[str]) -> Grid:
    idx = lines.index("")

    rules: dict[int, set[int]] = defaultdict(set)
    for line in lines[:idx]:
        if line.strip():
            a, b = map(int, line.split("|"))
            rules[a].add(b)

    updates = [list(map(int, line.split(","))) for line in lines[idx + 1 :] if line.strip()]

    return Grid(rules, updates)


def solve_part_one(grid: Grid) -> None:
    result = sum(grid.middle_value(u) for u in grid.valid_updates)
    # 143 / 5129
    print(f"Result part 1: {result}")


def solve_part_two(grid: Grid) -> None:
    result = sum(grid.middle_value(grid.sort_update(u)) for u in grid.invalid_updates)
    # 123 / 4077
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    grid = _parse(lines)
    solve_part_one(grid)
    solve_part_two(grid)
    calculate_duration()
