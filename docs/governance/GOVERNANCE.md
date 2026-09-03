# ASF-Core Governance

## Authority
GitHub is the source of truth. The Production Orchestrator is the sole promotion and merge authority.

## Change Path
Normal changes follow Issue/Task → Branch → Commit → PR → CI → Evidence → Production Orchestrator → Merge → Release/Monitoring/Recovery.

## Branch Protection
Development changes must not write directly to `main`. Foundation work remains on the approved existing branch and PR.

## Evidence Gate
Completion claims require exact-head evidence. Mandatory validation failures block promotion. Evidence is append-only and traceable to commits, workflows, and artifacts.

## Scope
ASF-Core owns reusable factory capabilities. Product-specific implementation remains in product repositories and adapter boundaries.

## Human Escalation
Human authorization is required for irreversible, security-critical, data-critical, or otherwise explicitly protected decisions.
