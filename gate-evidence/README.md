# Gate Evidence Aggregator Runtime

Reusable ASF-Core runtime: collectors -> exact-head correlation -> append-only evidence store -> fail-closed gate matrix -> Promotion Decision -> Production Orchestrator.

Required gate states: SUCCESS, FAILURE, PENDING, NOT_FOUND, NOT_EXPOSED. Only all-required-SUCCESS can produce ALLOW.
