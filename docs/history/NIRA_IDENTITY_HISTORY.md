# NIRA Identity History — Legacy Naming Record

**Status:** Historical record only  
**Authority:** None  
**Active factory identity:** NIRA

## Purpose

This document is the single intentional historical record of the factory's former names. The legacy identifiers below are retained solely so old commits, issues, pull requests, workflow runs, external links, branches, and provenance can be interpreted without creating a second or competing authority.

## Former identifiers

- `ASF-Core` — former repository/factory identifier used before NIRA became the canonical identity.
- `ASF-MOC` — earlier operating-model identifier.
- `ASF_MOC_v9_GITHUB_AUTONOMOUS_SOFTWARE_FACTORY_CONTINUOUS_COMPANY_OS` — historical document identifier associated with the earlier operating model.
- `asf-core` / `asf_moc` — historical lowercase/slug variants where they occurred in automation or references.

## Transition rule

Effective from the NIRA canonicalization change, none of the identifiers above is an active factory name, repository authority, queue authority, worker authority, promotion authority, workflow authority, registry identity, or client identity.

The Git repository is renamed to **NIRA** as the GitHub-level identity change. The active source tree is NIRA-only. Git history, immutable commit messages, already-created issue/PR records, workflow-run history, historical branch names, and provider-side historical URLs are provenance and are not rewritten merely to conceal history.

## Immutable commit provenance

The following historical commits contain legacy factory naming in immutable commit metadata/messages and therefore remain provenance only:

- `b73d6fb3b979c1ec17ab8e235c632e6a166ed6ab`
- `a5c0bd9b106ad1b7922bdba383a4874e746cdf93`
- `692dd65501e93f39c7b1dcf25651fb9a61c566f3`
- `9afbad7264b84619bb307d34e19eb2c0bb6d0398`
- `ba70ef1b40b21369f9178466885a7e0787a94e65` (transition documentation commit)

Rewriting these commits would change descendant SHAs and invalidate existing provenance, PR lineage, workflow evidence, and historical references. They are therefore intentionally not rewritten.

## Historical pull-request provenance

Legacy naming occurred in the historical PR records including, among others: #1, #2, #3, #4, #5, #6, #8, #9, #12, #13, #14, #15, #16, #17, #18, #21, #26, #28, #33, #40, and #44. These records are historical GitHub provenance, not active authority. Their old wording must not be copied into new implementation, workflows, configuration, or documentation.

## Historical branch provenance

A former branch named `docs/asf-moc-independent-architecture-20260904` remains a historical Git reference. It has no active PR and no authority. It should be deleted from the GitHub branch list as an external cleanup step so no legacy-named active branch remains.

## Repository metadata cleanup

The repository itself is already named **NIRA**. The GitHub repository description must also be NIRA-only; any description containing a former identifier is stale metadata and must be replaced manually if the connected GitHub interface cannot mutate repository administration metadata.

## Historical provenance

The factory evolved through an earlier operating model and repository identity before being separated into an independent NIRA control plane. Proven lessons from that period include exact-head/base validation, fail-closed promotion, independent evidence, bounded recovery, queue/lease ownership, worker fencing, and separation of factory authority from product repositories.

## Non-interference policy

Historical identifiers must never be used by new code, new workflows, new documentation, active configuration, registry entries, client bindings, tests, or runtime authority checks. If an old reference is needed for archaeology, it must point to this document rather than reintroducing the old identifier into active implementation.

## External GitHub configuration that must remain NIRA-only

- Repository name: `NIRA`.
- Repository description: NIRA-only wording.
- Active branch names: no former factory identifier.
- Active workflow names/artifacts: NIRA-only.
- GitHub Actions secrets: use `NIRA_GITHUB_APP_ID` and `NIRA_GITHUB_APP_PRIVATE_KEY`; remove obsolete legacy-named secrets after confirming the NIRA credentials are provisioned.
- GitHub App installation scope: NIRA + registered client repositories only; the App display/name should not introduce the former factory identity.

## Integrity rule

This file is intentionally the **only active-tree document permitted to contain the former factory names**. A conformance check must fail if any other active-tree file introduces them again.
