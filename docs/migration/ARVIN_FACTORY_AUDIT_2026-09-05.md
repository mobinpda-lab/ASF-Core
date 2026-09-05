# NIRA — Arvin Factory Extraction Audit

**Audit date:** 2026-09-05 (Iran)
**Source repository:** `mobinpda-lab/Arvin-clean`
**Source branch audited:** `main`
**Destination:** `mobinpda-lab/ASF-Core` / NIRA
**Migration rule:** inventory first; no destructive source change during audit.

## 1. Executive finding

Arvin contains a substantial set of factory-control artifacts that must be re-homed to NIRA. The product itself remains independent. Factory ownership must move to NIRA; Arvin should retain only product behavior and the minimum client/adapter contract required to consume NIRA services.

This audit identifies four classes:

- **TRANSFER** — factory-owned source of truth; move/rebuild canonically in NIRA.
- **ADAPT** — shared contract or product integration; canonical contract in NIRA, thin adapter remains in Arvin.
- **RETAIN** — Arvin product-only material; do not move.
- **HISTORY/ARCHIVE** — historical Arvin evidence retained for provenance, but not treated as current factory authority.

No Arvin deletion is authorized by this audit.

## 2. Confirmed factory workflows

| Source path | SHA | Classification | NIRA destination | Arvin end state |
|---|---|---|---|---|
| `.github/workflows/arvin-agent-worker.yml` | `6116c37b7ebccfb0e1c16793a7f92757bbfc447c` | TRANSFER/ADAPT | `workflows/agents/code-worker.yml` + `engine/agents/` | Replace with thin NIRA client adapter after validation |
| `.github/workflows/arvin-autonomous-queue.yml` | `31f537de06f50bbd770851a8dd9459a1d6d9fe20` | TRANSFER | `workflows/queue/intake.yml` + `engine/queue/` | Remove duplicate queue after NIRA parity |
| `.github/workflows/arvin-orchestrator.yml` | `690c5689bdf4e49ee8dfc4e3d3f77c63759a6d1d` | TRANSFER | `workflows/orchestration/` + `engine/orchestration/` | Replace with NIRA orchestration adapter |
| `.github/workflows/arvin-production-loop.yml` | `b7916f078e4e066bbbb447c187215fc052a3ca42` | TRANSFER/ADAPT | `workflows/feedback/production-loop.yml` | Keep only product-side callback/adapter |
| `.github/workflows/arvin-test-worker.yml` | `dba0f9edeee9a1ca88de9a9d0694a074e0d7a2b3` | TRANSFER/ADAPT | `workflows/agents/test-worker.yml` | Product CI remains; factory worker moves |
| `.github/workflows/factory-rest-promotion-bridge.yml` | `ba214d3b2bf4b20d56bdbb3db67b8eb7905e89b6` | TRANSFER/ADAPT | `workflows/promotion/rest-bridge.yml` | Retain only as NIRA client bridge until cutover |
| `.github/workflows/parallel-wave.yml` | `94dd06d7c41e84a4eb2f3441ebe4b9280af162a2` | TRANSFER/ADAPT | `workflows/execution/parallel-wave.yml` | Product-specific lanes stay Arvin; factory scheduler moves |
| `.github/workflows/production-orchestrator.yml` | `1d43097816b90d8316c9328658ebcac95c5d4fee` | TRANSFER | `workflows/promotion/production-orchestrator.yml` | Remove duplicate promotion authority after NIRA proves parity |
| `.github/workflows/progress-score.yml` | `42a6ad7fd0df10dbecf1d4a559d452b05706b89d` | ADAPT/TRANSFER | `observability/progress/` | Product score may remain; factory score becomes NIRA |
| `.github/workflows/release-closure.yml` | `3a4afd6a6ed8901c4862df2481191c0eab6a2e07` | ADAPT | `workflows/release/closure.yml` | Arvin release closure remains product-specific, NIRA owns factory evidence |
| `.github/workflows/build.yml` | `7c813bf8da29d5bcd09acb6648fecc44241e655a` | RETAIN/ADAPT | NIRA contract only | Keep Arvin product build workflow |
| `.github/workflows/device-smoke.yml` | `f74ec7b8be72740b662f468d892842352cb72e8b` | RETAIN/ADAPT | NIRA evidence contract only | Keep Arvin product/device validation |

