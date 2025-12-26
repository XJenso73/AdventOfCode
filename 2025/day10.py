import re

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from src.utils import calculate_duration, import_data

# FILE = "./datas/day10_debug.txt"
FILE = "./datas/day10.txt"

PATTERN_DIAGRAM = re.compile(r"\[.*?\]")
PATTERN_BUTTONS = re.compile(r"\(.*?\)")
PATTERN_JOLTAGE = re.compile(r"\{.*?\}")


def solve_mystery_one(lines: list[str]) -> None:
    key_press = 0
    for row in lines:
        found_diagram = PATTERN_DIAGRAM.findall(row)
        found_buttons = PATTERN_BUTTONS.findall(row)
        diagram = _get_bitmask_diagram(found_diagram[0][1:-1])
        buttons = [_get_bitmask_button(i[1:-1]) for i in found_buttons]
        key_press += _calculate_machine_mystery_one(diagram, buttons)
    # 457
    print(f"Result mystery 1: {key_press}")


def solve_mystery_two(lines: list[str]) -> None:
    total = 0
    for _, row in enumerate(lines):
        if not row.strip():
            continue
        joltage = _extract_joltage(row)
        buttons = _extract_buttons(row)
        total += _calculate_machine_mystery_two(joltage, buttons)
    # 17576
    print(f"Result mystery 2: {total}")


###################### Mystery One ######################


def _get_bitmask_diagram(diagram: str) -> int:
    mask = 0
    for i, c in enumerate(diagram):
        if c == "#":
            mask |= 1 << i

    return mask


def _get_bitmask_button(button: str) -> int:
    mask = 0
    if button:
        for n in map(int, button.split(",")):
            mask |= 1 << n
    return mask


def _calculate_machine_mystery_one(diagram: int, buttons: list[int]) -> int:
    m = len(buttons)
    mid = m // 2

    left = buttons[:mid]
    right = buttons[mid:]
    left_best = {}
    for xor, presses in _enumerate_subsets(left):
        if xor not in left_best or presses < left_best[xor]:
            left_best[xor] = presses

    best = float("inf")
    for xor, presses in _enumerate_subsets(right):
        need = diagram ^ xor
        if need in left_best:
            best = min(best, presses + left_best[need])

    return best


def _enumerate_subsets(buttons: list[int]):
    n = len(buttons)
    for subset in range(1 << n):
        xor = 0
        presses = 0
        for i in range(n):
            if subset & (1 << i):
                xor ^= buttons[i]
                presses += 1
        yield xor, presses


###################### Mystery two ######################


def _extract_joltage(row: str) -> list[int]:
    target = PATTERN_JOLTAGE.findall(row)
    if target:
        return list(map(int, target[0][1:-1].split(",")))
    raise ValueError("no target found")


def _extract_buttons(row: str) -> list[tuple[int]]:
    return [tuple(map(int, element[1:-1].split(","))) for element in PATTERN_BUTTONS.findall(row)]


def _calculate_machine_mystery_two(joltage: list[int], buttons: list[tuple[int]]) -> int:
    num_counters = len(joltage)
    num_buttons = len(buttons)

    # Matrix A: Zeilen = Counter, Spalten = Buttons
    A = np.zeros((num_counters, num_buttons))
    for col, btn in enumerate(buttons):
        for row in btn:
            A[row, col] = 1

    # Zielfunktion: Summe der x_i minimieren (alle Koeffizienten sind 1)
    c = np.ones(num_buttons)

    # Constraints: A * x == target
    # Wir definieren eine Gleichung durch lb (lower bound) == ub (upper bound)
    constraints = LinearConstraint(A, lb=joltage, ub=joltage)

    # x muss eine nicht-negative Ganzzahl sein
    bounds = Bounds(0, np.inf)
    integrality = np.ones(num_buttons)  # 1 bedeutet: muss Ganzzahl sein

    # MILP Solver (Mixed-Integer Linear Programming)
    res = milp(c=c, constraints=constraints, bounds=bounds, integrality=integrality)

    if res.success:
        # res.fun ist der Wert der Zielfunktion (hier die Summe der x_i)
        return int(np.round(res.fun))

    return 0


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)

    calculate_duration()
