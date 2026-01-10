# Advent of Code 2023 - Day 21
import sys
from dataclasses import dataclass
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.utils import calculate_duration, import_data

FILE = "./datas/day21_debug.txt"
# FILE = "./datas/day21.txt"
DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
OFFSET = 65  # von Startpunkt
PERIOD = 131  # Grid länge
STEPS = 26501365  # für part 2
# steps / länge
EXPANSION_FACTOR = (STEPS - OFFSET) // PERIOD


@dataclass
class Garden:
    plots: set[tuple[int, int]]
    start: tuple[int, int]
    width: int
    height: int


def _parse(lines: list[str]) -> Garden:
    plots = set()
    start_pos = None
    height = len(lines)
    width = len(lines[0].strip())

    for pos_y, line in enumerate(lines):
        for pos_x, char in enumerate(line.strip()):
            if char == ".":
                plots.add((pos_x, pos_y))
            elif char == "S":
                start_pos = (pos_x, pos_y)
                plots.add((pos_x, pos_y))

    return Garden(plots=plots, start=start_pos, width=width, height=height)


def _process_mystery_one(garden: Garden, steps: int = 64) -> int:
    current_positions = {garden.start}

    for _ in range(steps):
        current_positions = _calculate_positions(garden, current_positions)

    return len(current_positions)


def _calculate_positions(garden: Garden, current_positions: set[tuple[int, int]]) -> set[tuple[int, int]]:
    next_positions = set()
    for pos_x, pos_y in current_positions:
        for dir_x, dir_y in DIRECTIONS:
            next_pos_x, next_pos_y = pos_x + dir_x, pos_y + dir_y
            if (next_pos_x % garden.width, next_pos_y % garden.height) in garden.plots:
                next_positions.add((next_pos_x, next_pos_y))

    return next_positions


def _process_mystery_two(garden: Garden) -> list[int]:
    current_positions = {garden.start}
    values = []

    goals = [OFFSET + i * PERIOD for i in range(3)]

    for step in range(1, goals[-1] + 1):
        current_positions = _calculate_positions(garden, current_positions)

        if step in goals:
            values.append(len(current_positions))

    return values


def solve_mystery_one(garden: Garden) -> None:
    result = _process_mystery_one(garden)
    # 16 mit 6 Steps, 42 / 3617
    print(f"Result mystery 1: {result}")


def solve_mystery_two(garden: Garden) -> None:
    # die Zahl die Anzahl der vollständigen Zyklen der Gitterbreite berechnen (KI Hilfe gebraucht)
    # Quadratische Interpolation basierend auf 3 Datenpunkten:
    # f(n) = a₀ + a₁*n + a₂*n*(n-1)/2
    # Wobei: a₀ = a
    #        a₁ = b (erste Differenz)
    #        a₂ = c (zweite Differenz)
    values = _process_mystery_two(garden)
    a = values[0]
    b = values[1] - values[0]
    c = (values[2] - values[1]) - (values[1] - values[0])

    result = a + EXPANSION_FACTOR * b + (EXPANSION_FACTOR * (EXPANSION_FACTOR - 1) // 2) * c
    # 596857397104703
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    garden = _parse(lines)
    solve_mystery_one(garden)
    solve_mystery_two(garden)
    calculate_duration()
