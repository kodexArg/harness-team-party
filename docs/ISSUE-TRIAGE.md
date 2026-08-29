---
title: Generic issue triage nomenclature
type: reference
status: active
version: v0.1.4
tags: [harness, github, issues, triage]
description: "Three-axis issue scoring vocabulary and the bounded Adventurer single-agent eligibility calculation."
applies_when:
  - When scoring an issue as triaged versus leaving it untriaged.
  - When reading historical issues that carry mixed label glyphs.
  - When deciding autonomous versus supervised merge from issue labels.
  - When deciding whether a small task qualifies for The Adventurer.
related_adrs:
  - adr-08-github
---
# ISSUE-TRIAGE — scoring vocabulary

> A resource, not a rule. Triage is optional and uncommon. When it happens, these three axes are the names. Label spellings live in [[GITHUB]].

Issues may be filed without scores. That is the untriaged path ([[adr-08-github]] rule 3): a PR from an untriaged issue, or an orphan PR, is supervised. A **triaged** issue is one that carries one score on each axis below plus at least one domain. That is the whole bar.

## Axes

Three independent 1–3 scores. One label per axis. The stem is the name; the glyph is decoration.

| Axis | Asks | `1` | `2` | `3` |
|---|---|---|---|---|
| **severity** | How much it hurts today | cosmetic / nice-to-have | real recurring friction | broken, blocking, or data at risk |
| **collateral** | Blast radius of the change | isolated / new files | shared surface, few consumers | wide shared state or many consumers |
| **effort** | Size of the work | mechanical, one pass | investigation, iteration, tests | architectural, multi-session |

If the fix clearly needs a heavyweight model, effort is never `1`.

Canonical label stems: `severity:N`, `collateral:N`, `effort:N`. Prefer the single-glyph form on new issues (`🟢 severity:1`, `📦 collateral:2`, `⚙️ effort:2`).

## Domain

At least one of: `service`, `surface`, `infra-cicd`, `harness`. More than one is allowed.

## Adventurer lane

A task is a score candidate for The Adventurer (`hb-ag-adventurer`) when it has one score on every axis and:

`severity + collateral + effort < 5`

Because each axis has a minimum of `1`, this permits only `1/1/1` and permutations of `2/1/1`; an axis at `3` necessarily makes the total at least `5`. The explicit checks are therefore **total below 5** and **no axis above 2**.

The parent dispatches this lane from a completed triage card or Hunter bulletin. The Hunter records the scores but does not call a builder. Missing scores, a total of `5+`, an axis at `3`, an unresolved decision, or an excluded governance boundary returns the task to normal [[ADND-DISPATCH]].

## Optional, only if clearly true

Type and qualifier labels from the [[GITHUB]] fixed set (`bug`, `feat`, `enhancement`, `docs`, `tech-debt`, `security`, `performance`, `needs-repro`, `needs-design`, `complex`, …). ADR labels (`📜 adr` plus `adr-NN`) only when an existing ADR governs the work.

## What this is not

- Not a requirement to score every issue. Both scored and unscored issues are valid.
- Not merge authorization. The three-tier model (triaged / untriaged / orphan) is [[adr-08-github]] rule 3; this file only names the scores that make an issue triaged.
- Not permission to bypass [[INTERFACES]], ADR, Git/GitHub, secret, or deployment ownership. The Adventurer's agent contract closes those boundaries.
