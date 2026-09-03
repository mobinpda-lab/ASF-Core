# ASF-Core Architecture

ASF-Core is the independent reusable factory platform. Product repositories connect through adapters and contracts; product implementation remains outside the factory core.

```text
ASF-Core
 |
 +-- Arvin Adapter
 +-- YadNegar Adapter
 +-- NCM Adapter
```

## Layers

### ASF-Core
Owns reusable factory concerns: orchestration, scheduling, queue and lease semantics, worker contracts, validation, evidence, lifecycle state, guarded promotion, release lifecycle, monitoring, recovery, and resume.

### Product Adapters
Adapters translate product-specific task intake, state, evidence, workflow triggers, and validation boundaries into ASF-Core contracts. The initial adapters are Arvin, YadNegar, and NCM.

### Product Repositories
Product repositories own application code, business rules, UI, domain models, storage, product-specific workflows, and product features. They remain independent and are not migrated into ASF-Core.

## Boundary Rules
1. ASF-Core must not import product source code.
2. ASF-Core must not modify product repositories as part of factory implementation.
3. Product features are not implemented in ASF-Core.
4. Reusable factory capabilities belong in ASF-Core.
5. Product-specific behavior belongs in the product repository or its adapter.
6. Cross-repository operations must use explicit adapter/contract boundaries.
7. Development changes follow branch → commit → PR → CI → evidence.
8. Production promotion is controlled by the Production Orchestrator; direct `main` writes are prohibited for development changes.

## Evolution Model
Factory evolution and product evolution proceed in parallel. New products can attach through new adapters without changing the factory's product-independent core.
