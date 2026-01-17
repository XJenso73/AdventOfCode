# Advent of Code 2024 - Day 13
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from dataclasses import dataclass
from functools import cached_property

from src.utils import calculate_duration, import_data


@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int


@dataclass(frozen=True)
class Game:
    button_a: Coordinate
    button_b: Coordinate
    prize: Coordinate

    @cached_property
    def determinant(self) -> int:
        """The determinant is independent of the prize/offset."""
        return self.button_a.x * self.button_b.y - self.button_a.y * self.button_b.x

    @staticmethod
    def is_non_negative_integer(a: float, b: float) -> bool:
        return a >= 0 and b >= 0 and a.is_integer() and b.is_integer()

    def solve(self, offset: int) -> int | None:
        """
        Solves the system of equations using Cramer's rule.
        Returns the minimum tokens (3*a + 1*b) or None if no integer solution exists.
        """
        target_x = self.prize.x + offset
        target_y = self.prize.y + offset

        # Determinant of the coefficient matrix
        # | ax bx |
        # | ay by |
        det = self.determinant  # self.button_a.x * self.button_b.y - self.button_a.y * self.button_b.x

        if det == 0:
            return None

        # Cramer's rule for a and b
        # det_a = | target_x  bx |
        #         | target_y  by |
        a = (target_x * self.button_b.y - target_y * self.button_b.x) / det
        b = (self.button_a.x * target_y - self.button_a.y * target_x) / det

        # Check if solutions are non-negative integers
        if Game.is_non_negative_integer(a, b):
            return int(a) * 3 + int(b)

        return None


FILE = "./datas/day13_debug.txt"
FILE = "./datas/day13.txt"


def _parse(lines: list[str]) -> list[Game]:
    games: list[Game] = []
    coords = []
    for line in lines:
        line = line.replace(" ", "").strip()
        if not line:
            games.append(Game(coords[0], coords[1], coords[2]))
            coords = []
            continue

        coords.append(_get_coords(line))

    if coords:
        games.append(Game(coords[0], coords[1], coords[2]))

    return games


def _get_coords(line: str) -> Coordinate:
    _, values = line.split(":")
    x, y = (int(v.split("+" if "+" in v else "=")[1]) for v in values.split(","))
    return Coordinate(x, y)


def calculate_total_costs(games: list[Game], offset: int = 0) -> int:
    return sum(cost for game in games if (cost := game.solve(offset)) is not None)


def solve_part_one(games: list[Game]) -> None:
    result = calculate_total_costs(games)
    # 480 / 31623
    print(f"Result part 1: {result}")


def solve_part_two(games: list[Game]) -> None:
    result = calculate_total_costs(games, offset=10000000000000)
    # 875318608908 / 93209116744825
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines: list[str] = import_data(FILE)
    games: list[Game] = _parse(lines)
    solve_part_one(games)
    solve_part_two(games)
    calculate_duration()
