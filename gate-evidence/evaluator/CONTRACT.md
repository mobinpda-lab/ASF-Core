# Gate Evidence Evaluator Contract

The evaluator produces a deterministic promotion decision from normalized gate evidence.

## States
`SUCCESS | FAILURE | PENDING | NOT_FOUND | NOT_EXPOSED`

## Decision
- `ALLOW` iff every required gate is `SUCCESS`.
- `BLOCK` for any `FAILURE`, `PENDING`, `NOT_FOUND`, or `NOT_EXPOSED`.
- No worker, adapter, or connector may override the decision.

The evaluator MUST fail closed when required evidence is unresolved or stale.
