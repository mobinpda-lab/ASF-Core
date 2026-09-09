# NIRA Architecture Decisions

This is the append-only decision ledger for factory-level choices. Product-specific decisions belong in client repositories.

## ADR-001 — NIRA is the sole factory authority

**Decision:** NIRA is an independent factory control plane. Arvin-clean, YadNegar, NetworkCenterMonitor, and future repositories are clients/workloads.

**Reason:** Prevent product/factory coupling and competing authorities.

## ADR-002 — GitHub is the operational source of truth

**Decision:** Live repository, issue, PR, workflow, artifact, and exact-SHA state override memory and generated documentation.

**Trade-off:** Derived state documents can briefly lag live GitHub state.

## ADR-003 — Workers never own promotion

**Decision:** Code-generation workers, deterministic workers, and validators cannot merge their own output. Promotion is a separate guarded authority.

**Reason:** Worker claims are not independent evidence.

## ADR-004 — Exact-head and exact-main fail closed

**Decision:** Stale base/head, missing gates, missing evidence, unknown state, or changed main blocks promotion.

## ADR-005 — Parallelism is portfolio-aware

**Decision:** Independent repositories may execute in parallel; the same client repository cannot have competing AI leases against one main.

## ADR-006 — Provider pressure is a control-plane condition

**Decision:** 429/502/503/504 conditions release/requeue the AI lease with bounded cooldown. They are not product failures and do not consume code-repair attempts.

## ADR-007 — No unreliable provider fallback

**Decision:** NIRA does not add Copilot as an automatic fallback for OpenAI. The Arvin experiment showed quota/runtime reliability problems; NIRA keeps bounded OpenAI pressure handling and fail-closed behavior.

## ADR-008 — Client-native validation

**Decision:** NIRA records workflow metadata and observes each client's own CI/security workflows instead of embedding Flutter/Gradle/npm/product toolchains.

## ADR-009 — Generated state must not bypass promotion

**Decision:** Project-state snapshots are updated through a `nira/` branch and normal NIRA promotion, never by direct writes to protected `main`.

## ADR-010 — Release remains client-native

**Decision:** NIRA may orchestrate and verify release, but product repositories own their release workflows, signing/build inputs, and release semantics. NIRA never embeds product build commands in release policy.

**Reason:** Preserve factory independence while still providing end-to-end autonomous release.

## ADR-011 — Monitoring creates evidence before repair

**Decision:** NIRA Client Monitor may create/reconcile recovery issues from exact-main workflow failures, but it never directly launches AI repair. Monitoring evidence must be classified before bounded repair is queued.

**Reason:** Prevent transient, environment, security, or permission failures from being misclassified as code defects.
