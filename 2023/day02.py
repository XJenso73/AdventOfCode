# Advent of Code 2023 - Day 02


import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration, import_data

FILE = "./datas/day02_debug.txt"
# FILE = "./datas/day02.txt"
MAX_COUNTS = {"red": 12, "green": 13, "blue": 14}


def solve_mystery_one(lines: list[str]) -> None:
    sets = _parse_allowed_lines(lines)
    result = sum(id for id in sets)
    # 2716
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    sets = _parse_all_lines(lines)
    result = _calculate_game_power(sets)
    # 72227
    print(f"Result mystery 2: {result}")


def _parse_allowed_lines(lines: list[str]) -> dict[int, list[dict[str, int]]]:
    games = {}
    for line in lines:
        header, data = line.split(":")
        game_id = int(header.split()[1])
        sets = [{color: int(count) for item in s.split(",") for count, color in [item.split()]} for s in data.split(";")]
        if _is_allowed(sets):
            games[game_id] = sets
    return games


def _is_allowed(sets: list[dict[str, int]]) -> bool:
    return all(count <= MAX_COUNTS[color] for s in sets for color, count in s.items())


def _parse_all_lines(lines: list[str]) -> dict[int, list[dict[str, int]]]:
    games = []
    for line in lines:
        _, data = line.split(":")
        sets = [{color: int(count) for item in s.split(",") for count, color in [item.split()]} for s in data.split(";")]
        games.append(sets)
    return games


def _calculate_game_power(sets: list[dict[str, int]]) -> int:
    power = []

    for games in sets:
        max_red = 0
        max_green = 0
        max_blue = 0
        for game in games:
            max_red = max(max_red, game.get("red", 0))
            max_green = max(max_green, game.get("green", 0))
            max_blue = max(max_blue, game.get("blue", 0))
        power.append(max_red * max_green * max_blue)

    return sum(power)


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)
    calculate_duration()
