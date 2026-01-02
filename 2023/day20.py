# Advent of Code 2023 - Day 20
import copy
import math
import re
from collections import Counter, deque
from dataclasses import dataclass
from enum import Enum

from src.utils import calculate_duration, import_data


class Status(str, Enum):
    START = "broadcaster"
    CONJUNCTIONS = "&"
    FLIPFLOPS = "%"


class Pulse(int, Enum):
    LOW = 0
    HIGH = 1


@dataclass
class Module:
    name: str
    m_type: str  # '%', '&', 'broadcaster'
    outputs: list[str]
    memory: bool | dict[str, int]  # bool für %, dict für &

    def process_pulse(self, sender: str, pulse: int) -> int | None:
        match self.m_type:
            case Status.START:
                return pulse

            case Status.FLIPFLOPS:
                if pulse == Pulse.HIGH:
                    return None
                self.memory = not self.memory
                return Pulse.HIGH if self.memory else Pulse.LOW

            case Status.CONJUNCTIONS:
                self.memory[sender] = pulse
                return Pulse.LOW if all(v == Pulse.HIGH for v in self.memory.values()) else Pulse.HIGH

            case _:
                return None


FILE = "./datas/day20_debug.txt"
FILE = "./datas/day20.txt"
MODULE_PATTERN = re.compile(r"^([%&]?)(\w+)\s*->\s*(.+)$")


def _parse(lines: list[str]) -> dict[str, Module]:
    modules = {}
    for line in lines:
        if not (line := line.strip()):
            continue

        if match := MODULE_PATTERN.match(line.replace(" ", "")):
            prefix, name, outputs = match.groups()
            ways = [t.strip() for t in outputs.split(",")]
            m_type = {"%": Status.FLIPFLOPS, "&": Status.CONJUNCTIONS, "": Status.START}.get(prefix, Status.START)

            initial_memory = {} if m_type == Status.CONJUNCTIONS else False
            modules[name] = Module(name, m_type, ways, initial_memory)
    for module in modules.values():
        for target in module.outputs:
            if target in modules and modules[target].m_type == Status.CONJUNCTIONS:
                modules[target].memory[module.name] = 0

    return modules


def _prozess_mystery_one(modules: dict[str, Module]) -> int:
    pulse_counts = Counter()

    for _ in range(1000):
        queue = deque([("button", Status.START, Pulse.LOW)])

        while queue:
            sender, target, pulse = queue.popleft()
            pulse_counts[pulse] += 1

            if target in modules:
                module = modules[target]
                new_pulse = module.process_pulse(sender, pulse)

                # Wenn ein neuer Puls erzeugt wurde, an alle Ausgänge senden
                if new_pulse is not None:
                    for output in module.outputs:
                        queue.append((target, output, new_pulse))
    return pulse_counts[Pulse.LOW] * pulse_counts[Pulse.HIGH]


def _prozess_mystery_two(modules: dict[str, Module]) -> int:
    # Vorgänger von 'rx' finden
    pre_rx_module = next((name for name, module in modules.items() if "rx" in module.outputs), None)
    if not pre_rx_module:
        raise ValueError("No module outputs to 'rx'")
    # Module finden, die 'rx' triggern
    feeders = {name: 0 for name, modul in modules.items() if pre_rx_module in modul.outputs}

    presses = 0
    while True:
        presses += 1
        queue = deque([("button", Status.START, Pulse.LOW)])

        while queue:
            sender, target, pulse = queue.popleft()

            if target == pre_rx_module and pulse == Pulse.HIGH:
                if feeders[sender] == Pulse.LOW:
                    feeders[sender] = presses

                # Haben wir alle Zyklen gefunden?
                if all(value > 0 for value in feeders.values()):
                    result = math.lcm(*feeders.values())
                    return result

            if target in modules:
                module = modules[target]
                new_pulse = module.process_pulse(sender, pulse)
                if new_pulse is not None:
                    for output in module.outputs:
                        queue.append((target, output, new_pulse))


def solve_mystery_one(modules: dict[str, Module]) -> None:
    result = _prozess_mystery_one(modules)
    # 32000000 / 861743850
    print(f"Result mystery 1: {result}")


def solve_mystery_two(modules: dict[str, Module]) -> None:
    result = _prozess_mystery_two(modules)
    # / 247023644760071
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    initial_modules = _parse(lines)
    # deepcopy, damit wir einen sauberen Status haben
    solve_mystery_one(copy.deepcopy(initial_modules))
    solve_mystery_two(copy.deepcopy(initial_modules))
    calculate_duration()
