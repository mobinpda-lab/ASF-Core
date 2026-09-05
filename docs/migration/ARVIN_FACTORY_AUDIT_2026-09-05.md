# NIRA — Arvin Factory Extraction Audit

**Audit date:** 2026-09-05 (Iran time)
**Source repository:** `mobinpda-lab/Arvin-clean`
**Source ref audited:** `main`
**Destination repository:** `mobinpda-lab/ASF-Core` (canonical NIRA repository)
**Destination branch:** `feat/nira-independent-platform`
**Audit purpose:** identify Factory-owned files, workflows, issues and contracts in Arvin and assign a canonical destination in NIRA without deleting or mutating Arvin during discovery.

## 1. Safety status

- This audit is **read-only against Arvin**. No Arvin file, workflow, issue, branch or PR was modified by this audit.
- No deletion is authorized from Arvin by this audit.
- Every migration item must preserve source path, source commit/ref and provenance.
- Product-only code remains in Arvin.
- Factory ownership moves to NIRA only after destination validation and client-adapter replacement.

## 2. Classification law

| Class | Meaning | Canonical destination |
|---|---|---|
| F1 | Factory Core | NIRA Core / `factory/` |
| F2 | Factory Governance / policy | NIRA Governance / `docs/governance/` |
| F3 | Factory orchestration / queue / lease / worker | NIRA Engine / `factory/`, `workers/` |
| F4 | Evidence / gates / recovery / observability | NIRA Evidence / `gate-evidence/`, `docs/evidence/` |
| F5 | Shared client contract | NIRA `contracts/`; Arvin retains only adapter/reference |
| F6 | Product adapter | Arvin `.github/` adapter layer |
| P | Product-only | Remains Arvin |
| L | Legacy/duplicate | Preserve provenance; canonicalize in NIRA, then deprecate source copy |

## 3. Confirmed Factory workflows

| Source path | Class | NIRA destination | Migration action |
|---|---|---|---|
| `.github/workflows/arvin-agent-worker.yml` | F3/F4 | `workers/code-worker/` + `docs/contracts/worker.md` | Extract generic worker protocol; replace Arvin-specific names/paths with client adapter |
| `.github/workflows/arvin-autonomous-queue.yml` | F3 | `factory/queue/` + `docs/orchestration/queue.md` | Extract lease, eligibility, priority and exact-main rules |
| `.github/workflows/arvin-orchestrator.yml` | F3/F5 | `factory/engine/` + `contracts/intake-routing.md` | Extract task classification/routing; Arvin becomes client |
| `.github/workflows/arvin-production-loop.yml` | F3/F4 | `factory/feedback/` + `docs/recovery/feedback-loop.md` | Extract queue routing and failure-feedback semantics |
| `.github/workflows/arvin-test-worker.yml` | F3/F4 | `workers/test-worker/` + `docs/evidence/test-gates.md` | Extract test-worker/evidence protocol; product test execution remains client-side |
| `.github/workflows/production-orchestrator.yml` | F3/F4/F5 | `factory/promotion/` + `docs/governance/promotion.md` | Extract guarded promotion, exact-head, current-main and serial merge authority |
| `.github/workflows/factory-rest-promotion-bridge.yml` | F3/F5 | `factory/promotion/adapters/rest.md` | Treat as transitional client bridge; NIRA owns canonical promotion contract |
| `.github/workflows/parallel-wave.yml` | F3 | `factory/parallelism/` | Extract parallel-wave scheduling contract; product-specific jobs stay in Arvin |
| `.github/workflows/release-closure.yml` | F4/F5 | `factory/release/` + `contracts/release-evidence.md` | Extract generic release evidence/closure; Arvin release naming remains product-specific |

**Important:** `.github/workflows/build.yml` and `.github/workflows/device-smoke.yml` are primarily product validation executors. Their generic gate contract belongs in NIRA, but the actual Flutter build/device implementation remains Arvin. They are therefore F5/F6 rather than full migration candidates.

## 4. Confirmed Factory configuration/runtime files

| Source path | Class | NIRA destination | Migration action |
|---|---|---|---|
| `.github/arvin/production-queue.yml` | F3 | `factory/queue/production-queue.yml` | Canonicalize queue policy; remove `ARVIN` product prefix in NIRA version |
| `.github/arvin/agent-runtime.py` | F3/F4 | `workers/code-worker/runtime/` | Extract bounded AI provider, patch validation, retry budget and validation loop; retain product adapter separately |

The runtime contains explicit safety controls including bounded files/diff size, provider timeout/budget, structured unified-diff validation, `git apply --check`, bounded auto-fix attempts and project validation. These are Factory runtime behaviors, not Arvin product features.

## 5. Confirmed Factory documentation set

