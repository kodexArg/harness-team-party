---
title: adr-02-stack
type: adr
status: active
version: v0.1.2
tags: [stack, service, surface, infrastructure, devops]
description: "Defines the sanctioned conceptual technology stack across service, surface, infrastructure, and runtime toolchains. Ships as a placeholder: instantiation makes the decision."
applies_when:
  - When selecting technology components for the service, the surface, or infrastructure.
  - When verifying that a dependency belongs to the sanctioned conceptual stack.
  - When checking sanctioned runtime toolchains.
  - When verifying package adoption policies before adding dependencies.
related_agents:
  - hb-ag-service
  - hb-ag-surface
  - hb-ag-ops
  - hb-ag-test
---

# ADR-02 — stack

> A clean, conceptual architectural stack establishes clear system boundaries, eliminates toolchain ambiguity, and keeps technical adoption lean and predictable across the repository.

This file ships as a **placeholder template**. Every project instantiated from this harness makes this decision once, in this shape, and replaces each double-curly slot with the chosen component ([[ONBOARDING]], [[CLONE]]). The sections below are the shape of the decision every project must make.

1. **Stack authority.** This ADR defines the conceptual technology stack. Exact package pins, versions, check dates, and re-pin policies are strictly owned by [[REQUIREMENTS]].

2. **Service stack:**
   - Domain framework: `{{domain framework}}`
   - Interface framework: `{{interface framework}}`
   - Runtime and toolchain: `{{service toolchain}}` — no substitute package manager
   - Data layer: `{{data layer}}`
   - Integrations: `{{service integrations}}`

3. **Surface stack** (delete this section entirely in a headless project):
   - Surface framework: `{{surface framework}}`
   - Component framework: `{{component framework}}`
   - Runtime and toolchain: `{{surface toolchain}}` — no substitute package manager
   - Styling and primitives: `{{surface styling}}`

4. **Infrastructure, DevOps, and Data stack:**
   - Cloud deployment: `{{deploy target}}` on `{{cloud provider}}`, region `{{region}}`
   - Database: `{{database}}`
   - Secret storage: `{{secret store}}`
   - Deliberate absences: `{{infrastructure absences}}`

5. **Operational secret exception.** Runtime credentials live exclusively in the project's secret store. Any bounded exception (an operator-editable credential stored encrypted in the database) is named here explicitly, or this rule has no exceptions: `{{secret exceptions}}`

6. **Development variant:**
   - Local orchestration: `{{local runtime}}` with bind-mounted source directories ([[INFRASTRUCTURE]]).
   - Local configuration: a git-ignored `.env` mirrors the names declared in [[VARIABLES]].
   - Local testing: `{{test runner}}` on the service tree; the surface toolchain's test runner on the surface tree.

Service rules in detail: the [[adr-03-backend]] family (fill, rewrite, or delete subs). Surface rules in detail: the [[adr-04-frontend]] family (delete the whole family if headless).
