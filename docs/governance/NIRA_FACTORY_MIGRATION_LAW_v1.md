# NIRA Factory Migration Law v1

## Authority
NIRA is the sole canonical home for factory-core implementation, governance, orchestration, queue/lease lifecycle, worker runtime, evidence, gates, recovery, promotion, release automation and factory observability.

## Mandatory migration order
`Inventory → Canonicalize → Implement → Contract-test → Adapter → E2E → Observe → Deprecate → Remove`

## Non-negotiable rules
1. Never delete an operational Arvin factory path before its NIRA replacement is proven.
2. Never copy product-specific logic into NIRA merely because it participates in automation.
3. Preserve original issue, commit, workflow and document provenance.
4. Treat stale, missing or inaccessible evidence as non-PASS.
5. No worker may merge its own output.
6. Exact base/head validation is mandatory before promotion.
7. Recovery must be bounded and fenced.
8. Factory progress and product progress are reported separately.
9. L10 cannot be marked verified from design claims or worker self-report.

## Cleanup gate
A legacy product factory asset becomes removable only when:
- the NIRA capability exists;
- contract tests pass;
- the client adapter is active;
- at least one real E2E cycle succeeds;
- failure/fencing/recovery behavior is evidenced;
- promotion/release postconditions are independently observed;
- no remaining product responsibility depends on the legacy implementation.
