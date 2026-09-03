# Gate Evidence Aggregator Runtime

Evidence Matrix -> Gate Evaluator -> Promotion Decision -> Production Orchestrator.

Collectors: workflow run, check run, job result, artifact result. Correlation: repository + exact commit SHA + workflow/event/run/job/artifact/check identifiers + branch provenance.

Gate states: SUCCESS, FAILURE, PENDING, NOT_FOUND, NOT_EXPOSED. ALLOW only when all required gates are SUCCESS; every other state, empty input, stale SHA, or wrong branch blocks.

Evidence is append-only and duplicate IDs are rejected. Recovery/retry requires recollection for the exact candidate SHA before promotion.
