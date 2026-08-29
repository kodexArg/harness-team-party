---
title: adr-07-git
type: adr
status: active
version: v0.1.0
tags: [adr, git, trunk, branching, release, harness]
description: "Establishes single-trunk git discipline, ephemeral branch rules, commit standards, and harness triggers per git movement."
applies_when:
  - When creating feature branches or executing git commits and checkouts.
  - When cutting SemVer release tags or verifying single-trunk main invariants.
  - When determining which harness checks trigger upon git lifecycle events.
related_agents:
  - hb-ag-git
---

# ADR-07 — Git

> A strict single-trunk git model and deterministic harness triggers across repository movements eliminate branching drift, ensure continuous deployability, and bind development actions to automated validation.

1. **Single-trunk invariant.** `main` is the sole integration and production branch. Every change merged into `main` constitutes a direct deployment to production.

2. **No persistent release or production branches.** A `prod`, `release`, or `staging` branch carries no authority, holds no deploy trust, and is strictly prohibited from creation or recreation.

3. **Ephemeral working branches.** All non-direct work occurs on short-lived branches cut exclusively from `main`. This includes functional prefixes (`feat/*`, `fix/*`, `refactor/*`, `docs/*`, `test/*`, `chore/*`) and agent/tooling branches (`cursor/*`, `claude/*`, `agy/*`, `grok/*`, `kbot/*`, `kwf/*`). All working branches are strictly ephemeral, governed by the retention rule ([[GITHUB]]), and must be deleted immediately upon merge.

4. **Scoped commit discipline.** Commit messages follow modern scoped conventional formatting: `type(scope): concise imperative subject [trailer]`.
   - **Types:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, and `release`.
   - **First-class scopes:**
     - `harness`: Skills, hooks, agents (`agents/`), workflows, MCP tooling, and automation logic.
     - `adrs`: Architecture Decision Records (`adrs/`).
     - `service` / `<domain>`: units of the service tree (`{{service tree}}`).
     - `surface` / `<surface>`: views, UI components, styles, or client logic of the surface tree (`{{surface tree}}`).
     - `infra`: cloud resources, secret-store wiring, DNS, load balancing, identity federation, or local orchestration.
   - **Language & imperative mood:** English only, imperative present tense (`add`, `fix`, `refactor`, `enforce`), with optional issue references `(#123)` or release trailers `[vA.B.C]`.

5. **Release tagging convention.** Git release tags follow SemVer formatting cut exclusively from `main` ([[adr-05-after-versioning]]). Cutting a git tag is **mandatory for milestone releases (`vA.B`)**, locking the architectural feature grouping. Granular commit-level iterations (`.C`) are tracked in `CHANGELOG.md` and document frontmatters, and do **not** require a git tag on every batch. A tag records an immutable historical release milestone and triggers no deployment.

6. **Harness movement triggers:**
   - **Branch creation / checkout:** Resolves issue context, links working branch, and validates working branch naming.
   - **Commit:** Enforces atomic updates to `CHANGELOG.md` and applies the Boy Scout versioning rule to updated harness documentation.
   - **Pre-push / PR readiness:** Executes static typechecking, AST/linter validations, and relevant test gates for the changed diff.
   - **Merge to main:** Signals continuous deployment to `{{deploy target}}` and locks the integration record.
   - **Tag creation:** Verifies version alignment across CHANGELOG and active documentation.
