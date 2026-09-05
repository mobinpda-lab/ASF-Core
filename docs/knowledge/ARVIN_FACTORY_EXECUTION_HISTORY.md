# Arvin Factory Execution History Transferred to NIRA

This is a provenance record, not a claim of NIRA execution.

## Reference client

Repository: `mobinpda-lab/Arvin-clean`
PR: `#659`
Issue: `#658`
Head SHA: `ac827a8336274a6db18470b80d60ea812d3fc700`
Base SHA: `9a773b7898ff63276ad6a214009b163f904e8923`
Head branch: `nira/issue-658-calendar-target-label`

## Verified workflow evidence previously observed

- Arvin Build workflow run: `33960512193` — SUCCESS
- Arvin Build Quality job: `101291475286` — SUCCESS
- Android V2 audit: SUCCESS
- APK release job: `101291842964` — SUCCESS
- APK debug job: `101291842965` — SUCCESS
- Arvin Device Smoke workflow run: `33960512211` — SUCCESS
- Device jobs: `101291481427`, `101291481520` — SUCCESS
- ARVIN Production Loop run: `33960512206` — SUCCESS
- ARVIN Orchestrator run: `33960512190` — SUCCESS
- Arvin Parallel Wave run: `33960512194` — SKIPPED

## Artifact provenance observed

Release APK:
- artifact ID: `9967894829`
- digest: `sha256:f919660c59aae944d84ddcd49fd2f2644965258e8968b38f72fa1a92e5706913`

Debug APK:
- artifact ID: `9967897919`
- digest: `sha256:a1ea17d90cdc36f8dfb26195a3b3264de31a382b6c495f246126102483a60c18`

## Important negative evidence

The combined GitHub commit status for the exact PR head was observed with zero status entries. Therefore the commit-status chain was not proven.

A dedicated security workflow was not present in the verified Arvin build workflow. Therefore the required security gate evidence for PR #659 remained incomplete.

Full build provenance/attestation linking artifact, workflow, commit, triggering event and digest was not independently reconstructed. This remains an explicit NIRA gap.

## Earlier failure/recovery history

The same PR initially failed on the calendar integration regression test. The failure was:
- test: `calendar_integration_settings_page_test.dart`
- symptom: `Bad state: No element`

Subsequent test-only repair commits included:
- `33bd49...`
- `c79efd...`
- `809e64...`

The `809e64...` repair introduced analyzer dead-code warnings and was followed by another repair. Final current head became `ac827a...` with the test structure restored.

This history is useful to NIRA as a real failure/recovery learning record, but it must not be represented as NIRA recovery execution.

## NIRA interpretation

The record establishes that the Arvin client has a meaningful autonomous-workflow history. NIRA must independently reproduce the reusable control-plane behavior and collect its own evidence. The historical Arvin evidence is source material and regression knowledge, not substitute L10 evidence.
