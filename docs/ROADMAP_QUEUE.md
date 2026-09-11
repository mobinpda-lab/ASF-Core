# NIRA Roadmap Queue

> Generated from live GitHub Issues. Issue state/labels are authoritative.
> Operational alignment: NIRA Autonomous Software Factory Operating Standard v2.0

## NOW

| Task | Goal | Priority | Status | Evidence/Labels |
|---|---|---:|---|---|
| #86 | dogfood(nira): exact-main intelligence pipeline completion proof | P1 | READY | automation, factory, factory:ready, nira, priority:core |
| #68 | execute: YadNegar completion wave #244 | P4 | BLOCKED | factory:blocked, factory:ready |

## NEXT

| Task | Goal | Priority | Status | Evidence/Labels |
|---|---|---:|---|---|
| #25 | feat(nira): activate real cross-repository execution plane from migrated Arvin factory patterns | P2 | QUEUED | factory:queued, factory:ready, priority:automation |
| #29 | feat(nira): establish Future Projects registration boundary | P2 | READY | factory:ready, priority:automation |

## LATER

| Task | Goal | Priority | Status | Evidence/Labels |
|---|---|---:|---|---|
| #27 | feat(nira): provision real cross-repository execution plane | P4 | QUEUED | enhancement, factory:queued |
| #97 | [AUTO-FIX] NIRA Factory Conformance failed | P4 | QUEUED | factory:queued, factory:ready |

## Standard v2 Task Contract

Every new or modified task must define:

- Task ID
- Goal
- Priority
- Dependencies
- Owner / Worker
- Lease
- Fence
- Acceptance Criteria
- Required Evidence
- Validation Requirements
- Promotion Requirements
- Result

## Queue Contract

- Existing code/issues/PRs/branches must be reused before new work is created.
- Independent repositories may execute in parallel; competing mutations against one client main are serialized.
- Failure is routed through classification/recovery; it is never counted as completion.
- Completion requires exact-SHA execution evidence.
- Queue state must remain consistent with live GitHub state.
