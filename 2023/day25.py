# Advent of Code 2023 - Day 25
import networkx as nx
from src.utils import calculate_duration, import_data

FILE = "./datas/day25_debug.txt"
# FILE = "./datas/day25.txt"


def solve_part_one(lines: list[str]) -> int | None:
    # Create an undirected graph
    graph = nx.Graph()
    for line in lines:
        node, neighbors = line.strip().split(": ")
        for neighbor in neighbors.split(" "):
            graph.add_edge(node, neighbor)

    # nx.minimum_edge_cut returns the 3 edges that disconnect the graph
    # We know from the puzzle description that the min cut is exactly 3
    cut_edges = nx.minimum_edge_cut(graph)

    if len(cut_edges) == 3:
        # Remove the identified edges
        graph.remove_edges_from(cut_edges)

        # Find the two resulting connected components
        components = list(nx.connected_components(graph))

        if len(components) == 2:
            size1 = len(components[0])
            size2 = len(components[1])
            return size1 * size2

    return None


def solve_mystery_one(lines: list[str]) -> None:
    result = solve_part_one(lines)
    # 54 / 543256
    print(f"Result mystery 1: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    calculate_duration()
