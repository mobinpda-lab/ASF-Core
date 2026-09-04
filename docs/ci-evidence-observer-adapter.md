# Authoritative adapter requirements

An adapter feeding `EvidenceObserver` must expose authoritative workflow runs, check runs, jobs, artifacts, and commit statuses where the provider permits. Each item should retain provider identity, repository, exact commit/head SHA, event type, run/job/artifact identity, conclusion/state, and timestamps. If access is unavailable, the adapter must set `accessible=false` rather than returning fabricated empty success evidence.
