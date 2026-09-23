---
title: Roadmap and current stage
type: reference
status: active
version: v0.1.0
tags: [roadmap, stages]
description: "Current stage of this repository."
applies_when:
  - When checking what stage the project is in.
related_adrs:
  - adr-07-git
---
# ROADMAP

## Current stage

**v0.1.0 — code baseline.** The tree is the skills, the code graph, the hooks, and the tests.

## Settled

- `main` is the trunk. Changes land through pull requests ([`adrs/adr-07-git.md`](../adrs/adr-07-git.md)).
- Graphify is the first exploration step when `graph.json` is present ([`adrs/adr-35-graphify.md`](../adrs/adr-35-graphify.md)).
- English is the language of code and technical docs ([`adrs/adr-01-nomenclature.md`](../adrs/adr-01-nomenclature.md)).
- Local model access is OpenRouter via `.env` ([`docs/VARIABLES.md`](VARIABLES.md)).
