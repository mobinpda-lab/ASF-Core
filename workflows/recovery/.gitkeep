# ASF-MOC v9.0

## Scope
ASF-MOC v9.0 defines the operating model for an autonomous, evidence-first software factory. ASF-Core is the reusable factory platform; product repositories remain independent product spaces.

## Factory / Product Separation
- ASF-Core contains reusable factory capabilities only.
- Arvin, YadNegar, NCM, and future products remain separate repositories.
- ASF-Core must not import, copy, modify, or own product-specific business logic, UI, domain models, or product features.
- Product-specific integration belongs behind product adapters and explicit contracts.

## Autonomous Software Factory Principles
The governed lifecycle is:
IDEA → PRODUCT DEFINITION → ARCHITECTURE → BOOTSTRAP → TASK DECOMPOSITION → ISSUES → PARALLEL WORKERS → CODE → TEST → AUTO-FIX → DOCS → PR → CI → BUILD → DEVICE TEST → SECURITY GATE → EXACT-HEAD VALIDATION → PRODUCTION ORCHESTRATOR → MERGE → RELEASE → MONITORING → RECOVERY → RESUME.

Workers execute bounded tasks; promotion authority is centralized. No worker or human bypasses required gates.

## Evidence-First Execution
Claims of completion require verifiable evidence. Relevant evidence includes commit SHA, branch, PR, CI/workflow results, test/build artifacts, exact-head validation, release state, monitoring state, and recovery state where applicable. Never claim an operation that has not been directly verified.

## Parallel Product Evolution
Factory evolution and product evolution proceed concurrently. ASF-Core must not block product development while factory capabilities mature, and product repositories must not be absorbed into the factory. Reusable capabilities are promoted into ASF-Core; product-specific behavior remains in product spaces or adapters.

## Governance and Safety
- GitHub is the source of truth for repository state.
- Normal changes follow Issue/Task → Branch → Commit → PR → CI → Evidence.
- Production Orchestrator is the sole promotion/merge authority.
- No direct writes to `main` for development changes.
- Exact-head validation is required before promotion.
- Bounded, safe auto-fix is permitted; irreversible or security/data-critical decisions require human authorization.
- Recovery and resume are first-class lifecycle capabilities.

## Maturity
ASF maturity levels L0–L10 describe increasing autonomy. L10 must never be claimed without complete, verified end-to-end evidence covering execution, validation, promotion, release, monitoring, recovery, and resume.
