# NIRA Migration — Arvin Factory Audit & Destination Map

**Audit date:** 2026-09-05 (Iran)
**Source repository:** `mobinpda-lab/Arvin-clean`
**Source ref audited:** `main`
**Destination:** `mobinpda-lab/ASF-Core` / NIRA
**Migration branch:** `feat/nira-independent-platform`
**Safety state:** AUDIT-ONLY; no Arvin deletion or destructive migration performed.

## 1. Audit objective

Identify Factory-owned documentation, workflows, runtime/agent assets, contracts and Factory issues currently living in Arvin, classify each item, and assign a canonical destination in NIRA without moving product-owned functionality.

The governing boundary is:

`NIRA = Factory / control plane`

`Arvin = Product / registered Factory client`

No item is deleted from Arvin merely because it appears in this inventory. Transfer must be followed by canonicalization, validation, adapter replacement, and only then cleanup.

## 2. High-confidence Factory inventory

### A. Factory documentation — TRANSFER TO NIRA

| Arvin source | Classification | NIRA destination | Action |
|---|---|---|---|
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE.md` | Factory governance + product/factory mixed master | `docs/governance/NIRA_FACTORY_OPERATING_STANDARD.md` + product-specific residue stays in Arvin | Extract Factory portions; preserve provenance; do not copy product requirements wholesale |
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE_v48.2_TRANSFER_MANIFEST.md` | Factory/document provenance | `docs/migration/provenance/ARVIN_V48_2_TRANSFER_MANIFEST.md` | Preserve as historical transfer evidence |
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE_v48.2_FINAL_OPERATIONAL_feshordeh*.md` | Historical mixed operating package | `docs/migration/provenance/arvin-operating-package-v48.2/` | Archive/extract only; preserve history |
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE_v48.2_FINAL_OPERATIONAL_feshordeh_SOURCE_VERIFIED.md` | Source verification/provenance | `docs/migration/provenance/` | Preserve provenance |
| `docs/ARVIN_PRODUCTION_ORCHESTRATOR_5MIN_MODE.md` | Factory orchestration | `docs/orchestration/NIRA_ORCHESTRATOR.md` | Canonicalize into NIRA; retain Arvin adapter reference |
| `docs/FACTORY_DOCUMENTATION_POLICY.md` | Factory governance | `docs/governance/NIRA_FACTORY_DOCUMENTATION_POLICY.md` | **SOURCE REFERENCED BY ISSUE #640 BUT CURRENT FILE NOT FOUND ON Arvin main**; reconstruct only from verified history/issue evidence, not guesswork |
| `docs/AI_WORKER_PATCH_HARDENING_2026-08-31.md` | Factory AI worker safety | `docs/agents/NIRA_AI_WORKER_SAFETY.md` | Extract provider, patch validation, timeout/budget, trusted-runtime boundary |
| `docs/AI_WORKER_SINGLE_LAUNCH_AUTHORITY_2026-08-31.md` | Factory worker routing | `docs/agents/NIRA_WORKER_LAUNCH_AUTHORITY.md` | Canonicalize |
| `docs/AI_WORKER_PATCH_RECOUNT_2026-08-31.md` | Factory patch safety | `docs/agents/NIRA_PATCH_VALIDATION.md` | Canonicalize |
| `docs/AI_WORKER_PROVIDER_FALLBACK_2026-08-31.md` | Factory provider boundary | `docs/agents/NIRA_PROVIDER_BOUNDARY.md` | Canonicalize, remove Arvin naming from canonical contract |
| `docs/AUTOMATION_FAILURE_FEEDBACK_2026-08-31.md` | Factory failure/recovery | `docs/recovery/NIRA_AUTOMATION_FAILURE_FEEDBACK.md` | Canonicalize |
| `docs/CI_FAST_LANE_2026-08-26.md` | Factory validation contract | `docs/ci/NIRA_FAST_GATE.md` | Extract generic exact-head/fast-gate rules; Arvin-specific build commands remain adapter-side |
| `docs/CI_RELEASE_VALIDATION_NOTE.md` | Product CI implementation detail + validation contract | `docs/ci/clients/arvin-release-validation.md` | Keep as client adapter evidence; generic gate contract moves to NIRA |
| `docs/CI_TRIGGER_AUDIT_2026-08-15.md` | Product CI audit + reusable trigger lessons | `docs/ci/clients/arvin-trigger-audit.md` | Keep Arvin evidence; extract generic lessons to NIRA |
| `docs/RELEASE_EVIDENCE_COMPLETION_LANE_2026-08-26.md` | Factory evidence/gate procedure | `docs/evidence/NIRA_RELEASE_EVIDENCE_LANE.md` | Extract generic evidence contract |
| `docs/CI_STALE_RUN_CONCURRENCY_2026-08-26.md` | Factory CI scheduling policy | `docs/ci/NIRA_STALE_RUN_POLICY.md` | Extract generic policy; Arvin workflow details stay adapter-side |
| `docs/REPORTING_STANDARD.md` | Mixed reporting/product policy | `docs/governance/NIRA_REPORTING_STANDARD.md` | Extract Factory reporting/audit requirements; Arvin presentation conventions remain Arvin |
| `docs/AI_CONTINUATION_STATE.md` | Product continuation + source-of-truth policy | `docs/governance/NIRA_SOURCE_OF_TRUTH.md` | Extract generic precedence rule; Arvin continuation remains client-side |
| `docs/DOCUMENT_AUTHORITY_INDEX.md` | Mixed authority model | `docs/governance/NIRA_DOCUMENT_AUTHORITY.md` | Extract generic hierarchy; Arvin product index remains Arvin |
| `docs/DEVELOPMENT_RULES.md` | Mixed product/factory rules | `docs/governance/NIRA_DEVELOPMENT_GOVERNANCE.md` | Extract Factory governance; retain product UI/data rules in Arvin |
| `docs/PROJECT_ROADMAP_2026-08-14.md` | Mixed product + Factory execution | `docs/migration/provenance/arvin-project-roadmap.md` | Preserve historical evidence; extract only Factory execution model |
| `docs/ARVIN_PROJECT_STATE.md` | Mixed current-state control | `docs/migration/provenance/arvin-project-state.md` | Preserve as historical client evidence; NIRA owns Factory state going forward |
| `docs/ARVIN_STATUS.md` | Product management snapshot | `docs/migration/provenance/arvin-status.md` | Preserve only where it records Factory migration evidence; product status remains Arvin |

