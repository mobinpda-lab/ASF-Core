"""Deterministic, fail-closed gate evaluation.

A gate is PASS only when its predicate is explicitly verified. Unknown,
missing, stale, or provider-inaccessible evidence can never become PASS.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterable


class GateResult(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_EXPOSED = "NOT_EXPOSED"
    STALE = "STALE"
    INVALID = "INVALID"


@dataclass(frozen=True)
class Gate:
    name: str
    predicate: Callable[[object], bool]
    required: bool = True


@dataclass(frozen=True)
class GateDecision:
    result: GateResult
    failed_gates: tuple[str, ...] = ()


def evaluate(gates: Iterable[Gate], context: object) -> GateDecision:
    failed: list[str] = []
    for gate in gates:
        try:
            passed = gate.predicate(context)
        except Exception:
            passed = False
        if gate.required and not passed:
            failed.append(gate.name)
    return GateDecision(GateResult.PASS if not failed else GateResult.BLOCKED, tuple(failed))


def exact_head_gate(expected: str, observed: str) -> bool:
    return bool(expected) and expected == observed


def exact_base_gate(expected: str, observed: str) -> bool:
    return bool(expected) and expected == observed


def artifact_gate(required_name: str, artifacts: Iterable[dict]) -> bool:
    return any(a.get("name") == required_name and not a.get("expired", True) for a in artifacts)
