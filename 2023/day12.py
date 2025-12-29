# Advent of Code 2023 - Day 12
from functools import cache

from src.utils import calculate_duration, import_data

FILE = "./datas/day12_debug.txt"
FILE = "./datas/day12.txt"
type ParsedData = list[tuple[str, tuple[int, ...]]]


def _parse(lines: list[str]) -> ParsedData:
    grid = []
    for line in lines:
        line = line.strip()
        config, order = line.split(" ")
        groups = tuple(map(int, order.split(",")))
        grid.append((config, groups))
    return grid


@cache
def _count_arrangements(config: str, groups: tuple[int, ...]) -> int:
    # keine Gruppen mehr übrig?
    if not groups:
        return 0 if "#" in config else 1

    # String leer, aber noch Gruppen übrig?
    if not config:
        return 0

    result = 0

    # aktuelle Zeichen ist ein '.' oder '?' wie einen '.' behandeln
    if config[0] in ".?":
        result += _count_arrangements(config[1:], groups)

    # aktuelle Zeichen ist ein '#' oder '?' wie ein '#' behandeln
    if config[0] in "#?":
        group_len = groups[0]

        if group_len <= len(config) and "." not in config[:group_len] and (group_len == len(config) or config[group_len] != "#"):
            # der Block passt, über den Block UND das Trennzeichen danach springen
            result += _count_arrangements(config[group_len + 1 :], groups[1:])

    return result


def _prepare_mystery_two(grid: ParsedData) -> ParsedData:
    return [("?".join([config] * 5), groups * 5) for config, groups in grid]


def solve_mystery_one(grid: ParsedData) -> None:
    result = sum(_count_arrangements(config, groups) for config, groups in grid)
    # 21 / 7191
    print(f"Result mystery 1: {result}")


def solve_mystery_two(grid: ParsedData) -> None:
    grid = _prepare_mystery_two(grid)
    result = sum(_count_arrangements(config, groups) for config, groups in grid)
    # 525152 / 6512849198636
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    grid = _parse(lines)
    solve_mystery_one(grid)
    solve_mystery_two(grid)
    calculate_duration()
