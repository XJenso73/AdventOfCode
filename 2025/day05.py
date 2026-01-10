import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration, import_data

FILE = "./datas/day05_debug.txt"
# FILE = "./datas/day05.txt"


def solve_mystery_one(lines: list[str]) -> None:
    fresh_product_id_range = _extract_fresh_ranges(lines)
    product_ids = _extract_product_ids(lines)
    fresh_products = sum(_is_fresh(pid, fresh_product_id_range) for pid in product_ids)
    # 737
    print(f"Result mystery 1: {fresh_products}")


def solve_mystery_two(lines: list[str]) -> None:
    fresh_product_id_range = _extract_fresh_ranges(lines)
    merged_fresh_product_id_range = _merge_fresh_ranges(fresh_product_id_range)
    count_fresh_ranges = _get_count_of_fresh_product_ids(merged_fresh_product_id_range)
    # 357485433193284
    print(f"Result mystery 2: {count_fresh_ranges}")


def _extract_product_ids(lines: list[str]) -> list[int]:
    return [int(elem) for elem in lines if elem and "-" not in elem]


def _extract_fresh_ranges(lines: list[str]) -> list[tuple[int, int]]:
    return [tuple(map(int, elm.split("-"))) for elm in lines if "-" in elm]


def _is_fresh(pid: int, ranges: list[tuple[int]]) -> bool:
    return any(start <= pid <= end for start, end in ranges)


def _merge_fresh_ranges(lines: list[tuple[int, int]]) -> list[tuple[int, int]]:
    lines.sort()
    merged = [lines[0]]

    for start, end in lines[1:]:
        last_start, last_end = merged[-1]

        if start <= last_end + 1:
            merged[-1] = (last_start, max(last_end, end))
        else:
            merged.append((start, end))

    return merged


def _get_count_of_fresh_product_ids(lines: list[tuple[int, int]]) -> int:
    return sum(end - start + 1 for start, end in lines)


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)

    calculate_duration()
