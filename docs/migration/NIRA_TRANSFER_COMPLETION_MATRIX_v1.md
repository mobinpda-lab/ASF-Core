# NIRA Transfer Completion Matrix v1

**Date:** 2026-09-05
**Issue:** #23
**Status:** Controlled migration — not yet operationally complete

## Completion rule
The Arvin → NIRA transfer is complete only when every factory-core responsibility has a canonical NIRA implementation, a tested client boundary, and at least one independently reconstructible registered-client E2E cycle. Until then, legacy Arvin factory automation remains protected from deletion.

| Area | Canonical NIRA home | Contract/test state | Arvin legacy state | Transfer status |
|---|---|---|---|---|
| Intake | NIRA Factory Intake | Contract defined | Present | Pending executable boundary |
| Registry | NIRA Registry | Existing foundation | Present/implicit | Pending client registration proof |
| Queue | NIRA Queue | Contract defined | `arvin-autonomous-queue.yml` | Pending executable NIRA dispatch |
| Lease/Fencing | NIRA Runtime | Contract + tests | Arvin queue/worker leases | Pending cross-repo proof |
| Worker lifecycle | NIRA Workers | Contract defined | `arvin-agent-worker.yml` etc. | Pending NIRA worker execution |
| AI/provider policy | NIRA Runtime/Agents | Boundary defined | `agent-runtime.py` | Pending provider-neutral executable runtime |
| Gates | NIRA Gates | Existing contract tests | Arvin gates/workflows | Pending independent promotion gate |
| Evidence | NIRA Evidence | Schema + tests | Arvin evidence docs/workflows | Pending independent collector/E2E evidence |
| Recovery | NIRA Recovery | Contract + bounded policy | Arvin production loop | Pending real stale/failure recovery proof |
| Promotion | NIRA Promotion | Contract defined | Arvin promotion bridge | Pending single NIRA authority proof |
| Release | NIRA Release | Boundary defined | Arvin release automation | Pending NIRA-owned orchestration |
| Documentation law | NIRA Governance | Migration law defined | Arvin documentation policy | Pending executable enforcement |
| Arvin adapter | NIRA client boundary | v1 contract defined | Not yet connected | **Pending** |
| Registered Arvin E2E | NIRA ↔ Arvin | Test scaffold exists | Legacy flow available | **Not proven** |
| L10 | NIRA | Rule defined | Historical claims only | **UNVERIFIED** |

## Required remaining sequence
1. Rebase/refresh the NIRA branch against the latest `main` without losing migration commits.
2. Implement executable NIRA intake/queue/lease/worker/gate/evidence/recovery/promotion boundaries using existing ASF-Core foundation rather than duplicating it.
3. Register Arvin as a NIRA client and connect the adapter without granting client-side merge authority.
4. Run NIRA contract/conformance tests.
5. Execute one real Arvin cycle through NIRA.
6. Execute a controlled failure/fencing/recovery path and capture independent evidence.
7. Execute promotion/release and independently re-read postconditions.
8. Reconstruct the complete evidence bundle from immutable identifiers.
9. Only after all gates pass, open separate Arvin PRs to deprecate/remove superseded factory-core workflows.
10. Re-audit Arvin for residual factory-core ownership and update the migration manifest.
11. Promote NIRA PRs only after CI and exact-head validation.

## Prohibited until completion
- Deleting Arvin factory workflows merely because equivalent documentation exists in NIRA.
- Claiming L10.
- Giving an Arvin adapter direct merge authority.
- Treating worker self-report as independent evidence.
- Merging a stale/diverged migration branch without revalidation.

## Current conclusion
The **knowledge/document/contract transfer is substantially established**, but the **operational transfer is NOT COMPLETE**. The remaining blocker is executable cross-repository NIRA control plus independently reconstructible E2E evidence. This matrix is the canonical completion gate for the migration.
