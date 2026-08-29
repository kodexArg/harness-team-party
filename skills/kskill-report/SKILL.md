---
name: kskill-report
description: CONVERT a given markdown summary (prose, lists, code, ```mermaid blocks) into ONE self-contained, opinionated, mobile-first (and desktop-friendly) dark HTML artifact — meant to be sent over WhatsApp and opened on a phone. This skill CONVERTS markdown→HTML in a fixed format; it does NOT write, summarize, or research the content — the caller supplies the markdown, and if none is given the skill asks for it. Use when kodex asks for "un resumen en html", "reporte html", "dame esto en html para el celular/WhatsApp", a status report, concept explainer, comparison, stat highlight, or decision summary. Aesthetic is fixed ("Presentation Orange"): warm near-black, rationed orange glow, Nunito + DM Mono, Lucide icons, themed mermaid. Fast and deterministic — it fills templates, never improvises design.
---

# kskill-report

Convert a **given** markdown summary (prose, lists, code, and `mermaid` blocks)
into a single self-contained dark HTML file — mobile-first, also readable on
desktop — following the **Presentation Orange** design system. The output is one
`.html` opened on a phone over WhatsApp. **You fill templates; you do not invent
a new look.**

## Responsibility — read first

This skill has ONE job: **convert markdown → HTML in this fixed format.**

> [!important] Default source = your last answer
> When kodex invokes `/kskill-report` with **no markdown attached**, the content
> to convert is **the assistant's own immediately-preceding message** (the last
> substantive answer rendered to kodex before this invocation). Do **not** ask
> for content and do **not** re-summarize from scratch — take that last answer
> verbatim as the markdown input and convert it. Only ask if there is genuinely
> no prior assistant answer to grab (e.g. first turn). If kodex *does* attach
> markdown or a file path in the same turn, that explicit content wins over the
> last-answer default.

- It is **NOT** a summarizer, writer, or researcher. The markdown summary is an
  **input** the caller provides (or, per the box above, the last answer). Do
  **not** invent, expand, or fact-find the content — convert exactly what you're
  given.
- Be **fast and deterministic**: no deliberation about design, no exploring
  options. Fixed pipeline below, every time.

## The one rule

This skill is opinionated to the extreme. The aesthetic is settled and lives in
`references/`. Your job is: receive the markdown → pick a template → fill it with
that content → emit one file → validate → report its path. Do not change colors,
fonts, radii, or layout. Do not add frameworks. Do not improvise.

## Pipeline

1. **Read the design contract** (once): `references/design-tokens.css` is the
   literal CSS you embed inline. `references/EXTRACTED-DESIGN-SYSTEM.md` is the
   rationale (read only if a judgment call comes up — do not re-fetch any URL).
2. **Take the supplied markdown** (the caller's summary — never write your own).
   If it's missing, ask for it and stop. Identify sections, code/diff blocks,
   and any ```mermaid fences.
3. **Pick a template** from `references/templates/` (see mapping below). Copy it
   as the skeleton.
4. **Fill it.** Replace placeholder content with the user's. Map markdown:
   - `# / ##` → `<h1>/<h2>` (lowercase, kept lowercase by CSS).
   - tiny eyebrow like `03 · QUÉ ES` → `<p class="kicker">`.
   - paragraphs → `<p>`; `**bold**` → `<strong>`. **Ration `<strong>` hard** —
     reserve it for the one genuinely load-bearing phrase in a passage, not every
     key term. Most paragraphs should carry zero `<strong>`. Over-bolding flattens
     emphasis and reads as noise.
   - fenced ```lang code → `<pre><code>`; a diff (lines `+`/`-`) → `<pre class="diff">` with `<span class="add">` / `<span class="del">` per line.
   - ```mermaid → `<div class="diagram"><pre class="mermaid">…</pre></div>` with the minimal `%%{init}%%` + the classDef component kit (see `references/mermaid-guide.md`), and the loader present. **HARD RULE: never emit `{{ }}` or `{ }` placeholders inside a mermaid block** — they collide with mermaid node syntax and break the parse. Write LITERAL, concrete lowercase labels at generation time. State diagrams: ids can't contain spaces/braces, use the `s1 : etiqueta` form. Style nodes with `class id hero|step|cool|ok|bad`, not themeVariables.
   - the ONE conclusion of the report → `<div class="takeaway">` (solid orange
     block, black type, hard contrast). At most one per report — it is loud on
     purpose. Everything else stays flat prose.
   - status words / tags → `<span class="chip ok|work|stop">`. Group two or more
     tags in a `<div class="chips">…</div>` row (they wrap side by side) — prefer a
     couple of short, specific tags over one long catch-all chip.
   - keep the hero hook to ONE tight line — no trailing filler clauses ("· la idea
     completa en cuatro pasos" and the like). The number, title and one hook line
     carry the top; don't pad it.
   - icons → inline Lucide SVG (`references/icons.md`); one accent icon per section, orange `.icon-lg` for a hero.
   - **images** (only if the caller passes one) → `.figure` component (see Images below). One image per section, room around it.
5. **Emit ONE file.** All CSS inline (`design-tokens.css` verbatim inside
   `<style>`), fonts via Google Fonts `<link>`, mermaid via CDN `<script>`,
   icons inline SVG. No external CSS/JS files. **Exception:** interactive
   compare reports may add one **inline** vanilla-JS block (IIFE tab switcher) —
   see `references/interactive-compare.md`. **Never React** and no npm/bundler.
6. **Validation gate (mandatory).** See below — run it before saving/reporting.
7. **Save a local copy & report (MANDATORY — always).** ALWAYS persist the
   artifact to disk before anything else downstream. There is **no** in-memory /
   send-only path: every report MUST leave a copy in a folder, every time, with
   no asking. Canonical archive dir is `~/Documents/kskill-report/` (create it with
   `mkdir -p` if missing); write `~/Documents/kskill-report/<slug>-YYYYMMDD.html`. If the
   user named a different target folder in the request, ALSO write a copy there,
   but the `~/Documents/kskill-report/` archive copy is always written regardless. Tell the
   user the absolute path(s). If a chrome-devtools MCP is available and they want
   a preview, offer to open it. **Never** deliver a report (Telegram or
   otherwise) without first having written its local copy — the saved file is the
   source of truth that the send step reuses.
8. **Auto-send to Telegram (mandatory, no asking).** After the gate passes and
   the file is saved, ALWAYS send it to kodex's Telegram — do NOT ask first,
   this is the default close of every report. Invoke the `kskill-send-to-telegram`
   skill (or its direct Bot API path) with the saved `.html` as a
   `sendDocument`, caption = the report's `<h1>` + one-line summary. Send the
   self-contained `.html` itself (it carries all CSS inline; fonts/mermaid load
   from CDN when opened), NOT a screenshot. Report the returned `message_id`. If
   the send fails, surface the error and the local path so the user still has
   the artifact. The only time to skip the send is if the user explicitly says
   "no lo mandes" / "solo local" in the same request.

## Validation gate (mandatory)

After emitting the HTML artifact and BEFORE delivering it, run the deterministic
mermaid validator:

```bash
python3 skills/kskill-report/scripts/validate_mermaid.py <artifact.html>
```

- Exit `0` → all mermaid blocks pass; proceed to save & report.
- Exit `1` → at least one block is broken. Read the per-block report, FIX the
  offending block (almost always a `{{ }}` brace collision or a bad
  stateDiagram id), and re-run. Loop until exit `0`.
- **NEVER deliver an artifact that fails the gate.**

Tier 1 (stdlib, always runs) catches the brace collision and bad state ids
deterministically. Tier 2 renders each block through `bunx @mermaid-js/mermaid-cli`
(`PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium`, `--no-sandbox`) for an
authoritative parse; it degrades to a WARN (Tier-1-only) if bun/mmdc is absent —
the gate still blocks brace bugs. `--selftest` runs bundled fixtures.

## Images (only when the caller attaches one)

Images are an **input**, like the markdown — never invent or generate them. The
caller passes a photo by **local file path** (or pastes one; if pasted, ask for
or save it to a path first). Default handling is **local reference, not
embedding**:

1. Copy the image into an `assets/` folder beside the saved report
   (`<report-dir>/assets/<name>`), keeping the original untouched.
2. Reference it **relatively**: `<figure class="figure figure--veil"><img
   src="./assets/<name>" alt="…"><figcaption>… · uso local</figcaption></figure>`.
   For an empty placeholder, use the `.image-slot` variant.
3. **WARN the user, every time an image is used:** *"La imagen es de **uso
   local** — se ve al abrir el .html en esta máquina (con su carpeta `assets/`),
   pero NO viaja si mandás solo el .html por WhatsApp. Para un archivo realmente
   portable, pedímelo incrustado (base64)."* Only base64-embed (`data:` URI
   inside the `<img src>`) if the user explicitly asks for a portable single file.

Keep images tidy: one per section, the `.figure` framing, optional `--veil` warm
overlay. Treat them as moments, not wallpaper.

## Template mapping (markdown intent → template)

| If the request / content is… | use `references/templates/…` |
|---|---|
| status / progress of a task, with recent code snippets + a flow (the canonical case) | `status-report.html` |
| explaining a concept: a big question answered in steps, diagram-heavy | `concept-explainer.html` |
| weighing two options / tools / approaches side by side | `comparison.html` (orange = A, teal = B) |
| same as comparison but reader should **toggle** sides (buttons, topology/workflow depth) | `comparison-interactive.html` + `interactive-compare.md` |
| one or few numbers that matter (metrics, counts, money) | `stat-highlight.html` |
| a decision made + brief rationale, or a wrap-up summary | `decision-summary.html` |

If content mixes intents, lead with the dominant one and fold the rest in as
sections; do not stitch two templates into a Frankenstein.

## Hard constraints (never violate)

- **Mobile-first, not mobile-only**: `<meta name="viewport" content="width=device-width, initial-scale=1">`, single column, tap-sized targets. The phone layout is the base (~480px); the CSS adds progressive desktop enhancement at `≥768px`/`≥1024px` (wider column ~660/880px, larger display type, bigger glow). First ≠ only — it must read well on desktop too. Keep this responsive layer; do not strip it back to a fixed narrow width.
- **Dark by default**: warm near-black bg, cream text, ONE off-center orange radial glow (`.po-glow`). Ration the orange — roughly one orange accent per section.
- **Type**: Nunito 400/500/800 + DM Mono for code/terminal, via Google Fonts CDN. Lowercase headings; the only uppercase is the kicker eyebrow.
- **Surface**: as few shapes as possible — flat flow, squared corners (pills only for chips), 1.5px hairlines, NO drop shadows (only the orange halo). Prefer the browser defaults over a new box; a left rule beats a card. Liminal slow fades, gated behind `@media (prefers-reduced-motion: no-preference)` so WhatsApp/print previews show the end state.
- **Mermaid has priority over everything else on the page.** Full width, centred,
  no background, no frame, no card. Size contract (RULE 3 in `mermaid-guide.md`,
  enforced by the loader script — paste it verbatim, never hand-tune a diagram):
  vertical ≥ `800px` and then unbounded, **never** vertical scroll; horizontal
  scrolls when needed (thin orange hairline under the diagram, invisible when it
  isn't), and **shapes never shrink** — the scale is `max(1, 800/height)`,
  upscale-only. Same minimum legible scale for the simplest and the biggest
  diagram alike. **No white background anywhere inside the svg.**
- **The templates embed `design-tokens.css` verbatim** in their `<style>`. It is
  a generated copy, not a fork: never hand-edit CSS inside a template — change
  `references/design-tokens.css` and re-inline it into the six templates.
- **Self-contained**: a single `.html`. Inline CSS, CDN `<link>`/`<script>` only for fonts and mermaid. Prefer inline SVG icons over JS. Interactive compare: vanilla JS only (tab IIFE from `interactive-compare.md`) — no React/Vue/framework of the week.
- **Voice** (if generating copy): terse, lowercase, pointers not paragraphs; Spanish rioplatense when the content is Spanish; middot `·` for beats, arrow `→` for transformation.

## References

- `references/design-tokens.css` — the `:root{}` + base classes to embed verbatim.
- `references/mermaid-guide.md` — intensive-mermaid theming: the `%%{init}%%` block, load strategy, worked in-palette examples.
- `references/icons.md` — Lucide inline-SVG playbook + 12+ ready glyphs + Simple Icons for brand logos.
- `references/templates/` — 6 templates (5 static + `comparison-interactive.html`).
- `references/interactive-compare.md` — tab switcher contract (`data-compare-panel`), nav markup, inline script. Use for A-vs-B reports with buttons.
- `references/EXTRACTED-DESIGN-SYSTEM.md` — full rationale / token provenance (consult only for judgment calls).
- `scripts/validate_mermaid.py` — the mandatory validation gate (Tier-1 stdlib lint + Tier-2 mmdc parse; `--selftest`).

**Design SSOT.** This system is also vendored into the design repo at
`~/Dev/design.kodexarg.com` (`src/styles/report.css` + `docs/report-lineage/`),
the home that serves other `*.kodexarg.com` projects. The copies under
`references/` here are the skill's working set; keep them in sync with the design
repo if the design changes.

## Self-check before delivering

- One file, opens offline except fonts/mermaid CDN.
- Renders on a 390px phone AND a desktop window with no horizontal scroll (except inside `pre`/`.diagram`); desktop shows the wider centered column, not a tiny strip.
- Orange is rationed; glow present once; headings lowercase; kicker uppercase.
- Any mermaid block carries the dark theme init; diagrams match the report.
- Local copy ALWAYS written to `~/Documents/kskill-report/` (+ any user-named folder) and its absolute path reported — no report is ever send-only.
- Sent to Telegram automatically (step 8) and `message_id` reported — unless the user explicitly asked to keep it local.
- Interactive compare: every panel tagged; tabs work on phone (44px targets); `contrast` mode has side-by-side `.compare-row`.
