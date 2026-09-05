# ARVIN Factory Runtime Migration -> NIRA

Status: ACTIVE MIGRATION SOURCE
Source repository: mobinpda-lab/Arvin-clean
Source baseline: 9a773b7898ff63276ad6a214009b163f904e8923
Target repository: mobinpda-lab/ASF-Core
Target branch: feat/nira-arvin-factory-migration-v1

## Purpose

This document transfers the reusable factory-runtime knowledge discovered and exercised in Arvin into NIRA. It does NOT transfer Arvin product logic, product roadmap, business rules, or client-owned implementation into the factory.

## Reusable Arvin execution evidence

Arvin already contains GitHub-native automation patterns for:
- issue-triggered and scheduled queue routing;
- idempotent lease markers using labels/comments;
- exact-main snapshot validation before worker execution;
- explicit workflow_dispatch worker activation;
- bounded AI code generation with patch-structure validation;
- bounded self-fix/test attempts;
- guarded draft PR creation;
- exact-head Build/Device validation;
- fail-closed stale-head handling;
- single promotion/orchestrator authority;
- post-merge main verification;
- immediate orchestrator wake-up after successful promotion.

These patterns are evidence and design input for NIRA. They are not accepted as proof that NIRA itself executed the same chain.

## Source files inspected

1. `.github/workflows/arvin-autonomous-queue.yml`
   - issue/schedule intake
   - candidate selection and priority ordering
   - lease labels and durable GitHub issue comment marker
   - exact-main snapshot capture
   - explicit worker dispatch

2. `.github/workflows/arvin-agent-worker.yml`
   - workflow_dispatch worker contract
   - exact-main lease validation
   - bounded AI provider execution
   - patch validation/application
   - project validation
   - worker branch and draft PR creation
   - delegation to canonical orchestrator

3. `.github/arvin/agent-runtime.py`
   - bounded provider timeout/budget
   - complete unified-diff requirement
   - diff size/file-count limits
   - `git apply --check`
   - bounded auto-fix loop
   - validation after each attempt
   - safe reset after failed attempts

4. `.github/workflows/arvin-orchestrator.yml`
   - task classification
   - idempotent routing markers
   - security/credential/destructive/migration fail-closed routing
   - explicit worker dispatch
   - scheduled recovery sweep

5. `.github/workflows/production-orchestrator.yml`
   - exact current-main check
   - exact-head CI discovery
   - stale-head rejection
   - Build + Device gate coordination
   - merge only after exact-head validation
   - post-merge main verification

6. `.github/workflows/factory-rest-promotion-bridge.yml`
   - historical bridge pattern; to be treated as legacy input only and redesigned under NIRA authority.

## NIRA adaptation rules

The following Arvin concepts MUST become factory-generic before reuse:
- `ARVIN_*` names -> NIRA contract names;
- client-specific labels -> factory task states;
- client-specific workflow IDs -> registry-resolved workflow identities;
- client-specific test/build/device commands -> adapter-declared capabilities;
- client-specific promotion logic -> NIRA promotion authority;
- client-specific evidence -> independent factory evidence collector.

NIRA MUST NOT copy:
- Arvin product code;
- Arvin business logic;
- Arvin feature decisions;
- Arvin product roadmap;
- Arvin issue backlog as NIRA backlog;
- Arvin client merge authority.

## Trust-model corrections required during migration

Arvin's worker model is useful as a source pattern but NIRA must improve it in three areas:
1. Worker identity and lease state must be factory-authoritative, not merely workflow parameters.
2. Evidence verification must be independently derived from GitHub state; a worker must not self-assert `verified=true`.
3. Security/provenance must be first-class gates, including artifact digest and attestation where the environment supports it.

## Current Arvin proof target

PR #659 remains the reference client execution candidate:
- Issue: #658
- PR: #659
- Head: ac827a8336274a6db18470b80d60ea812d3fc700
- Base: 9a773b7898ff63276ad6a214009b163f904e8923
- Build/Device/Production workflow evidence: available
- Security evidence: incomplete
- Commit status chain: unverified
- Full NIRA-controlled production E2E: unproven

## Acceptance rule

Arvin historical automation is considered migrated only when NIRA can reproduce the reusable behavior through NIRA-owned generic control-plane contracts and produce reconstructible GitHub evidence. Documentation-only similarity does not count as execution proof.
