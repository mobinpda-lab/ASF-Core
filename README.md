# ASF-Core

Autonomous Software Factory Core Platform based on ASF-MOC v9.0.

ASF-Core is an independent, reusable factory platform for building, validating, releasing, operating, recovering, and improving multiple independent software products.

## Multi-Product Architecture
ASF-Core provides reusable orchestration, queue/lease semantics, worker execution contracts, evidence, lifecycle state, validation, guarded promotion, release, monitoring, recovery, and resume capabilities. Product repositories connect through explicit adapters and remain independently buildable and deployable.

Initial adapter targets include Arvin, YadNegar, and NCM. The adapter contract is defined in `adapters/PRODUCT_ADAPTER_CONTRACT.md`.

## Factory / Product Separation
Factory capabilities live in ASF-Core. Product repositories remain independent. Product-specific source code, business logic, UI, domain behavior, storage, and features are not implemented in the factory core.

## Foundation
The Foundation Wave defines core contracts, machine-readable lifecycle schemas, governance/security/operations baselines, CI validation workflows, and contract/integration tests. Schema definitions live under `schemas/`; reusable contracts live under `core/` and `adapters/`.

## Governance
Normal development follows Issue/Task → Branch → Commit → PR → CI → Evidence → Production Orchestrator → Merge → Release/Monitoring/Recovery.

Evidence-first execution and exact-head validation are mandatory. Development changes must not write directly to `main`, and workers/adapters cannot bypass promotion authority.

See `docs/ASF-MOC-v9.md`, `docs/architecture/ARCHITECTURE.md`, `docs/governance/GOVERNANCE.md`, `docs/security/SECURITY.md`, and `docs/operations/OPERATIONS.md` for the governing model.
