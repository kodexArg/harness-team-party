---
title: adr-04.b-design-system
type: adr
status: active
version: v0.1.2
tags: [design-system, tokens]
description: "One token stylesheet is the visual SSOT; literals in components are not."
applies_when:
  - When styling a component or adding a color, type, or radius token.
  - When choosing light/dark pairs or semantic tones.
related_agents:
  - hb-ag-surface
---

# ADR-04.b — design system

> Tokens let theme and contrast change without rewriting markup.

Instantiation: point `{{token stylesheet}}` at this project's token file. Color space, brand hue, and financial-tone rules are **invitations** — replace them with this product's system or delete the rules that do not apply.

1. **Token file.** `{{token stylesheet}}` is the SSOT for color, type, space, and radius. Hardcoded color literals in components are not the path.

2. **Pairs.** If this product has light and dark (or more), every surface token declares each mode in that file.

3. **Accent discipline.** Brand/accent hue stays on the tokens named for it, not on every canvas.

4. **Semantic tones.** If the product tints values (success, debit, warning), those tokens are named here and kept distinct from form-validation reds.
