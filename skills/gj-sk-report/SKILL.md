---
name: gj-sk-report
title: Mobile-first low-verbosity HTML reports (English)
type: skill
status: active
version: v0.1.0
tags: [skill, report, mobile, diagram-design]
description: >
  Converts a given markdown summary into ONE self-contained, mobile-first,
  low-verbosity dark HTML report. Diagrams are produced via diagram-design
  (SVG embed), not Mermaid CDN. Soft Presentation Orange chrome; diagram-design
  owns visuals. English delivery. Twin: gj-sk-reporte (identical, Castellano).
  Use when kodex asks for a report, status HTML, phone/WhatsApp summary, or
  /gj-sk-report. Replaces kskill-report.
---

# gj-sk-report

Convert a **given** markdown summary into one self-contained dark HTML file —
**mobile-first**, **low verbosity**, phone-readable. Fill templates; do not
invent a new look.

Spanish twin (identical pipeline): `gj-sk-reporte`.

## Responsibility

**One job:** markdown → HTML in this fixed format.

> Default source = last assistant answer when no markdown/file is attached.
> Explicit content in the same turn wins. Do not re-summarize from scratch
> unless the caller asks for a rewrite. If there is no prior answer and no
> markdown, ask once and stop.

- Not a researcher. Convert (and lightly compress per [voice.md](references/voice.md)).
- Fast and deterministic. No design deliberation.

## Non-negotiables

1. **Mobile-first** — base ~480px; enhance at ≥768 / ≥1024. Viewport meta required.
2. **Low verbosity** — default terse ([voice.md](references/voice.md)). Expand only on express request (verbose / full / largo / completo).
3. **diagram-design for visuals** — when a diagram earns its place, follow [diagram-bridge.md](references/diagram-bridge.md). Prefer minimal-dark SVG embeds. No Mermaid CDN by default.
4. **kskill-report spirit** — single artifact, template by intent, archive to disk, auto-Telegram, one takeaway, rationed accent. Soft glow / chips / squared flow live in [shell.css](references/shell.css); diagram-design tokens/fonts lead.

## Pipeline

1. Read [shell.css](references/shell.css) (embed verbatim) and [voice.md](references/voice.md).
2. Take supplied markdown (or last answer). Compress to low-verbosity structure unless asked otherwise.
3. Detect diagram needs → invoke **diagram-design** per [diagram-bridge.md](references/diagram-bridge.md); extract `<svg>` for embed.
4. Pick a template from `references/templates/` (table below). Copy as skeleton.
5. Fill placeholders. Map:
   - `#` / `##` → `<h1>` / `<h2>` (lowercase)
   - eyebrow → `<p class="kicker">`
   - paragraphs / lists → sparse HTML; ration `<strong>`
   - fenced code → `<pre><code>`; diffs → `<pre class="diff">` with `.add` / `.del`
   - diagrams → `.diagram > .dd-frame > <svg…>` (from diagram-design)
   - conclusion → one `.takeaway`
   - status tags → `.chip.ok|work|stop` inside `.chips`
6. Emit one `.html`. Inline CSS only (+ Google Fonts). Interactive compare may add the vanilla tab IIFE from [interactive-compare.md](references/interactive-compare.md). Never React.
7. **Validation gate** (mandatory):

```bash
python3 skills/gj-sk-report/scripts/validate_report.py <artifact.html>
```

Exit 0 only. Fix leftovers / viewport / Mermaid CDN / a11y until green.

8. **Save always** to `~/Documents/gj-sk-report/<slug>-YYYYMMDD.html` (`mkdir -p`). If the user named another folder, write there too; the Documents archive is always written. Report absolute path(s).
9. **Auto-send Telegram** (mandatory unless "no lo mandes" / "solo local"): use `kskill-send-to-telegram` with the saved `.html` as `sendDocument`, caption = `<h1>` + one-line hook. Report `message_id`. On send failure, still surface the local path.

## Template mapping

| Intent | Template |
|---|---|
| status / progress (+ optional flow) | `status.html` |
| concept explained in steps + picture | `concept.html` |
| two options side by side | `comparison.html` |
| same, with toggle tabs | `comparison-interactive.html` |
| one or few numbers | `stat.html` |
| decision + short why | `decision.html` |

Lead with the dominant intent; do not stitch two templates.

## Images

Only if the caller passes a path. Copy beside the report under `assets/`, reference relatively with `.figure`. Warn: local use only unless they ask for base64 embed.

## Hard constraints

- Self-contained single `.html`.
- Dark shell; one soft orange glow; accent rationed.
- Type: Instrument Serif (display) + Geist + Geist Mono (diagram-design).
- Mermaid CDN is a gate failure unless the caller explicitly demanded live Mermaid.
- After CSS changes: edit `references/shell.css`, then re-inline into all six templates.

## Language

English prose in the artifact. For Castellano use **`gj-sk-reporte`** (identical skill).

## References

- [shell.css](references/shell.css) — chrome tokens (embed verbatim)
- [diagram-bridge.md](references/diagram-bridge.md) — diagram-design integration
- [voice.md](references/voice.md) — low-verbosity rules
- [interactive-compare.md](references/interactive-compare.md) — tab IIFE
- `references/templates/` — six skeletons
- `scripts/validate_report.py` — mandatory gate

## Self-check

- [ ] Mobile viewport; reads on ~390px and desktop
- [ ] Low verbosity unless asked otherwise
- [ ] Diagrams are diagram-design SVG (or none)
- [ ] Gate exit 0
- [ ] Saved under `~/Documents/gj-sk-report/`
- [ ] Telegram sent (or explicitly skipped) with `message_id` / error
