# Advent of Code 2023 - Day 15
from collections import defaultdict

from src.utils import calculate_duration, import_data

FILE = "./datas/day15_debug.txt"
FILE = "./datas/day15.txt"


def parse(lines: list[str]):
    return next((line.split(",") for line in lines if line.strip()), [])


def _calculate_mystery_one(data: list[str]):
    hash_values = []
    for field_value in data:
        hash_values.append(_get_hash(field_value))
    return sum(hash_values)


def _get_hash(field_value: str) -> int:
    value = 0
    for char in field_value:
        value += _get_ascii_count(char)
        value = _get_calculated_count(value)
    return value


def _get_ascii_count(char: str) -> int:
    return ord(char)


def _get_calculated_count(curent: int) -> int:
    curent *= 17
    curent %= 256
    return curent


def _calculate_mystery_two(data: list[str]) -> int:
    boxes = _create_boxes(data)
    result = 0
    for box_nr, lenses in boxes.items():
        for slot_nr, focal_length in enumerate(lenses.values(), start=1):
            result += (box_nr + 1) * slot_nr * focal_length
    return result


def _create_boxes(data: list[str]) -> dict[int, dict[str, int]]:
    boxes = defaultdict(dict)
    for step in data:
        if "-" in step:
            label = step[:-1]
            box_number = _get_hash(label)
            boxes[box_number].pop(label, None)

        elif "=" in step:
            label, focal_length = step.split("=")
            box_number = _get_hash(label)
            boxes[box_number][label] = int(focal_length)
    return boxes


def solve_mystery_one(chars: list[str]) -> None:
    result = _calculate_mystery_one(chars)
    # 1320 / 522547
    print(f"Result mystery 1: {result}")


def solve_mystery_two(chars: list[str]) -> None:
    result = _calculate_mystery_two(chars)
    # 145 /
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    chars = parse(lines)
    solve_mystery_one(chars)
    solve_mystery_two(chars)
    calculate_duration()
