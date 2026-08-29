---
title: adr-04.d-components
type: adr
status: active
version: v0.1.2
tags: [components, surface]
description: "Host files route and compose; components present; reuse before inventing."
applies_when:
  - When adding a page, layout, or component file.
  - When choosing a headless widget library.
related_agents:
  - hb-ag-surface
---

# ADR-04.d — components

> The host assembles pages; components present. Reuse beats a second card.

Instantiation: fill the catalog location and the mount rule. Zero-prop mount is a strong default — drop it if this `{{component framework}}` cannot honor it. Name a headless kit or write "none".

1. **Host vs component.** Pages and layouts under `{{surface tree}}` fetch and compose. Presentation lives in components (`{{component extension}}` files).

2. **Reuse.** Check the existing tree and `{{component catalog}}` before adding a component.

3. **Taxonomy.** Components sit in a documented folder convention, not a flat dump.

4. **Mount.** A component mounts with zero required props without throwing or firing a mutating request — unless this sub is rewritten to say otherwise.

5. **Headless widgets.** Accessible builders, if any, are the kit named here.
