# Arvin Factory Artifact Catalog for NIRA

Source: mobinpda-lab/Arvin-clean @ 9a773b7898ff63276ad6a214009b163f904e8923
Purpose: preserve discoverable provenance for factory-relevant Arvin material while keeping NIRA independent.

## Canonical / high-value source documents

| Source artifact | NIRA treatment | Reason |
|---|---|---|
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE.md` | historical factory-operating source | operating model, parallel execution, evidence-first rules |
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE_v48.2_TRANSFER_MANIFEST.md` | provenance source | transfer/integrity history |
| `docs/ARVIN_PROJECT_STATE.md` | state-history source | project-state and authority rules |
| `docs/ARVIN_STATUS.md` | reporting-history source | evidence-oriented status/reporting model |
| `docs/DEVELOPMENT_RULES.md` | governance source | foundation protection and quality-before-merge rules |
| `docs/REPORTING_STANDARD.md` | reporting source | STATUS/EVIDENCE/BLOCKER reporting vocabulary |
| `docs/DOCUMENT_AUTHORITY_INDEX.md` | authority source | GitHub reality and document precedence |
| `docs/AI_HANDOFF_CURRENT_FA.md` | continuity source | exact-head/evidence continuation model |
| `docs/AI_CONTINUATION_STATE.md` | continuity source | source-of-truth and continuation rules |
| `docs/PROJECT_PROGRESS_METRIC.md` | metric source | evidence-backed progress scoring |
| `docs/PROJECT_STATUS.md` | execution-history source | lane independence and exact-head merge rules |
| `docs/CI_FAST_LANE_2026-08-26.md` | CI/recovery source | exact-head validation fallback |
| `docs/RELEASE_EVIDENCE_COMPLETION_LANE_2026-08-26.md` | release-evidence source | release gate evidence |
| `docs/ARVIN_PRODUCTION_ORCHESTRATOR_5MIN_MODE.md` | orchestration source | autonomous production operating direction |

## Runtime source artifacts

- `.github/workflows/arvin-autonomous-queue.yml`
- `.github/workflows/arvin-agent-worker.yml`
- `.github/arvin/agent-runtime.py`
- `.github/workflows/arvin-orchestrator.yml`
- `.github/workflows/production-orchestrator.yml`
- `.github/workflows/factory-rest-promotion-bridge.yml`
- `.github/workflows/release-closure.yml`
- `test/production_orchestrator_contract_test.dart`

## What the source proves

The Arvin repository contains real GitHub workflow implementations that demonstrate useful patterns for intake/routing, lease markers, exact-main validation, bounded worker execution, draft PR creation, exact-head gates, guarded promotion, post-merge verification, and watchdog-style re-evaluation.

## What it does NOT prove for NIRA

These Arvin runs are client-side evidence. They do not establish NIRA L10. NIRA must independently execute and observe the chain through its own factory control plane.

## Migration policy

The catalog is intentionally a manifest rather than a blind repository copy. NIRA is the factory and Arvin is a client. Client-specific implementation remains in Arvin; reusable factory behavior is re-expressed generically inside NIRA.

## Provenance target

The migration must preserve:
- source repository;
- source commit/ref;
- source file path;
- capability extracted;
- NIRA destination;
- adaptation required;
- validation evidence;
- resulting NIRA commit/PR.

No artifact is considered migrated merely because a similar filename exists in NIRA.
