# NIRA L10 Activation Wave — Issue #171

## Purpose

This runbook is the controlled final activation path for proving NIRA as a real autonomous software factory. It does not claim L10 completion by documentation alone.

## Registered proof target

- Client: `mobinpda-lab/Arvin-clean`
- Client issue: `#863`
- NIRA control issue: `#171`
- Client main observed when the proof task was created: `7e35f66498327b7382d5c99be22d256c3d843d3e`

The client `main` SHA is never trusted from historical data. The activation workflow reads the live SHA immediately before dispatch and passes that exact value to the worker. Any HEAD drift must fail closed.

## Required execution chain

`ISSUE → INTAKE → QUEUE → LEASE → WORKER → FENCING → CLIENT BRANCH → CLIENT COMMIT → CLIENT PR → CI → SECURITY → ARTIFACT → INDEPENDENT EVIDENCE → PROMOTION AUTHORIZATION → RELEASE/POSTCONDITION`

## Negative-path proof

The L10 claim requires independently reconstructible evidence for:

1. stale lease / fencing rejection;
2. duplicate worker rejection;
3. timeout and bounded requeue/recovery;
4. client HEAD drift rejection;
5. CI or build failure and recovery;
6. missing/invalid evidence rejection.

All negative paths must remain fail-closed. A worker's own claim is not sufficient evidence.

## Credential boundary

The real worker requires the NIRA GitHub App runtime credentials already referenced by the worker contract. No PAT, personal credential, private key, or secret value may be committed to this repository. If runtime credentials are unavailable, the activation must fail closed rather than bypassing the authority model.

## Activation mechanism

`.github/workflows/nira-l10-activation.yml` is a controlled dispatch entrypoint. It:

1. validates the registered client allowlist;
2. reads the client's current `main` SHA;
3. validates the real lease and positive fencing token supplied by NIRA;
4. dispatches the existing `nira-cross-repo-worker.yml` on `main`;
5. records the exact activation inputs as an Actions artifact.

It does not create a fake lease, invent a fence token, or grant merge authority.

## Definition of Done

L10 may change from `UNVERIFIED` to `VERIFIED` only after GitHub provides independently observable evidence that the real client task completed the positive path, the required negative paths recovered correctly, promotion/release postconditions were verified, and the complete evidence chain is reconstructible from immutable GitHub identifiers.
