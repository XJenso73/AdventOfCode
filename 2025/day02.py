# from datas.day2 import data_debug as data
import sys
from pathlib import Path

from datas.day02 import data

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration


def calculate_mystery_one() -> None:
    ranges = [map(int, elm.split("-")) for elm in data.split(",")]
    invalid_ids = []
    for start, end in ranges:
        for number in range(start, end + 1):
            if _is_invalid_id(number):
                invalid_ids.append(number)
    # 24157613387
    print(f"Result mystery 1: {sum(invalid_ids)}")


def calculate_mystery_two() -> None:
    ranges = [map(int, elm.split("-")) for elm in data.split(",")]
    not_valid = []
    for start, end in ranges:
        for number in range(start, end + 1):
            if _has_repeating_pattern(number):
                not_valid.append(number)
    # 33832678380
    print(f"Result mystery 2: {sum(not_valid)}")


def _is_invalid_id(number: int) -> bool:
    if len(str(number)) % 2 != 0:
        return False
    number_str = str(number)
    middle_index = len(number_str) // 2
    left = number_str[:middle_index]
    right = number_str[middle_index:]
    return left == right


def _has_repeating_pattern(number: int) -> bool:
    s = str(number)
    n = len(s)

    return any(n % size == 0 and s[:size] * (n // size) == s for size in range(1, n // 2 + 1))


if __name__ == "__main__":
    calculate_mystery_one()
    calculate_mystery_two()
    calculate_duration()
