# Gate Evidence Aggregator — Orchestrator Integration Contract

The Production Orchestrator is the sole consumer authorized to convert gate evidence into a promotion decision.

## Contract
`get_promotion_snapshot(commit_sha, required_gates) -> GateEvidenceSnapshot`

The snapshot MUST be bound to the requested exact SHA and contain one normalized evaluation for every required gate.

## Consumption rules
1. Reject any snapshot whose commit SHA differs from the current PR head SHA.
2. Reject missing required gates.
3. Allow promotion only when every required gate is `SUCCESS`.
4. Block on `FAILURE`, `PENDING`, `NOT_FOUND`, or `NOT_EXPOSED`.
5. Require traceable evidence references and immutable publication metadata.
6. Never infer success from PR state, branch state, workflow name, or partial connector output.

The aggregator has no merge authority and cannot write to `main`.
