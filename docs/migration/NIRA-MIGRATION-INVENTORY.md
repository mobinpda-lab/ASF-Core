# NIRA Migration Inventory

Date: 2026-09-05 (Iran time)
Status: Discovery baseline; continuously extensible

| Source | Capability / knowledge | Location / evidence | Purpose | Migration decision | Destination | Risk |
|---|---|---|---|---|---|---|
| ASF-Core | Independent factory control-plane boundary | README.md; factory/* | Generic factory authority | Preserve and evolve | NIRA Core/Engine/Runtime | High if duplicated |
| ASF-Core | Contracts, lifecycle, gates, evidence, recovery | factory/contracts; factory/gates; factory/recovery; factory/runtime | Fail-closed factory primitives | Reuse/redesign, do not duplicate | NIRA Core | High |
| ASF-Core | Registered-client conformance | factory/tests/test_registered_client_e2e.py | Deterministic lifecycle proof | Preserve as conformance only | NIRA Evidence/Tests | Medium; not L10 proof |
| ASF-Core | Real client registry | commit 90a5f11 | Registry-driven client boundary | Preserve | NIRA Registry | Medium |
| ASF-Core | Promotion hardening | commits afe4c76, b73d6fb | Exact HEAD/base, CI, artifact, fail-closed promotion | Preserve | NIRA Promotion/Governance | High |
| ASF-Core | ASF-MOC v9.0 operating model | docs/governance/ASF_MOC_v9_GITHUB_AUTONOMOUS_SOFTWARE_FACTORY_CONTINUOUS_COMPANY_OS.md | Historical/normative source knowledge | Preserve verbatim as provenance; implement in NIRA | NIRA Governance/Memory | High |
| Arvin-clean | Production orchestrator | .github/workflows/production-orchestrator.yml; docs/ARVIN_PRODUCTION_ORCHESTRATOR_5MIN_MODE.md | Existing production automation experience | Extract knowledge; adapter only | NIRA orchestration + Arvin adapter | High |
| Arvin-clean | Production queue | .github/arvin/production-queue.yml | Parallel task scheduling experience | Extract patterns; retire authority after proof | NIRA Queue | High |
| Arvin-clean | AI/agent workers | .github/workflows/arvin-agent-worker.yml and related workflows | Worker execution lessons | Extract contracts/lessons | NIRA Workers/Agents | High |
| Arvin-clean | Worker launch authority | docs/AI_WORKER_SINGLE_LAUNCH_AUTHORITY_2026-08-31.md | Avoid duplicate worker launch | Preserve lesson | NIRA Governance/Runtime | High |
| Arvin-clean | Provider fallback/hardening | docs/AI_WORKER_PROVIDER_FALLBACK_2026-08-31.md; docs/AI_WORKER_PATCH_HARDENING_2026-08-31.md | Provider isolation and bounded repair | Extract patterns | NIRA Agents/Runtime | High |
| Arvin-clean | Production merge boundary | docs/AUTOMATION_FAILURE_FEEDBACK_2026-08-31.md; tests | Single guarded promotion authority | Extract and centralize | NIRA Promotion | Critical |
| Arvin-clean | Product CI/release/device flows | .github/workflows/* | Product-specific validation | Keep product-owned | Arvin repository | Medium |
| YadNegar | Product architecture and CI | repository main and project docs/workflows | Product knowledge | Keep client-owned | YadNegar + adapter | Medium |
| NetworkCenterMonitor | Runtime control-plane experience | commit 8ebe93b | Persistent state, worker capacity, event-driven recovery, heartbeat/lease | Extract proven recovery patterns | NIRA Runtime/Recovery | High |
| NetworkCenterMonitor | Recovery/lease lessons | commit 8ebe93b and associated issue history | Stale lease recovery and worker heartbeat | Preserve as knowledge, reimplement centrally | NIRA Recovery | High |

## Discovery rules
- This inventory is additive; new evidence must be appended, never silently discarded.
- Factory authority is migrated only after executable NIRA capability and independent evidence exist.
- Historical commits/issues/PRs remain source provenance even after authority moves.
- Product code remains in client repositories.
- Existing client factory workflows remain protected until supersession is proven.

## Current gap
A complete historical extraction of every issue/PR/artifact across all four repositories is a continuing discovery lane. The baseline above is evidence-backed and must not be represented as exhaustive until that lane completes.
