---
title: adr-04-frontend
type: adr
status: active
version: v0.1.2
tags: [adr, frontend, surface]
description: "Surface (frontend) family: host, tokens, theme, components, toolchain, client fetch, responsive. Template — fill or delete."
applies_when:
  - When designing pages, layouts, or interactive components in the surface tree.
  - When changing tokens, theme, toolchain, or how the surface calls the service.
sub_adrs:
  - adr-04.a-architecture
  - adr-04.b-design-system
  - adr-04.c-theming
  - adr-04.d-components
  - adr-04.e-toolchain
  - adr-04.f-client-api
  - adr-04.g-responsive
related_agents:
  - hb-ag-surface
---

# ADR-04 — frontend

> The surface is one host: reuse components, tokens for paint, and a declared interactivity ladder so the screen stays coherent.

This family is a **template**. It is the frontend/surface rulebook. Instantiation fills slots from [[ONBOARDING]] to match [[adr-02-stack]] and **deletes any sub this project does not use**. A **headless** project deletes this whole family in the same batch as The Elf ([[CLONE]]). Keep the parent if a screen exists.

1. **Host.** `{{surface framework}}` in `{{surface rendering mode}}` is the surface under `{{surface tree}}`. Client JavaScript is opt-in (`{{hydration default}}`).

2. **Reuse first.** New chrome starts from existing components and the catalog this project keeps (fill [[adr-04.d-components]]).

3. **Interactive layer.** `{{component framework}}` is the stateful island/widget layer. Headless accessible builders are welcome when this project names them in that sub.

4. **Tokens.** Visual decisions are tokens, not one-off literals ([[adr-04.b-design-system]]).

5. **Facts.** Layout, tokens, and component lists live in docs the surface skills point at — not in this ADR.
