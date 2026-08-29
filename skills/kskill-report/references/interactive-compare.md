# Interactive compare — vanilla JS tab switcher

Use when a report compares **two sides** (A vs B, grok vs kodex, before/after) and
the reader should **filter** or **contrast** without scrolling through both stacks
every time.

**No React. No build step.** One inline `<script>` at the bottom of the artifact,
plus the compare CSS already in `design-tokens.css`.

---

## When to use

| Use interactive compare | Use static `comparison.html` |
|---|---|
| Long explainers with parallel sections per side | Short A/B card + verdict only |
| Reader will toggle while learning topology/workflow | One-screen decision summary |
| User asked for buttons / interactividad / comparar | No interaction requested |

Template skeleton: `references/templates/comparison-interactive.html`.

---

## Panel tagging contract

Every `<section>` (or block) gets **`data-compare-panel`** with one of:

| Value | Shown when |
|---|---|
| `shared` | Always (hero, nav, footer, runtime notes) |
| `grok` (or `a`) | Mode **grok** and **both** |
| `kodex` (or `b`) | Mode **kodex** and **both** |
| `contrast` | Mode **contrast** only — side-by-side rows |

Example:

```html
<section data-compare-panel="shared" class="rise d1">…hero…</section>
<section data-compare-panel="grok" class="rise d2">…topología grok…</section>
<section data-compare-panel="kodex" class="rise d3">…topología kodex…</section>
<section data-compare-panel="contrast" class="rise d4">
  <div class="compare-row">
    <div class="compare-col compare-col--a">
      <span class="compare-col-label">grok</span>
      <h3>estrella</h3>
      <p>…condensado…</p>
    </div>
    <div class="compare-col compare-col--b">
      <span class="compare-col-label">kodex</span>
      <h3>equipo</h3>
      <p>…condensado…</p>
    </div>
  </div>
</section>
```

**Contrast panels** carry abbreviated bullets — not full duplicate mermaid. Full
diagrams live in the `grok` / `kodex` panels.

---

## Nav markup (copy verbatim, adjust labels)

Place immediately after the hero (`shared` section):

```html
<nav class="compare-nav" role="tablist" aria-label="comparar">
  <button type="button" class="compare-tab is-active" role="tab"
    data-compare="both" aria-selected="true">ambos</button>
  <button type="button" class="compare-tab" role="tab"
    data-compare="grok" aria-selected="false">grok</button>
  <button type="button" class="compare-tab" role="tab"
    data-compare="kodex" aria-selected="false">kodex</button>
  <button type="button" class="compare-tab" role="tab"
    data-compare="contrast" aria-selected="false">contraste</button>
</nav>
```

Rename tab labels to match sides (`opción a` / `cloudflare` / `antes`…) but keep
`data-compare` values stable: `both`, side-a key, side-b key, `contrast`.

---

## Script (inline before `</body>`, after mermaid loader)

Copy from `references/templates/comparison-interactive.html` or paste:

```html
<script>
(function () {
  var VIS = {
    both:     { shared: 1, grok: 1, kodex: 1, contrast: 0 },
    grok:     { shared: 1, grok: 1, kodex: 0, contrast: 0 },
    kodex:    { shared: 1, grok: 0, kodex: 1, contrast: 0 },
    contrast: { shared: 1, grok: 0, kodex: 0, contrast: 1 }
  };
  var nav = document.querySelector('.compare-nav');
  if (!nav) return;
  var tabs = nav.querySelectorAll('.compare-tab');
  var panels = document.querySelectorAll('[data-compare-panel]');
  var KEY = 'kdx-compare-mode';

  function setMode(mode) {
    if (!VIS[mode]) mode = 'both';
    tabs.forEach(function (t) {
      var on = t.getAttribute('data-compare') === mode;
      t.classList.toggle('is-active', on);
      t.setAttribute('aria-selected', on ? 'true' : 'false');
    });
    panels.forEach(function (p) {
      var side = p.getAttribute('data-compare-panel');
      p.hidden = !VIS[mode][side];
    });
    try { sessionStorage.setItem(KEY, mode); } catch (e) {}
  }

  tabs.forEach(function (t) {
    t.addEventListener('click', function () {
      setMode(t.getAttribute('data-compare'));
    });
  });

  var saved = null;
  try { saved = sessionStorage.getItem(KEY); } catch (e) {}
  setMode(saved && VIS[saved] ? saved : 'both');
})();
</script>
```

Rules:
- **IIFE only** — no modules, no bundler, no React/Vue/framework of the week.
- Mermaid loader stays **above** this script; `startOnLoad:true` renders all
  blocks once (including panels that start hidden).
- Tap targets ≥ 44px — `.compare-tab` min-height in CSS.

---

## Color mapping

| Side | Accent | CSS |
|---|---|---|
| A / grok / orange option | Presentation Orange | `.compare-col--a`, `.card.good`, `chip.work` |
| B / kodex / teal option | petroleo | `.compare-col--b`, `.card.teal`, `chip.stop` |
| Contrast active tab | salvia | `data-compare="contrast"` active state |

---

## Self-check (interactive reports)

- [ ] `design-tokens.css` embedded verbatim (includes compare CSS).
- [ ] Every non-nav block has `data-compare-panel`.
- [ ] At least one `contrast` row with `.compare-row` + two cols.
- [ ] Buttons are `<button type="button">`, not `<div onclick>`.
- [ ] `role="tablist"` / `role="tab"` / `aria-selected` present.
- [ ] Works on 390px width — tabs wrap, no horizontal page scroll.
- [ ] Mermaid gate still passes (`validate_mermaid.py`).