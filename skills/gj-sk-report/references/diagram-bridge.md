# Diagram bridge — how `gj-sk-report` uses `diagram-design`

Reports never invent diagram chrome. When a visual earns its place, **call `diagram-design` and embed its SVG**.

## When to draw

Ask: *Would the reader learn more from this than from one short paragraph?*

Draw when the answer is yes AND one of:

- flow / architecture / state / sequence / decision branches
- comparison topology that text alone muddies
- a single metric story that a small chart clarifies

Do **not** draw for: bullet lists, simple before/after, one-shape “diagrams”, or decoration.

## How to call diagram-design (intelligence rules)

1. **Load** the project or host `diagram-design` skill (`skills/diagram-design` or `~/.claude/skills/diagram-design`).
2. **Pick type** from its §3 guide. Prefer one primary type. Prefer a semantic pattern when behavior/risk/queue/governance is the point.
3. **Size for the phone shell**: default `doc-inline` or `fit`. Prefer **minimal dark** (`assets/template-dark.html`) so the SVG matches this report’s dark paper.
4. **Budget**: stay inside diagram-design §7 (≤9 nodes, ≤2 accent, …). Split overview + detail into two report sections rather than one overstuffed SVG.
5. **Confirm** type + cuts in one short line only when the caller is reachable and the request did not pin them; otherwise proceed.
6. **Produce** a self-contained diagram HTML, then **extract the `<svg>…</svg>`** (with its `<title>` / `<desc>` / markers). Drop the diagram page chrome (eyebrow/h1/frame) — the report shell owns titles.
7. **Embed** inside the report:

```html
<div class="diagram" role="region" aria-label="diagram">
  <div class="dd-frame">
    <!-- paste diagram-design <svg> here; keep role=img + aria-labelledby -->
  </div>
</div>
```

8. **Prefix IDs** if the report embeds more than one SVG (`marker` ids, title/desc ids) so they never collide.
9. **Do not** ship Mermaid CDN as the diagram engine. Mermaid in the *source markdown* is an import hint: run diagram-design’s mermaid import path (`scripts/mermaid_extract.py` + redraw), then embed SVG. Escape hatch only if the caller explicitly demands live Mermaid — then note it as a downgrade.

## Mobile hosting

- The shell’s `.diagram` scrolls horizontally; never shrink nodes below legibility.
- Avoid `min-width: 900px` forcing unreadably tiny text — redraw at a phone-sensible viewBox when needed (narrower ranks, fewer nodes).
- One diagram per section. Two diagrams max per short report unless the user asked for depth.

## Style alignment

- diagram-design owns node/connector grammar and tokens inside the SVG.
- The report shell owns kickers, prose, chips, takeaway, and the soft orange glow.
- Do not re-skin SVG fills to Presentation Orange hexes; keep diagram-design dark roles.
