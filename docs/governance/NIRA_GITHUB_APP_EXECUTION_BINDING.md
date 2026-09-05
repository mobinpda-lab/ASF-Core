# NIRA GitHub App Execution Binding

Status: FAIL-CLOSED / PROVISIONING REQUIRED
Authority: GitHub repository state + registered-client configuration

## Objective
Provide the only approved credential path for real NIRA cross-repository execution. NIRA must use an auditable GitHub App identity, never a personal access token.

## Identity model
- Credential type: GitHub App installation token.
- App identity: dedicated NIRA execution App; App ID is provisioned externally and recorded only as non-secret metadata.
- Installation: organization/account installation restricted to the registered NIRA client repositories.
- Token source: GitHub Actions secret material containing the App ID and private key; the private key is never committed to Git.
- Token lifetime: short-lived installation token generated at worker runtime; never persist the token as repository data.
- Rotation: rotate/revoke the App private key and/or installation authorization without changing NIRA source code.
- Audit: GitHub App identity + Actions run ID + worker ID + lease ID + client repository + exact HEAD are recorded in evidence.

## Minimum repository permissions
The App must receive only the repository permissions required by the execution contract:

| Permission | Access | Purpose |
|---|---|---|
| Metadata | Read | repository identity/discovery |
| Contents | Read/Write | exact HEAD validation, worker branch, bounded commit |
| Issues | Read/Write | issue intake/queue/lease markers where applicable |
| Pull requests | Read/Write | create/update the worker PR and observe PR state |
| Actions | Read | observe CI runs/jobs/artifacts |
| Security events | Read | observe security results where supported |

The App must NOT receive repository administration, Actions write/dispatch authority, secrets administration, ruleset administration, or merge/promotion authority unless a separately approved future policy explicitly requires it.

## Repository scope
The installation must be limited to:
- `mobinpda-lab/ASF-Core`
- `mobinpda-lab/Arvin-clean`
- `mobinpda-lab/YadNegar`
- `mobinpda-lab/NetworkCenterMonitor`

No other repository is required for the first proof cycle. Client repositories remain independent products; NIRA remains the factory platform.

## Required secret interface
Secrets are configured outside source control. Recommended names:
- `NIRA_GITHUB_APP_ID` — non-secret numeric App ID may alternatively be repository/org configuration metadata.
- `NIRA_GITHUB_APP_PRIVATE_KEY` — secret PEM private key.

The worker must generate a short-lived installation token at runtime using the App identity. No PAT is permitted.

## Provisioning verification checklist
Before enabling mutation, an operator must verify all of the following from GitHub:
1. `APP_ID` identifies the dedicated NIRA App.
2. `INSTALLATION_SCOPE` contains only the four registered repositories above.
3. `PERMISSION_SCOPE` matches the minimum table and has no merge/admin authority.
4. `SECRET_SOURCE` is GitHub Actions encrypted secret storage; no private key exists in Git history.
5. `TOKEN_LIFETIME` is the GitHub App installation-token lifetime and is not persisted.
6. The App can read exact client `main` HEAD.
7. The App can create a dedicated worker branch and bounded commit.
8. The App can create a client PR.
9. The App cannot directly merge/promote to `main`.
10. All operations are attributable to the App installation identity and Actions run.

## Fail-closed enforcement
If App ID, private key, installation access, permission scope, token generation, repository scope, or exact client HEAD validation cannot be independently verified, the worker must stop before client mutation.

Missing credentials are an expected BLOCKED state, not a success condition.

## First real execution
Target: `mobinpda-lab/Arvin-clean` as proof target only.

Required immutable evidence chain:
`ISSUE_ID → INTAKE_ID → QUEUE_ID → LEASE_ID → WORKER_ID → APP_INSTALLATION_ID → BRANCH → COMMIT_SHA → PR → CI_RUN → SECURITY_RUN → ARTIFACT → PROVENANCE → EVIDENCE_ID`

Worker execution must not import or execute Arvin product logic as NIRA factory logic. The worker may modify only the bounded client task selected by NIRA.

## Promotion boundary
Worker identity has no merge authority. Promotion authorization is a separate NIRA gate and is allowed only after independent evidence collection validates the exact commit, CI/security results, provenance, and policy gates.

## Current verified state
As of this branch revision, the required external App installation and credential binding are NOT verified through the available GitHub interface. Therefore no real client mutation is authorized and no L10 claim is valid.
