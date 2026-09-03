# ASF-Core Gate Evidence Aggregator

## Status
PLANNED FACTORY CAPABILITY — specification only.

## Purpose
The Gate Evidence Aggregator provides a reusable, exact-head evidence boundary between GitHub execution systems and the Production Orchestrator. It discovers and correlates quality-gate evidence for one commit SHA without assuming that absence from one observation interface means that a workflow did not execute.

The capability must distinguish genuine execution states from observation limitations and must never manufacture evidence.

## Scope
The aggregator is factory-level infrastructure. It MUST NOT contain product-specific business logic. Product repositories remain independent and integrate only through product adapters and explicit contracts.

## Architecture
```text
GitHub Actions / Checks / Jobs / Artifacts
                |
                v
        Evidence Collectors
                |
                v
       Correlation Layer
   SHA + workflow + event + run
                |
                v
       Gate Evidence Record
                |
                v
       Gate State Evaluator
                |
                v
      Production Orchestrator
```

### Components
1. **Collectors** — retrieve workflow runs, check runs, jobs, artifacts, and relevant commit status information through supported GitHub interfaces.
2. **Correlation Layer** — binds observations to an exact commit SHA and normalizes workflow identity, event type, run ID, job result, artifact result, and check result.
3. **Evidence Store** — preserves immutable normalized evidence records and their observation source/availability metadata.
4. **Gate Evaluator** — evaluates required gates deterministically from correlated evidence.
5. **Orchestrator Adapter** — exposes promotion-safe gate state to the Production Orchestrator.

## API / Interface Contract
Conceptual interface:

```text
collect(commit_sha, required_gates) -> GateEvidenceSnapshot
observe_workflow(commit_sha, workflow_identity) -> WorkflowEvidence
observe_check(commit_sha, check_identity) -> CheckEvidence
observe_jobs(run_id) -> JobEvidence[]
observe_artifacts(run_id) -> ArtifactEvidence[]
evaluate(snapshot, required_gates) -> GateEvaluation
```

### Required invariants
- `commit_sha` is mandatory and immutable for a snapshot.
- Every observation carries its source and observation timestamp.
- Workflow identity is explicit; workflow name alone is insufficient when IDs are available.
- Event type is retained (`pull_request`, `push`, or other supported event).
- Run ID is retained when execution exists.
- Job, artifact, and check results are independently represented.
- An unobservable record MUST NOT be converted into SUCCESS.
- Collector limitations MUST be represented separately from GitHub execution absence.
- The evaluator MUST fail closed for promotion when a required gate is unresolved.

## Evidence Model
A normalized gate evidence record contains at minimum:

```text
commit_sha
workflow_identity
workflow_id
workflow_path
event_type
run_id
run_status
run_conclusion
job_results[]
artifact_results[]
check_result
observation_source
observed_at
state
```

Optional fields may include branch, PR number, check-suite ID, artifact IDs, URLs, run attempt, and collector diagnostics.

Evidence is immutable after publication. Corrections create a new observation linked to the prior record rather than mutating historical evidence.

## Evidence State Model
Required normalized states:

- **SUCCESS** — execution/check evidence is observed and conclusively successful for the exact commit SHA.
- **FAILURE** — execution/check evidence is observed and conclusively failed.
- **PENDING** — execution exists or is expected and remains incomplete/non-terminal.
- **NOT_FOUND** — authoritative discovery confirms that the requested execution/check record does not exist for the exact SHA within the supported source boundary.
- **NOT_EXPOSED** — the execution may exist, but the collector/source cannot expose or verify it; this is an observability limitation, not a failure claim.

`NOT_FOUND` and `NOT_EXPOSED` MUST remain distinct.

## Correlation Rules
Correlation MUST require exact SHA equality. The aggregator MUST correlate, where available:

1. commit SHA
2. workflow identity and workflow ID/path
3. event type
4. run ID
5. run status/conclusion
6. job result(s)
7. artifact result(s)
8. check result/check-suite identity
9. branch/PR context where relevant

Evidence from another commit, stale PR head, or unrelated workflow execution MUST NOT satisfy a gate.

## Gate Evaluation
For each required gate, the evaluator emits:

```text
GateEvaluation {
  gate_id
  commit_sha
  state
  evidence_refs[]
  blocking_reason
}
```

Promotion eligibility is deterministic:

```text
PROMOTABLE = every required gate == SUCCESS
```

`FAILURE`, `PENDING`, `NOT_FOUND`, or `NOT_EXPOSED` for any required gate prevents promotion unless a separately defined, authoritative recovery policy resolves the state. No worker may override this rule.

## Production Orchestrator Integration
The Production Orchestrator consumes only the normalized GateEvaluation produced by ASF-Core. It MUST NOT infer gate success from raw workflow names, branch state, PR state, or partial connector results.

Before promotion, the Orchestrator requests an exact-head snapshot and verifies:
- requested SHA equals current PR head SHA;
- all required gates are present;
- every required gate is `SUCCESS`;
- evidence references are internally correlated;
- no unresolved `NOT_EXPOSED`/`NOT_FOUND` state remains;
- evidence snapshot is immutable and traceable.

Only after these checks may the existing promotion authority proceed.

## Observability Boundary
The aggregator explicitly models the distinction between **execution state** and **observation state**. A connector/API that returns no workflow record does not, by itself, prove `NOT_FOUND`. The collector must classify the result as `NOT_EXPOSED` when its query surface is known to be incomplete or filtered.

This prevents the current ASF-Core contract-check ambiguity from being misclassified in future promotion decisions.

## Recovery and Retry
Collectors may retry transient retrieval failures within bounded limits. Retries MUST NOT create synthetic evidence. A failed collector operation is recorded as collector diagnostics and may result in `NOT_EXPOSED` when execution cannot be authoritatively determined.

Recovery/resume is evidence-producing: a resumed workflow must be correlated to its actual run ID, attempt, and exact commit SHA.

## Security / Governance
- Read-only evidence collection is preferred.
- No secret values are stored in evidence.
- No evidence may be fabricated, edited in place, or detached from its source.
- Production Orchestrator remains the sole promotion/merge authority.
- The aggregator cannot merge PRs, write to `main`, or bypass required gates.
- Human authorization remains required for irreversible or security/data-critical exceptions.

## Acceptance Criteria
The implementation is ready only when contract/integration tests prove that the aggregator can:

1. correlate successful evidence to an exact SHA;
2. correlate failed and pending runs;
3. distinguish `NOT_FOUND` from `NOT_EXPOSED`;
4. correlate workflow, event, run, job, artifact, and check evidence;
5. reject stale-SHA evidence;
6. fail closed when a required gate is unresolved;
7. provide a deterministic promotion snapshot to the Production Orchestrator;
8. preserve immutable evidence history across retries and recovery.

## Relationship to ASF-MOC v9.0
This capability operationalizes the ASF-MOC evidence-first and exact-head promotion requirements while preserving factory/product separation and centralized Production Orchestrator authority.
