# Advent of Code 2023 - Day 14
from src.utils import calculate_duration, import_data

FILE = "./datas/day14_debug.txt"
FILE = "./datas/day14.txt"


def _parse_mystery_one(lines: list[str]) -> list[list[str]]:
    return [list(line) for line in lines]


def _calculate_mystery_one(lines: list[list[str]]) -> int:
    # Transponieren, Norden =>  Westen
    grid = [list(col) for col in zip(*lines, strict=False)]

    total_load = 0
    num_rows = len(lines)

    for row in grid:
        tilted_row = _tilt_line(row)
        total_load += sum(num_rows - idx for idx, char in enumerate(tilted_row) if char == "O")
    return total_load


def _tilt_line(line: list[str]) -> list[str]:
    sections = "".join(line).split("#")
    tilted_sections = []

    for section in sections:
        tilted_sections.append("".join(sorted(section, reverse=True)))

    return list("#".join(tilted_sections))


def _parse_mystery_two(lines: list[str]) -> list[tuple[str]]:
    return [tuple(line) for line in lines]


def _calculate_mystery_two(grid: list[tuple[str]]) -> int:
    num_rows = len(grid)
    history = {}
    total_cycles = 1000000000

    for i in range(total_cycles):
        grid = _run_full_cycle(grid)

        if grid in history:
            # Zyklus gefunden!
            start_index = history[grid]
            cycle_length = i - start_index

            # how many cycles can be skipped?
            remaining = (total_cycles - 1 - i) % cycle_length
            for _ in range(remaining):
                grid = _run_full_cycle(grid)
            break

        history[grid] = i

    return sum(row.count("O") * (num_rows - r_idx) for r_idx, row in enumerate(grid))


def _run_full_cycle(grid: tuple[str, ...]) -> tuple[str, ...]:
    """run a complete cycle, north, west, south and east"""

    # North
    grid = tuple("".join(col) for col in zip(*grid, strict=False))
    grid = _tilt_left(grid)
    # back transponieren
    grid = tuple("".join(col) for col in zip(*grid, strict=False))

    # West
    grid = _tilt_left(grid)

    # South like north but change sorting
    grid = tuple("".join(col) for col in zip(*grid, strict=False))
    # 'reverse=False' sort 'O' to the end
    grid = tuple("#".join("".join(sorted(s)) for s in row.split("#")) for row in grid)
    grid = tuple("".join(col) for col in zip(*grid, strict=False))

    # East like West, but change sorting
    grid = tuple("#".join("".join(sorted(s)) for s in row.split("#")) for row in grid)

    return grid


def _tilt_left(grid: tuple[str, ...]) -> tuple[str, ...]:
    result_grid = []
    for row in grid:
        sections = row.split("#")
        tilted_sections = "#".join("".join(sorted(s, reverse=True)) for s in sections)
        result_grid.append(tilted_sections)
    return tuple(result_grid)


def solve_mystery_one(lines: list[str]) -> None:
    lines = _parse_mystery_one(lines)
    result = _calculate_mystery_one(lines)
    # 136 / 106378
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[list[str]]) -> None:
    lines = _parse_mystery_two(lines)
    result = _calculate_mystery_two(lines)
    # 64 / 90795
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)
    calculate_duration()
