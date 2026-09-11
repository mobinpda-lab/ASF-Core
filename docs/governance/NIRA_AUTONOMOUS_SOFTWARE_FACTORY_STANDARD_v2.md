# NIRA Autonomous Software Factory Operating Standard v2.0

## Purpose

NIRA is an autonomous software factory and GitHub control plane. This document is the operational governing standard for continuous software production, self-improvement, evidence-based execution, and safe automation.

## Authority Model

- GitHub is the operational source of truth.
- Architecture authority remains `NIRA_FACTORY_CONTROL_PLANE_v1`.
- This standard defines operating behavior, lifecycle rules, and alignment requirements.

## Core Lifecycle

DISCOVER → ANALYZE → RESEARCH → PRIORITIZE → PLAN → ARCHITECT → BUILD → TEST → SECURE → REVIEW → MERGE → RELEASE → MONITOR → LEARN → OPTIMIZE → REPEAT

## Evidence First Operation

Automation is only real when execution evidence exists.

Valid evidence includes:

- Commit SHA
- Workflow Run
- Test Results
- Build Results
- Security Results
- Artifact Evidence
- Release Evidence
- Worker Provenance
- Lease and Fence Provenance

No Evidence → No Promotion.

## Task Lifecycle

DISCOVERED → QUEUED → LEASED → RUNNING → VALIDATING → EVIDENCE_READY → PROMOTABLE → PROMOTED → RELEASED → MONITORED

## Worker Governance

Workers must have:

- Identity
- Scope
- Permission boundary
- Lease
- Fence token
- Evidence responsibility

Worker, Validator, and Promoter are separate responsibilities.

## Self-Dogfooding

NIRA must operate itself through the same factory process used for registered clients.

NIRA Factory → NIRA Self Client → NIRA Factory

No special bypass path is allowed.

## Quality and Security

Required gates may include:

- Formatting
- Static Analysis
- Unit Tests
- Integration Tests
- Security Checks
- Build Validation
- Product Validation

Security and quality controls cannot be bypassed for speed.

## Recovery

Failure handling:

Detect → Classify → Root Cause → Repair Task → Patch → Test → Verify → Resume

Retries must be policy controlled.

## Continuous Improvement

Release is not the end of operation.

Feedback → Analysis → Learning → Task → Implementation → Validation → Improvement

## L10 Definition

L10 means a real autonomous software factory with reconstructible evidence of complete lifecycle execution, including safe failure handling and recovery.

Existence of workflows, scripts, or documentation alone does not prove automation.

## Alignment Rule

All NIRA workflows, workers, queue systems, evidence systems, promotion systems, and documentation must remain aligned with this standard and the canonical architecture contract.
