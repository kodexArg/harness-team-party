---
title: adr-04.a-architecture
type: adr
status: active
version: v0.1.2
tags: [architecture, surface]
description: "Surface host runtime, layout wrapping, and the interactivity ladder."
applies_when:
  - When adding a page, layout, or choosing how a control hydrates.
  - When changing the surface host output mode or listen address.
related_agents:
  - hb-ag-surface
---

# ADR-04.a — architecture

> One host and one layout shell keep pages from inventing a second chrome.

Instantiation: name the host and the ladder. Rewrite the rungs (static HTML / fragments / islands are a common three; this project may have two or four). Delete a rung that does not exist.

1. **Host runtime.** `{{surface framework}}` runs as `{{surface rendering mode}}` on the port in `{{local ports}}`.

2. **Layout wrapping.** User-facing pages render through `{{layout convention}}` (example: a base layout and a print layout). Hand-authored document shells that skip the token stylesheet are not the path.

3. **Interactivity ladder.** `{{interactivity ladder}}` (example: 1 server HTML, 2 fragments per [[adr-03.c-htmx]], 3 `{{component framework}}` islands). Pick hydration only as high as the rung requires (`{{hydration default}}`).

4. **Script placement.** Domain TypeScript/JS lives in the surface lib; host page scripts stay thin; component scripts own component state.
