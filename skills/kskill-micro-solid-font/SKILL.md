---
name: kskill-micro-solid-font
description: >
  Slash /micro-solid-font. Render uppercase text as a 3-row
  variable-width solid block font (█ and space only). Use for
  banner words, cowsay legends, QUICK WIN, GITHUB TASK, GOAL!.
  Triggers: micro-solid, block font, 3-row font, QUICK WIN art.
  Run skills/kskill-micro-solid-font/render.py. Do not hand-draw
  letters. Glyphs live in font.py — that file is the font.
---

# kskill-micro-solid-font

Three rows. Solid `█` cells. Variable width. This is the banner
font for `/cowsay` legends and for any other all-caps shout.

The glyph dictionary in `font.py` **is** the font. Do not copy
letters into a prompt. Do not invent a fourth row.

## Alphabet

A–Z, space, and `!`. Lowercase folds to uppercase. Any other
character is a 3-wide blank — it does not become a new letter.

Width is per glyph, not a fixed 3×3 cell:

| Width | Glyphs |
|---|---|
| 1 | `I`, `!` |
| 3 | the rest of A–Z except `M` and `W` |
| 5 | `M`, `W` |
| 2 | space |

`O` is the diamond (` █ ` / `█ █` / ` █ `) so it does not collide
with `G` (full box). `S` is the zigzag (` ██` / ` █ ` / `██ `).
`!` is stem, gap, dot (`█` / ` ` / `█`).

## Do this

1. Take the string (already the words to show).
2. Run, from the repo root:

   ```bash
   python skills/kskill-micro-solid-font/render.py "QUICK WIN"
   ```

3. Show stdout in a fenced `text` block. Do not paraphrase.

`/cowsay` legends go through this renderer. Do not put a second
copy of the glyphs in `kskill-cowsay`.

## Locked examples

These three strings are the visual contract. If a glyph change
breaks one of them, the glyph is wrong, not the example.

- `QUICK WIN`
- `GITHUB TASK`
- `GOAL!`

## Do not

- Hand-draw a letter.
- Add a row, a shade, or a serif.
- Duplicate the dictionary into cowsay or a chat reply.
- Treat a blank (unknown character) as permission to design a digit
  or punctuation mark. Add the glyph in `font.py` first, with a test.
