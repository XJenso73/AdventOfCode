import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from src.utils import calculate_duration, import_data

FILE = "./datas/day04_debug.txt"
# FILE = "./datas/day04.txt"
# 8 Richtungen: oben, unten, links, rechts + Diagonale
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


def calculate_mystery_one(lines: list[str]) -> int:
    rows = len(lines)
    cols = len(lines[0])
    count = 0

    # über alle Zellen im Raster iterieren
    for row in range(rows):
        # über alle Spalten in der aktuellen Zeile iterieren
        for col in range(cols):
            if lines[row][col] == "@":
                neighbors = _search_neighbors_mystery_one(lines, rows, cols, row, col)
                if neighbors < 4:
                    count += 1
    # Zugängliche Rollen: 1505
    print(f"Result mystery 1: {count}")


def calculate_mystery_two(lines: list[str]) -> None:
    rows = len(lines)
    cols = len(lines[0])

    # Mutable Grid für die Simulation
    grid = [list(row) for row in lines]

    total_removed = 0

    while True:
        accessible_positions = []

        # Alle Rollen prüfen
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == "@":
                    neighbor_count = _search_neighbors_mystery_two(rows, cols, grid, row, col)
                    if neighbor_count < 4:
                        accessible_positions.append((row, col))

        # Keine zugänglichen Rollen mehr → Stop
        if not accessible_positions:
            break

        # Entferne alle zugänglichen Rollen dieser Runde
        for row, col in accessible_positions:
            grid[row][col] = "."  # Papierrolle entfernt

        total_removed += len(accessible_positions)
    # 9182
    print(f"Result mystery 2: {total_removed}")


def _search_neighbors_mystery_one(lines: list[str], rows: int, cols: int, row: int, col: int) -> int:
    neighbors = 0
    for delta_row, delta_col in DIRECTIONS:
        neighbor_row, neighbor_col = row + delta_row, col + delta_col
        if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols and lines[neighbor_row][neighbor_col] == "@":
            neighbors += 1
    return neighbors


def _search_neighbors_mystery_two(rows: int, cols: int, grid: list[list[str]], row: int, col: int) -> int:
    neighbor_count = 0
    for delta_row, delta_col in DIRECTIONS:
        neighbor_row = row + delta_row  # Zeilenindex des Nachbarn
        neighbor_col = col + delta_col  # Spaltenindex des Nachbarn
        if 0 <= neighbor_row < rows and 0 <= neighbor_col < cols and grid[neighbor_row][neighbor_col] == "@":
            neighbor_count += 1
    return neighbor_count


if __name__ == "__main__":
    lines = import_data(FILE)
    calculate_mystery_one(lines)
    calculate_mystery_two(lines)

    calculate_duration()
