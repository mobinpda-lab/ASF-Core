# NIRA Recovery and Provider-Pressure Policy

NIRA treats provider pressure as a control-plane condition, not as an ordinary failure.

## Rules

- HTTP 429 and bounded upstream-unavailable conditions may retry only within an explicit attempt and delay budget.
- Retry-After values are capped; provider-controlled values cannot create unbounded waits.
- HTTP 422 and routing/contract rejection are non-retryable by default and must return to validation or route-selection logic.
- Provider pressure never grants merge, promotion, lease, or evidence authority.
- A failed provider call must release or preserve its execution lease according to the normal recovery contract; it must not strand work.
- Recovery remains bounded and fail-closed.

The policy is provider-agnostic and is intentionally separate from any product-specific client behavior.
