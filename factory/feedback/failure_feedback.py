"""Bounded failure -> Auto-Fix feedback primitives owned by NIRA Factory.

This module is provider- and product-agnostic. It only decides whether a
failed validation may enter a bounded corrective attempt; it never merges,
promotes, or executes unbounded changes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256


@dataclass(frozen=True)
class Failure:
    task_id: str
    attempt: int
    category: str
    retryable: bool
    evidence_digest: str

    def key(self) -> str:
        raw = f"{self.task_id}|{self.attempt}|{self.category}|{self.evidence_digest}"
        return sha256(raw.encode()).hexdigest()


@dataclass(frozen=True)
class AutoFixDecision:
    action: str
    reason: str
    key: str


@dataclass
class FailureFeedback:
    max_auto_fix_attempts: int = 2
    _seen: set[str] = field(default_factory=set, init=False)

    def decide(self, failure: Failure) -> AutoFixDecision:
        key = failure.key()
        if key in self._seen:
            return AutoFixDecision("SUPPRESS", "DUPLICATE_FAILURE", key)
        self._seen.add(key)
        if not failure.retryable:
            return AutoFixDecision("ESCALATE", "NON_RETRYABLE", key)
        if failure.attempt >= self.max_auto_fix_attempts:
            return AutoFixDecision("ESCALATE", "AUTO_FIX_BUDGET_EXHAUSTED", key)
        return AutoFixDecision("AUTO_FIX", "BOUNDED_RETRYABLE_FAILURE", key)
