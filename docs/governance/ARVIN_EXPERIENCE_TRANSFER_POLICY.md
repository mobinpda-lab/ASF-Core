# Arvin → NIRA Factory Experience Transfer Policy

NIRA continuously incorporates validated, generic Factory engineering lessons discovered in Arvin.

## Allowed transfer

- orchestration invariants
- queue/lease semantics
- exact-head and exact-main fencing
- CI/build/device/evidence gate patterns
- bounded worker safety
- idempotency and single-launch controls
- failure feedback and bounded Auto-Fix patterns
- parallelism scheduling
- recovery/watchdog patterns
- promotion and release evidence contracts
- observability/reporting and documentation authority

## Forbidden transfer

- Arvin product business logic
- Arvin product data
- product-specific Flutter implementation
- product-specific feature scope
- secrets or credentials
- direct copying of product-specific workflow commands when a generic client adapter is required

## Operating rule

Every transferred capability must be independently reimplemented in NIRA, covered by acceptance criteria and evidence, and validated at the exact NIRA head. Arvin remains a source of lessons and reference evidence; NIRA remains the canonical Factory authority.

## Completion standard

A capability is not considered transferred merely because documentation exists. It becomes **Proven** only after real execution produces reproducible evidence tied to an exact commit/HEAD.
