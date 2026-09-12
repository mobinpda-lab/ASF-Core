# NIRA L10 Activation Wave — Issue #171

## Purpose

This runbook defines the controlled L10 proof path for NIRA itself. It does not claim L10 completion by documentation alone and it does not use Arvin or any other external product as the current proof target.

## Current proof target

- Repository: `mobinpda-lab/NIRA`
- Self-completion task family: `SC-01` through `SC-06`
- Parent control issues: `#157` and `#158`

External clients such as Arvin remain deferred until NIRA completes and proves its own self-completion plan. The L10 activation workflow must fail closed if an external repository is supplied while this NIRA-first boundary is active.

The NIRA `main` SHA is never trusted from historical data. The activation workflow reads the live SHA immediately before dispatch and passes that exact value to the worker. Any HEAD drift must fail closed.

## Required execution chain

`ISSUE → INTAKE → QUEUE → LEASE → WORKER → FENCING → NIRA BRANCH → NIRA COMMIT → NIRA PR → CI → SECURITY → ARTIFACT → INDEPENDENT EVIDENCE → PROMOTION AUTHORIZATION → MAIN POSTCONDITION`

## Negative-path proof

The L10 claim requires independently reconstructible evidence for:

1. stale lease / fencing rejection;
2. duplicate worker rejection;
3. timeout and bounded requeue/recovery;
4. NIRA HEAD drift rejection;
5. CI or conformance failure and recovery;
6. missing or invalid evidence rejection;
7. external-client activation rejection before NIRA self-certification.

All negative paths must remain fail-closed. A worker's own claim is not sufficient evidence.

## Credential boundary

The real worker requires the NIRA GitHub App runtime credentials and at least one configured AI provider supported by the provider router. No PAT, personal credential, private key, or secret value may be committed to this repository. If runtime credentials or provider capacity are unavailable, execution must stop or requeue through the bounded recovery policy rather than bypassing authority.

## Activation mechanism

`.github/workflows/nira-l10-activation.yml` is a controlled self-proof dispatch entrypoint. It:

1. rejects any target other than `mobinpda-lab/NIRA` while the NIRA-first boundary is active;
2. reads the current NIRA `main` SHA;
3. validates the real lease and positive fencing token supplied by NIRA;
4. dispatches the existing `nira-cross-repo-worker.yml` against NIRA itself;
5. records the exact activation inputs as an Actions artifact.

It does not create a fake lease, invent a fence token, grant merge authority, or use an external client to substitute for NIRA self-proof.

## Definition of Done

L10 may change from `UNVERIFIED` to `VERIFIED` only after GitHub provides independently observable evidence that NIRA completed the positive self-proof path, the required negative paths recovered correctly, promotion and exact-main postconditions were verified, and the complete evidence chain is reconstructible from immutable GitHub identifiers.

Only after the NIRA self-completion plan is certified may a later governance change explicitly reopen external-client L10 activation for Arvin or another registered product.
