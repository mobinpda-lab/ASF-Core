"""Bounded provider-pressure classification and retry policy.

NIRA must treat provider pressure as a control-plane condition, not as an
ordinary retryable failure. The policy is deliberately provider-agnostic:
it classifies common throttling/routing signals and returns a bounded action.
It never launches work, merges, or promotes.
"""
from __future__ import annotations

from dataclasses import dataclass


PRESSURE_CATEGORIES = frozenset({
    "PROVIDER_RATE_LIMIT",
    "PROVIDER_UNAVAILABLE",
    "PROVIDER_ROUTING_REJECTED",
})


@dataclass(frozen=True)
class ProviderPressureDecision:
    category: str
    retryable: bool
    retry_after_seconds: int
    reason: str


def classify_provider_pressure(
    *,
    status_code: int | None = None,
    message: str = "",
    retry_after_seconds: int | None = None,
) -> ProviderPressureDecision | None:
    """Classify provider pressure without treating it as an ordinary retry.

    429 and common upstream-unavailable responses are retryable only with a
    bounded delay. A 422 is classified as a routing/contract rejection and
    is never retried blindly; it must return to validation/fallback logic.
    """
    text = message.lower()
    if status_code == 429 or any(token in text for token in ("rate limit", "too many requests", "provider pressure")):
        delay = max(1, min(retry_after_seconds or 30, 300))
        return ProviderPressureDecision(
            "PROVIDER_RATE_LIMIT", True, delay, "BOUNDED_PROVIDER_BACKOFF"
        )
    if status_code in {502, 503, 504} or any(token in text for token in ("temporarily unavailable", "upstream unavailable", "service unavailable")):
        delay = max(1, min(retry_after_seconds or 15, 120))
        return ProviderPressureDecision(
            "PROVIDER_UNAVAILABLE", True, delay, "BOUNDED_UPSTREAM_BACKOFF"
        )
    if status_code == 422 or any(token in text for token in ("routing rejected", "invalid model route", "unsupported route")):
        return ProviderPressureDecision(
            "PROVIDER_ROUTING_REJECTED", False, 0, "VALIDATE_OR_SELECT_ALLOWED_ROUTE"
        )
    return None


def pressure_allows_retry(decision: ProviderPressureDecision, attempt: int, max_attempts: int = 2) -> bool:
    """Return whether one bounded provider retry is still permitted."""
    if not decision.retryable:
        return False
    if max_attempts < 1:
        return False
    return attempt < max_attempts
