# Gate Evidence Collector Contract

The collector is a read-only boundary over supported GitHub evidence sources.

## Operations
- discover_workflows(commit_sha)
- discover_checks(commit_sha)
- discover_jobs(run_id)
- discover_artifacts(run_id)

## Rules
- Exact `commit_sha` is mandatory for commit-scoped discovery.
- Every returned observation retains source, event type, workflow identity, and run identity when available.
- A filtered or unsupported observation surface MUST yield `NOT_EXPOSED`, never synthetic absence.
- Authoritative absence yields `NOT_FOUND` only when the source boundary is known to be complete for the requested query.
- Collector retries are bounded and never manufacture evidence.
