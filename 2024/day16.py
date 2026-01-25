# Advent of Code 2024 - Day 16
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

import heapq
from collections import deque
from dataclasses import dataclass
from typing import Self

import numpy as np

from src.utils import calculate_duration, import_data


@dataclass(frozen=True, slots=True)  # slots für weniger Memory + Speed
class Position:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Position(self.x + other.x, self.y + other.y)

    def as_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)


@dataclass(frozen=True, slots=True)
class State:
    position: Position
    direction: int

    def __lt__(self, other: Self) -> bool:
        return (self.position.x, self.position.y, self.direction) < (other.position.x, other.position.y, other.direction)


FILE = "./datas/day16_debug.txt"
# FILE = "./datas/day16.txt"

DIRECTION_DELTAS = [
    (0, -1),  # 0: North
    (1, 0),  # 1: East
    (0, 1),  # 2: South
    (-1, 0),  # 3: West
]


@dataclass(frozen=True)
class Workflow:
    grid: set[tuple[int, int]]
    start: tuple[int, int]
    end: tuple[int, int]
    width: int
    height: int


def _parse(lines: list[str]) -> Workflow:
    """Parse maze - nur freie Felder speichern."""
    free_cells = set()
    start = end = None
    height = len(lines)
    width = len(lines[0]) if lines else 0

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != "#":
                free_cells.add((x, y))
                if char == "S":
                    start = (x, y)
                elif char == "E":
                    end = (x, y)

    if start is None or end is None:
        raise ValueError("Start or End not found")

    return Workflow(free_cells, start, end, width, height)


def _find_shortest_path(work_flow: Workflow) -> tuple[int, int]:
    """Optimierte Dijkstra mit numpy array für costs."""
    grid = work_flow.grid
    start_pos = work_flow.start
    end_pos = work_flow.end

    INF = 10**9
    width, hight = work_flow.width, work_flow.height

    # costs[y][x][dir]
    costs = np.full((hight, width, 4), INF, dtype=np.int32)

    # Start: facing East (direction 1)
    costs[start_pos[1], start_pos[0], 1] = 0

    # Priority queue: (cost, x, y, direction)
    pq = [(0, start_pos[0], start_pos[1], 1)]

    # Predecessors nur für Part 2
    predecessors = {}

    min_end_cost = INF
    end_states = []

    while pq:
        cost, x, y, direction = heapq.heappop(pq)

        if cost > costs[y, x, direction]:
            continue

        # Ziel erreicht?
        if (x, y) == end_pos:
            if cost < min_end_cost:
                min_end_cost = cost
                end_states = [(x, y, direction)]
            elif cost == min_end_cost:
                end_states.append((x, y, direction))
            continue

        # Vorwärts bewegen
        dx, dy = DIRECTION_DELTAS[direction]
        nx, ny = x + dx, y + dy

        if (nx, ny) in grid:
            new_cost = cost + 1
            if new_cost <= costs[ny, nx, direction]:
                if new_cost < costs[ny, nx, direction]:
                    costs[ny, nx, direction] = new_cost
                    predecessors[(nx, ny, direction)] = []
                predecessors[(nx, ny, direction)].append((x, y, direction))
                heapq.heappush(pq, (new_cost, nx, ny, direction))

        # Drehungen (links und rechts)
        for turn_delta in [-1, 1]:  # -1=links, 1=rechts
            new_dir = (direction + turn_delta) % 4
            new_cost = cost + 1000

            if new_cost <= costs[y, x, new_dir]:
                if new_cost < costs[y, x, new_dir]:
                    costs[y, x, new_dir] = new_cost
                    predecessors[(x, y, new_dir)] = []
                predecessors[(x, y, new_dir)].append((x, y, direction))
                heapq.heappush(pq, (new_cost, x, y, new_dir))

    tiles_on_path = set()
    queue = deque(end_states)
    visited = set(end_states)

    while queue:
        state = queue.popleft()
        x, y, d = state
        tiles_on_path.add((x, y))

        for pred in predecessors.get(state, []):
            if pred not in visited:
                visited.add(pred)
                queue.append(pred)

    return min_end_cost, len(tiles_on_path)


def solve_part_one(work_flow: Workflow) -> None:
    result, _ = _find_shortest_path(work_flow)
    print(f"Result part 1: {result}")


def solve_part_two(work_flow: Workflow) -> None:
    _, result = _find_shortest_path(work_flow)
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    work_flow = _parse(lines)
    solve_part_one(work_flow)
    solve_part_two(work_flow)
    calculate_duration()
