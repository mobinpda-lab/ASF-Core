# NIRA Identity History — Legacy Naming Record

**Status:** Historical record only  
**Authority:** None  
**Active factory identity:** NIRA

## Purpose

This document is the single intentional historical record of the factory's former names. The legacy identifiers below are retained solely so old commits, issues, pull requests, workflow runs, external links, and provenance can be interpreted without creating a second or competing authority.

## Former identifiers

- `ASF-Core` — former repository/factory identifier used before NIRA became the canonical identity.
- `ASF-MOC` — earlier operating-model identifier.
- `ASF_MOC_v9_GITHUB_AUTONOMOUS_SOFTWARE_FACTORY_CONTINUOUS_COMPANY_OS` — historical document identifier associated with the earlier operating model.
- `asf-core` / `asf_moc` — historical lowercase/slug variants where they occurred in automation or references.

## Transition rule

Effective from the NIRA canonicalization change, none of the identifiers above is an active factory name, repository authority, queue authority, worker authority, promotion authority, workflow authority, registry identity, or client identity.

The Git repository is renamed to **NIRA** as the final GitHub-level identity change. Git history, immutable commit messages, already-created issue/PR records, workflow-run history, and provider-side historical URLs are provenance and are not rewritten merely to conceal history.

## Historical provenance

The factory evolved through an earlier operating model and repository identity before being separated into an independent NIRA control plane. Proven lessons from that period include exact-head/base validation, fail-closed promotion, independent evidence, bounded recovery, queue/lease ownership, worker fencing, and separation of factory authority from product repositories.

## Non-interference policy

Historical identifiers must never be used by new code, new workflows, new documentation, active configuration, registry entries, client bindings, tests, or runtime authority checks. If an old reference is needed for archaeology, it must point to this document rather than reintroducing the old identifier into active implementation.

## Integrity rule

This file is intentionally the **only active-tree document permitted to contain the former factory names**. A conformance check must fail if any other active-tree file introduces them again.
