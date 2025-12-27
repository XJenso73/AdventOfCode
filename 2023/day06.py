# Advent of Code 2023 - Day 06
import math
import re

from src.utils import calculate_duration, import_data

FILE = "./datas/day06_debug.txt"
FILE = "./datas/day06.txt"
PATTERN = re.compile(r"\d+")


def solve_mystery_one(lines: list[str]) -> None:
    data = _parse_datas(lines)
    times = data.get(0, [])
    records = data.get(1, [])
    result = _calculate_result(times, records)
    # 288 / 1312850
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    data = _parse_datas(lines)
    times = [int("".join(map(str, data.get(0, []))))]
    records = [int("".join(map(str, data.get(1, []))))]
    result = _calculate_result(times, records)
    # 71503 / 36749103
    print(f"Result mystery 2: {result}")


def _parse_datas(lines: list[str]) -> dict[int, list[int]]:
    data = {}
    for idx, line in enumerate(lines):
        data[idx] = list(map(int, PATTERN.findall(line)))
    return data


def _calculate_result(times, records):
    count_of_new_records = []

    for T, R in zip(times, records, strict=False):
        # Diskriminante berechnen
        discriminant = math.sqrt(T**2 - 4 * R)

        # Die theoretischen Grenzen (Nullstellen)
        h1 = (T - discriminant) / 2
        h2 = (T + discriminant) / 2

        # suche die kleinste Ganzzahl, die GRÖSSER als h1 ist
        # die größte Ganzzahl, die KLEINER als h2 ist
        # +1e-9 (oder +1) fängt Fälle ab, in denen h genau eine Ganzzahl ist
        low = math.floor(h1 + 1)
        high = math.ceil(h2 - 1)

        count_of_new_records.append(high - low + 1)

    return math.prod(count_of_new_records)


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)
    calculate_duration()
