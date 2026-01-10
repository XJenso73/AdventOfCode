import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration, import_data

FILE = "./datas/day03_debug.txt"
# FILE = "./datas/day03.txt"


def _highest_digit(s: str) -> int:
    digits = [int(c) for c in s if c.isdigit()]
    return max(digits)


def _get_highest_and_position(line: str) -> tuple[int, int]:
    digit = _highest_digit(line)
    index = line.index(str(digit))
    return (digit, index)


def _get_complete_number(a: int, b: int) -> int:
    return a * 10 + b


def calculate_mystery_one(lines: list[str]) -> None:
    all_numbers = []
    for line in lines:
        digit_a, index = _get_highest_and_position(line[:-1])
        digit_b = _highest_digit(line[index + 1 :])
        all_numbers.append(_get_complete_number(digit_a, digit_b))
    print(f"Result mystery 1: {sum(all_numbers)}")


def calculate_mystery_two(lines: list[str]) -> None:
    all_numbers = []
    for line in lines:
        all_digs = []
        for i in range(11, 0, -1):
            digt, index = _get_highest_and_position(line[:-i])
            all_digs.append(digt)
            line = line[index + 1 :]
        digt, index = _get_highest_and_position(line)
        all_digs.append(digt)
        all_numbers.append(int("".join([str(d) for d in all_digs])))
    print(f"Result mystery 2: {sum(all_numbers)}")


if __name__ == "__main__":
    lines = import_data(FILE)
    calculate_mystery_one(lines)
    calculate_mystery_two(lines)
    calculate_duration()
