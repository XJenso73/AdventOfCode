# Advent of Code 2023 - Day 11
import sys
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.utils import calculate_duration, import_data

FILE = "./datas/day11_debug.txt"
# FILE = "./datas/day11.txt"


@dataclass
class Universum:
    empty_rows: list[int]
    empty_cols: list[int]
    galaxies: list[tuple[int, int]]
    expansions_factor: int = 2

    @property
    def offset(self) -> int:
        return self.expansions_factor - 1

    def calculate_dist(self, point_1: tuple[int, int], point_2: tuple[int, int]) -> int:
        y1, x1 = point_1
        y2, x2 = point_2

        # Standard-Distanz
        dist = abs(y1 - y2) + abs(x1 - x2)

        # Ausdehnung für jede leere Zeile
        for r in self.empty_rows:
            if min(y1, y2) < r < max(y1, y2):
                dist += self.offset

        for c in self.empty_cols:
            if min(x1, x2) < c < max(x1, x2):
                dist += self.offset

        return dist


def _create_universum(lines: list[str]) -> Universum:
    empty_rows, empty_cols = _get_expanded_universe_indices(lines)
    galaxies = _get_galaxies(lines)
    return Universum(empty_rows=empty_rows, empty_cols=empty_cols, galaxies=galaxies)


def _get_expanded_universe_indices(lines: list[str]) -> tuple[list[int]]:
    empty_rows = [i for i, line in enumerate(lines) if "#" not in line]
    empty_cols = [j for j, col in enumerate(zip(*lines, strict=False)) if "#" not in col]

    return empty_rows, empty_cols


def _get_galaxies(lines: list[str]) -> list[tuple[int, int]]:
    return [(y, x) for y, line in enumerate(lines) for x, char in enumerate(line) if char == "#"]


def _calculate_distance(universum: Universum) -> int:
    result = 0
    # combinations(galaxies, 2) gibt Paare wie (p1, p2)
    for point_1, point_2 in combinations(universum.galaxies, 2):
        distance = universum.calculate_dist(point_1, point_2)
        result += distance
    return result


def solve_mystery_one(universum: Universum) -> None:
    result = _calculate_distance(universum)
    # 374 / 9805264
    print(f"Result mystery 1: {result}")


def solve_mystery_two(universum: Universum) -> None:
    universum.expansions_factor = 1000000
    result = _calculate_distance(universum)
    # 82000210 / 779032247216
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    universum = _create_universum(lines)
    solve_mystery_one(universum)
    solve_mystery_two(universum)
    calculate_duration()
