# NIRA Architecture Decisions

This is the append-only decision ledger for factory-level choices. Product-specific decisions belong in client repositories.

## ADR-001 — NIRA is the sole factory authority

**Decision:** NIRA is an independent factory control plane. Client repositories are workloads and must not create competing factory authorities.

## ADR-002 — GitHub is the operational source of truth

**Decision:** Live repository, issue, PR, workflow, artifact, and exact-SHA state override memory and generated documentation.

## ADR-003 — Workers never own promotion

**Decision:** Workers and validators cannot promote their own output. Promotion is a separate guarded authority.

## ADR-004 — Exact-head and exact-main fail closed

**Decision:** Stale base/head, missing gates, missing evidence, unknown state, or changed main blocks promotion.

## ADR-005 — Parallelism is portfolio-aware

**Decision:** Independent work may execute in parallel, while conflicting mutations against the same protected target are serialized.

## ADR-006 — Provider pressure is a control-plane condition

**Decision:** Provider availability failures are classified as infrastructure conditions and handled through bounded retry/requeue policy.

## ADR-007 — Client-native validation

**Decision:** NIRA observes and validates client workflows instead of embedding product-specific toolchains.

## ADR-008 — Generated state must not bypass promotion

**Decision:** State documents and generated metadata follow normal NIRA change flow and promotion controls.

## ADR-009 — Release remains client-native

**Decision:** NIRA orchestrates and verifies release but does not own client-specific signing/build semantics.

## ADR-010 — Monitoring creates evidence before repair

**Decision:** Monitoring evidence must be classified before recovery tasks are created.

## ADR-011 — Standard v2.0 is the operational alignment authority

**Decision:** NIRA Autonomous Software Factory Operating Standard v2.0 is the operational standard for lifecycle, evidence, governance, recovery, and continuous improvement.

**Constraint:** The standard extends operations but does not override NIRA Control Plane safety rules.
