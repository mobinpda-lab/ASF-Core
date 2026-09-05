# NIRA Execution Roadmap v1

## Phase A — Foundation (current)
- Establish NIRA identity and boundary.
- Audit Arvin factory surface.
- Canonicalize factory contracts.
- Establish migration law and client adapter contract.

## Phase B — Executable control plane
- Implement machine-readable intake/queue/lease state.
- Implement worker identity, capacity, heartbeat and fencing.
- Implement provider-neutral bounded runtime.
- Implement exact-base/head gates.
- Implement evidence ledger and recovery state.

## Phase C — Orchestration
- Implement single launch authority.
- Implement scheduling, dependency/conflict checks and bounded parallelism.
- Implement failure feedback and idempotent recovery.
- Implement serialized promotion and independent postcondition reads.

## Phase D — Arvin integration
- Add thin Arvin adapter.
- Submit a real Arvin issue through NIRA.
- Capture reconstructible evidence for every lifecycle transition.
- Exercise at least one failure/fencing/recovery path.
- Validate promotion/release postconditions.

## Phase E — Product cleanup
- Deprecate corresponding Arvin factory workflows one subsystem at a time.
- Remove only proven duplicates in separate governed PRs.
- Retain historical provenance and link old issues/docs to NIRA replacements.

## Phase F — L10 verification
L10 becomes `VERIFIED` only after independent evidence proves the full lifecycle across a registered client, including recovery and release/promotion. Until then it remains `UNVERIFIED`.
