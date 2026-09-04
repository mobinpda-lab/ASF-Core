# ASF Factory Control Plane v1

**Status:** Canonical implementation contract
**Scope:** ASF-Core only
**Date:** 2026-09-04

## Objective

ASF-Core is an independent autonomous software factory control plane. It operates registered repositories through explicit contracts and adapters. Product repositories never become the source of truth for factory behavior.

## Control-plane domains

1. Governance and authorization
2. Project Registry
3. Task Intake
4. Priority Queue
5. Lease and fencing
6. Worker lifecycle
7. Agent execution
8. Independent evidence collection
9. Deterministic gates
10. Security gates
11. Promotion and release
12. Recovery/resume
13. Observability and append-only audit
14. Adapter/conformance contracts

## Canonical state model

```text
READY -> LEASED -> RUNNING -> VALIDATING -> PROMOTABLE -> PROMOTED -> COMPLETED
                  |                     |
                  v                     v
                FAILED --------------> READY/ESCALATED
```

Terminal states are immutable. A stale worker may not mutate a task after its lease expires or its fence token is superseded.

## Concurrency invariants

- At most one active lease owns a task.
- Each lease has a unique monotonically increasing fence token.
- Branch mutation, promotion and release are serialized per task/project.
- Observation, CI monitoring and independent analysis may run in parallel.
- Every mutating action is idempotent or guarded by an exact precondition.
- Evidence is invalidated by relevant HEAD/base drift.

## Evidence invariants

Worker claims are not evidence. Evidence is collected independently from the provider/runtime. `UNKNOWN`, `NOT_EXPOSED`, `STALE`, and `INVALID` never satisfy a required gate.

For promotion, the factory must establish at minimum:

- PR is authorized and eligible.
- PR HEAD equals the expected result SHA.
- PR base equals the verified current main SHA.
- Required CI completed successfully on that exact HEAD.
- Required artifacts exist and are not expired.
- Required security gates pass.
- Promotion postcondition changes main to the provider-reported merge result.
- The final main SHA is independently re-read after mutation.

## Recovery

Default operational policy is a five-minute lease TTL, sixty-second heartbeat, and at most three attempts. Expired ownership is fenced before requeue. Non-retryable failures or exhausted attempts escalate instead of looping indefinitely.

## Project boundary

Arvin-clean, YadNegar and NetworkCenterMonitor are clients/workloads. Their product code, product-specific workflows and domain logic do not belong in ASF-Core. Product-side integrations must use an adapter contract.

## L10 completion definition

L10 is not a file-count or workflow-count metric. It requires authentic, reconstructible evidence of a real registered project task completing the complete factory lifecycle, including failure/fencing/recovery behavior, without synthetic passes or manual promotion.

Until that evidence exists, ASF-Core must report `L10_UNVERIFIED`.
