# Advent of Code 2024 - Day 12
import sys
from dataclasses import dataclass
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration, import_data

FILE = "./datas/day12_debug.txt"
# FILE = "./datas/day12.txt"
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

type Visited = set[tuple[int, int]]
type Coord = tuple[int, int]
type Region = dict[str, str | set[Coord]]


@dataclass()
class Grid:
    cells: dict[tuple[int, int], str]
    rows: int
    cols: int

    def __post_init__(self):
        self.region = self._find_regions()

    @staticmethod
    def next_coord(current, direction):
        return (current[0] + direction[0], current[1] + direction[1])

    def _find_regions(self) -> list[Region]:
        visited = set()
        region = []

        for coord, char in self.cells.items():
            if coord not in visited:
                visited, region_coords = self._find_neighbors(coord, char, visited)
                region.append({"char": char, "coords": set(region_coords)})

        return region

    def _find_neighbors(self, start: Coord, char: str, visited: Visited) -> list[Coord]:
        stack = [start]
        region_coords = []

        while stack:
            coord = stack.pop()
            if coord in visited or self.cells.get(coord) != char:
                continue

            visited.add(coord)
            region_coords.append(coord)

            # Add all valid neighbors to stack
            stack.extend(
                next_coord
                for direction in DIRECTIONS
                if (next_coord := self.next_coord(coord, direction)) in self.cells
                and next_coord not in visited
                and self.cells[next_coord] == char
            )

        return visited, region_coords


def _parse(lines: list[str]) -> Grid:
    cells = {(r, c): char for r, line in enumerate(lines) for c, char in enumerate(line)}
    return Grid(cells, len(lines), len(lines[0]) if lines else 0)


def _calculate_part_one(grid: Grid) -> int:
    result = 0
    for region in grid.region:
        coords = region.get("coords", [])
        total_perimeter = sum(1 for coord in coords for direction in DIRECTIONS if Grid.next_coord(coord, direction) not in coords)
        result += total_perimeter * len(coords)
    return result


def _calculate_part_two(grid: Grid) -> int:
    result = 0
    for region in grid.region:
        coords_set = region.get("coords", [])
        area = len(coords_set)
        total_corners = 0

        for row, col in coords_set:
            corners_to_check = [
                ((row - 1, col), (row, col - 1), (row - 1, col - 1)),
                ((row - 1, col), (row, col + 1), (row - 1, col + 1)),
                ((row + 1, col), (row, col - 1), (row + 1, col - 1)),
                ((row + 1, col), (row, col + 1), (row + 1, col + 1)),
            ]

            for side_a, side_b, diag in corners_to_check:
                is_a_in = side_a in coords_set
                is_b_in = side_b in coords_set
                is_diag_in = diag in coords_set

                # Outer corner: Both adjacent sides are outside the region
                if not is_a_in and not is_b_in or is_a_in and is_b_in and not is_diag_in:
                    total_corners += 1

        result += total_corners * area
    return result


def solve_part_one(grid: Grid) -> None:
    result = _calculate_part_one(grid)
    # 1930 / 1402544
    print(f"Result part 1: {result}")


def solve_part_two(grid: Grid) -> None:

    result = _calculate_part_two(grid)
    # 1206 / 862486
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    grid = _parse(lines)

    solve_part_one(grid)
    solve_part_two(grid)
    calculate_duration()
