# NIRA — Arvin Factory Experience Transfer Matrix

**Status:** Active canonical migration register
**Scope:** Generic autonomous-factory capabilities only
**Independence rule:** No Arvin product code, business logic, product data, or product-specific CI implementation is transferred.

## Capability matrix

| Capability learned/validated in Arvin | NIRA status | Target | Priority |
|---|---|---|---|
| Exact-current-main fencing | Implemented | Worker + promotion | P0 |
| Exact-head CI evidence | Implemented | Promotion | P0 |
| Current-main ancestry check | Implemented | Promotion | P0 |
| Guarded squash promotion | Implemented | Promotion | P0 |
| Post-merge main verification | Implemented | Promotion | P0 |
| Immediate self-wake after merge | Implemented | Promotion | P0 |
| 5-minute recovery watchdog | Implemented | Recovery | P0 |
| Authorization label + branch prefix | Implemented | Promotion registry | P0 |
| Complete CI/E2E/conformance/security gate set | Implemented in promotion policy | Promotion | P0 |
| Evidence artifact validation | Implemented | Promotion | P0 |
| Draft-to-ready only after all gates pass | Implemented | Promotion | P0 |
| Candidate serialization / max candidates per cycle | Implemented | Promotion | P0 |
| Fail-closed on base drift / HEAD drift / main movement | Implemented | Promotion | P0 |
| Durable issue queue + intake | Implemented | Intake | P1 |
| Lease + stale lease recovery | Implemented | Queue/lease | P1 |
| Bounded AI worker execution | Existing NIRA capability | Worker | P1 |
| Single-launch / idempotency | Existing contract; must remain enforced | Worker | P1 |
| Failure → bounded Auto-Fix feedback | Planned transfer | Feedback loop | P1 |
| Duplicate Auto-Fix suppression | Planned transfer | Feedback loop | P1 |
| Exact-main worker dispatch contract | Existing / verified | Worker | P1 |
| Parallel wave scheduling | Planned transfer | Runtime | P1 |
| Worker routing by task class | Planned transfer | Intake/runtime | P1 |
| Test-worker evidence protocol | Planned transfer | Evidence | P1 |
| Release closure / reproducible release evidence | Planned transfer | Release | P1 |
| Evidence-first status vocabulary | Existing NIRA governance | Observability | P1 |
| Canonical document authority | Existing NIRA governance | Governance | P1 |
| Cross-repository client adapter model | Existing NIRA direction | Client adapters | P1 |
| Persistent runtime control plane | Planned / verify against current implementation | Runtime | P1 |
| Cross-repo E2E: Issue → Worker → PR → CI → Promotion → Release | Required proof | E2E | P0 |

## Promotion contract now canonical in NIRA

A candidate may advance only when:

1. It is explicitly authorized by the NIRA registry.
2. Its branch uses the NIRA branch prefix.
3. Its base SHA equals current `main`.
4. Every required NIRA gate passes on the exact candidate HEAD.
5. Required evidence artifacts exist and are unexpired.
6. The PR remains open and points to the exact validated HEAD.
7. `main` has not moved during validation.
8. Merge is performed only by the canonical NIRA Production Orchestrator.
9. The resulting `main` SHA equals the confirmed merge SHA.
10. The orchestrator immediately wakes itself for the next candidate; the scheduled sweep remains the recovery path.

## Transfer law

Arvin remains the reference source for engineering lessons, but NIRA is the canonical owner of generic Factory behavior. Transfer means **reimplementation of generic invariants**, not copying product-specific implementation.

## Remaining migration waves

### P0 — Proof
- Complete cross-repository E2E evidence.
- Prove automatic promotion without a human Merge click.
- Prove recovery after stale lease and failed gate.
- Prove idempotent replay and duplicate suppression.

### P1 — Runtime
- Port bounded failure-feedback / Auto-Fix loop.
- Port parallel-wave scheduling and worker routing.
- Port test-worker evidence contract.
- Port release-closure evidence contract.
- Verify persistent runtime control-plane behavior.

### P2 — Hardening
- Contract-test every invariant.
- Add failure-injection coverage.
- Add provenance and reproducibility checks.
- Keep security and project-independence gates mandatory.
