# Orchestrator Contract

## Authority
The orchestrator is the control-plane authority for task scheduling and lifecycle coordination. Promotion authority is guarded and may only delegate promotion to the Production Orchestrator policy.

## Scheduling
Tasks are admitted only from validated intake, ordered by priority and dependency constraints, and assigned to eligible workers under bounded execution limits.

## Promotion Control
Promotion requires validated gates, exact-head evidence, and an auditable lifecycle record. No orchestrator contract permits direct writes to `main` or bypasses required PR governance.

## Worker Restrictions
Workers execute only leased tasks within declared scope. Workers must not self-promote, alter authority state, bypass gates, or write outside their assigned branch/scope.
