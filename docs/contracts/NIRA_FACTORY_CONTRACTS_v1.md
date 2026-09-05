# NIRA Factory Contracts v1

**Issue:** #23  
**Status:** Canonical draft for implementation  
**Historical source:** Arvin factory audit / ASF-MOC lineage

## Purpose
This document defines the minimum provider-neutral contract boundary between NIRA and registered client repositories. It is the canonical replacement for factory-core assumptions embedded in product repositories.

## 1. Intake
A client submits a work item containing:
- client_id
- project_id
- issue_id
- requested_operation
- priority
- dependency/conflict metadata
- expected_base_sha
- requested worker class
- acceptance/gate profile

NIRA assigns the canonical queue identity. Client text is untrusted input and cannot grant merge authority.

## 2. Queue
Queue state is machine-readable and monotonic:
`RECEIVED -> ELIGIBLE -> LEASED -> RUNNING -> VALIDATING -> PROMOTABLE -> PROMOTED | FAILED | BLOCKED`

Only NIRA may change lease/queue ownership state. Duplicate active work is rejected or deterministically coalesced.

## 3. Lease
A lease binds:
- queue_item_id
- client/project
- issue_id
- expected_base_sha
- worker_id
- lease_version
- acquired_at
- expiry_at
- heartbeat

Workers must fail closed if the checked-out base differs from expected_base_sha or the lease is stale/fenced.

## 4. Worker
Workers are capability-specific and have no merge authority. They may read, propose changes, run bounded tests, and publish evidence. Write access is restricted to the leased branch/worktree and authorized paths.

## 5. Gate
A promotion gate evaluates exact head/base, required CI, tests, build/device checks where applicable, security/policy checks, and evidence integrity. Missing or stale evidence is not PASS.

## 6. Evidence
Every terminal decision must be reconstructible from immutable identifiers:
- client/project
- issue/PR
- base_sha
- head_sha
- worker/lease identity
- workflow/run identifiers
- gate results
- artifact/release identifiers
- timestamps
- failure/recovery history

Worker self-report is not independent evidence.

## 7. Promotion
Promotion is serialized per project/task and owned by one NIRA authority. Before promotion NIRA re-reads the target state and verifies exact base/head. Post-promotion state is independently re-read and recorded.

## 8. Recovery
Recovery is bounded and idempotent. Default policy:
- lease TTL: 5 minutes
- heartbeat: 60 seconds
- retry budget: 3
- stale workers are fenced
- terminal failure creates or updates one recovery item

Recovery may resume work only after revalidation of base SHA, lease ownership, and gate prerequisites.

## 9. Client boundary
Arvin, YadNegar, NetworkCenterMonitor and future repositories implement only client adapters. They may expose product-specific acceptance rules, build commands and domain metadata, but must not implement NIRA queue/lease/worker/promotion authority.

## 10. L10 rule
These contracts establish a foundation, not proof of L10. L10 remains `UNVERIFIED` until a genuine registered-client E2E cycle produces reconstructible evidence covering success, failure/fencing/recovery, and promotion/release.
