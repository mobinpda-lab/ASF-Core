# Queue Contract

## Intake
Queue intake accepts normalized tasks with identity, scope, priority, dependencies, and lifecycle metadata.

## Priority
Priority is explicit, bounded, and deterministic. Dependency constraints override priority when prerequisites are incomplete.

## Lease
A worker receives a renewable, time-bounded lease. Expired leases become recoverable and must not permit concurrent ownership.

## State Transition
Allowed transitions are validated and auditable. Invalid transitions are rejected rather than coerced.
