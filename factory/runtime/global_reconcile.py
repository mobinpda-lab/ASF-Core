"""NIRA Autonomous Global Reconcile decision engine.

This module is intentionally decision-only. It does not dispatch workers,
modify main, merge PRs, or bypass human gates.

Flow:
GitHub snapshot -> reconcile -> WAIT/RECOVER/CONTINUE decision -> queue handoff
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class ReconcileDecision(str, Enum):
    WAIT = "WAIT"
    RECOVER = "RECOVER"
    CONTINUE = "CONTINUE"


@dataclass(frozen=True)
class ReconcileSnapshot:
    main_sha: str
    active_workers: int = 0
    active_leases: int = 0
    open_prs: int = 0
    active_workflows: int = 0
    release_blockers: tuple[str, ...] = field(default_factory=tuple)
    retryable_failures: tuple[str, ...] = field(default_factory=tuple)
    security_holds: tuple[str, ...] = field(default_factory=tuple)
    pending_product_tasks: int = 0


@dataclass(frozen=True)
class ReconcileResult:
    decision: ReconcileDecision
    reason: str


class GlobalReconciler:
    """Deterministic policy layer for autonomous continuation."""

    def reconcile(self, state: ReconcileSnapshot) -> ReconcileResult:
        if state.security_holds:
            return ReconcileResult(
                ReconcileDecision.WAIT,
                "human/security gate required",
            )

        if self._has_active_execution(state):
            return ReconcileResult(
                ReconcileDecision.WAIT,
                "existing worker, lease, workflow or PR is active",
            )

        if state.retryable_failures:
            return ReconcileResult(
                ReconcileDecision.RECOVER,
                "bounded recovery required",
            )

        if state.release_blockers:
            return ReconcileResult(
                ReconcileDecision.CONTINUE,
                "release blocker remediation has priority",
            )

        if state.pending_product_tasks:
            return ReconcileResult(
                ReconcileDecision.CONTINUE,
                "product work available",
            )

        return ReconcileResult(
            ReconcileDecision.WAIT,
            "no safe action available",
        )

    @staticmethod
    def _has_active_execution(state: ReconcileSnapshot) -> bool:
        return any(
            value > 0
            for value in (
                state.active_workers,
                state.active_leases,
                state.open_prs,
                state.active_workflows,
            )
        )
