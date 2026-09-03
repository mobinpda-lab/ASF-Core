# ASF-Core Control Plane

## Boundary
ASF-Core observes product execution and evaluates factory lifecycle state; it does not own product business state. Workers operate within leased scope. Promotion remains delegated to the Production Orchestrator.

## Observe → Evaluate → Decide
GitHub execution observations become normalized FactoryObservation records. The gate matrix evaluates exact repository and commit SHA evidence. The orchestrator decision layer produces ALLOW, BLOCK, WAIT, or RECOVER. Unknown evidence never becomes success.

## Lifecycle
CREATED → QUEUED → RUNNING → VALIDATING → WAITING_EVIDENCE → READY → COMPLETED, with FAILED and RECOVERING branches for failure handling. Every transition records an immutable StateTransition in execution history.

## Decision model
ALLOW requires complete successful evidence and ready dependencies. WAIT represents unresolved dependencies or evidence. BLOCK represents non-recoverable failure or failed gates. RECOVER represents a classified recoverable failure.

## Governance
No control-plane component writes directly to main or bypasses PR governance. Exact-head evidence and the Production Orchestrator are mandatory for promotion.
