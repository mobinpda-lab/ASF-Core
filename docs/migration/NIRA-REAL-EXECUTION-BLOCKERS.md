# NIRA Real Execution Blockers

## Purpose
This document records only infrastructure prerequisites that cannot be safely fabricated by repository code.

## Current blocker
The cross-repository worker requires a least-privilege GitHub credential or GitHub App installation capable of reading and mutating registered client repositories. The worker intentionally fails closed when `NIRA_CROSS_REPO_TOKEN` is absent.

## Required capability
The credential must be scoped to registered client repositories and permit only the operations required by the NIRA execution contract: read exact HEAD, create/update a dedicated worker branch, write the authorized change, create a pull request, and observe CI/security/artifact results. It must not grant arbitrary administrative authority or permit direct promotion to `main`.

## Proof required after provisioning
1. NIRA dispatches a real client task.
2. Lease and fence are bound to the exact client HEAD.
3. Worker validates the credential and exact HEAD.
4. Worker creates only the authorized client branch.
5. Worker performs a real bounded client change.
6. Worker creates a client commit and PR.
7. Client CI/security runs are linked to the exact commit.
8. Independent evidence collector records workflow/run/check/artifact provenance.
9. Promotion authority validates the immutable evidence chain.
10. Failure injection demonstrates detection, recovery, refencing and evidence recording.

## Fail-closed rule
Until all ten conditions are reconstructible from GitHub evidence, NIRA must remain below L10 and must not claim a real production factory cycle.
