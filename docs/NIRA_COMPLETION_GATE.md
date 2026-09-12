# NIRA Autonomous Completion Gate

This document defines the machine-enforced path that lets NIRA continue its own completion in GitHub without requiring a user to type `continue` in ChatGPT.

## Authority model

GitHub remains the source of truth. The autonomous controller does not write directly to `main` and does not merge pull requests. It creates/reconciles bounded factory tasks and delegates execution to the existing canonical NIRA path:

`Self-completion controller -> Intake Queue -> Queue Scheduler -> Lease -> Worker -> PR -> CI/E2E/Conformance/Security -> Production Orchestrator -> main`

The controller runs every five minutes and on pushes to `main`.

## Stages 1-8

1. **Permanent scheduled GitHub Action** — `.github/workflows/nira-autonomous-self-completion.yml` runs every five minutes.
2. **Real orchestrator** — the controller reuses the existing Production Orchestrator and canonical Queue Scheduler instead of creating a second execution authority.
3. **Controlled mutation authority** — mutations are PR-only, scope-checked against the machine-readable plan, exact-main fenced, and merged only by the canonical promotion authority after required gates pass.
4. **Official queue** — GitHub Issues with `factory:*` labels remain the durable queue. `factory/registry/self-completion-plan.json` supplies dependency order and exact file scope.
5. **Auto-fix / worker path** — existing NIRA lease, worker, failure-feedback and recovery workflows execute bounded repair work and create evidence.
6. **Main protection** — NIRA automation never directly writes `main`; the promotion workflow requires exact base/head and successful NIRA CI, Factory E2E, Factory Conformance and Security Gate evidence. Repository-host branch protection/rulesets remain an external GitHub setting and are not replaced by this document.
7. **Self-completion goal** — the machine-readable plan defines the remaining NIRA v1 completion tasks and their acceptance criteria.
8. **No ChatGPT continuation dependency** — after this controller is merged, eligible completion work is created, queued, scope-authorized, reconciled and advanced by GitHub Actions without requiring a new chat message.

## Fail-closed rules

NIRA must not self-certify when any of these conditions is true:

- a planned task is incomplete;
- a task PR changes a file outside its exact allowlist;
- a task PR changes a protected factory-authority file;
- retry budget is exhausted;
- an exact-main required workflow is missing or not successful;
- active self-completion work remains in ready/queued/leased/in-progress states;
- evidence cannot be reconstructed from GitHub.

## Completion state

`NIRA_V1_SELF_COMPLETION=CERTIFIED` is emitted only when all tasks in `factory/registry/self-completion-plan.json` are complete and the required workflows are successful on the exact current `main` SHA. At that point parent completion issues can be closed automatically.

## Protected authority files

The autonomous self-completion task workers are not authorized to change the canonical promotion, queue, lease, worker, conformance, security or autonomous-policy files listed in `factory/registry/autonomous-mutation-policy.json`. Changes to those files require a separately reviewed bootstrap or governance change.