## 3. Confirmed factory runtime files

| Source path | SHA | Classification | NIRA destination |
|---|---|---|---|
| `.github/arvin/agent-runtime.py` | `7815fc1b83debc498017fcfc34fd7862a73f33f4` | TRANSFER | `runtime/agents/agent-runtime.py` |
| `.github/arvin/production-queue.yml` | `e940d0f3f7ae00640cdc3cfbf419d9d37aee7f2d` | TRANSFER | `contracts/queue/production-queue.yml` |
| `.github/arvin/task-router.yml` | `4fd2ea86aab0a0c7cc4e150427ed9c49378c1b23` | TRANSFER | `contracts/routing/task-router.yml` |
| `tool/validate_fast_lane.py` | audited by factory/workflow searches | TRANSFER/ADAPT | `tools/validation/fast-lane-validator.py` |

The AI Worker runtime is explicitly factory-oriented: provider fallback, bounded retry/timeout, structural patch validation, trusted runtime writes, evidence feedback, and guarded PR delivery. It must not remain an Arvin-owned factory core. The current Arvin hardening record states that model output is untrusted until structural validation, `git apply --check`, project validation and delivery gates succeed.

## 4. Confirmed factory documentation / policy sources

| Source path | Classification | NIRA destination | Notes |
|---|---|---|---|
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE.md` v49.0 | TRANSFER + split | `docs/governance/NIRA_FACTORY_OPERATING_STANDARD.md` | Extract factory rules; product-specific sections remain Arvin |
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE_v48.2_TRANSFER_MANIFEST.md` | HISTORY/PROVENANCE | `docs/migration/provenance/arvin-v48.2-transfer-manifest.md` | Preserve transfer history |
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE_v48.2_FINAL_OPERATIONAL_feshordeh_PART02.md` | HISTORY/PROVENANCE | `docs/migration/provenance/arvin-v48.2/` | Historical source segment; classify before canonicalization |
| `docs/ARVIN_PROJECT_OPERATING_PACKAGE_v48.2_FINAL_OPERATIONAL_feshordeh_SOURCE_VERIFIED.md` | HISTORY/PROVENANCE | `docs/migration/provenance/` | Controlled transfer evidence |
| `docs/FACTORY_DOCUMENTATION_POLICY.md` | TRANSFER | `docs/governance/FACTORY_DOCUMENTATION_POLICY.md` | Factory governance |
| `docs/ARVIN_PRODUCTION_ORCHESTRATOR_5MIN_MODE.md` | TRANSFER | `docs/orchestration/PRODUCTION_ORCHESTRATOR.md` | 5-minute monitoring/orchestration concept |
| `docs/AI_WORKER_PATCH_HARDENING_2026-08-31.md` | TRANSFER | `docs/agents/AI_WORKER_PATCH_HARDENING.md` | Factory worker safety |
| `docs/AI_WORKER_SINGLE_LAUNCH_AUTHORITY_2026-08-31.md` | TRANSFER | `docs/agents/AI_WORKER_SINGLE_LAUNCH_AUTHORITY.md` | Single launch authority |
| `docs/CI_FAST_LANE_2026-08-26.md` | TRANSFER/ADAPT | `docs/gates/FAST_GATE.md` | Generic factory gate; Arvin-specific build details remain client-side |
| `docs/CI_RELEASE_VALIDATION_NOTE.md` | ADAPT | `docs/contracts/client-release-validation.md` | Client build environment contract |
| `docs/CI_TRIGGER_AUDIT_2026-08-15.md` | TRANSFER/PROVENANCE | `docs/evidence/ci-trigger-audit.md` | Generic trigger/evidence rules |
| `docs/CI_STALE_RUN_CONCURRENCY_2026-08-26.md` | TRANSFER | `docs/gates/stale-run-concurrency.md` | Generic stale-run protection |
| `docs/RELEASE_EVIDENCE_COMPLETION_LANE_2026-08-26.md` | TRANSFER | `docs/evidence/release-completion-lane.md` | Factory evidence pattern |
| `docs/REPORTING_STANDARD.md` | SPLIT | `docs/governance/reporting-standard.md` | Generic reporting rules to NIRA; product report semantics stay Arvin |
| `docs/AI_CONTINUATION_STATE.md` | SPLIT | `docs/governance/continuation-state.md` | Factory source-of-truth hierarchy to NIRA; product continuity remains Arvin |
| `docs/ARVIN_CONTINUATION_COMMAND.md` | SPLIT | `docs/governance/continuation-protocol.md` | Generic continuation protocol to NIRA |
| `docs/DOCUMENT_AUTHORITY_INDEX.md` | SPLIT | `docs/governance/document-authority.md` | Generic authority hierarchy to NIRA |
| `docs/DEVELOPMENT_RULES.md` | SPLIT | `docs/governance/development-rules.md` | Factory governance subset to NIRA; product/UI rules remain Arvin |
| `docs/PROJECT_ROADMAP_2026-08-14.md` | SPLIT | `docs/migration/provenance/` | Only factory execution/parallelism concepts migrate |
| `docs/ARVIN_PROJECT_STATE.md` | SPLIT | `docs/migration/provenance/` | Factory status claims migrate only as historical evidence |
| `docs/ARVIN_STATUS.md` | HISTORY | `docs/migration/provenance/` | Product status remains Arvin |

## 5. Confirmed factory issues / execution records

| Issue | Title | Classification | NIRA destination |
|---|---|---|---|
| #617 | Activate ARVIN Autonomous Software Factory: Continuous Production Mode | TRANSFER | `docs/execution/continuous-production.md` + backlog mapping |
| #619 | ARVIN Factory Execution: Evidence Pipeline and First Autonomous Cycle | TRANSFER | `docs/evidence/first-autonomous-cycle.md` + evidence engine backlog |
| #620 | ARVIN Parallel Worker Wave 1 - Automation Runtime Execution | TRANSFER | `engine/runtime/` + execution backlog |
| #621 | ARVIN Parallel Worker Wave 2 - Smart FollowUp Engine Production | RETAIN/ADAPT | Product feature stays Arvin; factory execution contract moves |
| #637 | ASF: Runtime Control Plane — persistent state, worker capacity and event-driven recovery | TRANSFER | `engine/control-plane/` |
| #640 | ASF: enforce immutable event-driven documentation law | TRANSFER | `governance/documentation-law/` |
| #641 | ASF: Canonical Product + Observation Intake and Priority Queue | TRANSFER | `engine/intake/` + `engine/queue/` |
| #644 | ASF: enforce exact-main lease validation in Arvin Code Worker | TRANSFER | `engine/leases/` + `agents/code-worker/` |
| #616 | ARVIN Autonomous Software Factory - Continuous Production Mode | HISTORY/CONSOLIDATE | Merge into canonical NIRA operating model; preserve provenance |
| #615 | exec: Bootstrap Autonomous Factory Execution Evidence | TRANSFER/HISTORY | `docs/evidence/bootstrap.md` |
| #610 | docs: adopt Universal Autonomous Software Factory Protocol v2 | TRANSFER | `docs/governance/universal-factory-protocol.md` |
| #553 | [AUTO] Activate Arvin production worker runtime | TRANSFER/HISTORY | `engine/runtime/` |
| #588 | ci(agent): make Orchestrator the single AI Worker launch authority | TRANSFER | `governance/launch-authority.md` |
| #576 | [AUTO] Normalize Copilot patch output and bound provider latency | TRANSFER | `agents/providers/patch-safety.md` |
| #562 | [AUTO] Ignore expected gate cancellations in Production feedback loop | TRANSFER | `engine/feedback/cancellation-policy.md` |
| #551 | ARVIN Full Autonomous Production Loop - Maximum Parallel Automation | TRANSFER/HISTORY | `docs/execution/production-loop.md` |
| #550 | ARVIN Smart Documentation Policy + Maximum Parallel Production Activation | TRANSFER/HISTORY | `governance/documentation-law/` |
| #549 | ARVIN AI Worker Activation - Task Analyzer + Code Generation Loop | TRANSFER | `engine/agents/task-analysis.md` |
| #548 | ARVIN Production Orchestrator - First Full Automation Loop | TRANSFER/HISTORY | `docs/execution/first-automation-loop.md` |
| #547 | ARVIN Production Orchestrator Phase 3: Auto PR Flow | TRANSFER | `engine/promotion/draft-pr.md` |
| #546 | ARVIN Production Orchestrator Phase 2: Auto Issue Tracking + Auto Documentation | TRANSFER | `engine/intake/` + `governance/documentation-law/` |
| #544 | ARVIN Production Orchestrator (5 Minute Monitoring Mode) | TRANSFER | `engine/orchestration/` |
| #540 | consolidate autonomous production rules and release execution priorities | TRANSFER/HISTORY | `docs/governance/priority-and-production-modes.md` |
| #538 | ARVIN-CLEAN Autonomous Finish Mode Pipeline | ADAPT/HISTORY | Product release process stays Arvin; generic gate pattern to NIRA |

## 6. Important issue relationship

The audit confirms that Arvin issues contain both factory and product work. They must not all be moved wholesale. In particular, #621 is a product feature despite being executed through the factory; its FollowUp implementation belongs to Arvin. Likewise calendar/report/UI issues such as #516/#529/#438 remain product-owned and are not factory migrations.

## 7. Factory contracts extracted from Arvin

The following are canonical candidates for NIRA contracts:

1. **Issue intake contract:** source, affected area, evidence, dependency, risk, effort, product value, urgency, current-main SHA, audit trail.
2. **Classification contract:** RELEASE_BLOCKER, SECURITY, CORE, BUGFIX, PRODUCT_FEATURE, UX, QUALITY, FACTORY_AUTOMATION, DOCUMENTATION, OBSERVATION, IDEA, HUMAN_DECISION.
3. **Priority contract:** evidence/risk/dependency/readiness-based ordering.
4. **Lease contract:** exact current-main SHA captured at lease time; worker must fail closed if main moved.
5. **Worker contract:** one worker per issue; bounded execution; isolated branch; no direct main write.
6. **Patch trust contract:** model output is untrusted until structural diff validation and `git apply --check`.
7. **Provider budget contract:** bounded per-call timeout and aggregate retry budget.
8. **Launch authority contract:** one explicit orchestrator dispatch authority; no duplicate label-triggered worker launch.
9. **Gate contract:** Draft → Fast → Ready → Build/APK + Device → guarded promotion.
10. **Promotion contract:** one Production Orchestrator / one merge authority.
11. **Failure feedback contract:** real failure/timed-out is actionable; expected protective cancellation is not an auto-fix trigger.
12. **Evidence contract:** Issue → Commit → PR → CI/Test/Build/Device → Merge → Release evidence.
13. **Documentation law:** meaningful factory changes require canonical documentation/evidence; enforcement is fail-closed.
14. **Recovery contract:** stale lease detection, bounded requeue/self-fix, event-driven state transitions, resumability.
15. **Parallelism contract:** independent work may run concurrently; conflicting tasks may not share a lease.
16. **L10 evidence rule:** no Level-10/full-autonomy claim without a real reconstructible end-to-end autonomous cycle.

## 8. Explicit non-migration list

The following remain Arvin-owned:

- Flutter product source and UI
- Task / Reminder / FollowUp / Calendar / Report product models and storage
- product-specific Android integrations
- product-specific build/device tests
- canonical Arvin visual/UI acceptance
- product roadmap and product feature requirements
- product-only issues and feature implementations

## 9. Safety gates before Arvin cleanup

No source file/workflow/issue artifact should be deleted merely because it appears in this inventory. Cleanup is permitted only after:

1. NIRA canonical implementation/documentation exists.
2. NIRA contract tests pass.
3. A real Arvin client adapter path is validated.
4. NIRA can operate without Arvin-specific factory code.
5. Exact-head CI evidence is available on both sides where applicable.
6. Historical provenance is recorded.
7. A dedicated Arvin cleanup PR removes only proven duplicates.
8. Rollback path is documented.

**Status:** AUDIT COMPLETE FOR CONFIRMED FACTORY SURFACES; migration/cleanup NOT yet executed.
