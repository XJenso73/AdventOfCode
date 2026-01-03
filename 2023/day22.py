# Advent of Code 2023 - Day 22
import re
from collections import deque
from dataclasses import dataclass
from functools import cached_property

from src.utils import calculate_duration, import_data

FILE = "./datas/day22_debug.txt"
FILE = "./datas/day22.txt"
PATTERN = re.compile(r"(\d+),(\d+),(\d+)~(\d+),(\d+),(\d+)")

type SupportGraph = dict[int, set[int]]


@dataclass
class Brick:
    id: int
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

    def __lt__(self, other: "Brick") -> bool:
        return self.z1 < other.z1

    @property
    def height(self) -> int:
        return self.z2 - self.z1 + 1

    @cached_property
    def occupied_xy(self) -> set[tuple[int, int]]:
        # Gibt alle (x,y) Paare zurück, die dieser Brick belegt
        return {(x, y) for x in range(self.x1, self.x2 + 1) for y in range(self.y1, self.y2 + 1)}


def _parse(lines: list[str]) -> list[Brick]:
    bricks = []
    for idx, line in enumerate(lines):
        if match := PATTERN.search(line):
            x1, y1, z1, x2, y2, z2 = map(int, match.groups())
            bricks.append(Brick(idx, min(x1, x2), min(y1, y2), min(z1, z2), max(x1, x2), max(y1, y2), max(z1, z2)))

    return sorted(bricks)


def _settle(bricks: list[Brick]) -> tuple[SupportGraph, SupportGraph]:
    height_map: dict[tuple[int, int], tuple[int, int]] = {}
    supports = {b.id: set() for b in bricks}
    supported_by = {b.id: set() for b in bricks}

    for brick in bricks:
        coords = brick.occupied_xy

        # Max height and supporting bricks in one pass
        max_height = 0
        supporters = set()
        for pos_x, pos_y in coords:
            height, bid = height_map.get((pos_x, pos_y), (0, -1))
            if height > max_height:
                max_height, supporters = height, {bid} if bid != -1 else set()
            elif height == max_height and bid != -1:
                supporters.add(bid)

        # Update relationships
        for sid in supporters:
            supports[sid].add(brick.id)
            supported_by[brick.id].add(sid)

        # Update height map
        new_height = max_height + brick.height
        for pos_x, pos_y in coords:
            height_map[(pos_x, pos_y)] = (new_height, brick.id)

    return supports, supported_by


def _is_safe(brick_id: int, supports: SupportGraph, supported_by: SupportGraph) -> bool:
    return all(len(supported_by[b]) > 1 for b in supports[brick_id])


def solve_mystery_one(bricks: list[Brick], supports: SupportGraph, supported_by: SupportGraph) -> None:
    result = sum(_is_safe(brick.id, supports, supported_by) for brick in bricks)
    # 5 / 457
    print(f"Result mystery 1: {result}")


def solve_mystery_two(bricks: list[Brick], supports: SupportGraph, supported_by: SupportGraph) -> None:
    result = 0
    for start_brick in bricks:
        fallen = {start_brick.id}
        queue = deque(supports[start_brick.id])

        while queue:
            current_id = queue.popleft()

            if current_id in fallen:
                continue

            if supported_by[current_id] <= fallen:  # Set subset check
                fallen.add(current_id)
                queue.extend(s for s in supports[current_id] if s not in fallen)

        result += len(fallen) - 1
    # 7 / 79122
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    bricks = _parse(lines)
    supports, supported_by = _settle(bricks)
    solve_mystery_one(bricks, supports, supported_by)
    solve_mystery_two(bricks, supports, supported_by)
    calculate_duration()
