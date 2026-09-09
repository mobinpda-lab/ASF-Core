# NIRA Roadmap Queue

> Derived operating queue. GitHub Issues and live factory labels are authoritative.

## NOW

| Task ID | Goal | Priority | Dependencies | Acceptance Criteria | Status | Evidence |
|---|---|---|---|---|---|---|
| #86 | Complete NIRA intelligence dogfood proof | P0 | current main, deterministic worker | exact lease/fence, README-only PR, FAST impact, four gates, orchestrator merge | ACTIVE | GitHub issue/workflow evidence |
| #68 | Execute YadNegar completion wave | P0 | GitHub App, registered client, safe bounded scope | client branch/PR, native CI/security, independent evidence, guarded promotion | READY/BLOCKED BY LIVE CONDITIONS | GitHub issue/workflow evidence |
| #25/#27 | Prove real cross-repository execution plane | P0 | registered client credentials and safe task | full issue→lease→worker→PR→CI/security→evidence→promotion chain | IN PROGRESS | GitHub issues #25/#27 |

## NEXT

| Task ID | Goal | Priority | Dependencies | Acceptance Criteria | Status | Evidence |
|---|---|---|---|---|---|---|
| #30 | Continuous wave orchestration and learning | P1 | stable real execution evidence | repeatable recovery, parallel independent clients, retained provenance | PLANNED | GitHub issue #30 |
| #51 | Reconcile reusable Arvin-proven patterns | P1 | no client coupling | NIRA-owned generic contracts with exact-head evidence | IN PROGRESS | GitHub issue #51 |

## LATER

| Task ID | Goal | Priority | Dependencies | Acceptance Criteria | Status | Evidence |
|---|---|---|---|---|---|---|
| #29 | Future-project registration boundary | P2 | registry stability | new clients onboard by contract/adapter only | PLANNED | GitHub issue #29 |

## Queue Rules

- One canonical active path per capability.
- Existing code/issue/PR/branch evidence must be reused before new work is created.
- Independent client work may run in parallel; mutations against the same client main are serialized.
- No task is complete without reconstructible execution evidence.
