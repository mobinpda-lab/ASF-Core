# NIRA

**NIRA** is the official and sole canonical name of the autonomous software factory control plane.

**Repository identity:** `mobinpda-lab/NIRA` after the repository rename. The former repository slug is retained only in the historical record and must not be used as an active authority identifier.

## Mission

NIRA is the independent factory control plane for operating multiple software repositories. Product repositories are workloads/clients of NIRA, never containers of the factory core.

## Canonical boundary

```text
NIRA
  Governance / Registry / Intake / Queue / Lease / Fencing
  Workers / Execution / Evidence / Gates / Security
  Promotion / Release / Recovery / Audit / Observability
                    |
          +---------+---------+
          |                   |
       adapters            workloads
          |                   |
       Arvin            YadNegar / NetworkCenterMonitor
```

The factory is generic. Project-specific behavior belongs behind adapters and explicit contracts.

## Core invariants

- No direct main mutation for factory development.
- Exact HEAD and exact base are mandatory for promotion.
- Worker claims are never accepted as independent evidence.
- Missing, stale, invalid or inaccessible evidence is never a PASS.
- One active lease owns a task; stale owners are fenced.
- Recovery is bounded (default: 3 attempts; 5-minute lease TTL; 60-second heartbeat).
- Promotion is serialized per project/task and verified by an independent postcondition read.
- Factory progress and product progress are reported separately.

## Canonical lifecycle

```text
IDEA -> DEFINITION -> ARCHITECTURE -> TASK -> QUEUE -> LEASE
 -> WORKER -> CODE -> TEST -> AUTOFIX -> CI -> EVIDENCE
 -> SECURITY -> GATES -> EXACT-HEAD -> PROMOTION -> RELEASE
 -> MONITOR -> FAILURE/FENCING -> RECOVERY/RESUME -> COMPLETE
```

## Current maturity statement

NIRA has the architectural boundary, production orchestrator bootstrap, canonical contracts, fail-closed lifecycle primitives, evidence model foundation, gate primitives, recovery policy and conformance tests in place.

**L10 remains `UNVERIFIED` until a real registered client task produces reconstructible end-to-end factory evidence, including bounded failure/fencing/recovery and release/promotion evidence.**

The complete historical naming transition is recorded in `docs/history/NIRA_IDENTITY_HISTORY.md`. Historical identifiers are provenance only and are never active factory authority.

See `docs/architecture/NIRA_FACTORY_CONTROL_PLANE_v1.md` and `docs/architecture/NIRA_INDEPENDENT_FACTORY_ARCHITECTURE.md` for the canonical boundary and implementation contract.

## Self-dogfood execution

NIRA can execute bounded maintenance against its own repository while remaining a separate control plane from product clients. Self-dogfood work is leased against the exact current `main` SHA, protected by lease/fence validation, executed on a dedicated branch, and proposed through a pull request. Workers have no merge or promotion authority. Promotion remains fail-closed behind exact-head NIRA CI, Factory E2E, Factory Conformance, Security Gate, independent artifacts/evidence, and post-merge verification. Recovery and retries are bounded, and lessons learned from Arvin are generalized into NIRA-owned contracts without importing Arvin product logic.
