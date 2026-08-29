---
name: hb-sk-hawk
title: Historical issue scout — Graphify then GitHub
type: skill
status: active
version: v0.1.3
tags: [skill, hawk, issues, scout]
description: >
  Historical-issue scout for The Hawk: Graphify first on the Hunter
  brief, then gh issue search, then a cheap repetition verdict.
  Load when The Hunter (or a Hawk dispatch) needs prior-issue
  forensics — even if the skill is not named. Triggers: hawk,
  halcon, related issues, duplicate issue, previously attempted.
  Owner: The Hawk (hb-ag-hawk) only. The Hunter Agents this
  familiar; it does not load this skill itself.
applies_when:
  - When searching this repo's past issues for repetition or prior attempts
  - When The Hawk is dispatched with an issue brief
related_adrs:
  - adr-08-github
---

# hb-sk-hawk

Knowledge contract for **The Hawk**. Aim with the graph, then fly GitHub. Very cheap. Then stop.

## Load

The brief from The Hunter is the map. Do not load [[PRD]] or [[INTERFACES]]. Issue thread fetch: [[GITHUB]] (REST comments). Graph: [[adr-35-graphify]] — first tool, not an issue index.

## Order

1. **Graphify.** `query_graph` the brief's keywords and symbols. Optional `get_node` / `get_neighbors` on one hit. Collect repo terms (file stems, handlers, labels in docs) that should appear in `gh`. Graphify does not list GitHub issues; it aims the search. Graph absent → skip to 2, still `gh`.
2. **GitHub.** This repo only. `gh issue list --state all --search "…"` and/or `gh search issues --repo {owner}/{repo}`. Include closed. Drop the current issue from the pack. Cap ~5.
3. **Thread.** For a hit that might be the same work: `gh issue view <n>` then `gh api repos/{owner}/{repo}/issues/<n>/comments`. Never `gh issue view --comments`.
4. **Pack.** Return and stop.

Auth: `. scripts/cursor_cloud_gh_auth.sh` when Issues 403 on the injected token ([[GITHUB]]).

## Pack

```
HAWK
status: novel | repeat | related
current: #<n>
hits:
  - issue: #<m>
    state: open | closed
    relation: duplicate | prior-attempt | same-area | weak
    why: <one line>
prior_attempts: <one line or none>
```

`repeat` — same defect or same ask, already filed or tried. `related` — overlapping area, not the same ask. `novel` — no useful hit.

## Quick exit

A codebase walk is The Hound. A bulletin is The Hunter. Empty pack + one line beats a long flight.

## Do not

- `git`, labels, comments, PRs.
- Grep the tree for Hound's job.
- Agent anyone. Load area-owner skills.
- Dump issue bodies in full.

## Instantiation

This is a template skill: rename the folder to `{{prefix}}-sk-hawk`.
See [[ONBOARDING]] and [[CLONE]].
