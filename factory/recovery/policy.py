"""Bounded retry and recovery policy shared by all project adapters."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RecoveryPolicy:
    max_attempts: int = 3
    lease_ttl_seconds: int = 300
    heartbeat_seconds: int = 60

    def __post_init__(self) -> None:
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be positive")
        if self.lease_ttl_seconds <= self.heartbeat_seconds:
            raise ValueError("lease TTL must exceed heartbeat interval")

    def decision(self, attempt: int, retryable: bool) -> str:
        if attempt >= self.max_attempts:
            return "ESCALATE"
        if retryable:
            return "REQUEUE"
        return "ESCALATE"
