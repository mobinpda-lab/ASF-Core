# NIRA Factory Knowledge Migration Manifest

**Issue:** #20
**Purpose:** Establish an evidence-driven inventory for moving factory-owned knowledge out of product repositories and into NIRA.

## Scope

This manifest covers factory-related material found across the project ecosystem, with priority on Arvin-clean and then YadNegar and NetworkCenterMonitor.

## Classification contract

| Class | Canonical home | Action |
|---|---|---|
| Factory Core | NIRA | Re-home and make canonical |
| Factory Governance | NIRA | Re-home and make canonical |
| Factory Orchestration / Queue / Lease / Worker | NIRA | Re-home and make canonical |
| Factory Evidence / Gates / Recovery | NIRA | Re-home and make canonical |
| Shared Client Contract | NIRA contract + product adapter | Canonicalize contract in NIRA |
| Product Adapter | Product repository | Keep, minimize, and conform |
| Product-only behavior | Product repository | Do not migrate |
| Legacy duplicate | Case-by-case | Replace/reduce/remove after evidence |

## Initial audit evidence

### NIRA / ASF-Core

The repository already contains an independent-factory architecture decision, control-plane documentation, factory runtime primitives, evidence/gate components, registry, recovery policy, and factory workflows. The current README explicitly defines ASF-Core as an independent factory control plane and separates workloads from factory ownership.

### Arvin-clean

The audit identified factory-related operational material in the product repository, including autonomous queue/orchestrator work, factory promotion integration, factory operating packages, and issues describing factory runtime/evidence behavior. These are candidates for classification and re-homing when they represent factory-core knowledge rather than Arvin product behavior.

Known examples from the audit:

- `docs/ARVIN_PROJECT_OPERATING_PACKAGE.md`
- `docs/ARVIN_PROJECT_OPERATING_PACKAGE_v48.2_TRANSFER_MANIFEST.md`
- `docs/ARVIN_PROJECT_OPERATING_PACKAGE_v48.2_FINAL_OPERATIONAL_feshordeh_PART01.md`
- `.github/workflows/factory-rest-promotion-bridge.yml`
- `.github/workflows/arvin-autonomous-queue.yml`
- Factory-related issues including #617, #619, #620, #637, #640, #641, and #644.

These references are evidence for migration planning, not permission to copy Arvin-specific product logic into NIRA.

## Migration principles

- NIRA becomes the canonical source of factory policy and implementation.
- Arvin remains a client/workload; its product roadmap and product features remain in Arvin.
- Product-side bridges are retained only where an explicit client integration is required.
- No destructive product cleanup is performed until the replacement contract is implemented and validated.
- Historical references remain traceable.
- Every re-homed capability requires tests/evidence in NIRA.

## Next audit waves

1. Arvin-clean: complete inventory of factory-owned documents, workflows, scripts, and contracts.
2. YadNegar: inventory and classify factory-related material.
3. NetworkCenterMonitor: inventory provisional/legacy factory mechanisms and decide re-home vs adapter vs removal.
4. NIRA: absorb canonical factory knowledge and close duplicate authority paths.
5. Cross-project validation: prove clients operate through NIRA contracts without transferring factory ownership.

## Completion condition

Migration is complete only when NIRA is the authoritative factory source, product repositories contain only intentional client integrations, and the separation is enforced by documentation, contracts, tests, and CI/evidence gates.
