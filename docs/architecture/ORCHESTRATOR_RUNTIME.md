# Orchestrator Runtime

The ASF-Core orchestrator runtime is the deterministic control-plane boundary between validated task intake and later queue/worker execution.

## Flow

`intake → execution context → dependency validation → evidence evaluation → decision → lifecycle transition → immutable decision history`

The runtime does not execute product code, lease workers, merge pull requests, or write product repositories. Those capabilities remain behind the existing queue/worker and adapter contracts.

## Decision model

Every decision evaluates task lifecycle state, dependency readiness, evidence state, and optional failure class. The result is one of `ALLOW`, `BLOCK`, `WAIT`, or `RECOVER` and records a UTC timestamp, reason, previous state, and resulting transition where applicable.

`ALLOW` means the task satisfies runtime gates. `WAIT` means an external prerequisite is incomplete. `BLOCK` is fail-closed for invalid state, invalid evidence, governance failures, or unknown failures. `RECOVER` moves an eligible failed/running/validation state into `RECOVERING`.

## Dependencies

The dependency engine validates the complete graph, rejects unknown dependencies and cycles, and reports a task ready only when every prerequisite is `COMPLETED`.

## Failure handling

| Failure | Runtime action |
|---|---|
| TRANSIENT | RETRY |
| EVIDENCE | WAIT |
| VALIDATION | RECOVER |
| GOVERNANCE | BLOCK |
| UNKNOWN | BLOCK |

This mapping is intentionally fail-closed. Retry execution itself belongs to the later queue/worker wave.

## Evidence and history

Evidence records are append-only in the runtime: duplicate evidence IDs are rejected. Decision history is append-only, while lifecycle transitions are validated by the existing lifecycle state machine. No decision can bypass lifecycle validation.

## Wave boundary

This wave establishes an operational orchestration decision runtime. Queue leasing, worker execution, retries, and autonomous task dispatch remain the next wave so that execution cannot begin without this control-plane gate.
