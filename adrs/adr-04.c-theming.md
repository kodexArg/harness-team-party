---
title: adr-04.c-theming
type: adr
status: active
version: v0.1.2
tags: [theming, surface]
description: "How user theme preference is stored, mirrored, and applied with no flash."
applies_when:
  - When persisting appearance, density, or theme packs.
  - When injecting theme classes during surface SSR or first paint.
related_agents:
  - hb-ag-surface
---

# ADR-04.c — theming

> Preference storage, cookie (or equivalent) mirror, and first-paint classes keep theme from flashing.

Instantiation: **rewrite or delete.** A product with one fixed theme deletes this sub. A product with user packs fills `{{theme persistence}}`.

1. **Persistence.** `{{theme persistence}}` (example: JSON on the user record plus a non-HttpOnly cookie the layout reads).

2. **First paint.** The layout shell applies classes/tokens from that store during render so the first HTML already matches.

3. **Packs.** If curated palettes exist, they are data in the surface tree, not a second CSS framework.
