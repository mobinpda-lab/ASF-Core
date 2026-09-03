# ASF-Core Operations

## Lifecycle Operations
Operate through validated task intake, bounded workers, evidence capture, CI gates, Production Orchestrator promotion, release, monitoring, recovery, and resume.

## Monitoring
Monitor workflow outcomes, lifecycle state, release state, worker leases, validation failures, and recovery events. Operational claims must reference current evidence.

## Recovery
On failure, preserve the last known good SHA and evidence, classify the failure, apply bounded retry where safe, and prevent duplicate execution through lease/state controls.

## Resume
Resume only from an authorized recoverable state with required dependencies and gates revalidated.

## Release Safety
Release promotion requires exact-head validation and complete mandatory evidence. Rollback is a governed lifecycle transition, not an ad hoc branch write.
