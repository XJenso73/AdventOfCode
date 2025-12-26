from collections import Counter

from src.UnionFind import UnionFind
from src.utils import calculate_duration, import_data

# FILE = "./datas/day08_debug.txt"
FILE = "./datas/day08.txt"


def solve_mystery_one(lines: list[str]) -> int:
    lines = _prepair_data(lines)
    pairs = _create_pairs(lines)
    result = _calculate_mystery_one(lines, pairs)
    # 29406
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> int:
    lines = _prepair_data(lines)
    pairs = _create_pairs(lines)
    result = _calculate_mystery_two(lines, pairs)
    # 7499461416
    print(f"Result mystery 2: {result}")


def _prepair_data(lines: list[str]) -> list[tuple[int, int]]:
    return [tuple(map(int, line.split(","))) for line in lines]


def _create_pairs(points: list[tuple[int, int]]) -> list[tuple[int, int, int]]:
    pairs = []

    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):
            d = _distance_two(points[i], points[j])
            pairs.append((d, i, j))

    pairs.sort(key=lambda x: x[0])
    return pairs


def _distance_two(point1: tuple[int, int, int], point2: tuple[int, int, int]) -> int:
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2


def _calculate_mystery_one(points: list[tuple[int, int]], pairs: list[tuple[int, int, int]]) -> int:
    pair_key = 10 if len(points) == 20 else 1000

    uf = UnionFind(len(points))
    for _, i, j in pairs[:pair_key]:
        uf.union(i, j)

    circuits = Counter(uf.find(i) for i in range(len(points)))
    largest = sorted(circuits.values(), reverse=True)[:3]
    return largest[0] * largest[1] * largest[2]


def _calculate_mystery_two(points: list[tuple[int, int]], pairs: list[tuple[int, int, int]]) -> int:
    uf = UnionFind(len(points))
    for _, point_a_idx, point_b_idx in pairs:
        if uf.union(point_a_idx, point_b_idx):
            last_union = (point_a_idx, point_b_idx)
            if uf.size[uf.find(point_a_idx)] == len(points):
                break

    # Get the two points that were last united
    point_a_idx, point_b_idx = last_union
    cord_a = points[point_a_idx][0]
    cord_b = points[point_b_idx][0]

    return cord_a * cord_b


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)

    calculate_duration()
