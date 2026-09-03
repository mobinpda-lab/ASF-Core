# ASF-Core Observability Layer

## Purpose

The observability layer makes factory execution evidence discoverable, explainable, and promotion-safe. It answers both **what passed** and **what remains unknown, and why**.

## Observation model

`FactoryObservation` records repository, exact commit SHA, gate name, workflow identity, event type, run/check identifiers, job and artifact results, visibility, confidence, timestamp, and an explicit reason.

Visibility is explicit:

- `WORKFLOW_VISIBLE`: workflow evidence is exposed to the observer.
- `WORKFLOW_NOT_VISIBLE`: the workflow may exist, but the observer cannot expose it.
- `CHECK_VISIBLE`: check evidence is exposed.
- `CHECK_NOT_VISIBLE`: check evidence may exist but is not exposed.
- `EVIDENCE_COMPLETE`: all required evidence for the observation is available.
- `EVIDENCE_INCOMPLETE`: required evidence is missing from the observable set.

`NOT_FOUND` and `NOT_EXPOSED` retain different meanings. `NOT_FOUND` is emitted only when the authoritative observer reports no matching evidence. `NOT_EXPOSED` is used when the observation boundary cannot establish the underlying state.

## Confidence

`HIGH` means the execution result is directly observed. `MEDIUM` represents an incomplete but meaningful observation. `LOW` is reserved for unknown or non-authoritative visibility. Confidence never upgrades an unknown state to success.

## Promotion safety

The observability layer builds the promotion matrix only for the exact repository and commit SHA. Missing, hidden, stale, wrong-repository, or incomplete evidence produces a blocking matrix. There is no silent success path.

Flow:

`GitHub observations → FactoryObservation → promotion matrix → Gate Evaluator → Production Orchestrator`

The Production Orchestrator remains the sole promotion/merge authority. ASF-Core development remains branch/commit/PR governed, with no direct main writes.

## Operational interpretation

For every blocked gate, consumers can inspect `status`, `visibility_state`, `confidence`, and `reason` to distinguish an actual failure from an observation limitation. This makes connector visibility limitations explicit rather than misclassifying them as execution failures or successes.
