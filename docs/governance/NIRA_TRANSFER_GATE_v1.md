# NIRA Transfer Gate v1

**Purpose:** Prevent premature declaration of completion during ASF-Core → NIRA and Arvin Factory → NIRA migration.

## Gate states
- `DOCUMENTARY_COMPLETE`: identity, audit, destination map and migration law exist.
- `CONTRACT_COMPLETE`: canonical NIRA contracts and client boundary are defined and tested.
- `OPERATIONALLY_COMPLETE`: NIRA executes a registered client lifecycle independently.
- `CLEANUP_COMPLETE`: superseded client-side factory-core implementations are removed through governed PRs.
- `L10_VERIFIED`: independent end-to-end evidence proves the complete lifecycle, including failure/fencing/recovery and promotion/release.

## Current state
`CONTRACT_COMPLETE` is the highest state that may be claimed from repository evidence at this point. `OPERATIONALLY_COMPLETE`, `CLEANUP_COMPLETE`, and `L10_VERIFIED` are not yet proven.

## Mandatory promotion rule
No migration cleanup PR may remove an Arvin factory workflow until:
1. NIRA equivalent exists and is executable.
2. Arvin adapter is connected.
3. Conformance tests pass.
4. A real Arvin task completes through NIRA.
5. Failure/fencing/recovery evidence is independently reconstructible.
6. Promotion/release postconditions are independently observed.
7. The exact legacy artifact is mapped to its NIRA replacement.
8. The cleanup occurs in a separate Arvin PR.

## Evidence principle
Documentation, planned workflows, or worker self-reports are not sufficient evidence of operational completion.

## Safety
No direct `main` mutation. No destructive cleanup before validation. Historical ASF-Core/ASF-MOC identifiers and Arvin provenance remain traceable.
