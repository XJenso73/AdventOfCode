#!/bin/bash

# $1 ist der erste Parameter (Tag)
# $2 ist der zweite Parameter (Jahr)

DAY=$1
DAY=$(printf "%02d" $DAY)

# Wenn $2 leer ist, wird das aktuelle Datum im Format YYYY genommen
YEAR=${2:-$(date +%Y)}


mkdir -p ${YEAR}
mkdir -p ${YEAR}/datas
mkdir -p ${YEAR}/src

FILE_PATH_DATA=/datas/day${DAY}.txt
FILE_PATH_DATA_DEBUG=/datas/day${DAY}_debug.txt
FILE_PATH=${YEAR}/day${DAY}.py
touch $YEAR$FILE_PATH_DATA
touch $YEAR$FILE_PATH_DATA_DEBUG



# Erzeugt die Python-Datei mit Standard-Inhalt
cat <<EOF > "$FILE_PATH"
# Advent of Code $YEAR - Day $DAY
import sys
from src.utils import calculate_duration, import_data

FILE = ".$FILE_PATH_DATA_DEBUG"
# FILE = ".$FILE_PATH_DATA"

def solve_mystery_one(lines: list[str]) -> None:
    result = "xy"
    print(f"Result mystery 1: {result}")


def solve_mystery_two(lines: list[str]) -> None:
    result = "xy"
    print(f"Result mystery 2: {result}")

if __name__ == "__main__":
    lines = import_data(FILE)
    solve_mystery_one(lines)
    solve_mystery_two(lines)
    calculate_duration()
EOF

