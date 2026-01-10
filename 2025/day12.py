import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration, import_data

FILE = "./datas/day12_debug.txt"
# FILE = "./datas/day12.txt"


def solve_mystery_one(lines: list[str]) -> int:
    result = _calculate(lines)
    print(f"Result mystery 1: {result}")


def _calculate(lines: list[str]) -> int:
    standard_presents, data = _parse(lines)

    result = 0
    for line in data:
        dimension, present_index = line.split(":")
        width, height = map(int, dimension.lower().split("x"))
        numbers_of_present_index = list(map(int, present_index.strip().split(" ")))
        used_space = width * height
        minimal_space_is_needed = sum(
            present_index * "".join(standard_presents[idx]).count("#") for idx, present_index in enumerate(numbers_of_present_index)
        )
        if minimal_space_is_needed < used_space:
            result += 1
    return result


def _parse(lines: list[str]) -> tuple[dict[int, list[str]], list[str]]:
    standard_presents = {}
    data = []
    current_index = None
    for line in lines:
        line = line.rstrip()
        if not line:
            continue

        if "x" in line.lower():
            data.append(line)
        elif ":" in line:
            current_index = int(line[:-1])
            standard_presents[current_index] = []
        elif current_index is not None:
            standard_presents[current_index].append(line)
    return standard_presents, data


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)

    calculate_duration()
