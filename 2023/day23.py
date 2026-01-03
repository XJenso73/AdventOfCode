# Advent of Code 2023 - Day 23
import sys
from dataclasses import dataclass

from src.utils import calculate_duration, import_data

# Erhöhen des Rekursionslimits, da DFS bei langen Pfaden tief gehen kann
sys.setrecursionlimit(10000)

FILE = "./datas/day23_debug.txt"
# FILE = "./datas/day23.txt"
# Slope directions mapping (als Konstante)
SLOPE_DIRS = {">": (1, 0), "<": (-1, 0), "v": (0, 1), "^": (0, -1)}
POSSIBLE_DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
# Ein Dictionary: { Knoten_A: { Nachbar_B: Distanz, Nachbar_C: Distanz } }
type CompressedGraph = dict[tuple[int, int], dict[tuple[int, int], int]]
type Visited = set[tuple[int, int]]


@dataclass
class Maze:
    walkable: set[tuple[int, int]]
    slopes: dict[tuple[int, int], str]  # Für Teil 1: Pos -> Richtung
    start: tuple[int, int]
    end: tuple[int, int]
    width: int
    height: int


def _parse(lines: list[str]) -> Maze:
    walkable = set()
    slopes = {}
    height = len(lines)
    width = len(lines[0].strip())
    start = end = None

    for pos_y, line in enumerate(lines):
        for pos_x, char in enumerate(line.strip()):
            if char == "#":
                continue

            pos = (pos_x, pos_y)
            walkable.add(pos)

            if char in SLOPE_DIRS:
                slopes[pos] = char

            # Start/End detection
            if pos_y == 0:
                start = pos
            elif pos_y == height - 1:
                end = pos

    return Maze(walkable, slopes, start, end, width, height)


def _build_graph(maze: Maze) -> CompressedGraph:
    intersections = _get_intersections(maze)
    graph = {pos: {} for pos in intersections}

    for start_node in intersections:
        # in alle 4 Richtungen von der Kreuzung wegzugehen
        for dir_x, dir_y in POSSIBLE_DIRECTIONS:
            current = (start_node[0] + dir_x, start_node[1] + dir_y)
            if current not in maze.walkable:
                continue

            prev = start_node
            dist = 1
            valid = True

            # den Gang entlang bis zur nächsten Kreuzung
            while current not in intersections:
                # muss die Richtung der Bewegung mit der Slope übereinstimmen
                if current in maze.slopes:
                    slope_char = maze.slopes[current]
                    allowed_dir = SLOPE_DIRS[slope_char]
                    actual_dir = (current[0] - prev[0], current[1] - prev[1])
                    if actual_dir != allowed_dir:
                        valid = False
                        break

                # Finde den nächsten Schritt (darf nicht zurück gehen)
                next_steps = []
                for next_x, next_y in POSSIBLE_DIRECTIONS:
                    neighbor = (current[0] + next_x, current[1] + next_y)
                    if neighbor in maze.walkable and neighbor != prev:
                        next_steps.append(neighbor)

                if not next_steps:
                    valid = False
                    break

                if len(next_steps) != 1:
                    # Sollte nicht passieren in einem Gang
                    valid = False
                    break
                prev, current = current, next_steps[0]
                dist += 1

            if valid:
                graph[start_node][current] = dist

    return graph


def _find_longest(graph: CompressedGraph, current: tuple[int, int], end: tuple[int, int], visited: Visited) -> int:
    if current == end:
        return 0

    max_dist = -float("inf")
    visited.add(current)

    for neighbor, weight in graph[current].items():
        if neighbor not in visited:
            dist = _find_longest(graph, neighbor, end, visited)
            if dist != -float("inf"):
                max_dist = max(max_dist, dist + weight)

    visited.remove(current)  # Backtracking
    return max_dist


def _get_intersections(maze: Maze) -> list[tuple[int, int]]:
    intersections = [maze.start, maze.end]

    for pos in maze.walkable:
        neighbor_count = sum(1 for dir_x, dir_y in POSSIBLE_DIRECTIONS if (pos[0] + dir_x, pos[1] + dir_y) in maze.walkable)
        if neighbor_count > 2:
            intersections.append(pos)

    return intersections


def _build_graph_part_two(maze: Maze) -> CompressedGraph:
    intersections = set(_get_intersections(maze))
    graph = {p: {} for p in intersections}
    neighbors = _precomputed_neighbors(maze)
    visited_edges = set()

    for start in intersections:
        for nxt in neighbors[start]:
            prev, current = start, nxt
            dist = 1

            while current not in intersections:
                nexts = [n for n in neighbors[current] if n != prev]
                if not nexts:
                    break
                prev, current = current, nexts[0]
                dist += 1

            if current in intersections:
                edge = frozenset({start, current})
                if edge not in visited_edges:
                    visited_edges.add(edge)
                    graph[start][current] = dist
                    graph[current][start] = dist

    return graph


def _precomputed_neighbors(maze: Maze) -> dict[tuple[int, int], list[tuple[int, int]]]:
    neighbors: dict[tuple[int, int], list[tuple[int, int]]] = {}

    for pos_x, pos_y in maze.walkable:
        pos_neighbors = []
        for dir_x, dir_y in POSSIBLE_DIRECTIONS:
            next = (pos_x + dir_x, pos_y + dir_y)
            if next in maze.walkable:
                pos_neighbors.append(next)
        neighbors[(pos_x, pos_y)] = pos_neighbors

    return neighbors


def _build_index_graph(graph: CompressedGraph) -> tuple[list[list[tuple[int, int]]], dict[tuple[int, int], int]]:
    nodes = list(graph)
    index = {n: i for i, n in enumerate(nodes)}

    edges = [[] for _ in nodes]
    for a, neighbors in graph.items():
        a_id = index[a]
        for b, w in neighbors.items():
            edges[a_id].append((index[b], w))

    return edges, index


def _longest_path_fast(edges: list[list[tuple[int, int]]], start_id: int, end_id: int) -> int:
    fast_edges = [[(v, 1 << v, w) for v, w in neighbors] for neighbors in edges]

    max_dist = 0

    def dfs(u, current_dist, visited):
        nonlocal max_dist

        if u == end_id:
            if current_dist > max_dist:
                max_dist = current_dist
            return

        # Die Schleife ist der absolute Hot-Spot
        for v, v_mask, weight in fast_edges[u]:
            if not (visited & v_mask):
                dfs(v, current_dist + weight, visited | v_mask)

    dfs(start_id, 0, 1 << start_id)
    return max_dist


def solve_mystery_one(maze: Maze) -> None:
    graph = _build_graph(maze)
    # Start der Rekursion
    result = _find_longest(graph, maze.start, maze.end, set())
    # 94 / 2018
    print(f"Result mystery 1: {result}")


def solve_mystery_two(maze: Maze) -> None:
    graph = _build_graph_part_two(maze)
    edges, index = _build_index_graph(graph)

    result = _longest_path_fast(
        edges,
        index[maze.start],
        index[maze.end],
    )
    # 154 / 6406 (Beispielwerte)
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    maze = _parse(lines)
    solve_mystery_one(maze)
    solve_mystery_two(maze)
    calculate_duration()
