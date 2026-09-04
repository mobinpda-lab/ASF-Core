# CI Evidence Observer → Gate Evidence Aggregator

The observer produces a normalized exact-head evidence record. The gate integration converts that record into explicit promotion gates with status, evidence, confidence, and decision.

Promotion is fail-closed: `NOT_EXPOSED`, `PENDING`, `FAILURE`, `NOT_FOUND`, or any unknown state cannot produce an `ALLOW` decision. Required artifact gates explicitly block when artifacts are absent.

Self-observation must correlate repository identity and exact commit SHA across workflow runs, checks, jobs, artifacts, and statuses. Stale or cross-repository observations are rejected.
