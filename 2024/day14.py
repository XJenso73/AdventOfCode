# Advent of Code 2024 - Day 14
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
import math
import re
from dataclasses import dataclass

from src.utils import calculate_duration, import_data

FILE = "./datas/day14_debug.txt"
GRID_WIDTH = 11
GRID_HEIGHT = 7
FILE = "./datas/day14.txt"
GRID_WIDTH = 101
GRID_HEIGHT = 103

# Regex-Erklärung:
# (?P<id>[a-z])      -> Gruppe 'id': Ein Buchstabe
# =                  -> Das Gleichheitszeichen
# (?P<x>-?\int+)     -> Gruppe 'x': Optionales Minus und Ziffern
# ,                  -> Das Komma
# (?P<y>-?\int+)     -> Gruppe 'y': Optionales Minus und Ziffern
PATTERN = re.compile(r"(?P<id>[a-z])=(?P<x>-?\d+),(?P<y>-?\d+)")


@dataclass(frozen=True)
class Robot:
    position: tuple[int, int]
    velocity: tuple[int, int]

    def new_position(self, seconds: int, width: int, height: int) -> tuple[int, int]:
        # Formula: (start + velocity * time) % boundary
        new_pos_x = (self.position[0] + self.velocity[0] * seconds) % width
        new_pos_y = (self.position[1] + self.velocity[1] * seconds) % height
        return (new_pos_x, new_pos_y)


def _parse(lines: list[str]) -> list[Robot]:
    robots: list[Robot] = []

    for line in lines:
        matches = PATTERN.findall(line)
        if len(matches) != 2:
            continue  # oder raise ValueError

        (px, py), (vx, vy) = (
            (int(matches[0][1]), int(matches[0][2])),
            (int(matches[1][1]), int(matches[1][2])),
        )
        robots.append(Robot((px, py), (vx, vy)))

    return robots


def _calculate_part_one(robots: list[Robot]) -> int:
    middle_x, middle_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
    quadrants = [0, 0, 0, 0]  # TopLeft, TopRight, BottomLeft, BottomRight

    for robot in robots:
        pos_x, pos_y = robot.new_position(100, GRID_WIDTH, GRID_HEIGHT)
        if pos_x == middle_x or pos_y == middle_y:
            continue  # Ignore robots on the lines

        # Determine quadrant index
        idx = (0 if pos_x < middle_x else 1) + (0 if pos_y < middle_y else 2)
        quadrants[idx] += 1

    return math.prod(quadrants)


def _calculate_part_two(robots: list[Robot]) -> int:
    # das Muster widerholt sich nach width * height
    for seconds in range(GRID_WIDTH * GRID_HEIGHT):
        positions = set()
        overlap = False

        for r in robots:
            position = r.new_position(seconds, GRID_WIDTH, GRID_HEIGHT)
            if position in positions:
                overlap = True
                break
            positions.add(position)

        # alle Roboter sind an einer einzigartigen Position:
        if not overlap:
            return seconds

    return -1


def solve_part_one(robots: list[Robot]) -> None:
    result = _calculate_part_one(robots)
    # 12 / 216772608
    print(f"Result part 1: {result}")


def solve_part_two(robots: list[Robot]) -> None:
    result = _calculate_part_two(robots)
    # 1 / 6888
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines: list[str] = import_data(FILE)
    robots: list[Robot] = _parse(lines)
    solve_part_one(robots)
    solve_part_two(robots)
    calculate_duration()
