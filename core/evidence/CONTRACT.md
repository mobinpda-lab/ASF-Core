# Evidence Contract

## Immutable Evidence
Evidence is append-only lifecycle output. Existing records are not silently rewritten; corrections create a new linked record.

## SHA References
Evidence identifies repository, ref, commit SHA, and relevant object or artifact identifiers needed to reproduce the claimed state.

## Workflow and Artifact Records
Workflow run identifiers, job/check results, artifact identifiers, and release references are recorded when they exist. Claims without corresponding evidence are not completion evidence.

## Integrity
Evidence must not contain secrets or unnecessary sensitive data. Evidence is associated with the task and lifecycle event that produced it.
