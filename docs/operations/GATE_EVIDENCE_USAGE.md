# Gate Evidence Aggregator Operational Usage

The Gate Evidence Aggregator is fail-closed. A promotion decision is `ALLOW` only when every required gate for the exact candidate commit has `SUCCESS` evidence.

## Normal flow

1. Identify the candidate repository, branch, and exact 40-character commit SHA.
2. Collect workflow-run and check evidence for that SHA.
3. Correlate run/job/artifact/check identifiers and branch provenance.
4. Store evidence append-only; duplicate evidence IDs are rejected.
5. Evaluate the required-gate matrix.
6. Pass the resulting promotion decision to the Production Orchestrator.

## Evidence states

- `SUCCESS`: observed successful evidence.
- `FAILURE`: observed failed/cancelled/timed-out evidence.
- `PENDING`: evidence exists but execution is not complete.
- `NOT_FOUND`: the requested evidence is absent.
- `NOT_EXPOSED`: the source exists conceptually but the current observation boundary cannot expose it.

`NOT_EXPOSED` is never upgraded to `SUCCESS`.

## Blocking conditions

Promotion is blocked for failure, pending, missing or hidden evidence, empty gate input, stale SHA, or wrong branch. Recovery/retry requires recollection for the exact candidate SHA before reevaluation.

## Normalized output

The normalized gate surface contains: `commit_sha`, `workflow`, `event`, `run_id`, `checks`, `jobs`, `artifacts`, `conclusion`, `timestamp`, and `decision`.

## Governance

ASF-Core changes remain on the development branch. Main is never written directly. Promotion remains the responsibility of the Production Orchestrator and requires complete observable evidence.
