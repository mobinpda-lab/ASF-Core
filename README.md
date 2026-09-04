# ASF-Core

Autonomous Software Factory Core Platform based on ASF-MOC v9.0.

## Mission

ASF-Core is the **independent factory control plane** for operating multiple software repositories. Product repositories are workloads/clients of the factory, never containers of the factory core.

## Canonical boundary

```text
ASF-Core (FACTORY)
  Governance / Registry / Intake / Queue / Lease / Fencing
  Workers / Execution / Evidence / Gates / Security
  Promotion / Release / Recovery / Audit / Observability
                    |
          +---------+---------+
          |                   |
       adapters            workloads
          |                   |
       Arvin            YadNegar / NCM
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

ASF-Core has the architectural boundary, production orchestrator bootstrap, canonical contracts, fail-closed lifecycle primitives, evidence model foundation, gate primitives, recovery policy and conformance tests in place.

**L10 remains `UNVERIFIED` until a real registered client task produces reconstructible end-to-end factory evidence, including bounded failure/fencing/recovery and release/promotion evidence.**

See `docs/architecture/ASF_MOC_INDEPENDENT_FACTORY_ARCHITECTURE.md` and `docs/architecture/ASF_FACTORY_CONTROL_PLANE_v1.md` for the canonical boundary and implementation contract.
