# Gate Evidence Aggregator Runtime

## Integration boundary
Evidence Matrix -> Gate Evaluator -> Promotion Decision -> Production Orchestrator.

## Collection and correlation
Collector interfaces cover workflow runs, check runs, jobs, and artifacts. Evidence carries repository, exact commit SHA, workflow/event, run, job, artifact, check, branch, status, and timestamp. Correlation accepts only exact repository+SHA matches.

## Fail-closed evaluation
Required gates are ALLOW only when every gate is SUCCESS. FAILURE, PENDING, NOT_FOUND, NOT_EXPOSED, empty input, stale SHA, or wrong branch context blocks promotion.

## Storage
Evidence is append-only and duplicate evidence IDs are rejected; existing records are never silently rewritten.

## Recovery
After recovery/retry, evidence must be recollected for the exact candidate SHA before a new promotion decision. Secrets are outside the evidence model.
