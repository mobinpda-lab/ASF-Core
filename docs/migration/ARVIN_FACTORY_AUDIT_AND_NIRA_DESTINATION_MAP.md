# Arvin Factory Audit → NIRA Destination Map

**Audit date:** 2026-09-05 (Iran time)
**Source repository:** `mobinpda-lab/Arvin-clean`
**Destination:** `mobinpda-lab/ASF-Core` / NIRA
**Audit status:** Phase-1 evidence-backed inventory; no Arvin deletion performed.
**Safety rule:** classify first, copy/re-home second, validate third, cleanup last.

## 1. Executive finding

The Arvin repository contains a substantial autonomous-factory control surface in addition to product code. The factory surface includes queueing, routing, workers, AI patch generation/self-fix, production orchestration, exact-head validation, failure feedback, promotion, evidence and factory governance documentation.

The current Arvin canonical operating package still explicitly describes Arvin as a software factory and contains factory operating rules. This is now a legacy ownership conflict with NIRA's independent-factory boundary. The content is therefore **source material for migration**, not evidence that Arvin should remain the factory owner.

No destructive cleanup is authorized by this audit.

## 2. Classification rules

- **FCORE:** Factory Core → NIRA canonical implementation/documentation.
- **FGOV:** Factory Governance → NIRA canonical governance.
- **FORCH:** Factory Orchestration/Queue/Lease/Workers → NIRA Engine/Workers/Runtime.
- **FEVID:** Factory Evidence/Gates/Recovery/Observability → NIRA Evidence/Gates/Recovery.
- **FCON:** Shared client/factory contract → NIRA contract; Arvin keeps only a thin product adapter.
- **PADAPTER:** Product-side adapter/integration → remains in Arvin.
- **PRODUCT:** Arvin-only product behavior → remains in Arvin.
- **HIST:** Historical evidence → remains in Arvin and/or is archived in NIRA with provenance; never silently rewritten.
- **DUP:** Legacy duplicate → retain until canonical replacement is validated, then deprecate/remove by separate governed PR.

## 3. Verified factory workflows in Arvin

| Source path | Classification | NIRA destination | Arvin action later | Evidence |
|---|---|---|---|---|
| `.github/workflows/arvin-orchestrator.yml` | FORCH | `factory/orchestration/` + NIRA Engine | Replace with NIRA client adapter/dispatcher | Workflow explicitly analyzes/routs issues, adds `arvin-auto`, dispatches the AI worker and prevents duplicate launches. |
| `.github/workflows/arvin-autonomous-queue.yml` | FORCH | `factory/queue/` + `factory/leases/` | Replace with NIRA queue client | Leases up to three eligible issues, records exact `main` SHA, labels lease/in-progress, dispatches worker, fails closed. |
| `.github/workflows/arvin-agent-worker.yml` | FORCH | `workers/code-worker/` + `runtime/` | Replace with NIRA worker invocation adapter | Explicit `workflow_dispatch`; exact-main lease validation; AI provider selection; bounded retries; tests; isolated branch; Draft PR; no merge authority. |
| `.github/workflows/arvin-test-worker.yml` | FORCH/FEVID | `workers/test-worker/` + `evidence/` | Replace with NIRA test-worker adapter | Runs targeted automation contract tests, records evidence, creates isolated evidence branch/PR. |
| `.github/workflows/arvin-production-loop.yml` | FORCH/FEVID | `factory/feedback/` + `factory/recovery/` | Replace with NIRA feedback adapter | Routes issues, dispatches test worker, converts terminal failures into idempotent Auto-Fix issues, explicitly launches worker, ignores cancellation. |
| `.github/workflows/production-orchestrator.yml` | FORCH/FEVID | `factory/orchestration/promotion/` | Remove only after NIRA promotion gate is proven | Five-minute production orchestrator; exact-head Fast/Build/Device checks; controlled promotion/merge; failure feedback; single merge authority. |
| `.github/workflows/factory-rest-promotion-bridge.yml` | FORCH | `factory/orchestration/promotion/` | Replace with NIRA promotion mechanism | REST bridge promotes eligible Draft `arvin-auto` PRs after exact-head Fast and unchanged-main validation. |

## 4. Verified factory configuration/runtime files

| Source path | Classification | NIRA destination | Notes |
|---|---|---|---|
| `.github/arvin/production-queue.yml` | FORCH | `factory/queue/production-queue.yml` | Defines maximum-parallel queue, priority/dependency/conflict checks, core/code/test/documentation workers, CI feedback and controlled merge policy. |
| `.github/arvin/agent-runtime.py` | FORCH | `runtime/ai-worker/agent-runtime.py` | Bounded AI implementation runtime; OpenAI Responses provider with Copilot fallback; diff structure validation; apply-check; test loop; retry budget; no direct merge. Requires provider-agnostic NIRA configuration before reuse. |

## 5. Verified factory contract tests

