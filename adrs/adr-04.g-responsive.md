---
title: adr-04.g-responsive
type: adr
status: active
version: v0.1.2
tags: [responsive, surface]
description: "Every surface view adapts across viewports; breakpoints come from the token system."
applies_when:
  - When laying out a page, table, drawer, or dialog.
  - When setting breakpoints or touch targets.
related_agents:
  - hb-ag-surface
---

# ADR-04.g — responsive

> The screen works on a dense desktop and on a handset without a second product.

Instantiation: keep this sub for any visual surface. Rewrite breakpoint names to the token stylesheet. Delete only if the product has a single fixed viewport (kiosk, print-only, CLI with no screen).

1. **Fluid views.** Layouts, tables, nav, and dialogs adapt without unwanted horizontal page scroll.

2. **Density.** Desktop keeps operational density; narrow viewports stack, collapse, or card-summarize.

3. **Pointer and touch.** Controls stay usable as touch targets on handhelds and compact on pointer desktops.

4. **Breakpoints.** Adaptations use `{{token stylesheet}}` breakpoint tokens, not one-off media queries.
