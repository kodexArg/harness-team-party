# Source design system — "Presentation Orange" (extracted SSOT)

Extracted 2026-06-13 from kodex's claude.ai design artifact
`claude.ai/design/p/71a4390d-affa-4db4-95a5-e37eb5c38276` (authenticated).
This file is the canonical reference for the `kskill-report` skill. Do NOT
re-fetch the URL (auth-walled); use the tokens below verbatim.

Original premise: *liminal large-screen presentations* — restraint, 1–5
elements per screen, soft rounded type, warm charcoal + rationed orange,
emptiness as content. The `kskill-report` skill **re-targets this aesthetic
from a 1920×1080 wall display to a MOBILE-FIRST vertical HTML report** (a piece
sent over WhatsApp, opened on a phone). Keep the *vibe and tokens*; rescale the
geometry (no 160px margins, no 220px type) for a phone viewport.

## Color tokens (verbatim)

```
--ink-1000: #0C0B09;   /* deepest warm near-black — hero/curtain backdrop */
--ink-900:  #141210;   /* slide/body background */
--ink-600:  ~#3a352f;  /* hairline borders (1.5px) */
--ink-500:  ~#6b6358;  /* day-theme secondary text */
--cream-100:#F3EEE4;   /* primary text */
--warm-200: ~#cdbfa8;  /* secondary text (warm grey→cream) */
--orange-500:#FF6A1A;  /* LEAD accent — design-system canonical */
--orange-400:~#FF8A45; /* hover lighten */
--orange-600:~#E25510; /* press / day deepen */
--teal-500: #4FA6AB;   /* Petróleo — "second voice": column B, the other tool */
--teal-300/-700        /* text-size / canvas-deep variants */
--sage-500: #87A878;   /* Salvia — organic ok/go signal: confiar, safe */
--sage-300/-700
--bg-canvas:#F1F0ED;   /* light canvas — ONLY for icon-dense index slides */
```

### kodex reconciliation (IMPORTANT)
kodex's Claude Code terminal theme is `custom:orange`
(`~/.claude/themes/orange.json`): accent/promptBorder **`#ff8c42`**, shimmer
`#ffaa70`, bg `#1a0d00`, text `#ffe8cc`. He finds this tone *relaxing* and wants
it present. RULE: lead with **`#ff8c42`** as the primary interactive/heading
accent (the relaxing terminal tone), and use the design system's deeper
**`#FF6A1A`** for the radial glow/halo and high-emphasis hits. Both oranges
coexist; `#ff8c42` is the default, `#FF6A1A` the deep punctuation.

## Type
- One family: **Nunito** (soft rounded humanist sans). Weights 400/500 body, 800 display. "Lack of variety is deliberate — rhythm from size & space, not style mixing."
- **DM Mono** ONLY for code / terminal / live-typed moments (snippets, prompts).
- Both via Google Fonts CDN. Display is enormous on the original (mega 220px / display 148px) — **on mobile rescale down** but keep the *spirit* of big, airy headings.
- Casing: lowercase almost everywhere; the only uppercase is the tiny kicker eyebrow (`03 · QUÉ ES`). No Title Case.

## Space & layout
- Original: 160px safe margin, emptiness is content. **Mobile**: generous but phone-appropriate padding (e.g. 24–32px gutters), one idea per vertical block, lots of vertical breathing room.
- Kicker pins top-left of a section; hero element owns the visual center.

## Radii & surface
- `--radius-md 16px` standard, `--radius-lg 28px` panels, `--radius-pill` chips. Nothing sharp.
- Cards rare & quiet: surface fill + 1.5px hairline border + soft corners. The "good" variant swaps border to deep orange. **No drop shadows for elevation** — the dark lifts. The only shadow is `--shadow-glow` (orange ambient halo).

## The glow / halo (kodex's "spot rojo oscuro")
- `.po-glow` / `.halo`: a single low-opacity radial blur, off-center, orange. Keeps the void alive. Use sparingly — behind a stat, a hero, or the report header.
- Deep orange `#FF6A1A` at low alpha radial-gradient on `#0C0B09`.

## Motion
- Liminal pacing, nothing snaps. Slow soft fades `--dur-slow 760ms`, entrances rise 18px OR clear 8px blur, gentle settle ease. Stagger `.d1–.d5`.
- Gate all entrance animation on `@media (prefers-reduced-motion: no-preference)` so PDF/print/WhatsApp-preview show end-state. No bounce, no infinite loops.

## Iconography — SETTLED
- **Lucide** is the chosen set. CDN `unpkg.com/lucide@latest/dist/umd/lucide.js` then `lucide.createIcons()`. Markup `<i data-lucide="shield-check"></i>`; size via font-size, color via `currentColor`. **Stroke 1.75.** Rounded even-stroke matches the rounded type.
- For a self-contained artifact that must render offline (WhatsApp), PREFER **inlining the Lucide SVG path** directly (copy the `<svg>` from lucide.dev) rather than the CDN JS — guarantees the icon shows with no network. Document both paths; default to inline SVG for portability.
- Brand/product logos: **Simple Icons** `cdn.simpleicons.org/<name>/<hex>`, recolored to theme ink — or inline the SVG.
- Typographic glyphs as icons: middot `·` (beat separator) and arrow `→` (transformation) are load-bearing, not decorative.

## Day theme (bright rooms) — optional second mode
- `data-theme="day"` on `<html>`: white field + near-black ink, accents deepen one step (orange→`#E25510`, teal→`-700`, sage→`-700`), the section-break inverts to a SOLID ORANGE field with ink text, glow disappears (replaced by solid geometry — a digit on a filled orange disc), borders go 2px Swiss, shadows removed.

## Imagery
- One image per block, room around it. Treatments: framed hero (rounded hairline panel), full-bleed + bottom scrim gradient, split. Optional warm veil (soft-light orange ~22%) to pull a photo into the charcoal/orange mood. Images are moments, not wallpaper.

## Voice (when generating copy / labels)
- Terse, lowercase, pointers not paragraphs. Spanish rioplatense if content is Spanish. Middot · for beats, arrow → for transformation. Calm, dry, confident.
