---
name: hb-sk-tdd
title: TDD entries for this project's service — knowledge contract
type: skill
status: active
version: v0.1.4
tags: [skill, tdd, trickster]
description: >
  Writes docs/tdds/tdd-NN-slug.md entries and walks draft→red→green→done
  for framework-bound service work, and recognizes the Paladin's
  no-entry test-after path. Load when a service piece needs a TDD spec,
  a failing test list, a status transition, or post-Paladin tests —
  even if unnamed. Owner: The Trickster. Not the catalog or handler.
applies_when:
  - When authoring or transitioning a TDD entry under docs/tdds/
  - When a service unit of work has no tdd-NN spec yet
  - When listing the failing tests an entry must write first
related_adrs:
  - adr-02-stack
---

# hb-sk-tdd

Knowledge contract for **The Trickster**. Teach how this service is born in `docs/tdds/`, then stop. The Dwarf forges; you write the spec and the snare.

## Load

1. Read [[TDD]] (the manual). Copy section layout from `docs/tdds/tdd-00-template.md` — do not invent a parallel shape.
2. Classify the caller. Framework-neutral Python logic already implemented by The Paladin uses [[TDD]]'s test-after path: create no TDD entry, move to `hb-sk-test-runner`, and test the supplied invariants. Framework-bound work continues below.
3. Confirm a framework-bound need is a declared row in [[INTERFACES]] (read). Missing row → return to the caller; The Cleric writes the catalog. You do not.
4. Look at a neighbor entry in `docs/tdds/` for tone and grain. Entries are small: one model-plus-endpoints, one service, or one command.

## Why a spec before code

An unspecified framework integration has no trap to walk into. The Dwarf who forges without a red test is guessing. The entry is the contract between the Cleric's row and the test runner — not a diary of the implementation. The Paladin path is deliberately different: the pure rule exists first, and the later trap proves its invariants without inventing a retroactive TDD record.

## Frontmatter

```yaml
title: tdd-NN-slug
type: tdd
status: draft | red | green | done
created: YYYY-MM-DD
api: []        # [[INTERFACES]] paths this entry covers
tags: [tdd]
```

`NN` is the next unused sequential number (numbers have collided before — do not reuse a taken `NN`). Slug is kebab-case. `tdd-00-template` stays `draft` forever.

Status only moves forward: `draft` (spec, no tests yet) → `red` (tests exist and fail) → `green` (the Dwarf's code passes them) → `done` (implementation notes filled, entry closed).

## Sections (from the template)

| Section | What it is for |
|---|---|
| Context | Why this piece exists: the [[INTERFACES]] row, the issue, the need. `api: []` only when there is no route, and say so. |
| Design | Chosen shape and rejected alternatives. Placement, cache, [[VARIABLES]]. Not the test file. |
| Tests | Path `{{service tree}}/<area>/test_<subject>.*` and the traps **one by one**. They hit real routed handlers and the real database — not a stand-in for the product. |
| Status | How red became green. Empty until it did. |

Optional later: **What is deliberately absent** — a bound, not a backlog.

## The Trickster's two service paths

Cleric row → write the entry (`draft`) → write the failing tests (`red`, `hb-sk-test-runner`) → **stop**. The Dwarf forges the model and the handler. You re-run the slice and mark `green` / `done`. You do not implement the handler.

Paladin implementation → inspect changed paths and invariants → write focused tests with `hb-sk-test-runner` → run the slice → return failures or green. No `docs/tdds/` entry. You do not rewrite the pure rule.

Surface testing is not this flow ([[TDD]] scope). Components → surface tests via `hb-sk-surface-framework` when needed.

## Do not

- Skip `red` on the Dwarf path, or fabricate a retroactive TDD entry on the Paladin path.
- Write `docs/INTERFACES.md` or the handler.
- Load Elf / Cleric / Wizard / Inquisitor skills. Test-runner craft is `hb-sk-test-runner`.
- Fork the manual. [[TDD]] owns format; you fill entries.

## Instantiation

This is a template skill: replace every `{{placeholder}}`, then rename the
folder to `{{prefix}}-sk-tdd`. See [[ONBOARDING]] and [[CLONE]].
