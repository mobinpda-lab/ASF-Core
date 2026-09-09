"""Provider-neutral NIRA queue scheduling policy.

This module contains only factory control-plane decisions. It knows nothing
about product code and never mutates repositories or promotes pull requests.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ExecutionLane(str, Enum):
    AI = "AI"
    DETERMINISTIC = "DETERMINISTIC"


_PRIORITY = {
    "priority:release-blocker": 0,
    "priority:core": 1,
    "priority:automation": 2,
    "priority:feature": 3,
}


def priority_rank(labels: set[str] | frozenset[str]) -> int:
    """Return the best stable NIRA queue rank for a task label set."""
    ranks = [_PRIORITY[label] for label in labels if label in _PRIORITY]
    return min(ranks, default=4)


def execution_lane(issue_body: str) -> ExecutionLane:
    body = issue_body.lower()
    if "nira_execution_mode: deterministic-doc-append" in body:
        return ExecutionLane.DETERMINISTIC
    return ExecutionLane.AI


@dataclass(frozen=True)
class CapacityPolicy:
    max_ai_leases: int = 1
    max_deterministic_leases: int = 4

    def __post_init__(self) -> None:
        if self.max_ai_leases < 0 or self.max_deterministic_leases < 0:
            raise ValueError("capacity values cannot be negative")

    def available(self, lane: ExecutionLane, active_ai: int, active_deterministic: int) -> int:
        if lane is ExecutionLane.AI:
            return max(0, self.max_ai_leases - active_ai)
        return max(0, self.max_deterministic_leases - active_deterministic)
