import sys
from functools import lru_cache
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration, import_data

FILE = "./datas/day11_debug.txt"
# FILE = "./datas/day11.txt"
START_MYSTERY_ONE = "you"
START_MYSTERY_TWO = "svr"
TARGET = "out"
VIA_1 = "fft"
VIA_2 = "dac"


def solve_mystery_one(lines: list[str]) -> None:
    graph = _prepaire_data_to_graph_mystery_one(lines)
    result = _find_paths(graph, START_MYSTERY_ONE, TARGET)
    # 758
    print(f"Result mystery 1: {len(result)}")


def solve_mystery_two(lines: list[str]) -> None:
    graph = _prepaire_data_to_graph_mystery_two(lines)
    result = _calculate_mystery_two(graph)
    # 490695961032000
    print(f"Result mystery 2: {result}")


###################### Mystery one ######################


def _prepaire_data_to_graph_mystery_one(lines: list[str]) -> dict[str, dict[str]]:
    graph = {}
    for _, row in enumerate(lines):
        if not row.strip():
            continue
        node, path = row.split(":")
        path = path.replace("  ", "").strip()
        graph = {**graph, **{node: path.split(" ")}}
    return graph


def _find_paths(graph: dict[str, dict[str]], start: str, target: str) -> list[str]:
    paths = []

    def dfs(node, path):
        if node == target:
            paths.append(path)
            return
        for nxt in graph.get(node, []):
            if nxt not in path:
                dfs(nxt, path + [nxt])

    dfs(start, [start])
    return paths


###################### Mystery two ######################


def _prepaire_data_to_graph_mystery_two(lines: list[str]) -> dict[str, dict[str]]:
    graph = {}
    for _, row in enumerate(lines):
        if not row.strip():
            continue
        if ":" not in row:
            continue
        node, neighbors = row.split(":")
        graph[node.strip()] = neighbors.strip().split()
    return graph


def _calculate_mystery_two(graph: dict[str, dict[str]]) -> int:
    @lru_cache(None)
    def count_paths(current, target):
        if current == target:
            return 1
        total = 0
        for nxt in graph.get(current, []):
            total += count_paths(nxt, target)
        return total

    s1 = count_paths(START_MYSTERY_TWO, VIA_1)
    s2 = count_paths(VIA_1, VIA_2)
    s3 = count_paths(VIA_2, TARGET)
    path_a = s1 * s2 * s3

    # Pfad: svr -> dac -> fft -> out
    # (Nur nötig, falls die Reihenfolge auch umgekehrt sein kann)
    s4 = count_paths(START_MYSTERY_TWO, VIA_2)
    s5 = count_paths(VIA_2, VIA_1)
    s6 = count_paths(VIA_1, TARGET)
    path_b = s4 * s5 * s6

    return path_a + path_b


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)

    calculate_duration()
