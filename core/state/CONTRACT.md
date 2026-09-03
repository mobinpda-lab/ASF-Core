# State Contract

## Project State
Project state describes the aggregate factory lifecycle for an independent product connection.

## Task State
Task state records admission, queueing, execution, validation, completion, failure, cancellation, and recovery requirements.

## Lifecycle State
Lifecycle state records the authoritative stage and gate progression from intake through release, monitoring, recovery, and resume.

## Recovery State
Recovery state records failure cause, last known good revision/evidence, retry policy, ownership, and resume eligibility.

## Invariants
State transitions are explicit, validated, and backed by evidence. Product business state is not owned by ASF-Core.
