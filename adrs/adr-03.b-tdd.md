---
title: adr-03.b-tdd
type: adr
status: active
version: v0.1.4
tags: [tdd, testing]
description: "Framework-bound service code is test-first; framework-neutral Paladin logic is implemented first and tested afterward."
applies_when:
  - When creating or changing service models, handlers, or domain services.
  - When writing or closing a TDD entry under docs/tdds/.
  - When deciding whether pure Python business logic uses the Paladin test-after path.
related_agents:
  - hb-ag-service
  - hb-ag-paladin
  - hb-ag-test
---

# ADR-03.b — TDD

> Test-first protects framework integration, while a narrow test-after path keeps framework-neutral Python rules surgical and portable.

Instantiation: keep this sub unless the project is truly not a tested service. Surface tests stay under the frontend family / [[adr-04-frontend]], still written by The Trickster.

1. **Framework-bound service TDD.** Models, migrations, persistence, handlers, permissions, routes, and framework adapters under `{{service tree}}` are born through the [[TDD]] flow. Unspecified service integration is not the path.

2. **Lifecycle.** Each unit of work has `docs/tdds/tdd-NN-slug.md`: `draft` → `red` → `green` → `done`.

3. **Red first.** The Dwarf's framework-bound implementation follows failing tests in `red` ([[DEVELOPMENT-LOOP]]). Runner: `{{test runner}}`.

4. **Paladin path.** Framework-neutral Python business rules and complex script cores owned by The Paladin are implemented first. The Trickster writes focused tests afterward. A framework import, persistence change, route, payload, permission, or handler makes the work framework-bound and returns it to rules 1–3.

5. **Scope.** One TDD entry, one coherent unit. This sub does not govern surface-only tests.
