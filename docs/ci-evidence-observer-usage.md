# CI Evidence Observer usage contract

`EvidenceObserver.observe(repository, commit_sha, source)` accepts authoritative adapter output and returns an immutable `EvidenceRecord`. Adapters are responsible for obtaining workflow runs, check runs, jobs, artifacts, statuses, conclusions and timestamps. The observer validates identity and classifies visibility without inventing missing data.

Required promotion behavior:

1. Exact SHA and repository identity must match.
2. `NOT_EXPOSED`, `PENDING`, `FAILURE`, `NOT_FOUND`, and unknown values block promotion.
3. A successful observation is not itself authority to merge; the Gate Evidence Aggregator and Production Orchestrator remain authoritative.
4. Required artifacts are an explicit gate, and their absence blocks when that gate is required.
