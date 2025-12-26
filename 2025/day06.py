import operator
from functools import reduce

from src.utils import calculate_duration, import_data

# FILE = "./datas/day06_debug.txt"
FILE = "./datas/day06.txt"
OPS = {"+": operator.add, "*": operator.mul}


def solve_mystery_one(lines: list[str]) -> None:
    lines = [elem.replace("  ", " ") for elem in lines]
    all_numbers = _extract_all_numbers(lines)
    all_operations = _extract_all_operations(lines)
    result = _calculate_result(all_numbers, all_operations[0])
    # 5733696195703
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    """Berechnet die Summe aller Aufgaben im Arbeitsblatt."""
    lines = _normalize(lines)
    tasks = _split_tasks(lines)
    total = sum(_eval_task(t) for t in tasks)
    # 10951882745757
    print(f"Result mystery 2: {total}")


def _extract_all_numbers(lines: list[str]) -> list[int]:
    return [list(map(int, row.split())) for row in lines[:-1]]


def _extract_all_operations(lines: list[str]) -> list[str]:
    return [lines[-1].split()]


def _calculate_result(numbers: list[int], operations: list[str]) -> int:
    results = []
    for col, operation in enumerate(operations):
        values = [row[col] for row in numbers]

        if operation == "*":
            result = 1
            for v in values:
                result *= v
        elif operation == "+":
            result = sum(values)
        else:
            raise ValueError(f"Unbekannter Operator: {operation}")
        results.append(result)
    return sum(results)


def _normalize(lines: list[str]) -> list[str]:
    """Füllt alle Zeilen auf die gleiche Länge auf."""
    width = max(len(line) for line in lines)
    return [line.ljust(width) for line in lines]


def _split_tasks(lines: list[str]) -> list[list[list[str]]]:
    """Teilt das Grid in Aufgaben (rechts → links) anhand leerer Spalten."""
    width = len(lines[0])
    tasks = []
    current = []

    for c in range(width - 1, -1, -1):
        col = _get_col(lines, c)
        if all(ch == " " for ch in col):
            if current:
                tasks.append(current)
                current = []
        else:
            current.append(col)

    if current:
        tasks.append(current)
    return tasks


def _get_col(lines: list[str], c: int) -> list[str]:
    """Extrahiert eine Spalte aus dem Grid."""
    return [lines[r][c] for r in range(len(lines))]


def _eval_task(task: list[list[str]]) -> int:
    """Berechnet das Ergebnis einer einzelnen Aufgabe."""
    op = _extract_op(task)
    nums = [_col_to_int(col) for col in task if any(ch.isdigit() for ch in col)]
    return reduce(OPS[op], nums)


def _extract_op(task: list[list[str]]) -> str:
    """Findet den Operator + oder * in der Aufgabe."""
    for col in task:
        for ch in col:
            if ch in "+*":
                return ch
    raise ValueError("Kein Operator gefunden")


def _col_to_int(col: list[str]) -> int:
    """Konvertiert eine Spalte in eine ganze Zahl."""
    return int("".join(ch for ch in col if ch.isdigit()))


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)

    calculate_duration()
