# Gate Evidence Aggregator Runtime

Reusable ASF-Core runtime: collectors -> exact-head correlation -> append-only evidence store -> fail-closed gate matrix -> Promotion Decision -> Production Orchestrator.

Gate states: SUCCESS, FAILURE, PENDING, NOT_FOUND, NOT_EXPOSED. ALLOW requires all required gates to be SUCCESS.
