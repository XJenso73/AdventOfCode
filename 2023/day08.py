# Advent of Code 2023 - Day 08
import math
from collections.abc import Callable
from itertools import cycle

from src.utils import calculate_duration, import_data

FILE = "./datas/day08_debug.txt"
FILE = "./datas/day08.txt"
INSTRUCTIONS_MAP = {"L": 0, "R": 1}
type StepWay = dict[str, tuple[str, str]]
type ConditionFunc = Callable[[str], bool]


def _parse_data(lines: list[str]) -> tuple[str, StepWay]:
    instructions = lines[0].strip()
    step_way = {}

    for line in lines[2:]:
        if not line.strip():
            continue
        line = line.strip()
        line = line.replace(" ", "")

        node, connections = line.split("=")
        left, right = connections.strip("()").split(",")
        step_way[node] = (left, right)

    return instructions, step_way


def _get_steps_to_end(start_node: str, instructions: str, step_way: StepWay, is_at_end: ConditionFunc) -> int:
    steps = 0
    instruction_pool = cycle(instructions)
    current_node = start_node
    while not is_at_end(current_node):
        instruction = next(instruction_pool)
        index = INSTRUCTIONS_MAP[instruction]
        current_node = step_way[current_node][index]
        steps += 1

    return steps


def solve_mystery_one(lines: list[str]) -> None:
    instructions, step_way = _parse_data(lines)
    result = _get_steps_to_end("AAA", instructions, step_way, lambda node: node == "ZZZ")
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    instructions, step_way = _parse_data(lines)
    start_nodes = [key for key in step_way if key.endswith("A")]

    # Für jeden Startknoten einzeln berechnen, wie lange er bis zu einem 'Z' braucht
    path_lengths = []
    for node in start_nodes:
        steps = _get_steps_to_end(node, instructions, step_way, lambda node: node.endswith("Z"))
        path_lengths.append(steps)

    result = math.lcm(*path_lengths)
    # 17972669116327
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)
    calculate_duration()
