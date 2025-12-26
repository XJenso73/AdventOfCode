# Advent of Code 2023 - Day 05
from src.utils import calculate_duration, import_data

FILE = "./datas/day05_debug.txt"
FILE = "./datas/day05.txt"


def solve_mystery_one(lines: list[str]) -> None:
    seeds, all_maps = _prepaire_data_to_process(lines)
    result = _find_minimum_location_mystery_one(seeds, all_maps)

    # 35 / 57075758
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    seeds, all_maps = _prepaire_data_to_process(lines)
    result = _find_minimum_location_mystery_two(seeds, all_maps)
    # 46 / 31161857
    print(f"Result mystery 2: {result}")


def _prepaire_data_to_process(lines):
    seeds = [int(x) for x in lines[0].split(":")[1].split()]

    all_maps = []
    current_map_rules = []
    for line in lines[2:]:
        line = line.strip()

        if not line:
            if current_map_rules:
                all_maps.append(current_map_rules)
                current_map_rules = []
            continue

        if "map:" in line:
            continue

        parts = list(map(int, line.split()))
        current_map_rules.append(tuple(parts))

    if current_map_rules:
        all_maps.append(current_map_rules)

    return seeds, all_maps


def _find_minimum_location_mystery_one(seeds: list[int], all_maps: list[tuple[int, ...]]) -> int:
    locations = []

    for val in seeds:
        current_value = val

        for mapping_layer in all_maps:
            for dest_start, src_start, length in mapping_layer:
                if src_start <= current_value < src_start + length:
                    current_value = dest_start + (current_value - src_start)
                    break

        locations.append(current_value)

    return min(locations)


def _find_minimum_location_mystery_two(seeds: list[int], all_maps: list[tuple[int, ...]]) -> int:
    intervals = []
    for i in range(0, len(seeds), 2):
        start = seeds[i]
        length = seeds[i + 1]
        intervals.append((start, start + length))

    for mapping_layer in all_maps:
        new_intervals = []

        while intervals:
            start, end = intervals.pop()

            found_overlap = False
            for dest, src, length in mapping_layer:
                src_end = src + length
                overlap_start = max(start, src)
                overlap_end = min(end, src_end)

                if overlap_start < overlap_end:
                    offset = dest - src
                    new_intervals.append((overlap_start + offset, overlap_end + offset))

                    if overlap_start > start:
                        intervals.append((start, overlap_start))
                    if overlap_end < end:
                        intervals.append((overlap_end, end))

                    found_overlap = True
                    break

            if not found_overlap:
                new_intervals.append((start, end))

        intervals = new_intervals

    return min(start for start, end in intervals)


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)
    calculate_duration()
