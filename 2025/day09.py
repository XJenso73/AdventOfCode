from dataclasses import dataclass, field

from src.utils import calculate_duration, import_data

# FILE = "./datas/day09_debug.txt"
FILE = "./datas/day09.txt"


@dataclass
class CompressedGrid:
    red_tiles: list[tuple[int, int]]
    unique_x: list[int] = field(init=False)
    unique_y: list[int] = field(init=False)
    x_map: dict[int, int] = field(init=False)
    y_map: dict[int, int] = field(init=False)
    grid: list[list[int]] = field(init=False)


def solve_mystery_one(lines: list[str]) -> None:
    result = _parse_grid_mystery_one(lines)
    # 4749929916
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    max_area = _calculate_grid(CompressedGrid(_parse_grid_mystery_two(lines)))
    # 1572047142
    print(f"Result mystery 2: {max_area}")


###################### Mystery One ######################


def _parse_grid_mystery_one(lines: list[str]) -> int:
    return max(_calculate_max_flows(elem_x, elem_y) for idx, elem_x in enumerate(lines) for elem_y in lines[idx + 1 :])


def _calculate_max_flows(cord_a: str, cord_b: str) -> int:
    x1, y1 = map(int, cord_a.split(","))
    x2, y2 = map(int, cord_b.split(","))
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


###################### Mystery Two ######################


def _parse_grid_mystery_two(lines: list[str]) -> list[tuple[int, int]]:
    return [tuple(map(int, s.split(","))) for s in lines]


def _calculate_grid(compressed_grid: CompressedGrid) -> int:
    _create_compressed_grid(compressed_grid)
    _draw_lines(compressed_grid)
    _process_flood_fill(compressed_grid)
    return _calc_max_area(compressed_grid)


def _create_compressed_grid(compressed_grid: CompressedGrid) -> None:
    # 1. Alle relevanten X und Y Koordinaten extrahieren
    compressed_grid.unique_x = sorted({point[0] for point in compressed_grid.red_tiles})
    compressed_grid.unique_y = sorted({point[1] for point in compressed_grid.red_tiles})

    # Mapping von Koordinate auf Index (Compression)
    compressed_grid.x_map = {x: i for i, x in enumerate(compressed_grid.unique_x)}
    compressed_grid.y_map = {y: j for j, y in enumerate(compressed_grid.unique_y)}

    # Kleineres Grid erstellen (nur so groß wie die Anzahl der Unikate)
    compressed_grid.grid = [[0 for _ in range(len(compressed_grid.unique_y))] for _ in range(len(compressed_grid.unique_x))]


def _draw_lines(compressed_grid: CompressedGrid) -> None:
    for i in range(len(compressed_grid.red_tiles)):
        p1 = compressed_grid.red_tiles[i]
        p2 = compressed_grid.red_tiles[(i + 1) % len(compressed_grid.red_tiles)]

        start_x, end_x = sorted([compressed_grid.x_map[p1[0]], compressed_grid.x_map[p2[0]]])
        start_y, end_y = sorted([compressed_grid.y_map[p1[1]], compressed_grid.y_map[p2[1]]])

        for x in range(start_x, end_x + 1):
            for y in range(start_y, end_y + 1):
                compressed_grid.grid[x][y] = 1  # Rand/Rot/Grün-Linie


def _process_flood_fill(compressed_grid):
    # 3. Flood Fill im komprimierten Grid (Innenbereich markieren)
    # Da das Polygon geschlossen ist, füllen wir von außen
    rows, cols = len(compressed_grid.unique_x), len(compressed_grid.unique_y)
    stack = _search_borders(compressed_grid, rows, cols)

    external = set()
    while stack:
        r, c = stack.pop()
        if (r, c) in external:
            continue
        external.add((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and compressed_grid.grid[nr][nc] == 0 and (nr, nc) not in external:
                stack.append((nr, nc))

    # Alles was nicht external und nicht Rand ist, ist Innen (Grün)
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in external:
                compressed_grid.grid[r][c] = 1


def _search_borders(compressed_grid: CompressedGrid, rows: int, cols: int) -> list[tuple[int, int]]:
    stack = []
    # Ränder für Flood Fill suchen
    for r in range(rows):
        for c in [0, cols - 1]:
            if compressed_grid.grid[r][c] == 0:
                stack.append((r, c))
    for c in range(cols):
        for r in [0, rows - 1]:
            if compressed_grid.grid[r][c] == 0:
                stack.append((r, c))
    return stack


def _calc_max_area(compressed_grid) -> int:
    max_area = 0
    for i in range(len(compressed_grid.red_tiles)):
        for j in range(i + 1, len(compressed_grid.red_tiles)):
            x1, y1 = compressed_grid.red_tiles[i]
            x2, y2 = compressed_grid.red_tiles[j]

            x_min, x_max = sorted([x1, x2])
            y_min, y_max = sorted([y1, y2])

            # Schnell-Check: Lohnt sich die Prüfung überhaupt?
            current_area = (x_max - x_min + 1) * (y_max - y_min + 1)
            if current_area <= max_area:
                continue

            # Validierung im komprimierten Grid
            is_valid = True
            for rx in range(compressed_grid.x_map[x_min], compressed_grid.x_map[x_max] + 1):
                for ry in range(compressed_grid.y_map[y_min], compressed_grid.y_map[y_max] + 1):
                    if compressed_grid.grid[rx][ry] == 0:
                        is_valid = False
                        break
                if not is_valid:
                    break

            if is_valid:
                max_area = current_area
    return max_area


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)

    calculate_duration()
