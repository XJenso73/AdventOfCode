# Advent of Code 2023 - Day 19
import math
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from src.utils import calculate_duration, import_data

type Ranges = dict[str, tuple[int, int]]
type WorkflowRules = dict[str, list[Rule]]
type Workflows = list[Part]

FILE = "./datas/day19_debug.txt"
# FILE = "./datas/day19.txt"
RULE_PATTERN = re.compile(r"([xmas])([<>])(\d+):(\w+)")


class Status(str, Enum):
    ACCEPTED = "A"
    REJECTED = "R"
    START = "in"


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def total_value(self):
        return self.x + self.m + self.a + self.s


@dataclass(frozen=True, slots=True)
class Rule:
    attr: str | None
    op: str | None
    value: int | None
    target: str

    # Teil 1
    def matches(self, part: Part) -> bool:
        if self.attr is None:
            return True
        val = getattr(part, self.attr)
        return val > self.value if self.op == ">" else val < self.value

    # Teil 2
    def split_range(self, ranges: dict[str, tuple[int, int]]) -> tuple[dict | None, dict | None]:
        if self.attr is None:
            return ranges, None

        low, high = ranges[self.attr]
        match_range = dict(ranges)
        else_range = dict(ranges)

        if self.op == "<":
            # Regel: x < 2000 -> Passend: [low, 1999], Rest: [2000, high]
            match_range[self.attr] = (low, self.value - 1)
            else_range[self.attr] = (self.value, high)
        else:  # op == ">"
            # Regel: x > 2000 -> Passend: [2001, high], Rest: [low, 2000]
            match_range[self.attr] = (self.value + 1, high)
            else_range[self.attr] = (low, self.value)

        # Validierung: Falls ein Intervall unsinnig wird low > high, ist es None
        m_l, m_h = match_range[self.attr]
        e_l, e_h = else_range[self.attr]

        return (match_range if m_l <= m_h else None, else_range if e_l <= e_h else None)


def _parse(lines: list[str]) -> tuple[WorkflowRules, Workflows]:
    split_index = lines.index("")
    workflow_lines = lines[:split_index]
    part_lines = lines[split_index + 1 :]
    workflow_rules = {}
    for line in workflow_lines:
        line = line.strip()
        name, rules_str = line.strip("}").split("{")
        rules = rules_str.strip().split(",")
        parsed_rules = []
        for rule in rules:
            parsed_rules.append(_parse_rule(rule))
        workflow_rules[name] = parsed_rules
    workflow = [_parse_part(line) for line in part_lines]
    return (workflow_rules, workflow)


def _parse_part(line: str) -> Part:
    attrs = dict(part.split("=") for part in line.strip("{}").split(","))
    return Part(x=int(attrs["x"]), m=int(attrs["m"]), a=int(attrs["a"]), s=int(attrs["s"]))


def _parse_rule(rule: str) -> Rule:
    if match := RULE_PATTERN.match(rule):
        attr, op, value, target = match.groups()
        return Rule(attr, op, int(value), target)
    return Rule(None, None, None, rule)


def _is_accepted(workflow_rules: WorkflowRules, part: Part) -> bool:
    current = Status.START
    while current not in (Status.ACCEPTED, Status.REJECTED):
        rules = workflow_rules[current]
        for rule in rules:
            if rule.matches(part):
                current = rule.target
                break

    return current == Status.ACCEPTED


def _count_accepted(name: str, ranges: Ranges, rules: WorkflowRules) -> int:
    # Basis-Fälle
    if name == Status.REJECTED:
        return 0
    if name == Status.ACCEPTED:
        return math.prod(high - low + 1 for low, high in ranges.values())

    total = 0
    current_ranges = ranges

    #  aktuellen Workflow durchlaufen
    for rule in rules[name]:
        match, fallback = rule.split_range(current_ranges)

        if match:
            total += _count_accepted(rule.target, match, rules)

        if fallback:
            current_ranges = fallback
        else:
            # Wenn kein Rest übrig ist,
            break

    return total


def solve_mystery_one(rules: WorkflowRules, workflows: Workflows) -> None:
    result = 0
    for workflow in workflows:
        if _is_accepted(rules, workflow):
            result += workflow.total_value()
    # 19114 / 399284
    print(f"Result mystery 1: {result}")


def solve_mystery_two(rules: WorkflowRules) -> None:
    start_ranges = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
    result = _count_accepted("in", start_ranges, rules)
    # 167409079868057 / 121964982771486
    print(f"Result mystery 2: {result}")


if __name__ == "__main__":
    lines = import_data(FILE)
    rules, workflow = _parse(lines)
    solve_mystery_one(rules, workflow)
    solve_mystery_two(rules)
    calculate_duration()
