# NIRA Knowledge Base

Purpose: preserve experience before code migration. This document is an index; detailed lessons remain traceable to source repositories, commits, issues, PRs, workflows, and evidence.

## architecture_history
- ASF-Core evolved from ASF-MOC v9.0 into an independent factory control-plane boundary.
- The factory must be generic; project-specific behavior belongs behind explicit client adapters.
- NIRA is the forward canonical identity; ASF-Core/ASF-MOC identifiers remain historical provenance.

## factory_decisions
- One queue authority, one worker authority, one promotion authority.
- Exact HEAD and exact base are mandatory.
- Workers cannot merge and cannot self-author independent PASS evidence.
- Promotion requires fail-closed gates and independent postcondition verification.

## worker_lessons
- Arvin worker hardening established bounded provider attempts and rejection/validation feedback handling.
- Single-launch authority is essential to prevent duplicate workers.
- Provider fallback must remain bounded and policy-controlled.

## ci_cd_patterns
- Separate fast validation, build/device validation, and guarded promotion stages.
- Bind evidence to exact workflow run/head rather than merely to a workflow name.
- Product CI remains product validation; factory CI controls factory gates.

## security_lessons
- Least privilege and no client-side merge primitive are mandatory.
- Missing/stale/inaccessible evidence is not a PASS.
- Factory authority must not be recreated inside clients.

## failure_cases
- Duplicate orchestration/worker-launch paths create authority ambiguity.
- Self-reported worker success is insufficient as independent evidence.
- A branch behind current main cannot be promoted without refresh/revalidation.

## recovery_patterns
- NetworkCenterMonitor provides proven experience around persistent runtime state, worker capacity, heartbeat, lease TTL and event-driven stale-lease recovery.
- NIRA policy standardizes bounded, idempotent recovery and fencing.

## successful_workflows
- ASF-Core registry-authorized promotion and exact-head/base validation provide factory-side patterns.
- Arvin's production orchestration provides client-side automation experience to be converted into adapter requirements and NIRA-owned capabilities.

## product_integration_patterns
- Clients expose repository metadata, test/build/security/deployment requirements and product constraints.
- Clients do not expose factory authority.

## evidence_policy
Evidence must be independently reconstructible from immutable identifiers such as commit SHA, workflow run/result, test result, build artifact, security result, PR, promotion/release result, and postcondition read.

## L10 rule
Documentation, unit tests, deterministic conformance tests, or historical evidence are not current L10 proof. L10 requires a genuine registered-client production cycle plus failure/fencing/recovery and promotion/release evidence that can be independently reconstructed.
