# Gate Evidence Aggregator Runtime

Boundary: Evidence Matrix -> Gate Evaluator -> Promotion Decision. ASF-Core owns collection, exact-SHA correlation, append-only evidence, fail-closed evaluation, and decision production. Product repositories remain isolated.

Collectors cover workflow runs, check runs, jobs, and artifacts. Correlation keys cover repository, exact commit SHA, workflow, event, run, job, artifact, and check identifiers.

Statuses: SUCCESS, FAILURE, PENDING, NOT_FOUND, NOT_EXPOSED. ALLOW requires every required gate to be SUCCESS; otherwise BLOCK. Empty required-gate input blocks.

Evidence storage is append-only; duplicate evidence IDs are rejected. Existing records are not mutated. Recovery requires fresh evidence collection before promotion.
