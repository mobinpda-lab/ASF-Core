# Parallel Factory Evolution — Queue/Worker Wave

## Scope

This development wave adds provider-independent execution primitives without
waiting for CI Evidence Observer or Orchestrator Promotion closure.

## Components

- QueueCore: deterministic task intake, claim, completion, failure, and lease reclaim.
- TaskScheduler: reclaim-expired leases before selecting ready work.
- Lease: explicit task/worker ownership and expiration.
- WorkerIdentity: stable runtime identity for an execution attempt.
- ExecutionContext: immutable task + worker + lease boundary.
- WorkerRuntime: executes one scheduled task and records success/failure.

## Governance

Development branch only. No direct `main` write, manual merge, product-repository
modification, fabricated evidence, evidence-only commit, or workflow-only change.
Promotion remains the Production Orchestrator responsibility.

## Recovery boundary

Expired leases become `RETRY_WAIT` and can be reclaimed by another worker.
Terminal failures remain `FAILED` until a future retry policy explicitly requests
recovery. Persistent queue storage and distributed locking are adapters, not
assumed by this core.
