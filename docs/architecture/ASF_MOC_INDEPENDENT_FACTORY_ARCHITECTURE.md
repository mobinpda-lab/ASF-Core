# ASF-MOC Independent Factory Architecture

**Status:** Canonical architectural decision  
**Applies to:** ASF-MOC v9.0 / L10 Autonomous Software Production  
**Repository:** `mobinpda-lab/ASF-Core`  
**Issue:** #11  
**Date:** 2026-09-04

## 1. Purpose

This document establishes the ownership boundary between the autonomous software factory (**ASF-MOC**) and the software products it operates.

The factory is an independent system. Product repositories are workloads/clients of the factory, not containers of the factory core.

## 2. Canonical topology

```text
                         ASF-MOC / ASF-Core
                    Independent Factory System
                              |
                    +---------+---------+
                    |                   |
              Project Registry     Factory Runtime
                    |                   |
          +---------+---------+   +-----+----------------+
          |         |         |   |                      |
       Arvin    YadNegar    NCM  Queue / Workers /   Evidence /
                               |   Gates / Promotion   Recovery
                               |
                         External Projects
```

### Factory

**ASF-MOC / ASF-Core** owns:

- governance and execution policy
- Project Registry
- orchestration and dispatch
- queue and lease lifecycle
- workers and worker contracts
- CI/test/build gate integration
- evidence collection and validation
- recovery/resume and stale-work handling
- PR/promotion lifecycle
- release automation
- factory-level observability
- L10 evidence and capability assessment

### Products

The following remain independent projects:

- **Arvin-clean** — product/workload/client
- **YadNegar** — product/workload/client
- **NetworkCenterMonitor** — product/workload/client

A product may expose an observer, dashboard, adapter, webhook, or other integration for ASF-MOC. Such integration does not transfer factory ownership to the product.

## 3. NetworkCenterMonitor boundary

NetworkCenterMonitor is **not** ASF-MOC and must not become a second factory.

Factory-related workflows or control-plane mechanisms previously introduced into NetworkCenterMonitor are classified as **provisional/legacy factory integration** until they are audited.

For each such component, the target state is one of:

1. **Re-home into ASF-Core** when it is factory-core functionality.
2. **Reduce to a product-side adapter/integration** when the product genuinely needs to communicate with ASF-MOC.
3. **Remove** when it duplicates factory responsibility without a valid product integration purpose.

No product repository is an authoritative source for ASF-MOC core behavior.

## 4. Product Registry contract

ASF-MOC must manage products through an explicit registry/contract rather than repository ownership coupling.

A registered project should have, at minimum:

- stable project identifier
- repository identifier/URL
- default/base branch policy
- supported execution capabilities
- CI/build/test entry points
- factory integration contract
- evidence contract
- promotion policy
- project-specific constraints

The registry allows new projects to be added without cloning or rebuilding the factory.

## 5. Execution boundary

The canonical factory lifecycle remains:

```text
IDEA
  -> PRODUCT DEFINITION
  -> ARCHITECTURE
  -> PROJECT BOOTSTRAP
  -> TASK DECOMPOSITION
  -> GITHUB ISSUES
  -> PARALLEL WORKERS
  -> CODE
  -> TEST
  -> AUTO-FIX
  -> DOCS
  -> PR
  -> CI
  -> BUILD
  -> DEVICE TEST
  -> SECURITY GATE
  -> EXACT-HEAD VALIDATION
  -> AUTO MERGE
  -> RELEASE
  -> MONITORING
  -> RECOVERY / RESUME
  -> NEXT TASK
```

This lifecycle belongs to ASF-MOC. A product repository only supplies the workload and its project-specific execution surface.

## 6. Evidence and L10 rule

A product repository containing an autonomous workflow is not, by itself, evidence that ASF-MOC has achieved L10.

**L10 may be claimed only after the independent ASF-MOC system demonstrates authentic end-to-end evidence across registered client projects.**

Required evidence must establish, as applicable:

- authoritative task intake
- deterministic queue/lease ownership
- worker execution
- bounded recovery
- authentic CI/test/build evidence
- exact-head validation
- guarded PR/promotion
- release evidence
- failure/recovery evidence
- cross-project operation through the factory boundary

Evidence from one product or one PR can contribute to the proof but cannot substitute for factory-level end-to-end evidence.

## 7. Reporting rule

All operational reports must separate factory state from product state.

Canonical top-level sections:

1. **ASF-MOC** — factory capability, runtime, queue, workers, evidence, gates, recovery, releases, and L10 status.
2. **Arvin** — product implementation and product CI/release status.
3. **YadNegar** — product implementation and product CI/release status.
4. **NetworkCenterMonitor** — product implementation and product CI/release status, plus any explicitly identified observer/integration status.

Factory progress must never be presented as product progress, and product progress must never be presented as ASF-MOC progress.

## 8. Governance

All ASF-MOC core changes follow the governed path:

```text
Issue -> dedicated branch -> implementation -> CI/gates -> PR -> review/promotion -> main
```

No direct main modification is authorized merely because a change is architectural or urgent.

## 9. Architectural decision

This document supersedes any earlier interpretation in which NetworkCenterMonitor, Arvin, or YadNegar was described as the factory/control plane itself.

The canonical model is:

> **ASF-MOC is the factory. Products are independent clients/workloads.**

This boundary is mandatory for future implementation, reporting, documentation, automation, and L10 claims.