## 3. Factory workflows and runtime assets

### B. Factory-owned workflows — RE-HOME / REIMPLEMENT IN NIRA

| Arvin source | Current role | NIRA destination | Arvin future state |
|---|---|---|---|
| `.github/workflows/arvin-agent-worker.yml` | AI Code Worker | `workflows/nira-agent-worker.yml` | Client adapter/dispatch target only |
| `.github/workflows/arvin-autonomous-queue.yml` | Autonomous production queue | `workflows/nira-intake-queue.yml` | Replace with NIRA intake integration |
| `.github/workflows/arvin-orchestrator.yml` | Worker routing/orchestration | `workflows/nira-orchestrator.yml` | Arvin becomes registered client |
| `.github/workflows/arvin-production-loop.yml` | Failure feedback / production loop | `workflows/nira-failure-feedback.yml` | Arvin keeps only client-facing callback/adapter |
| `.github/workflows/arvin-test-worker.yml` | Autonomous test worker | `workflows/nira-test-worker.yml` | Product test execution remains Arvin; orchestration moves NIRA |
| `.github/workflows/production-orchestrator.yml` | Guarded promotion/merge authority | `workflows/nira-production-orchestrator.yml` | Arvin must not own Factory merge authority; product repo retains normal protected-branch mechanics |
| `.github/workflows/factory-rest-promotion-bridge.yml` | Factory REST promotion bridge | `workflows/nira-client-promotion-bridge.yml` | Replace Arvin-specific implementation with NIRA client adapter |

### C. Workflows that are NOT wholly Factory-owned

| Arvin source | Classification | Destination |
|---|---|---|
| `.github/workflows/build.yml` | Product CI gate; reusable Factory evidence surface | Keep Arvin; NIRA defines contract and consumes evidence |
| `.github/workflows/device-smoke.yml` | Product/device validation | Keep Arvin; NIRA consumes device evidence |
| `.github/workflows/parallel-wave.yml` | Mixed: product validation + Factory parallel scheduling | Keep product validation in Arvin; move generic scheduling/orchestration semantics to NIRA |
| `.github/workflows/progress-score.yml` | Product progress metric with reusable evidence principles | Keep Arvin score implementation; NIRA may define generic evidence semantics |
| `.github/workflows/release-closure.yml` | Product release closure | Keep Arvin; NIRA consumes release evidence |

