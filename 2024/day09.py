# Advent of Code 2024 - Day 09
from collections import deque
from itertools import accumulate

from src.utils import calculate_duration, import_data

FILE = "./datas/day09_debug.txt"
FILE = "./datas/day09.txt"
type Segment = list[int | None]
type Segments = list[Segment]


def _prepare_part_one(lines: list[str]) -> list[int | None]:
    input: str = "".join(lines)
    disk = []
    file_id = 0
    for i, char in enumerate(input):
        length = int(char)
        if i % 2 == 0:
            disk.extend([file_id] * length)
            file_id += 1
        else:
            disk.extend([None] * length)
    return disk


def _calculate_part_one(disk: list[int | None]) -> int:
    data_points = deque([value for value in disk if value is not None])
    layout = disk

    result_list = []
    for slot in layout:
        if not data_points:
            break
        if slot is not None:
            result_list.append(data_points.popleft())
        else:
            result_list.append(data_points.pop())

    return sum(i * v for i, v in enumerate(result_list))


def _prepare_part_two(lines: list[str]) -> tuple[Segments, int]:
    # Parse into segments
    input: str = "".join(lines).strip()
    segments = []
    file_id = 0
    for i, char in enumerate(input):
        length = int(char)
        if i % 2 == 0:
            segments.append([file_id, length])
            file_id += 1
        else:
            if length > 0:
                segments.append([None, length])

    return segments, file_id


def _move_files_part_two(segments: Segments, start_id: int) -> tuple[Segments, int]:

    for file_id in range(start_id - 1, -1, -1):
        file_idx, (_, file_len) = next((i, seg) for i, seg in enumerate(segments) if seg[0] == file_id)

        gap_idx = None
        for idx in range(file_idx):
            gid, glen = segments[idx]
            if gid is None and glen >= file_len:
                gap_idx = idx
                break

        if gap_idx is None:
            continue

        # move file
        segments[file_idx][0] = None
        gap_len = segments[gap_idx][1]
        segments[gap_idx] = [file_id, file_len]

        if gap_len > file_len:
            segments.insert(gap_idx + 1, [None, gap_len - file_len])

    return segments, file_id


def _calculate_part_two(segments: Segments) -> int:
    positions = accumulate((length for _, length in segments), initial=0)
    checksum = 0
    for (file_id, length), start in zip(segments, positions, strict=False):
        if file_id is not None:
            checksum += file_id * (length * start + length * (length - 1) // 2)
    return checksum


def solve_part_one(lines: list[str]) -> None:
    disk: list[int | None] = _prepare_part_one(lines)
    result = _calculate_part_one(disk)
    # 1928 / 6283404590840
    print(f"Result part 1: {result}")


def solve_part_two(lines: list[str]) -> None:
    segments, file_id = _prepare_part_two(lines)
    segments, file_id = _move_files_part_two(segments, file_id)
    result = _calculate_part_two(segments)
    # 2858 / 6304576012713
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines: list[str] = import_data(FILE)
    solve_part_one(lines)
    solve_part_two(lines)
    calculate_duration()
