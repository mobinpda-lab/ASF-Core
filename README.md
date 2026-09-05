# NIRA — نِیرا

**NIRA OS — نِیرا، سامانهٔ خودکار تولید نرم‌افزار**  
**NIRA Core — هستهٔ خودمختار کارخانهٔ نرم‌افزار**

> Historical repository/project identifier: `ASF-Core` — Autonomous Software Factory Core. Historical architecture identifier: `ASF-MOC v9.0`.

## Mission

NIRA is the **independent factory control plane** for operating multiple software repositories. Product repositories are external workloads/clients of NIRA, never containers of the factory core.

**Proposed name meaning:** «نِیرا = نیروی ایرانیِ راه‌انداز».

## Canonical boundary

```text
NIRA OS / NIRA Core (FACTORY)
  Governance / Registry / Intake / Queue / Lease / Fencing
  Workers / Execution / Evidence / Gates / Security
  Promotion / Release / Recovery / Audit / Observability
                    |
          +---------+---------+
          |                   |
       adapters            workloads
          |                   |
      Arvin / YadNegar / NetworkCenterMonitor / future clients
```

The factory is generic. Project-specific behavior belongs behind explicit client contracts and adapters.

## Naming

- **NIRA OS** — system/platform layer
- **NIRA Core** — factory execution/control core
- **NIRA Factory** — autonomous software production environment
- **NIRA Agents** — autonomous workers/agents
- **NIRA Engine** — orchestration engine
- **NIRA CI** — integration and validation subsystem
- **NIRA Governance** — policy, security, authority, and audit
- **NIRA Runtime** — controlled agent execution environment

## Independence law

NIRA is the sole canonical home for factory-core architecture, governance, orchestration, queue/lease lifecycle, worker contracts, evidence, gates, promotion, release automation, recovery, and factory observability.

Arvin, YadNegar, NetworkCenterMonitor, and future projects remain independent clients/workloads. Factory-related material discovered in those repositories is migrated by classification and provenance, not by blind copying.

See `docs/NIRA_IDENTITY_AND_INDEPENDENCE.md` and `docs/NIRA_FACTORY_MIGRATION_MANIFEST.md`.

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

See `docs/architecture/ASF_MOC_INDEPENDENT_FACTORY_ARCHITECTURE.md` and `docs/architecture/ASF_FACTORY_CONTROL_PLANE_v1.md` for the canonical boundary and implementation contract.
