# Advent of Code 2023 - Day 10
from src.utils import calculate_duration, import_data

FILE = "./datas/day10_debug.txt"
FILE = "./datas/day10.txt"
DIRECTIONS = {
    "|": [(-1, 0), (1, 0)],  # Norden, Süden
    "-": [(0, -1), (0, 1)],  # Westen, Osten
    "L": [(-1, 0), (0, 1)],  # Norden, Osten
    "J": [(-1, 0), (0, -1)],  # Norden, Westen
    "7": [(1, 0), (0, -1)],  # Süden, Westen
    "F": [(1, 0), (0, 1)],  # Süden, Osten
}


def _find_start(lines: list[str]) -> int:
    for idx, line in enumerate(lines):
        if "S" in line:
            return idx, line.index("S")
    raise ValueError("start is not found")


def _find_first_move(start_pos: tuple[int, int], lines: list[str]) -> tuple[int, int]:
    y, x = start_pos
    possible_moves = [
        ("N", -1, 0, ["|", "7", "F"]),
        ("S", 1, 0, ["|", "L", "J"]),
        ("W", 0, -1, ["-", "L", "F"]),
        ("O", 0, 1, ["-", "J", "7"]),
    ]

    for _, dy, dx, valid_pipes in possible_moves:
        ny, nx = y + dy, x + dx
        if 0 <= ny < len(lines) and 0 <= nx < len(lines[0]):
            neighbor_pipe = lines[ny][nx]
            if neighbor_pipe in valid_pipes:
                return (dy, dx)

    raise IndexError("cold not found first move")


def _run_loop(start_pos: tuple[int, int], first_move: tuple[int, int], lines: list[str]) -> list[tuple[int, int]]:
    loop = [start_pos]
    current_pos = (start_pos[0] + first_move[0], start_pos[1] + first_move[1])
    last_pos = start_pos

    while current_pos != start_pos:
        loop.append(current_pos)
        y, x = current_pos
        pipe_type = lines[y][x]

        for dy, dx in DIRECTIONS[pipe_type]:
            next_pos = (y + dy, x + dx)
            if next_pos != last_pos:
                last_pos = current_pos
                current_pos = next_pos
                break

    return loop


def _get_replacement_char(run_path: list[tuple[int, int]]) -> str:
    # Die beiden Nachbarn von S im Loop (der erste und der letzte Schritt)
    y_s, x_s = run_path[0]
    y_first, x_first = run_path[1]
    y_last, x_last = run_path[-1]

    # Berechne die Vektoren relativ zu S
    v1 = (y_first - y_s, x_first - x_s)
    v2 = (y_last - y_s, x_last - x_s)

    # Alle Richtungen, die S verbindet
    actual_connections = {v1, v2}

    # Finde heraus, welcher Rohr-Typ dieselben Verbindungen hat
    for char, connections in DIRECTIONS.items():
        if set(connections) == actual_connections:
            return char
    return "S"  # Fallback


def _calculate(lines: list[str], run_path: list[tuple[int, int]]) -> int:
    s_replacement = _get_replacement_char(run_path)
    run_path_set = set(run_path)
    inside_count = 0
    for y, line in enumerate(lines):
        is_inside = False
        for x, char in enumerate(line):
            # 1. Prüfen: Gehört dieses Zeichen zum Loop?
            if (y, x) in run_path_set:
                # Falls ja, checken ob es eine Wand ist (S berücksichtigen!)
                actual_char = char if char != "S" else s_replacement
                if actual_char in "|LJ":
                    is_inside = not is_inside
            else:
                # 2. Wenn es nicht zum Loop gehört, ist es "Dreck"
                # Wenn wir gerade "inside" sind, zählen wir es!
                if is_inside:
                    inside_count += 1
    return inside_count


def solve_mystery_one(run_path: list[tuple[int, int]]) -> None:
    result = len(run_path) // 2
    # 80 / 7005
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str], run_path: list[tuple[int, int]]) -> None:
    result = _calculate(lines, run_path)
    # 10 / 417
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    start_pos = _find_start(lines)
    first_move = _find_first_move(start_pos, lines)
    run_path = _run_loop(start_pos, first_move, lines)
    solve_mystery_one(run_path)
    solve_mystery_two(lines, run_path)
    calculate_duration()
