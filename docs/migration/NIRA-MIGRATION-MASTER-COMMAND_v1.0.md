# NIRA-MIGRATION-MASTER-COMMAND v1.0

## Status
Canonical execution directive registered on a fresh migration branch based on current `main`.

## Mission
Build NIRA as an independent autonomous software factory platform while preserving proven knowledge, evidence, documentation, history, and lessons from ASF-Core, Arvin-clean, YadNegar, and NetworkCenterMonitor. Migrate factory authority to NIRA and connect products through adapters without duplicating authorities or stopping product development.

## Source of truth
GitHub: repositories, branches, commits, pull requests, Actions/CI/CD, code, documentation, artifacts, history, and reconstructible evidence.

## Target boundary
NIRA owns factory core, orchestration, intake, queue, worker runtime, agents/providers, leases/fencing, evidence, governance, promotion, release control, monitoring, recovery, audit, memory, and learning.

Clients own product code, domain logic, UI, business rules, product tests, and product documentation. Clients must not own factory authority, queue authority, worker authority, promotion authority, or autonomous factory runtime.

## Execution phases
1. Complete discovery across ASF-Core, Arvin-clean, YadNegar, and NetworkCenterMonitor.
2. Preserve knowledge before code migration through a NIRA knowledge base covering architecture history, factory decisions, worker lessons, CI/CD patterns, security lessons, failure/recovery cases, successful workflows, and product integration patterns.
3. Build the independent NIRA platform from the existing ASF-Core foundation rather than duplicating it: registry, intake, queue, state machine, lease manager, worker identity, fencing, capacity control, provider abstraction, evidence ledger, promotion authority, audit, monitoring, recovery, memory, and learning.
4. Remove future factory authority from clients only through controlled PRs after NIRA capability and evidence gates are proven. Never delete historical knowledge, evidence, or product knowledge.
5. Create client adapters for Arvin, YadNegar, and NetworkCenterMonitor. Adapters expose repository metadata, build/test/security/deployment commands and product constraints; adapters do not execute factory authority.
6. Execute the real pipeline: issue → intake → priority → queue → lease → fence → worker → branch → code → test → security → PR → CI → exact-head validation → promotion → merge → release → monitor → recovery → next task.
7. Use Arvin as the first real client proof. No L10 claim before a real registered-client cycle, controlled failure/fencing/recovery, promotion/release, independent postcondition, and reconstructible evidence are proven.
8. Keep NIRA development, adapter work, and product development in parallel lanes whenever dependencies permit.
9. Final validation requires single NIRA factory authority, preserved knowledge, clean client separation, real E2E, tested recovery, reconstructible evidence, and no duplicate authority.

## Safety invariants
- NO_DIRECT_MAIN
- NO_DUPLICATE_WORKER
- NO_DUPLICATE_QUEUE
- NO_MULTIPLE_PROMOTION_AUTHORITY
- NO_FAKE_SUCCESS
- NO_DOCUMENTATION_ONLY_CLAIM
- NO_HISTORICAL_EVIDENCE_AS_CURRENT_PROOF
- FAIL_CLOSED
- BOUNDED_RETRY
- IDEMPOTENT_EXECUTION

## Operating rule
ASF-MOC v9.0 remains normative historical/source knowledge. NIRA is the canonical forward implementation. Existing ASF-Core/NIRA migration work is evidence and provenance, not permission to bypass exact-head/base, evidence, governance, recovery, or promotion gates.

## Current migration posture
Knowledge/document/contract transfer is substantially established. Operational cross-repository transfer remains incomplete until the real registered-client E2E and independent failure/fencing/recovery/promotion/release evidence are completed. Legacy client factory workflows remain protected until supersession is proven.
