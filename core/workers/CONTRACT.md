# Worker Contract

## Execution Lifecycle
A worker follows `leased → running → validating → completed|failed|recovery-required`. Cancellation and lease expiry are explicit terminal/recovery events.

## Validation
Workers must execute declared validation checks and return machine-readable pass/fail outcomes. A worker cannot waive a failed mandatory gate.

## Evidence Output
Each execution emits evidence containing task identity, worker identity, input revision, resulting SHA references, validation results, timestamps, and artifact/workflow references where applicable.

## Restrictions
Workers are bounded executors. They cannot merge, promote, rewrite protected authority state, or expand scope without a new authorized task.
