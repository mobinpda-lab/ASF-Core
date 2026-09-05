# NIRA — Canonical Identity and Independence

**Status:** Canonical
**Repository:** `mobinpda-lab/ASF-Core`
**Historical name:** ASF-Core — Autonomous Software Factory Core
**Product name:** NIRA OS — نِیرا، سامانهٔ خودکار تولید نرم‌افزار
**Core:** NIRA Core — هستهٔ خودمختار کارخانهٔ نرم‌افزار

## 1. Identity

`NIRA` is the canonical product/platform identity of the autonomous software factory previously identified as `ASF-Core` / `ASF-MOC`.

Proposed semantic meaning:

> **نِیرا = نیروی ایرانیِ راه‌انداز**

NIRA is a factory platform, not a product application. Its mission is to orchestrate the software-production lifecycle from idea and architecture through execution, testing, evidence, promotion, release, monitoring, recovery, and continuous improvement.

## 2. Canonical naming

- **NIRA OS** — system/platform layer
- **NIRA Core** — factory execution/control core
- **NIRA Factory** — autonomous software production environment
- **NIRA Agents** — autonomous workers/agents
- **NIRA Engine** — orchestration engine
- **NIRA CI** — integration and validation subsystem
- **NIRA Governance** — policy, security, authority, and audit
- **NIRA Runtime** — controlled execution environment

## 3. Independence law

NIRA is the sole canonical home for factory-core architecture, governance, orchestration, queue/lease lifecycle, worker contracts, evidence, gates, promotion, release automation, recovery, and factory observability.

Arvin, YadNegar, NetworkCenterMonitor, and future projects are external clients/workloads. They may contain only product-side adapters, explicit integration contracts, or product-specific automation. They are never authoritative sources for NIRA core behavior.

## 4. Migration rule

Factory knowledge found in product repositories is migrated by classification, not by blind copying:

1. **Factory-core** → re-home in NIRA.
2. **Shared contract/evidence** → canonicalize in NIRA and keep a thin product integration.
3. **Product adapter** → remain in the product repository behind the NIRA contract.
4. **Legacy duplicate** → document and remove only after a replacement path is verified.
5. **Product-only** → remain with the product and must not be promoted into NIRA.

Every migration must preserve provenance and avoid destructive deletion before validation.

## 5. Source-of-truth hierarchy

1. NIRA repository and its canonical governance/architecture documents.
2. NIRA contracts, schemas, workflows, tests, and evidence.
3. Product repositories only for client-side implementation and observed integration evidence.

A product repository must not redefine NIRA architecture by convention.

## 6. Historical compatibility

The GitHub repository remains `ASF-Core` for continuity until a separate repository rename is executed. `ASF-Core` and `ASF-MOC` remain valid historical identifiers and must be retained in provenance, migration records, and references where required.

Canonical forward-facing identity: **NIRA**.

## 7. L10 boundary

NIRA L10 claims require authentic end-to-end evidence through the independent factory boundary across registered client workloads. A product's local automation, even when sophisticated, is not itself proof of NIRA L10.
