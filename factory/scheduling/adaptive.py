"""Evidence-based adaptive capacity policy for NIRA."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CapacitySnapshot:
    queued_ai: int
    success_rate: float
    provider_pressure: int
    repeated_failures: int
    active_ai: int


@dataclass(frozen=True)
class CapacityDecision:
    max_ai_leases: int
    reason: str


def decide_ai_capacity(
    snapshot: CapacitySnapshot,
    *,
    minimum: int = 1,
    maximum: int = 4,
    current: int = 1,
) -> CapacityDecision:
    if minimum < 0 or maximum < minimum:
        raise ValueError("invalid capacity bounds")
    current = max(minimum, min(maximum, current))

    if snapshot.provider_pressure > 0:
        return CapacityDecision(max(minimum, current - 1), "PROVIDER_PRESSURE")
    if snapshot.repeated_failures >= 2 or snapshot.success_rate < 0.70:
        return CapacityDecision(max(minimum, current - 1), "QUALITY_DEGRADED")
    if snapshot.queued_ai >= max(3, current * 2) and snapshot.success_rate >= 0.90:
        return CapacityDecision(min(maximum, current + 1), "HEALTHY_BACKLOG")
    return CapacityDecision(current, "HOLD")
