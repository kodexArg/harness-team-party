---
title: Roadmap and current stage
type: reference
status: active
version: v0.1.0
tags: [roadmap, stages, ssot]
description: "The project's stages and which one is current. Ships as a placeholder."
applies_when:
  - When checking what stage the project is in.
  - When planning work against the next stage.
related_adrs:
  - adr-05-after-versioning
---
# ROADMAP

> This file is **expected** and currently a placeholder. It is the single
> source of truth for stage state; other docs deliberately do not restate it,
> because a second copy goes stale the moment a stage moves.

## What it must eventually contain

- **The stages** — the project's own stage list, each with a one-line exit
  condition: `{{stage 1}}`, `{{stage 2}}`, `{{stage 3}}`, …
- **The current stage** — exactly one, marked plainly.
- **What is settled** — the decisions already landed, stated as facts with
  their ADR or issue links.

Instantiation writes the first stage list when [[PRD]] is filled ([[CLONE]]).
