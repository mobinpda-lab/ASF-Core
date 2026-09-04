"""Fail-closed task lifecycle and lease fencing primitives."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum

from factory.contracts.schema import TaskState


class LeaseDecision(str, Enum):
    ACCEPT = "ACCEPT"
    REJECT_EXPIRED = "REJECT_EXPIRED"
    REJECT_FENCED = "REJECT_FENCED"
    REJECT_OWNER = "REJECT_OWNER"


@dataclass(frozen=True)
class Lease:
    lease_id: str
    task_id: str
    worker_id: str
    fence_token: int
    issued_at: datetime
    expires_at: datetime

    def active(self, now: datetime | None = None) -> bool:
        now = now or datetime.now(timezone.utc)
        return now < self.expires_at


def validate_lease(lease: Lease, worker_id: str, fence_token: int, now: datetime | None = None) -> LeaseDecision:
    if not lease.active(now):
        return LeaseDecision.REJECT_EXPIRED
    if worker_id != lease.worker_id:
        return LeaseDecision.REJECT_OWNER
    if fence_token != lease.fence_token:
        return LeaseDecision.REJECT_FENCED
    return LeaseDecision.ACCEPT


ALLOWED_TRANSITIONS: dict[TaskState, set[TaskState]] = {
    TaskState.READY: {TaskState.LEASED, TaskState.CANCELLED},
    TaskState.LEASED: {TaskState.RUNNING, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.RUNNING: {TaskState.VALIDATING, TaskState.FAILED, TaskState.CANCELLED},
    TaskState.VALIDATING: {TaskState.PROMOTABLE, TaskState.FAILED},
    TaskState.PROMOTABLE: {TaskState.PROMOTED, TaskState.FAILED},
    TaskState.PROMOTED: {TaskState.COMPLETED},
    TaskState.FAILED: {TaskState.READY, TaskState.ESCALATED},
    TaskState.ESCALATED: set(),
    TaskState.COMPLETED: set(),
    TaskState.CANCELLED: set(),
}


def transition(current: TaskState, target: TaskState) -> TaskState:
    if target not in ALLOWED_TRANSITIONS[current]:
        raise ValueError(f"illegal task transition: {current.value} -> {target.value}")
    return target


def expiry_from(now: datetime, ttl_seconds: int = 300) -> datetime:
    if ttl_seconds <= 0:
        raise ValueError("ttl_seconds must be positive")
    return now + timedelta(seconds=ttl_seconds)
