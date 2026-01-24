# Advent of Code 2024 - Day 15
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from dataclasses import dataclass
from typing import Self

from src.utils import calculate_duration, import_data


@dataclass(frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: int) -> Self:
        return Position(self.x + other.x, self.y + other.y)

    @property
    def gps(self) -> int:
        """GPS coordinate: 100 * y + x"""
        return self.y * 100 + self.x


@dataclass(frozen=True)
class Workflow:
    movements: str
    robot_position: Position
    grid: dict[Position, str]


FILE = "./datas/day15_debug.txt"
# FILE = "./datas/day15.txt"
DIRECTIONS = {"^": Position(0, -1), "v": Position(0, 1), "<": Position(-1, 0), ">": Position(1, 0)}
SCALE_MAP = {"#": ("##"), "O": ("[]"), ".": (".."), "@": ("@.")}


def _parse_part_one(lines: list[str]) -> Workflow:
    split_index = lines.index("")
    grid_lines, movement_lines = lines[:split_index], lines[split_index + 1 :]
    movements = "".join(movement_lines)
    grid = {Position(x, y): char for y, line in enumerate(grid_lines) for x, char in enumerate(line)}

    robot_pos = next(pos for pos, char in grid.items() if char == "@")
    return Workflow(movements, robot_pos, grid)


def _calculation_part_one(workflow: Workflow) -> int:
    grid = dict(workflow.grid)
    current_position = workflow.robot_position

    for move in workflow.movements:
        delta = DIRECTIONS[move]
        next_pos = current_position + delta

        match grid.get(next_pos):
            case ".":
                grid[current_position], grid[next_pos] = ".", "@"
                current_position = next_pos

            case "O":
                # Finde ersten freien Platz in Bewegungsrichtung
                check_pos = next_pos
                while grid.get(check_pos) == "O":
                    check_pos += delta

                if grid.get(check_pos) == ".":
                    grid[check_pos] = "O"
                    grid[next_pos] = "@"
                    grid[current_position] = "."
                    current_position = next_pos

    return sum(pos.gps for pos, char in grid.items() if char == "O")


def _parse_part_two(lines: list[str]) -> Workflow:
    split_index = lines.index("")
    grid_lines, movement_lines = lines[:split_index], lines[split_index + 1 :]

    movements = "".join(movement_lines)

    grid = {
        Position(x * 2 + offset, y): scaled_char
        for y, line in enumerate(grid_lines)
        for x, char in enumerate(line)
        for offset, scaled_char in enumerate(SCALE_MAP[char])
    }

    robot_pos = next(pos for pos, char in grid.items() if char == "@")
    return Workflow(movements, robot_pos, grid)


def _calculation_part_two(workflow: Workflow) -> int:
    grid = dict(workflow.grid)
    current_position = workflow.robot_position

    for move in workflow.movements:
        delta = DIRECTIONS[move]
        to_move = set()  # Changed to set

        if _can_move(grid, current_position, delta, to_move):
            # Sort positions by movement direction for correct order
            if delta.y != 0:  # vertical
                sorted_moves = sorted(to_move, key=lambda p: p.y, reverse=(delta.y > 0))
            else:  # horizontal
                sorted_moves = sorted(to_move, key=lambda p: p.x, reverse=(delta.x > 0))

            for p in sorted_moves:
                grid[p + delta] = grid[p]
                grid[p] = "."
            current_position += delta

    return sum(pos.gps for pos, char in grid.items() if char == "[")


def _can_move(
    grid: dict[Position, str],
    pos: Position,
    delta: Position,
    to_move: set[Position],  # Changed to set
) -> bool:
    """Recursively checks if a move is possible and collects all affected positions."""
    if pos in to_move:
        return True

    char = grid.get(pos)

    match char:
        case ".":
            return True
        case "#":
            return False
        case None:
            return False

    to_move.add(pos)  # Changed to add

    # For vertical moves, include the other half of boxes
    if delta.y != 0 and char in "[]":
        other_half = pos + Position(1 if char == "[" else -1, 0)
        if not _can_move(grid, other_half, delta, to_move):
            return False

    return _can_move(grid, pos + delta, delta, to_move)


def solve_part_one(lines: list[str]) -> None:
    work_flow: Workflow = _parse_part_one(lines)
    result = _calculation_part_one(work_flow)
    # 10092 / 1457740
    print(f"Result part 1: {result}")


def solve_part_two(lines: list[str]) -> None:
    work_flow: Workflow = _parse_part_two(lines)
    result = _calculation_part_two(work_flow)
    # 9021 / 1467145
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines: list[str] = import_data(FILE)
    solve_part_one(lines)
    solve_part_two(lines)
    calculate_duration()
