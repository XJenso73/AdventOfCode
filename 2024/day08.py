# Advent of Code 2024 - Day 08
from collections import defaultdict
from dataclasses import dataclass
from itertools import combinations

from src.utils import calculate_duration, import_data

FILE = "./datas/day08_debug.txt"
FILE = "./datas/day08.txt"

type Antinodes = set[tuple[int, int]]


@dataclass
class Grid:
    antennas: dict[str, list[tuple[int, int]]]
    rows: int
    cols: int

    def get_antinode_positions(self) -> Antinodes:
        antinodes: Antinodes = set()
        for positions in self.antennas.values():
            for (row_1, col_1), (row_2, col_2) in combinations(positions, 2):
                delta_row, delta_col = row_2 - row_1, col_2 - col_1
                node_1 = (row_2 + delta_row, col_2 + delta_col)
                node_2 = (row_1 - delta_row, col_1 - delta_col)
                antinodes.update(node for node in [node_1, node_2] if self._is_within_bounds(node))

        return antinodes

    def get_resonant_antinode_positions(self) -> Antinodes:
        antinodes: Antinodes = set()
        for positions in self.antennas.values():
            for (row_1, col_1), (row_2, col_2) in combinations(positions, 2):
                current = row_1, col_1
                delta_row, delta_col = row_2 - row_1, col_2 - col_1
                # Direction 1: Start at pos_1 and go "forwards"
                antinodes = self._loop_antinode_positions(antinodes, current, (delta_row, delta_col))
                # Direction 2: Start at (r1, c1) and go "backwards"
                antinodes = self._loop_antinode_positions(antinodes, current, (delta_row * -1, delta_col * -1))
        return antinodes

    def _is_within_bounds(self, node: tuple[int, int]) -> bool:
        row, col = node
        return 0 <= row < self.rows and 0 <= col < self.cols

    def _loop_antinode_positions(self, antinodes: Antinodes, current: tuple[int, int], delta: tuple[int, int]) -> Antinodes:
        while self._is_within_bounds(current):
            antinodes.add(current)
            current = (current[0] + delta[0], current[1] + delta[1])
        return antinodes


def _parse(lines: list[str]):
    antennas = defaultdict(list)
    rows = len(lines)
    cols = len(lines[0])
    for row, line in enumerate(lines):
        if not line.strip():
            continue
        for col, char in enumerate(line):
            if char not in ["."]:
                antennas[char].append((row, col))
    return Grid(antennas, rows, cols)


def solve_part_one(grid: Grid) -> None:
    antinodes: Antinodes = grid.get_antinode_positions()
    result: int = len(antinodes)
    # 14 / 367
    print(f"Result part 1: {result}")


def solve_part_two(grid: Grid) -> None:
    antinodes: Antinodes = grid.get_resonant_antinode_positions()
    result: int = len(antinodes)
    # 34 / 1285
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines: list[str] = import_data(FILE)
    grid: Grid = _parse(lines)
    solve_part_one(grid)
    solve_part_two(grid)
    calculate_duration()
