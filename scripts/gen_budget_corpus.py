#!/usr/bin/env python3
"""Independent integer-model contracts for overflow-safe cumulative admission."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX = (1 << 64) - 1


def integer(value):
    return {"integer": {"value": value, "type": {"bits": 64, "signed": False}}}


def case(identity, function, inputs, expected):
    return {"id": identity, "request": {"schema_version": "0.1",
            "target": {"module": "examples.budget_consumer", "function": function},
            "arguments": [integer(value) for value in inputs], "step_budget": 4096},
            "expected": [{"boolean": {"value": expected}} if isinstance(expected, bool)
                         else integer(expected)]}


def generate():
    cases = []
    scenarios = [
        ("zero", [0, 0, MAX, 0, 0]),
        ("exact", [100, 10, 9, 10, 0]),
        ("remaining", [100, 10, 3, 10, 4]),
        ("first-rejected", [100, 101, 0, 0, 0]),
        ("product-rejected", [100, 10, 10, 10, 0]),
        ("last-rejected", [100, 10, 9, 10, 1]),
        ("maximum", [MAX, 0, 1, MAX, 0]),
        ("sum-overflow", [MAX, MAX, 0, 0, 1]),
        ("product-overflow", [MAX, 0, MAX, 2, 0]),
        ("huge-zero-product", [MAX, 1, MAX, 0, MAX - 1]),
        ("zero-count", [MAX, 1, 0, MAX, MAX - 1]),
    ]
    for name, inputs in scenarios:
        limit, first, count, unit, last = inputs
        used, accepted = 0, True
        for charge in (first, count * unit, last):
            if accepted and used + charge <= limit:
                used += charge
            else:
                accepted = False
        for function, expected in (("used", used), ("admitted", accepted),
                                   ("available", limit - used if accepted else 0)):
            cases.append(case(name + "-" + function, function, inputs, expected))
    cases.append(case("malformed-state", "malformed_admitted", [1, MAX], False))
    return {"schema_version": "0.1", "name": "budget", "cases": cases}


if __name__ == "__main__":
    path = ROOT / "examples/execution/budget-corpus.json"
    path.write_text(json.dumps(generate(), indent=1) + "\n", encoding="utf-8")
