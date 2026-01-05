ifneq ($(day),)
  DAY := $(day)
endif
ifneq ($(year),)
  YEAR := $(year)
endif

# Variablen mit Standardwerten (Heute)
DAY ?= $(shell date +%d)
YEAR ?= $(shell date +%Y)
PADDED_DAY = $(shell printf "%02d" $(DAY))

# Pfade
BASE_DIR = $(YEAR)
DATA_DIR = $(BASE_DIR)/datas
SRC_DIR  = $(BASE_DIR)/src
FILE_PATH = $(BASE_DIR)/day$(PADDED_DAY).py

# --- HELP ---
# Das erste Target wird ausgeführt, wenn nur 'make' eingegeben wird
help:
	@echo "🎄 Advent of Code Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make setup          - Erstellt die Ordner und das Python-Template (Default: Heute)"
	@echo "  make run            - Führt das Script für den gewählten Tag aus"
	@echo ""
	@echo "Parameters:"
	@echo "  DAY=x               - Tag angeben (z.B. make setup DAY=5)"
	@echo "  YEAR=x              - Jahr angeben (z.B. make setup YEAR=2024)"
	@echo ""
	@echo "Example:"
	@echo "  make setup DAY=01 YEAR=2025"

.PHONY: help setup run

# --- SETUP ---
setup:
	@echo "📂 Creating structure for $(YEAR), Day $(PADDED_DAY)..."
	@mkdir -p $(DATA_DIR) $(SRC_DIR)
	@touch $(DATA_DIR)/day$(PADDED_DAY).txt
	@touch $(DATA_DIR)/day$(PADDED_DAY)_debug.txt
	@if [ ! -f $(FILE_PATH) ]; then \
		printf "# Advent of Code $(YEAR) - Day $(PADDED_DAY)\n\
import sys\n\
from src.utils import calculate_duration, import_data\n\
\n\
FILE = \"./datas/day$(PADDED_DAY)_debug.txt\"\n\
# FILE = \"./datas/day$(PADDED_DAY).txt\"\n\
\n\
def solve_part_one(lines: list[str]) -> None:\n\
    result = \"xy\"\n\
    print(f\"Result part 1: {result}\")\n\
\n\
def solve_part_two(lines: list[str]) -> None:\n\
    result = \"xy\"\n\
    print(f\"Result part 2: {result}\")\n\
\n\
if __name__ == \"__main__\":\n\
    lines = import_data(FILE)\n\
    solve_part_one(lines)\n\
    solve_part_two(lines)\n\
    calculate_duration()\n" > $(FILE_PATH); \
		echo "✅ Template created: $(FILE_PATH)"; \
	else \
		echo "⚠️  File $(FILE_PATH) already exists."; \
	fi

# --- RUN ---
run:
	@python3 $(FILE_PATH)