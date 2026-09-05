# NIRA Real Execution Blockers
## Purpose
This document records only infrastructure prerequisites that cannot be safely fabricated by repository code.
## Current blocker
The cross-repository worker requires a least-privilege GitHub App installation capable of reading and mutating the registered client repositories. NIRA must fail closed unless the required GitHub App credentials are available through the configured secret source.
## GitHub App requirements
The execution identity must be a dedicated GitHub App installation, not a PAT, personal token, shared credential, or broad organization credential. Required registered repositories are `mobinpda-lab/ASF-Core`, `mobinpda-lab/Arvin-clean`, `mobinpda-lab/YadNegar`, and `mobinpda-lab/NetworkCenterMonitor`.
Minimum required permissions are Metadata: read, Contents: write, Issues: write, Pull requests: write, Actions: read, and Security events: read. No merge/promotion authority, administration, Actions write/dispatch, secrets administration, or ruleset administration is required for worker execution.
Required secret material is `NIRA_GITHUB_APP_ID` and `NIRA_GITHUB_APP_PRIVATE_KEY`. The private key must never be committed to Git. Installation scope, permission scope, token generation, token lifetime, and attributable audit identity must be independently verifiable before execution.
## Required capability
The App installation must permit only the operations required by the NIRA execution contract: read exact client HEAD, create/update a dedicated worker branch, write the authorized bounded change, create a pull request, and observe CI/security/artifact results. It must not grant arbitrary administrative authority or permit direct promotion to `main`.
## Proof required after provisioning
1. NIRA dispatches a real client task.
2. Lease and fence are bound to the exact client HEAD.
3. Worker authenticates with the GitHub App installation and validates exact HEAD.
4. Worker creates only the authorized client branch.
5. Worker performs a real bounded client change.
6. Worker creates a client commit and PR.
7. Client CI/security runs are linked to the exact commit.
8. Independent evidence collector records workflow/run/check/artifact provenance.
9. Promotion authority validates the immutable evidence chain.
10. Failure injection demonstrates detection, recovery, refencing and evidence recording.
## Fail-closed rule
Until all ten conditions are reconstructible from GitHub evidence, NIRA must remain below L10 and must not claim a real production factory cycle.
