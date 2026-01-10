# Advent of Code 2023 - Day 18
# from shapely.geometry import Polygon
import sys
from dataclasses import dataclass
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.utils import calculate_duration, import_data


@dataclass(frozen=True, slots=True)
class Points:
    last_pos_x: int
    last_pos_y: int
    direction: str
    meters: int


DIRECTIONS = {
    "d": lambda x, y, me: (x, y + me),
    "u": lambda x, y, me: (x, y - me),
    "r": lambda x, y, me: (x + me, y),
    "l": lambda x, y, me: (x - me, y),
}

FILE = "./datas/day18_debug.txt"
# FILE = "./datas/day18.txt"


def _parse_mystery_one(lines: list[str]) -> list[tuple[int, int, str]]:
    cords = []
    current_point = (0, 0)
    for line in lines:
        direction, meters, _ = line.strip().split()
        new_point = _get_new_point(Points(current_point[0], current_point[1], direction, int(meters)))
        cords.append(new_point)
        current_point = (new_point[0], new_point[1])
    return cords


def _get_new_point(state: Points) -> tuple[int, int, str]:
    logic = DIRECTIONS.get(state.direction.lower())
    if logic:
        return logic(state.last_pos_x, state.last_pos_y, state.meters)

    raise ValueError(f"Direction {state.direction} is unknown")


def _calculate_area(grid: list[tuple[int, int, str]]) -> int:
    # Wir brauchen den Startpunkt (0,0) am Anfang der Liste
    points = [(0, 0)] + [(c[0], c[1]) for c in grid]

    # Shoelace Formula für die Fläche
    area = 0
    perimeter = 0

    for idx in range(len(points) - 1):
        current_pos_x, current_pos_y = points[idx]
        next_pos_x, next_pos_y = points[idx + 1]

        # Shoelace Kern Kreuzprodukt der Koordinaten
        area += (current_pos_x * next_pos_y) - (next_pos_x * current_pos_y)

        # Umfang berechnen
        perimeter += abs(next_pos_x - current_pos_x) + abs(next_pos_y - current_pos_y)

    area = abs(area) // 2

    # Satz von Pick:
    # Die tatsächlichen Felder sind die Innenfläche + halber Rand + 1
    return area + (perimeter // 2) + 1


def _parse_mystery_two(lines: list[str]) -> list[tuple[int, int, str]]:
    cords = []
    current_point = (0, 0)
    for line in lines:
        line = line.strip()
        _, colors = line.strip(")").split("#")
        direction, meters = _extract_direction_meters_from_color(colors)
        new_point = _get_new_point(Points(current_point[0], current_point[1], direction, meters))
        cords.append(new_point)
        current_point = (new_point[0], new_point[1])
    return cords


def _extract_direction_meters_from_color(color: str) -> tuple[str, int]:
    direction_map = {0: "R", 1: "D", 2: "L", 3: "U"}
    decimal_value = int(color[:-1], 16)
    return (direction_map[int(color[-1])], decimal_value)


def solve_mystery_one(lines: list[str]) -> None:
    grid = _parse_mystery_one(lines)
    result = _calculate_area(grid)
    # 62 / 49061
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    grid = _parse_mystery_two(lines)
    result = _calculate_area(grid)
    # 952408144115 / 92556825427032
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)
    calculate_duration()
