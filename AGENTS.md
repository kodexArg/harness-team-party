---
title: AGENTS
type: index
status: active
created: 2026-08-28
tags: [harness, index]
---

# AGENTS

> Entry point for project context, ownership, and tools. Load only the references required by the task.

## Instructions

Read `docs/PRD.md` first. It is the product constitution. Then read `docs/INTERFACES.md`. Every agent and subagent must hold both before planning, judging, or changing the repository.

Use this repository as the primary context. Read its contracts, docs, code, and tests before consulting external sources. When local sources disagree, name the conflict. Do not silently choose one.

Load context narrowly. Start from this index, query the graph, and open only the files relevant to the task. Do not preload the harness. If double-curly slots remain in this clone, fill them from `docs/ONBOARDING.md` first — that file is the fill-in map; this file is the runtime index.

Open `docs/DEVELOPMENT-LOOP.md` before changing code. Check the change against the PRD, applicable ADRs, and `docs/INTERFACES.md`.

Keep code and documentation in English. Render the product interface in `{{interface language}}`.

Do not invent product data, credentials, permissions, or production state. Never modify read-only upstream sources.

## Project

{{project name}} — {{one-line product statement}}.

The main flow is:

`{{main flow}}`

The service owns {{service responsibilities}}. The surface owns {{surface responsibilities}}. Authentication and authorization follow [[AUTH]].

The application deploys as {{deploy target}}. `main` is the single integration line and the production source.

Top-level structure:

- `{{service tree}}` — the service: framework integration, data, and Paladin-owned pure Python business logic.
- `{{surface tree}}` — the surface: pages, components, styles, and browser behavior. Absent in a headless project.
- `docs/` — product, contracts, architecture, operations, and workflows.
- `adrs/` — binding project decisions and rules.
- `skills/` — task-specific procedures and technical contracts.
- `agents/` — area ownership and delegation contracts.
- `tests/` — cross-repository and harness checks.
- `mcp/` — project MCP declarations.

## Context order

Use sources in this order:

1. `docs/PRD.md` for product purpose and acceptance.
2. `docs/INTERFACES.md`, applicable ADRs, and topic SSOTs under `docs/` for project contracts.
3. Code and tests for the implemented state.
4. External documentation for missing or version-specific facts.

Project contracts override generic external guidance. External research never overrides the PRD, ADRs, the interface catalog, or repository-specific stack rules.

## Tools

### 1. Repository orientation

Use Graphify before filesystem exploration. Install it when the host can: `skills/kskill-graphify/bin/ensure` (needs `uv`; no LLM key for a code-only graph). Enable the project MCP server. Worktree sessions must approve Graphify in that worktree.

- `query_graph` — find concepts, files, and dependency areas.
- `get_node` — inspect one symbol or document node.
- `get_neighbors` — find callers, parents, and dependencies.
- `shortest_path` — trace a relationship between two known nodes.

The project MCP declaration is `.mcp.json` → `mcp/mcp.json`. Graphify policy: `docs/GRAPHIFY.md` and `skills/kskill-graphify/SKILL.md`.

### 2. Local files

After graph orientation, use `Read` for named files, `rg` for text, and `Glob` for paths. Use the editor's patch tool for focused edits. Use the shell for commands, not for file discovery or file reading.

`docs/CODEMAP.md` maps documentation and ADRs back to governed code. It complements Graphify; it does not replace it.

### 3. Build and test

Use `{{service toolchain}}` in `{{service tree}}`. Use `{{surface toolchain}}` in `{{surface tree}}`. Do not substitute another package manager or lockfile owner.

Local orchestration is `{{local runtime}}`; its contract is the local-runtime section of `docs/INFRASTRUCTURE.md`. Runtime and verification commands belong in the relevant stack document or skill, not in this index.

### 4. Browser, cloud, and external systems

Use declared MCP tools through the responsible agent. **The Three Feathers** (Las Tres Plumas) is the inn: issues, PRs, and the agents that work them ([[GLOSSARY]], [[GITHUB]]). Issue hunt, the notice-board bulletin, and a later Hunter's `goal` belong to `hb-ag-hunter`. Ship (`git`, PR, merge) belongs to `hb-ag-git`. Cloud and environment operations belong to `hb-ag-ops`. Browser smoke checks are interactive and operator-run only.

Use external search after local context is insufficient. Prefer official vendor documentation for version-specific behavior.

## Skills

