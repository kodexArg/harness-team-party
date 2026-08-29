---
name: hb-sk-hound
title: Keyword codebase scout — Graphify then Grep
type: skill
status: active
version: v0.1.3
tags: [skill, hound, scout, codebase]
description: >
  Codebase scout for The Hound: Graphify first on Hunter clues
  (tags, keywords, symbols), then Grep/Read, then an ordered catalog
  of full paths and short excerpts. Load when The Hunter (or a Hound
  dispatch) needs code scent without opening the tree itself — even
  if the skill is not named. Triggers: hound, sabueso, keyword search,
  code clues, tags. Owner: The Hound (hb-ag-hound) only. The Hunter
  Agents this familiar; it does not load this skill itself.
applies_when:
  - When searching the codebase by keyword or tag clues for The Hunter
  - When The Hound is dispatched with a clue list
related_adrs: []
---

# hb-sk-hound

Knowledge contract for **The Hound**. Follow clues in the tree. Very cheap. Then stop.

## Load

The clue list from The Hunter is the scent. Do not load [[PRD]] or [[INTERFACES]]. Graph: [[adr-35-graphify]] first. Graph absent → Grep the clues ([[adr-35-graphify]] rule 5).

## Order

1. **Graphify.** `query_graph` per clue (or one query that names them). `get_neighbors` when a hit is a leaf. Record path + symbol.
2. **Grep / Read** only those files (or Grep-first if no graph). Keep excerpts short.
3. **Catalog.** Strongest scent first. Cap ~8 rows. Stop.

No `Bash`. No `gh`.

## Catalog

```
HOUND
clues: [tag, ...]
hits:
  - path: <repo-relative, full from repo root>
    symbol: <function/class/heading or —>
    lines: <start-end>
    excerpt: <≤8 lines>
    clue: <which clue hit>
    why: <one line>
```

Paths are complete. The Hunter must be able to evaluate without opening the file.

## Quick exit

A GitHub issue history question is The Hawk. A bulletin is The Hunter. Empty catalog + one line beats a long run.

## Do not

- `gh` or `git`.
- Dump whole files. Follow clues that were not in the brief.
- Agent anyone. Load area-owner skills.
- Write a triage score.

## Instantiation

This is a template skill: rename the folder to `{{prefix}}-sk-hound`.
See [[ONBOARDING]] and [[CLONE]].
