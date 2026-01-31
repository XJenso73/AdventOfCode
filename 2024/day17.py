# Advent of Code 2024 - Day 17
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from dataclasses import dataclass
from enum import IntEnum

from src.utils import calculate_duration, import_data

FILE = Path("datas/day17_debug.txt")
# FILE = Path("datas/day17.txt")


class State(IntEnum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


@dataclass
class Registers:
    a: int
    b: int
    c: int

    def get_combo_value(self, operand: int) -> int:
        if 0 <= operand <= 3:
            return operand
        if operand == 4:
            return self.a
        if operand == 5:
            return self.b
        if operand == 6:
            return self.c
        raise ValueError("Invalid combo operand")


@dataclass
class SystemState:
    program: list[int]
    registers: Registers

    @property
    def output(self) -> str:
        if not hasattr(self, "_output"):
            self._calculate()
        return ",".join(self._output)

    @property
    def quine_value(self) -> int | None:
        possible_a_values = [0]

        # von hinten nach vorne aufbauen
        for i in range(len(self.program)):
            target_suffix = self.program[-(i + 1) :]
            new_possible = []

            for base_a in possible_a_values:
                for bits in range(8):
                    test_a = (base_a << 3) | bits

                    state = SystemState(self.program.copy(), Registers(test_a, 0, 0))
                    output = [int(x) for x in state.output.split(",") if x]

                    if output == target_suffix:
                        new_possible.append(test_a)

            possible_a_values = new_possible

        if possible_a_values:
            return min(possible_a_values)

        return None

    def _calculate(self) -> None:
        self._ip = 0
        self._output = []
        while self._ip < len(self.program):
            opcode = State(self.program[self._ip])
            operand = self.program[self._ip + 1]
            combo_value = self.registers.get_combo_value(operand)

            # Default step
            next_ip = self._ip + 2

            match opcode:
                case State.ADV:
                    self.registers.a //= 2**combo_value
                case State.BXL:
                    self.registers.b ^= operand
                case State.BST:
                    self.registers.b = combo_value % 8
                case State.JNZ:
                    if self.registers.a != 0:
                        next_ip = operand
                case State.BXC:
                    self.registers.b ^= self.registers.c
                case State.OUT:
                    self._output.append(str(combo_value % 8))
                case State.BDV:
                    self.registers.b = self.registers.a // (2**combo_value)
                case State.CDV:
                    self.registers.c = self.registers.a // (2**combo_value)

            self._ip = next_ip


def _parse(lines: list[str]) -> SystemState:
    registers = {}
    for line in lines:
        if not line.strip():
            continue
        if ":" not in line:
            continue

        order, value = line.split(":")
        if "Register" in order:
            key = order.strip()[-1:]
            registers[key] = int(value)

        elif "Program" in order:
            program = [int(i) for i in value.split(",")]
        else:
            continue

    return SystemState(
        program,
        Registers(registers.get("A"), registers.get("B"), registers.get("C")),
    )


def solve_part_one(system_state: SystemState) -> None:
    result = system_state.output
    # 4,6,3,5,6,3,5,2,1,0 / 2,1,3,0,5,2,3,7,1
    print(f"Result part 1: {result}")


def solve_part_two(system_state: SystemState) -> None:
    result = system_state.quine_value
    # None / 107416732707226
    print(f"Result part 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    system_state: SystemState = _parse(lines)
    solve_part_one(system_state)
    solve_part_two(system_state)
    calculate_duration()
