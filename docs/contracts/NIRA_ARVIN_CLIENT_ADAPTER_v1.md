# NIRA ↔ Arvin Client Adapter v1

**Issue:** #23  
**Status:** Contract definition; not yet connected to Arvin runtime

## Principle
Arvin is a workload/client. NIRA is the factory. This adapter is the only intended boundary for submitting Arvin work to NIRA.

## Client responsibilities
Arvin supplies:
- project identity
- issue/PR identity
- product acceptance criteria
- product test/build/device commands
- product-specific environment requirements
- resulting artifact/release metadata

## NIRA responsibilities
NIRA owns:
- intake and routing
- queue and priority
- lease and fencing
- worker lifecycle
- AI/provider runtime policy
- exact-base/head validation
- gates and evidence
- recovery
- promotion/merge authority
- release orchestration and audit

## Adapter API (conceptual)
`submitWork(item)` → NIRA queue receipt  
`getExecutionStatus(id)` → authoritative state  
`publishClientEvidence(id, evidence)` → evidence ingestion  
`acknowledgePromotion(id, postcondition)` → post-promotion observation

The adapter must never expose a direct merge primitive.

## Migration rule
Current Arvin factory workflows remain operational until a NIRA-backed adapter is proven by E2E evidence. Cleanup happens only in separate Arvin PRs after validation.
