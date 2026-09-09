# Vazirharf v34.003 — Font Standard

## Canonical standard
Vazirharf v34.003 is the canonical Persian/Arabic font standard for NIRA where project typography is required.

- Upstream: `nadalaba/vazirharf`
- Version: `v34.003`
- Pinned upstream commit: `3cbc943b9fb9107baa77008b3e96b3c3e40e9ed8`
- Integration path: `assets/fonts/vazirharf`
- Integration method: Git submodule

## Policy
All active Persian/RTL typography, UI components, generated documents, tests, configuration, CI and project documentation must use Vazirharf v34.003 where a project font is required. The previous Persian font standard is superseded.

CI/build systems must initialize and update the submodule before consuming font assets. Any future typography change must update this specification and the pinned version deliberately.

Historical Git commits are immutable; this policy applies to the active source tree and current development state.
