# Advent of Code 2023 - Day 24
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from z3 import Real, Solver

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))


from src.utils import calculate_duration, import_data

FILE = "./datas/day24_debug.txt"
# FILE = "./datas/day24.txt"
PATTERN = re.compile(r"(\d+),(\d+),(\d+)\s*@\s*(-?\d+),(-?\d+),(-?\d+)")


@dataclass
class Hailstones:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int

    @property
    def slope(self) -> float:
        if self.vx:
            return self.vy / self.vx
        return 0

    @property
    def vertical_shift(self) -> float:
        return self.py - self.slope * self.px


def _parse(lines: list[str]) -> list[Hailstones]:
    hailstones = []
    for line in lines:
        if match := PATTERN.search(line.replace(" ", "")):
            px, py, pz, vx, vy, vz = map(int, match.groups())
            hailstones.append(Hailstones(px, py, pz, vx, vy, vz))
    return hailstones


def _calculate_part_one(hailstones: list[Hailstones], min_pos: int, max_pos: int) -> int:
    intersect_count = 0
    for idx in range(len(hailstones)):
        for next_idx in range(idx + 1, len(hailstones)):
            hailstone_one = hailstones[idx]
            hailstone_two = hailstones[next_idx]

            if hailstone_one.slope == hailstone_two.slope:  # Parallel lines
                continue
            if hailstone_one.vx == 0 or hailstone_two.vx == 0:
                continue
            # Intersection point
            # m1 * x + c1 = m2 * x + c2
            intersection_p1 = (hailstone_two.vertical_shift - hailstone_one.vertical_shift) / (hailstone_one.slope - hailstone_two.slope)
            intersection_p2 = hailstone_one.slope * intersection_p1 + hailstone_one.vertical_shift

            # Check if intersection is in the future for both hailstones
            in_future_h1 = _is_future(hailstone_one, intersection_p1)
            in_future_h2 = _is_future(hailstone_two, intersection_p1)
            in_bounds_h1 = _is_in_bounds(min_pos, intersection_p1, max_pos)
            in_bounds_h2 = _is_in_bounds(min_pos, intersection_p2, max_pos)
            if in_future_h1 and in_future_h2 and in_bounds_h1 and in_bounds_h2:
                intersect_count += 1

    return intersect_count


def _is_future(hailstone: Hailstones, intersection: float) -> bool:
    return (intersection - hailstone.px) / hailstone.vx > 0


def _is_in_bounds(min_pos: int, intersection: float, max_pos: int) -> bool:
    return min_pos <= intersection <= max_pos


def _calculate_part_two(hailstones: list[Hailstones]) -> int | None:
    # Variables for the rock's starting position and velocity
    rx, ry, rz = Real("rx"), Real("ry"), Real("rz")
    rvx, rvy, rvz = Real("rvx"), Real("rvy"), Real("rvz")

    solver = Solver()

    # We only need a few hailstones to find the unique solution for the rock
    for idx, hailstone in enumerate(hailstones[:5]):
        # Time variable for each hailstone intersection
        time = Real(f"t_{idx}")

        # The rock and the hailstone must be at the same position at time t
        # p_rock + v_rock * t = p_hail + v_hail * t
        solver.add(rx + rvx * time == hailstone.px + hailstone.vx * time)
        solver.add(ry + rvy * time == hailstone.py + hailstone.vy * time)
        solver.add(rz + rvz * time == hailstone.pz + hailstone.vz * time)
        solver.add(time >= 0)

    if solver.check() == sys.modules["z3"].sat:
        model = solver.model()
        # Sum of X, Y, Z coordinates
        return model.eval(rx + ry + rz).as_long()
    return None


def solve_mystery_one(hailstones: list[Hailstones]) -> None:
    min_bound, max_bound = (7, 27) if len(hailstones) < 10 else (200000000000000, 400000000000000)
    result = _calculate_part_one(hailstones, min_bound, max_bound)
    print(f"Result mystery 1: {result}")


def solve_mystery_two(hailstones: list[Hailstones]) -> None:
    result = _calculate_part_two(hailstones)
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    hailstones = _parse(lines)
    solve_mystery_one(hailstones)
    solve_mystery_two(hailstones)
    calculate_duration()
