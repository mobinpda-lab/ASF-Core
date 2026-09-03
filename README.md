# ASF-Core

Autonomous Software Factory Core Platform based on ASF-MOC v9.0.

ASF-Core is an independent, reusable factory platform for building, validating, releasing, operating, recovering, and improving multiple independent software products.

## Separation
Factory capabilities live in ASF-Core. Product repositories remain independent. Product-specific source code, business logic, UI, domain behavior, and features are not implemented in the factory core.

## Governance
Normal development follows Issue/Task → Branch → Commit → PR → CI → Evidence → Production Orchestrator → Merge → Release/Monitoring/Recovery.

Evidence-first execution and exact-head validation are mandatory. Development changes must not write directly to `main`.

## Initial Product Adapters
- Arvin
- YadNegar
- NCM

See `docs/ASF-MOC-v9.md` and `docs/architecture/ARCHITECTURE.md` for the governing model and architecture boundary.