## 4. Factory runtime/config files

| Arvin source | Classification | NIRA destination | Action |
|---|---|---|---|
| `.github/arvin/production-queue.yml` | Factory queue configuration | `config/queue/` | Re-home/canonicalize as NIRA queue schema; retain Arvin adapter config only |
| `.github/arvin/agent-runtime.py` | Factory worker runtime | `runtime/agents/` | Re-home after security/code audit; replace Arvin-specific assumptions with client abstraction |
| `tool/validate_fast_lane.py` | Factory CI contract validator + Arvin workflow assertions | `tools/validators/` | Split generic validator from Arvin-specific assertions; generic part becomes NIRA |
| `test/production_orchestrator_contract_test.dart` | Factory contract test implemented in product repo | `tests/contracts/` | Port generic invariants to NIRA; keep a small Arvin adapter contract test |
| `test/ai_worker_provider_contract_test.dart` | Factory AI worker contract | `tests/contracts/ai_worker/` | Port generic safety invariants to NIRA; retain client-specific assertions only in Arvin |

## 5. Factory contracts identified

### Contract families to become NIRA canonical

1. **Issue intake contract** — one canonical issue, classification, priority, dependency/conflict metadata, evidence and audit trail.
2. **Queue/lease contract** — exact-main SHA captured at lease time, worker identity, bounded lease, stale-lease recovery.
3. **Worker contract** — isolated branch, issue scope, bounded execution, no direct main write, traceable output.
4. **AI provider contract** — provider fallback, read-only model tools, trusted runtime owns writes, bounded timeout/budget.
5. **Patch contract** — complete unified diff, structural validation, `git apply --check`, fail closed on malformed/context-invalid patch.
6. **Test worker contract** — focused tests + evidence, no merge authority.
7. **Evidence contract** — Issue → Commit → PR → CI → Build/Device → Merge → Release evidence, exact SHA identity.
8. **Fast gate contract** — current-main/exact-head validation; stale evidence cannot promote.
9. **Failure feedback contract** — real failure/timed-out is actionable; protective cancellation is not an implementation failure; idempotent Auto-Fix routing.
10. **Promotion contract** — one guarded promotion/merge authority; no worker/model may merge.
11. **Documentation law** — meaningful Factory changes require canonical evidence/documentation; fail closed where required.
12. **Parallel scheduling contract** — independent work parallel, conflicting work serialized; no duplicate task execution.
13. **Runtime control-plane contract** — persistent execution state, worker capacity, event transitions, recovery, metrics.
14. **Source-of-truth contract** — GitHub reality > approved decision > canonical Factory contract > execution evidence > historical notes/chat.
15. **L10 evidence contract** — L10 remains unverified until a real registered client completes a reconstructible end-to-end Factory cycle.

## 6. Factory issues to migrate/reconcile

### Factory-owned issues — canonical record should move to NIRA