| Source path | Classification | NIRA destination | Arvin action later |
|---|---|---|---|
| `test/production_orchestrator_contract_test.dart` | FEVID/FCON | `test/contracts/production_orchestrator_contract_test.*` | Retain product-side smoke/adapter contract only after NIRA contract exists | Locks 5-minute schedule, exact-head Fast/Build/Device, controlled merge, failure feedback, single launch authority. |
| `test/ai_worker_provider_contract_test.dart` | FCON | `test/contracts/ai_worker_provider_contract_test.*` | Arvin keeps only adapter-level checks | Locks workflow dispatch-only behavior, no direct merge, provider/runtime boundaries. |
| `test/ai_worker_runtime_behavior_test.dart` | FEVID/FCON | `test/contracts/ai_worker_runtime_behavior_test.*` | Arvin keeps product integration subset if needed | Exercises the AI runtime implementation. |

## 6. Verified factory governance / operating documents

| Source path | Classification | NIRA destination | Arvin action later |
|---|---|---|---|
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE.md` (v49.0) | FGOV/FCORE | `docs/governance/NIRA_FACTORY_OPERATING_STANDARD.md` | Replace Arvin factory claims with product governance + NIRA client contract; retain historical lineage | Current Arvin canonical standard includes factory operating model, parallel execution, queue/worker concepts, evidence, exact-head, recovery, AI boundaries and documentation governance. |
| `docs/ARVIN_PRODUCTION_ORCHESTRATOR_5MIN_MODE.md` | FORCH | `docs/orchestration/NIRA_PRODUCTION_ORCHESTRATOR.md` | Archive/deprecate after NIRA equivalent validated | Defines five-minute loop, eligibility, CI/Build/Device gates, serialized merge and exact-SHA evidence. |
| `docs/AI_WORKER_PATCH_HARDENING_2026-08-31.md` | FORCH/FEVID | `docs/workers/NIRA_AI_WORKER_PATCH_HARDENING.md` | Archive after NIRA implementation validated | Defines provider fallback, read-only model boundary, diff validation, bounded timeout/retry budget, trusted write layer. |
| `docs/AI_WORKER_PATCH_HARDENING_ACCEPTANCE_2026-08-31.md` | FEVID | `docs/evidence/NIRA_AI_WORKER_HARDENING_ACCEPTANCE.md` | Historical source until NIRA acceptance is green | Contains explicit incomplete acceptance gates; therefore must not be migrated as a false PASS. |
| `docs/AI_WORKER_SINGLE_LAUNCH_AUTHORITY_2026-08-31.md` | FORCH/FGOV | `docs/orchestration/NIRA_SINGLE_WORKER_LAUNCH_AUTHORITY.md` | Replace with NIRA authority model | Establishes workflow_dispatch-only worker and idempotent single launch authority. |
| `docs/AUTOMATION_FAILURE_FEEDBACK_2026-08-31.md` | FEVID/FORCH | `docs/recovery/NIRA_AUTOMATION_FAILURE_FEEDBACK.md` | Replace with NIRA recovery contract | Defines success/cancel/failure handling, exact-head binding, idempotent Auto-Fix and no direct merge. |
| `docs/CI_FAST_LANE_2026-08-26.md` | FEVID/FORCH | `docs/gates/NIRA_FAST_LANE.md` | Keep product CI specifics in Arvin; migrate reusable gate semantics | Includes exact-head fallback using `gate/pr-<number>` and Fast/Build/Device separation. |
| `docs/DEVELOPMENT_RULES.md` | FGOV/FCON | `docs/governance/NIRA_CLIENT_DEVELOPMENT_RULES.md` (factory subset only) | Retain Arvin product rules separately | Only factory/repository governance portions migrate. Product rules stay Arvin. |
| `docs/DOCUMENT_AUTHORITY_INDEX.md` | FGOV/FCON | `docs/governance/NIRA_DOCUMENT_AUTHORITY_MODEL.md` | Arvin retains product document authority index | Authority hierarchy and evidence-first rules are reusable factory governance. |
| `docs/AI_HANDOFF_CURRENT_FA.md` | FCORE/HIST | `docs/continuity/NIRA_FACTORY_HANDOFF_MODEL.md` | Arvin retains product handoff subset | Exact-head, queue and CI continuity rules are factory-owned; product status remains Arvin. |
| `docs/AI_CONTINUATION_STATE.md` | HIST/FCON | `docs/continuity/NIRA_FACTORY_CONTINUATION_PROTOCOL.md` | Keep Arvin product state separately | Only generic factory continuation protocol migrates. |
| `docs/RC_ACCELERATION_PLAN_2026-08-31.md` | MIXED | `docs/migration/ARVIN_RC_FACTORY_EXTRACTION_NOTES.md` | Do not wholesale migrate | Contains both product RC work and factory automation; split by responsibility. |

## 7. Factory-related Issues verified in Arvin

| Issue | Title | Classification | NIRA destination | Arvin action later |
|---|---|---|---|---|
| #617 | Activate ARVIN Autonomous Software Factory: Continuous Production Mode | FCORE/FGOV/FORCH | `factory/roadmap/` + NIRA issue lineage | Close/reconcile as migrated only after NIRA replacement; retain historical issue. |
| #619 | ARVIN Factory Execution: Evidence Pipeline and First Autonomous Cycle | FEVID | `factory/evidence/` | Re-home requirement/evidence contract; preserve original issue history. |
| #620 | ARVIN Parallel Worker Wave 1 - Automation Runtime Execution | FORCH | `factory/runtime/` | Re-home execution target to NIRA; preserve Arvin issue as historical provenance. |
| #637 | ASF: Runtime Control Plane — persistent state, worker capacity and event-driven recovery | FORCH/FEVID | `runtime/control-plane/` + `factory/recovery/` | High-priority NIRA implementation candidate. |
| #640 | ASF: enforce immutable event-driven documentation law | FGOV/FEVID | `governance/documentation-law/` | Migrate policy/enforcement concept to NIRA. |
| #641 | ASF: Canonical Product + Observation Intake and Priority Queue | FORCH/FCON | `factory/intake/` + `factory/queue/` | NIRA should own canonical intake; Arvin keeps product observation adapter. |
| #644 | ASF: enforce exact-main lease validation in Arvin Code Worker | FORCH/FEVID | `factory/leases/` + `workers/code-worker/` | NIRA should own exact-main lease contract; Arvin becomes client adapter. |
| #621 | ARVIN Parallel Worker Wave 2 - Smart FollowUp Engine Production | PRODUCT | Not migrated to NIRA | Product feature work; factory execution references may be extracted, but FollowUp implementation stays Arvin. |

## 8. Important mixed/false-positive search results

The audit deliberately did **not** classify every search hit containing the word `factory` as factory infrastructure. Dart constructors such as `factory BackupSchedule.disabled()` and `factory RecurrenceRule.fromJson()` are normal product-language constructs and remain Arvin product code. Likewise, product-specific calendar, UI, storage, task, people and follow-up documents are not factory assets merely because they mention workflows or CI.

This distinction is mandatory to prevent accidental product-code migration.

## 9. Factory concepts detected in Arvin and their NIRA homes

- Issue intake/routing → `factory/intake/`
- Priority/dependency/conflict analysis → `factory/scheduling/`
- Queue → `factory/queue/`
- Lease → `factory/leases/`
- Worker identity/capacity → `runtime/control-plane/`
- Code worker → `workers/code-worker/`
- Test worker → `workers/test-worker/`
- Documentation worker concept → `workers/documentation-worker/`
- AI provider abstraction → `runtime/providers/`
- Patch/diff safety → `runtime/safety/patch-validation/`
- Self-fix/retry budget → `factory/recovery/`
- CI Fast/Build/Device gates → `factory/gates/`
- Exact-head validation → `factory/gates/exact-head/`
- Promotion/merge authority → `factory/orchestration/promotion/`
- Failure feedback → `factory/recovery/feedback/`
- Evidence → `factory/evidence/`
- Release evidence → `factory/release/`
- Continuous observation → `factory/observability/`
- Documentation law → `governance/documentation-law/`
- L10 proof → `governance/l10/`

## 10. Safety state

**No Arvin file has been deleted or rewritten by this audit.**

The current evidence shows that the factory surface is still operationally embedded in Arvin. In particular, Arvin workflows directly dispatch workers and the production orchestrator; therefore removing them before an equivalent NIRA execution path exists would break autonomous operation.

The correct migration order is:

`Inventory → Canonicalize → Implement NIRA equivalent → Contract-test → Cross-repo adapter → Run E2E → Observe → Deprecate Arvin factory path → Remove duplicates`

## 11. Next controlled migration wave

1. Create NIRA canonical contracts for Intake, Queue, Lease, Worker, Gate, Evidence, Promotion and Recovery.
2. Extract the provider-neutral logic from `agent-runtime.py`; do not blindly copy Arvin-specific names/environment variables.
3. Build NIRA orchestration/worker runtime and tests.
4. Create an Arvin client adapter that submits product work to NIRA.
5. Prove one real Arvin end-to-end cycle through NIRA.
6. Only after successful proof, deprecate the corresponding Arvin workflow(s) in separate PRs.
7. Repeat by subsystem until Arvin contains no factory-core implementation.
8. Keep historical issues/docs available for provenance and link them to their NIRA replacements.

## 12. Audit conclusion

**Result:** Factory ownership can safely be moved to NIRA, but the move is not yet a completed transfer. The audit identified the principal live factory implementation, governance, contract-test and issue surfaces in Arvin and assigned canonical NIRA destinations without destructive action.

**NIRA is the destination; Arvin remains operationally intact until NIRA replacement paths are proven.**