| Source path | Class | NIRA destination | Status |
|---|---|---|---|
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE.md` | F2/F3 | `docs/governance/NIRA_FACTORY_OPERATING_MODEL.md` | Extract + canonicalize; do not copy Arvin product rules |
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE_v48.2_TRANSFER_MANIFEST.md` | L/F2 | `docs/migration/provenance/ARVIN_v48.2_TRANSFER_MANIFEST.md` | Preserve as historical provenance/reference |
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE_v48.2_FINAL_OPERATIONAL_feshordeh_PART01.md` | L/F2 | `docs/migration/provenance/ARVIN_v48.2_FACTORY_OPERATIONAL_PART01.md` | Preserve provenance; extract Factory sections |
| `docs/ARVIN_PRODUCTION_ORCHESTRATOR_5MIN_MODE.md` | F3 | `docs/orchestration/NIRA_5MIN_ORCHESTRATOR_MODEL.md` | Extract generic 5-minute loop, gates, queue and continuous operation |
| `docs/AI_WORKER_PATCH_RECOUNT_2026-08-31.md` | F3/F4 | `docs/workers/AI_WORKER_PATCH_RECOUNT.md` | Extract patch normalization/recount recovery |
| `docs/AI_WORKER_PATCH_HARDENING_2026-08-31.md` | F3/F4 | `docs/workers/AI_WORKER_PATCH_HARDENING.md` | Extract bounded provider/patch safety |
| `docs/AI_WORKER_PATCH_HARDENING_ACCEPTANCE_2026-08-31.md` | F4 | `docs/workers/AI_WORKER_HARDENING_ACCEPTANCE.md` | Extract acceptance gates; preserve live evidence provenance |
| `docs/AI_WORKER_PATCH_HARDENING_PR_NOTE_2026-08-31.md` | L/F4 | `docs/migration/provenance/AI_WORKER_PATCH_HARDENING_PR_NOTE.md` | Historical traceability; not an active authority |
| `docs/AI_WORKER_PROVIDER_FALLBACK_2026-08-31.md` | F3/F4 | `docs/workers/AI_WORKER_PROVIDER_POLICY.md` | Extract provider fallback and read-only Copilot boundary |
| `docs/AI_WORKER_SINGLE_LAUNCH_AUTHORITY_2026-08-31.md` | F3 | `docs/workers/AI_WORKER_SINGLE_LAUNCH_AUTHORITY.md` | Extract single-launch/idempotency rule |
| `docs/AUTOMATION_FAILURE_FEEDBACK_2026-08-31.md` | F4 | `docs/recovery/AUTOMATION_FAILURE_FEEDBACK.md` | Extract cancellation, duplicate suppression and bounded Auto-Fix feedback |
| `docs/RC_ACCELERATION_PLAN_2026-08-31.md` | F2/F3 | `docs/governance/FACTORY_EXECUTION_MODES.md` | Extract Normal/Fast/Emergency execution-mode rules only |
| `docs/REPORTING_STANDARD.md` | F2/F4/F5 | `docs/observability/NIRA_REPORTING_STANDARD.md` | Extract evidence-first status/reporting vocabulary; Arvin product status remains local |
| `docs/DOCUMENT_AUTHORITY_INDEX.md` | F2 | `docs/governance/NIRA_DOCUMENT_AUTHORITY.md` | Extract source-of-truth hierarchy |
| `docs/CI_FAST_LANE_2026-08-26.md` | F4/F5 | `docs/evidence/EXACT_HEAD_FAST_GATE.md` | Extract exact-head validation/ref mechanics |
| `docs/PROJECT_PROGRESS_METRIC.md` | F4/F5 | `docs/observability/AUTOMATION_EVIDENCE_SCORE.md` | Extract evidence-based automation scoring; product progress remains Arvin |
| `docs/AI_CONTINUATION_STATE.md` | F2/F4 | `docs/governance/NIRA_CONTINUATION_STATE.md` | Extract continuity/source-of-truth rules |
| `docs/AI_HANDOFF_CURRENT_FA.md` | F2/F4 | `docs/governance/NIRA_HANDOFF_PROTOCOL.md` | Extract operational handoff rules |

## 6. Factory contract tests / verification artifacts

| Source path | Class | NIRA destination | Action |
|---|---|---|---|
| `test/production_orchestrator_contract_test.dart` | F4/F5 | `contracts/tests/production-orchestrator-contract/` | Port generic invariants; do not port Flutter/product assumptions |
| `test/ai_worker_provider_contract_test.dart` | F4 | `contracts/tests/ai-worker-provider/` | Port provider fallback and permission invariants |
| `test/ai_worker_runtime_behavior_test.dart` | F4 | `contracts/tests/ai-worker-runtime/` | Port malformed patch/recount/bounded-runtime tests |
| `test/` references to factory queue/worker markers | F4/F5 | `contracts/tests/` | Audit individually; only generic Factory assertions migrate |

## 7. Factory-related Issues identified

| Issue | Class | NIRA destination | Migration treatment |
|---|---|---|---|
| #610 — adopt Universal Autonomous Software Factory Protocol v2 | F2/F3 | `docs/governance/UNIVERSAL_AUTONOMOUS_FACTORY_PROTOCOL.md` | Extract protocol; Arvin adoption history remains provenance |
| #615 — Bootstrap Autonomous Factory Execution Evidence | F4 | `docs/evidence/FACTORY_EXECUTION_EVIDENCE.md` | Extract evidence requirements |
| #616 — ARVIN Autonomous Software Factory — Continuous Production Mode | F2/F3 | `docs/governance/CONTINUOUS_PRODUCTION_MODE.md` | Extract generic lifecycle |
| #617 — Activate ARVIN Autonomous Software Factory | F2/F3 | `docs/governance/CONTINUOUS_PRODUCTION_MODE.md` + provenance | Extract generic factory tracks; product feature tracks stay Arvin |
| #619 — Factory Execution: Evidence Pipeline and First Autonomous Cycle | F4 | `docs/evidence/FIRST_AUTONOMOUS_CYCLE.md` | Extract E2E evidence contract |
| #620 — Parallel Worker Wave 1 — Automation Runtime Execution | F3 | `factory/runtime/` | Extract runtime execution requirements |
| #621 — Parallel Worker Wave 2 — Smart FollowUp Engine Production | P/F5 | Arvin product roadmap + NIRA client-contract reference | **Do not migrate FollowUp feature scope**; only preserve generic evidence pipeline relationship |
| #637 — Runtime Control Plane — persistent state, worker capacity and event-driven recovery | F3/F4 | `factory/runtime-control-plane/` | Extract persistent state, worker capacity, event model, stale-lease recovery and metrics |
| #640 — immutable event-driven documentation law | F2/F4 | `docs/governance/DOCUMENTATION_LAW.md` | Extract enforcement policy and fail-closed rules |
| #641 — Canonical Product + Observation Intake and Priority Queue | F3/F5 | `factory/intake/` + `contracts/client-intake.md` | Extract generic intake/classification/priority/conflict/lease model; Arvin keeps product observation adapter |
| #644 — exact-main lease validation in Arvin Code Worker | F3/F4 | `workers/code-worker/exact-main-lease.md` | Extract exact-main lease invariant |

## 8. Explicit non-migration examples

The generic search term `factory` also matched normal Dart language constructs such as `factory` constructors in product models/services. These are **not** Factory platform artifacts and must not be moved. Examples observed include:

- `lib/backup_schedule.dart`
- `lib/models/recurrence.dart`
- `lib/models/person_reference.dart`
- `lib/models/task.dart`
- `lib/services/system_calendar_bridge.dart`
- `lib/services/task_sync_remote_transport.dart`
- `lib/quick_capture_dialog.dart`
- `lib/services/task_people_service.dart`
- related product tests

These remain Arvin product code.

## 9. Ownership result

After canonicalization:

`NIRA OS`
→ Factory governance + registry + intake + queue + lease + workers + orchestration + evidence + gates + recovery + promotion + release/observability.

`Arvin-clean`
→ Product implementation + product CI/build/device execution + NIRA client adapter + product-specific evidence.

NIRA must be able to control the Factory without depending on Arvin-specific workflow names, files, Flutter runtime, or product data.

## 10. Migration gates before Arvin cleanup

1. Destination artifact exists in NIRA.
2. Provenance recorded.
3. Generic behavior canonicalized.
4. NIRA tests/contracts cover the migrated invariant.
5. Arvin adapter/reference is defined.
6. Cross-repository validation succeeds.
7. NIRA can operate without Arvin-specific implementation.
8. Only then may duplicate Arvin Factory implementation be deprecated/removed.

**Current cleanup status: NOT AUTHORIZED.**

## 11. Evidence captured by this audit

- Arvin `main` contains dedicated Factory workflows for queue, worker, orchestrator, production loop, promotion bridge, parallel wave and production promotion.
- Arvin `.github/arvin/production-queue.yml` defines priority, dependency/conflict checks, workers, CI feedback and controlled auto-merge.
- Arvin `arvin-agent-worker.yml` enforces exact leased-main SHA before execution and delegates promotion to the Production Orchestrator.
- Arvin `arvin-autonomous-queue.yml` leases up to three eligible tasks, records exact main SHA and fails closed on dispatch failure.
- Arvin `production-orchestrator.yml` checks current-main ancestry and exact-head Fast/Build/Device gates before guarded squash merge and verifies the merged main SHA.
- Arvin `factory-rest-promotion-bridge.yml` is a transitional REST promotion mechanism and therefore should not become a second NIRA merge authority.
- Arvin `agent-runtime.py` implements bounded AI-provider execution, malformed-diff rejection, retry budgets and project validation.

## 12. Next migration wave

**Wave A — Documentation + contracts:** migrate and canonicalize the Factory operating model, worker contracts, evidence/gate contracts and governance laws.

**Wave B — Runtime:** port Queue/Lease/Worker/Orchestrator/Feedback semantics into NIRA Core.

**Wave C — Client adapter:** introduce the minimal Arvin adapter that delegates Factory control to NIRA.

**Wave D — Cross-project proof:** run NIRA against Arvin as a registered client and reconstruct Issue → Task → Lease → Worker → PR → CI → Build/Device → Promotion → Merge → Release evidence.

**Wave E — Cleanup:** remove/deprecate duplicated Arvin Factory implementation only after all previous gates are green.
