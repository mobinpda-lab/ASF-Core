# NIRA Standard v2 Alignment Audit

## Purpose

Align NIRA implementation with:

- NIRA Autonomous Software Factory Operating Standard v2.0
- NIRA_FACTORY_CONTROL_PLANE_v1

## Alignment Scope

- Governance
- Project State
- Roadmap Queue
- Decision Records
- Worker Lifecycle
- Evidence Model
- Promotion Controls
- Recovery Flow

## Required Controls

### Evidence First
No implementation is complete without reconstructible GitHub evidence.

### Promotion Separation
Worker execution, validation, and promotion remain separate authorities.

### State Management
PROJECT_STATE and derived documents must reflect GitHub state and never bypass normal promotion.

### Queue Contract
Tasks must include:

- Goal
- Priority
- Dependencies
- Worker
- Lease
- Fence
- Acceptance Criteria
- Evidence Requirements

## Remaining Alignment Work

- Validate workflow references against v2 standard.
- Validate evidence collection paths.
- Validate recovery and retry policies.
- Validate L10 readiness criteria.

## Completion Rule

Alignment is complete only after CI, security validation, and promotion evidence are produced through the normal NIRA path.
