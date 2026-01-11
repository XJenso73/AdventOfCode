# Advent of Code 2024 - Day 11
import sys
from collections import Counter
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration, import_data

FILE = "./datas/day11_debug.txt"
FILE = "./datas/day11.txt"


def _calculate(counter: Counter[int]) -> Counter[int]:
    result = Counter()

    for stone, count in counter.items():
        if stone == 0:
            result[1] += count
            continue

        stone_str = str(stone)
        length = len(stone_str)
        middle = len(stone_str) // 2

        if length % 2 == 0:
            result[int(stone_str[:middle])] += count
            result[int(stone_str[middle:])] += count
        else:
            result[stone * 2024] += count

    return result


def solve(lines: list[str]) -> None:
    stones = map(int, " ".join(lines).split())
    result = Counter(stones)
    for i in range(1, 76):
        result = _calculate(result)
        if i == 25:
            # 55312 / 216042
            print(f"Result part 1: {sum(result.values())}")

    # 65601038650482 / 255758646442399
    print(f"Result part 2: {sum(result.values())}")


if __name__ == "__main__":
    lines = import_data(FILE)
    solve(lines)
    calculate_duration()
