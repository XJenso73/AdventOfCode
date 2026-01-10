import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration, import_data

# FILE = "./datas/day01_debug.txt"
FILE = "./datas/day01.txt"


def _get_next_possition(direction: str, possition: int, count: int) -> int:
    return (possition - count) % 100 if direction == "L" else (possition + count) % 100


def calculate_mystery_one(input: list[str]) -> None:
    possition = 50
    result = 0

    for _, value in enumerate(input):
        direction, count = (value[0], int(value[1:]))
        possition = _get_next_possition(direction, possition, count)
        if possition == 0:
            result += 1
    print(f"Result mystery 1: {result}")


def _create_rotations(lines: list[str]) -> None:
    return [(value[0].upper(), int(value[1:])) for _, value in enumerate(lines)]


def calculate_mystery_two(lines: list[str], start: int = 50) -> None:
    rotations = _create_rotations(lines)
    position = start
    zero_hits = 0

    for direction, clicks in rotations:
        step = 1 if direction == "L" else -1

        for _ in range(clicks):
            position = (position + step) % 100
            if position == 0:
                zero_hits += 1

    print(f"Result mystery 2: {zero_hits}")


if __name__ == "__main__":
    lines = import_data(FILE)
    # Part 1
    calculate_mystery_one(lines)
    # Part 2
    calculate_mystery_two(lines)
    calculate_duration()
