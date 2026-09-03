# Gate Evidence Correlator Contract

The correlator converts raw observations into exact-head normalized evidence.

## Required identity
- commit SHA
- workflow ID
- workflow name/path
- event type
- run ID
- job result
- artifact result
- check result

## Rules
- SHA equality is mandatory; stale or unrelated evidence is rejected.
- Workflow name is not a unique identity when workflow ID is available.
- Missing observations remain explicitly unresolved.
- Correlation must preserve provenance and observation timestamps.