| Arvin issue | Factory content | NIRA treatment |
|---|---|---|
| #538 | Autonomous Finish Mode pipeline | Historical provenance; extract generic Detect→Analyze→Fix→Test→CI→Merge→Document loop |
| #540 | Autonomous production rules / priorities | Extract Factory rules; product release priorities stay Arvin |
| #544 | Production Orchestrator 5-minute monitoring | Move to NIRA orchestration roadmap |
| #546 | Orchestrator auto issue tracking/documentation | Move to NIRA governance/intake |
| #547 | Orchestrator auto Draft PR flow | Move to NIRA orchestration/PR lifecycle |
| #548 | First full automation loop | Move to NIRA lifecycle/evidence |
| #549 | AI Worker activation | Move to NIRA agent architecture |
| #550 | Smart documentation + parallel production | Move to NIRA governance/parallel execution |
| #551 | Full autonomous production loop | Move to NIRA core lifecycle |
| #553 | Production worker runtime | Move to NIRA runtime |
| #562 | Cancellation/failure feedback | Move to NIRA recovery/evidence |
| #576 | AI patch normalization/provider latency | Move to NIRA agent safety |
| #578 | Evidence-backed progress score | Extract generic evidence model; Arvin score remains product-specific |
| #583 | Deterministic evidence renderer | Generic renderer/evidence semantics to NIRA; Arvin dashboard remains client |
| #588 | Single AI Worker launch authority | Move to NIRA agent dispatch governance |
| #590 | Safe patch recount | Move to NIRA patch safety |
| #610 | Universal Autonomous Software Factory Protocol v2 | **Primary migration source** for NIRA Factory protocol |
| #615 | Bootstrap Factory execution evidence | Move to NIRA evidence bootstrap |
| #616 | Continuous autonomous Factory mode | Move to NIRA lifecycle |
| #617 | Activate autonomous Factory | Move to NIRA lifecycle/activation |
| #619 | Evidence pipeline + first autonomous cycle | Move to NIRA evidence/E2E proof |
| #620 | Automation runtime execution | Move to NIRA runtime |
| #637 | Runtime Control Plane | Move to NIRA core runtime control plane |
| #640 | Immutable event-driven documentation law | Move to NIRA governance |
| #641 | Canonical intake + priority queue | Move to NIRA intake/queue |
| #644 | Exact-main lease validation | Move to NIRA queue/lease safety |

### Issues that remain Arvin product/client issues

Examples explicitly excluded from Factory migration: #357, #438, #446, #460, #516, #529, #577, #608, #613 and product-specific Calendar/Task/FollowUp/Sync/UI issues. Their Factory-gate references may be replaced with NIRA client contracts, but their product requirements stay in Arvin.

### Historical automation-failure issues

#587, #603, #606, #628, #630, #633, #634 and similar `[AUTO-FIX]` issues are execution evidence/history, not reusable Factory specification. Preserve provenance where needed for evidence migration; do not recreate them as NIRA backlog items unless a generic failure class is still required.

## 7. Important findings

### Finding F1 — Arvin currently contains a substantial Factory layer
The audit confirms that Factory orchestration, queue, worker, promotion, evidence and governance concepts are not merely historical documentation; Arvin contains executable Factory-oriented workflows/runtime assets as well.

### Finding F2 — The AI Worker is bounded, not an unrestricted autonomous writer
The current Arvin worker design explicitly keeps model tools read-only, makes repository writes runtime/workflow-owned, validates generated patches, bounds provider time/budget, and forbids model-side push/merge/authentication changes. These are high-value NIRA safety contracts.

### Finding F3 — There are two different classes of CI
Arvin product CI (`Build`, `Device Smoke`, product tests) should remain in Arvin. Factory orchestration around those gates belongs in NIRA.

### Finding F4 — `FACTORY_DOCUMENTATION_POLICY.md` is referenced by Factory issue #640 but was not found on current Arvin main
This is a migration gap. It must not be reconstructed from assumptions. Recover from verified Git history/PR content before canonicalization.

### Finding F5 — Do not migrate product requirements merely because they mention Factory
Product feature issues can reference Factory gates without becoming NIRA-owned. Ownership is determined by whether the artifact defines/implements the Factory itself.

## 8. Safe migration sequence

1. Freeze this inventory as migration baseline.
2. Create NIRA canonical contracts and provenance records.
3. Port generic validators/tests before deleting any Arvin Factory workflow.
4. Register Arvin as a NIRA client and define its adapter boundary.
5. Run a real NIRA→Arvin dry-run/evidence cycle.
6. Run exact-head validation and evidence reconstruction.
7. Replace each Arvin Factory workflow with the minimal client adapter.
8. Re-run Arvin product CI and device validation.
9. Only after successful replacement, remove duplicate Factory implementation from Arvin through separate reviewed PRs.
10. Preserve historical issue/document references and migration provenance.

## 9. Current audit verdict

**AUDIT COMPLETE FOR THE IDENTIFIED ARVIN FACTORY SURFACE — MIGRATION NOT YET COMPLETE.**

The safe conclusion is not “delete Factory from Arvin now.” The safe conclusion is:

`Inventory → Classify → Canonicalize in NIRA → Register Arvin client → Validate E2E → Replace adapters → Cleanup duplicates`

No destructive Arvin operation was performed by this audit.
