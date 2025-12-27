# Advent of Code 2023 - Day 07
from collections import Counter

from src.utils import calculate_duration, import_data

type HandSortKey = tuple[int, list[int]]
type HandEntry = tuple[HandSortKey, int]


FILE = "./datas/day07_debug.txt"
FILE = "./datas/day07.txt"
CARD_VALUES_1 = {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
# Für Teil 2: J ist ein Joker (schwächer als 2)
CARD_VALUES_2 = {"T": 10, "J": 1, "Q": 12, "K": 13, "A": 14}
TYPE_MAP = {
    (5,): 6,  # Five of a kind
    (4, 1): 5,  # Four of a kind
    (3, 2): 4,  # Full House
    (3, 1, 1): 3,  # Three of a kind
    (2, 2, 1): 2,  # Two pair
    (2, 1, 1, 1): 1,  # One pair
}


def solve_mystery(lines: list[str], part_two: bool = False) -> None:
    prepared_hands = _prepare_data(lines, part_two)
    prepared_hands.sort()
    result = 0
    # startet den Zähler (Rank) direkt bei 1
    for rank, (_, bid) in enumerate(prepared_hands, 1):
        result += rank * bid
    if part_two:
        # 5905 / 253499763
        print(f"Result mystery 2: {result}")
        return
    # 6440 / 252656917
    print(f"Result mystery 1: {result}")


def _prepare_data(lines: list[str], part_two: bool = False) -> list[HandEntry]:
    prepared_hands = []
    # Card_Values je nach Rätzel auswählen
    current_card_values = CARD_VALUES_2 if part_two else CARD_VALUES_1

    for line in lines:
        if not line.strip():
            continue
        hand, bid_str = line.split()
        bid = int(bid_str)

        card_scores = [current_card_values.get(c, int(c) if c.isdigit() else 0) for c in hand]
        type_score = _get_type_score_part(hand, part_two)

        prepared_hands.append(((type_score, card_scores), bid))

    return prepared_hands


def _get_type_score_part(hand: str, part_two: bool = False) -> int:
    # wie oft jede Karte vorkommt, z.B. "AA8AA" -> {'A': 4, '8': 1}
    counts = Counter(hand)
    # Counter anpassen für das Rätzel 2
    if part_two:
        counts = _get_counts_with_joker(counts)

    # interessieren uns nur für die Häufigkeiten, absteigend sortiert
    # {'A': 4, '8': 1} -> [4, 1]
    frequencies = sorted(counts.values(), reverse=True)
    return TYPE_MAP.get(tuple(frequencies), 0)


def _get_counts_with_joker(counts: Counter) -> Counter:
    # Wenn Joker vorhanden sind und es nicht nur Joker sind (JJJJJ)
    if "J" in counts and counts["J"] < 5:
        joker_count = counts.pop("J")
        # Finde die Karte, die am häufigsten vorkommt
        most_common_card = counts.most_common(1)[0][0]
        # Addiere die Joker zu dieser Karte
        counts[most_common_card] += joker_count
    return counts


if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery(lines)
    solve_mystery(lines, True)
    calculate_duration()
