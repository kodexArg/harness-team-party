---
name: kskill-cowsay
description: >
  Slash /cowsay. kodexArg/cowsay renderer (stdlib bin/cowsay) with
  this project's micro-solid legends replacing the animal: QUICK WIN,
  GH ISSUE, GH REPO, EPIC DONE!. Stop brief is Tux and an {{interface language}}
  balloon, no legend. Triggers: /cowsay, cowsay, QUICK WIN, EPIC DONE.
  Run skills/kskill-cowsay/bin/cowsay --legend TOKEN or
  skills/kskill-cowsay/render.py --legend TOKEN. Never freehand.
  Homepage: https://github.com/kodexArg/cowsay
---

# kskill-cowsay

Vendored from [kodexArg/cowsay](https://github.com/kodexArg/cowsay)
(MIT). **The renderer is law** — run the binary; do not freehand the
balloon or the figure.

**Tux close-out:** `bin/cowsay -f tux`. Balloon text is **always {{interface language}}**, even when `/kdx-en` is on. Slash `/cowsay` only — there is no Stop hook.

**`/qw` close-out:** a closed micro-solid legend **replaces** the
animal. Glyphs live in `kskill-micro-solid-font`. Do not copy them here.

## Closed legend set

| Token | When |
|---|---|
| `QUICK WIN` | `/qw` / quick-win close-out only |
| `GH ISSUE` | a GitHub issue was opened or closed as the point of the turn |
| `GH REPO` | a repository-level announcement |
| `EPIC DONE!` | an epic (or equivalent multi-issue arc) landed |

Any other `--legend` token falls through to the default cow. Do not
invent a fifth legend. Matching is case-insensitive; spaces and `!`
are part of the token.

## Do this

Stop brief ({{interface language}} balloon, Tux):

```bash
python3 skills/kskill-cowsay/bin/cowsay -f tux <<'EOF'
Resumen corto en español.
EOF
```

`/qw` legend:

```bash
python3 skills/kskill-cowsay/bin/cowsay --legend "QUICK WIN" -W 40 -- "done"
# same:
python3 skills/kskill-cowsay/render.py --legend "QUICK WIN" -- "done"
```

Omit `--legend` for the bundled cow (`default` / `moose` / `tux` via
`-f`, same as kodexArg/cowsay). Show stdout in a fenced `text` block.
Do not paraphrase the art.

## Do not

- Draw the letters or the balloon by hand.
- Put a cow *and* a legend on the same print.
- `apt install cowsay` or invent a fifth legend.
- Duplicate the glyph table from `kskill-micro-solid-font`.
