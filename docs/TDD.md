---
title: Service Test-Driven Development instruction manual and TDD lifecycle
type: reference
status: active
version: v0.1.4
tags: [harness, tdd, service, testing]
description: "Manual for framework-bound service TDD plus the Paladin test-after and Adventurer single-agent paths."
applies_when:
  - When initiating service development through the TDD flow.
  - When authoring TDD specifications under docs/tdds/.
related_adrs:
  - adr-02-stack
  - adr-03-backend
---
# TDD — instruction manual for `docs/tdds/`

Dedicated owner: **The Trickster** (`hb-ag-test`) via `hb-sk-tdd`. The Dwarf implements after red and never writes this tree or the tests. The Paladin implements pure Python logic before The Trickster tests it. An eligible Adventurer owns both sides of its one small task.

Every new framework-bound service piece is born here, wherever its subject exists ([[DEVELOPMENT-LOOP]]). This manual rules the format; the `tdd-NN` entries live under `docs/tdds/`.

## Scope

This manual is the `docs/tdds/` service specification. Surface testing follows the surface architecture doc. The Trickster writes tests on the normal specialist paths (and may load `hb-sk-surface-framework`). The Adventurer is the only test-writing exception, limited to its eligible single-agent lane.

## Purpose

From activation onward, every framework-bound service integration is **born here**. `docs/tdds/` is where models, persistence, handlers, permissions, routes, and framework adapters start. Pure Python business logic and complex script cores use the Paladin path below.

## The specialist flow

1. An approved [[INTERFACES]] row exists — The Cleric wrote it (the contract comes first).
2. The Trickster creates `docs/tdds/tdd-NN-slug.md` — sequential `NN`, kebab-case slug — following the section layout described below.
3. The Trickster writes the failing tests the entry lists. Run them; they must fail.
4. The Dwarf writes the model changes and implements until the tests can pass.
5. The Trickster greens / adds more. No shadow tests from other agents.
6. The Trickster marks the entry `done`.

## Bounded alternate paths

### The Paladin — implementation, then tests

Framework-neutral Python business rules and complex script cores do **not** open a TDD entry. The Paladin implements the smallest coherent pure core, runs static checks and existing tests, then Agents The Trickster with the changed paths, invariants, and edge cases. The Trickster writes focused tests afterward.

This path ends as soon as the change needs a framework model, migration, persistence adapter, handler, permission, route, payload, or interface. That work returns to the specialist flow above; the Paladin path is not a route around service TDD.

### The Adventurer — one agent, applicable order

When the parent validates an Adventurer lane under [[ISSUE-TRIAGE]], The Adventurer may write both production code and tests for that one task. A framework-bound service task still creates the TDD entry and goes red → implementation → green inside the same agent. A genuinely Paladin-shaped pure Python task implements first and adds tests afterward. Ineligible scope returns to the specialist owners without an Agent call from The Adventurer.

## Entry frontmatter contract

Every entry carries:

```yaml
title: tdd-NN-slug
type: tdd
status: draft | red | green | done
created: YYYY-MM-DD
api: []        # list of the [[INTERFACES]] rows/paths this entry covers
tags: [tdd]
```

Status transitions:

- `draft` — entry written, tests not yet coded.
- `red` — tests exist and fail; implementation may begin.
- `green` — implementation passes every listed test.
- `done` — implementation notes filled; entry closed.

An entry covers a single coherent unit of code: a model plus its handlers, a service, a command. Entries are small. If an entry needs a plural of concerns, split it.

## Entry layout

Every entry follows the frontmatter contract and flow above; a project's first entry sets the section layout that the rest reuse (`docs/tdds/tdd-00-template.md`). Do not invent divergent layouts.