Skills encode the procedure and technical contract for a task. Read only the skills required by the task and permitted by the responsible agent definition; do not reconstruct their rules from memory. Product skills use `hb-sk-*`; reusable harness skills use `kskill-*`. The canonical copies are under `skills/`, with runtime links under `.claude/skills` and `.agents/skills`. Use `docs/HARNESS.md` to find each skill's owner and purpose.

## Agents

Agents preserve ownership boundaries in a large harness. A complete low-score triage card may open the mutually exclusive Adventurer lane; otherwise dispatch the specialist owner instead of crossing into its responsibility. Definitions live in `agents/`; the roster and dispatch graph live in `docs/ADND-AGENTS.md` and `docs/ADND-DISPATCH.md`.

- `hb-ag-contracts` — The Cleric ✝️ — owns `docs/INTERFACES.md` and interface contracts.
- `hb-ag-service` — The Dwarf 🔨 — owns framework-bound service implementation.
- `hb-ag-paladin` — The Paladin 🛡️ — owns framework-neutral Python business logic and complex scripts; tests follow implementation.
- `hb-ag-surface` — The Elf 🧝 — owns the surface implementation except tests. Optional: a headless project deletes it.
- `hb-ag-test` — The Trickster 🃏 — dedicated owner of TDD records and tests; The Adventurer is the bounded exception.
- `hb-ag-ops` — The Wizard 🧙 — owns the local runtime, CI, cloud, and secret surfaces.
- `hb-ag-judge` — The Inquisitor ⚖️ — reviews project fit and logic; read-only.
- `hb-ag-adventurer` — The Adventurer 🧭 — one eligible small task end to end, with broad context, default effort, and no subagents.
- `hb-ag-git` — The Bard 🎶 — owns git and PR shipping onto `main`.
- `hb-ag-hunter` — The Hunter 🏹 — El Cazador. Issue gateway at The Three Feathers; pins the bulletin for a later Hunter.
- `hb-ag-hawk` — The Hawk 🦅 — El Halcón. Hunter-only historical-issue scout.
- `hb-ag-hound` — The Hound 🐕 — El Sabueso. Hunter-only keyword codebase scout.

Changes to `AGENTS.md` or the PRD engage `kbot-prd`; ADR and rule changes engage `kbot-adr`; interface and routed service surfaces engage `kbot-api`. Canonical watchlists are in `scripts/guardian_watchlists.py`.

A dispatched agent does not inherit session context. Specialist and Adventurer agents read `docs/PRD.md`, then `docs/INTERFACES.md`, then their agent definition and only permitted task references. The Adventurer also validates the complete `severity` / `collateral` / `effort` card before writing. Hawk and Hound are familiars: they work from The Hunter's brief and do not load PRD or INTERFACES.

## Change routing

Route framework-bound service needs through `docs/INTERFACES.md`; new routed service behavior follows interface declaration → TDD → Dwarf implementation. Framework-neutral Python business logic and complex scripts go to The Paladin: implementation first, then The Trickster's tests. Before specialist dispatch, a complete triage card whose three scores total less than 5 (none above 2) may route one bounded task to The Adventurer; interfaces/contracts, ADRs, Git, secrets, and deployment are excluded.

Follow `docs/GITHUB.md` for issue, branch, PR, merge, and deployment rules. Issue hunt and the notice board are The Hunter at The Three Feathers. Ship through The Bard.

Do not copy detailed procedures into this file. Update the owning SSOT and keep this file as an index.

### References

- `docs/PRD.md` — mandatory product constitution.
- `docs/ROADMAP.md` — current project stage.
- `docs/INTERFACES.md` — route authority.
- `docs/DEVELOPMENT-LOOP.md` — change workflow and gates.
- `docs/SERVICES.md` — service architecture.
- `docs/INFRASTRUCTURE.md` — cloud and local runtime.
- `docs/VARIABLES.md` / `docs/REQUIREMENTS.md` — configuration and versions.
- `docs/HARNESS.md` — complete skills, agents, hooks, and MCP inventory.
- `docs/ADND-AGENTS.md` — agent ownership and dispatch.
- `docs/GRAPHIFY.md` / `docs/CODEMAP.md` — repository navigation.
- `docs/TDD.md` — service inception and test lifecycle.
- `docs/GITHUB.md` — repository delivery contract.
- `docs/CLONE.md` — operator copy, prefix rename, trees, first commit.
- `docs/ONBOARDING.md` — incoming-agent fill-in map and placeholder inventory (not this index).
