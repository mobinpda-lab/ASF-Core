# NIRA — Arvin Factory Extraction Audit

**Audit date:** 2026-09-05 (Iran time)
**Source repository:** `mobinpda-lab/Arvin-clean`
**Source ref audited:** `main`
**Destination repository:** `mobinpda-lab/NIRA`
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
