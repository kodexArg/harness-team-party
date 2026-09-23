---
title: Product requirements
type: reference
status: active
version: v0.1.0
tags: [prd, product]
description: "Purpose, users, and acceptance for the code in this repository."
applies_when:
  - When deciding whether work serves the repository.
  - When evaluating acceptance.
related_adrs:
  - adr-00-adr-doctrine
---
# PRD — harness-team-party

This repository holds the skills and checks used to work in the tree: a code graph, diagram tooling, and session stance skills, with tests that keep those wires intact.

## What we are building

A repository that:

1. Explores code through Graphify (`kskill-graphify`) before text search.
2. Draws diagrams through `diagram-design`.
3. Sets a session stance through `kskill-mood` and `kskill-qw`.
4. Proves the wiring with `tests/`.

## Who it is for

- People changing this repository, who need the graph, the skills, and a test run that fails when the wiring breaks.
- Agents working in the tree, who need `docs/PRD.md`, `docs/INTERFACES.md`, and the ADRs loaded before they edit.

## Purpose

Keep the code small and the contracts written down, so a change to a skill, a hook, or the graph is visible in docs and in `pytest`.

## User stories

```gherkin
Scenario: Explore the tree
  Given graphify-out/graph.json is present
  When an agent looks up a symbol
  Then query_graph returns the node before Grep or Read

Scenario: Missing graph
  Given graph.json is absent
  When a session starts
  Then skills/kskill-graphify/bin/ensure runs and Grep is the fallback only after that

Scenario: Ship a change
  Given tests cover the change
  When the branch is opened as a pull request
  Then CI runs pytest tests/
```

## Acceptance criteria

- `uv run --with pytest pytest tests/ -q` passes.
- `graphify-out/graph.json` is tracked and contains nodes.
- `OPENROUTER_API_KEY` and `OPENROUTER_MODEL_ID` are declared in `docs/VARIABLES.md` and seeded from `.env.example`. The key value lives only in gitignored `.env`.
- Docs name the skills and scripts that exist, and do not describe files that have been removed.
