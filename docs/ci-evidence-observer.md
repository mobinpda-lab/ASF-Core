# CI Evidence Observer

The CI Evidence Observer is a reusable ASF-Core capability for exact-head CI/CD evidence observation. It consumes authoritative observations keyed by repository and commit SHA and emits a normalized immutable evidence record.

## Visibility

- `SUCCESS`: observed evidence is complete enough for the supplied observation set and contains no failure/pending conclusion.
- `FAILURE`: an authoritative run/check/job reports failure or equivalent terminal failure.
- `PENDING`: authoritative execution is visible but not terminal.
- `NOT_FOUND`: an authoritative source was queried and confirms no evidence exists.
- `NOT_EXPOSED`: evidence may exist, but the observer cannot access the authoritative source.

Unknown or `NOT_EXPOSED` evidence is fail-closed for promotion. `NOT_FOUND` is not success; it must be interpreted by the gate policy.

## Exact-SHA correlation

Every observed item is correlated against repository identity and the requested 40-character commit SHA. Mismatched repository or stale SHA observations are rejected rather than downgraded to success. Workflow/check/job conclusions are preserved by the adapter for downstream gate evaluation.

## Promotion safety

The observer does not create CI evidence, trigger workflows merely to manufacture evidence, or infer success from an empty status list. The Gate Evidence Aggregator should consume the normalized record and produce `Gate / Status / Evidence / Decision`. Promotion remains blocked unless every required gate is `SUCCESS` and the Production Orchestrator authorizes promotion.

## Confidence and limitations

Confidence is highest when workflow run, check run, job, artifact, and commit-status observations all identify the same repository and exact SHA and provide terminal success conclusions. Missing or inaccessible evidence lowers confidence and must never be silently converted into success.
