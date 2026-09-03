# Product Adapter Contract

## Purpose
Adapters are the only integration boundary between ASF-Core and an independent product repository.

## Required Capabilities
- map product task intake to factory task records
- translate product state into factory lifecycle/evidence state
- trigger product-specific workflows through declared interfaces
- expose product validation through bounded adapters

## Isolation
Adapters must not import, relocate, or own product implementation. Product source, business logic, UI, domain models, storage, and product-specific behavior remain in product repositories.

## Security and Authority
Adapters operate with least privilege and cannot bypass factory gates or promotion authority. Secrets remain outside source and evidence.

## Compatibility
Adapter changes require contract validation and evidence. Unknown or incompatible product states fail closed rather than being silently mapped.
