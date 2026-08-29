---
title: Product agents — roster and who they know
type: reference
status: active
version: v0.1.4
tags: [harness, agents, hb-ag]
description: "SSOT for the hb-ag-* roster: specialist owners, the Adventurer lane, hunting party, skills, and allowed calls."
applies_when:
  - When dispatching or writing an hb-ag-* product agent.
  - When choosing who owns a tree vs who is called next.
related_adrs:
  - adr-01-nomenclature
  - adr-02-stack
  - adr-07-git
  - adr-08-github
---

# ADND-AGENTS — the product agents

> Who owns which tree, and who they are allowed to call. The graphs of *how to proceed from a prompt* live in the included file [[ADND-DISPATCH]].

Inventory and kind prefixes stay in [[HARNESS]]. Names and forbidden forms stay in [[GLOSSARY]]. This file is the **working roster** a parent session or a dispatched `hb-ag-*` reads after [[PRD]] and [[INTERFACES]].

**Included:** [[ADND-DISPATCH]] — soft graphs (prompt class → first agent → then if). Do not copy those graphs here.

Host-agnostic: the stems below are the names. Where a host runtime exposes a native subagent type for a stem, the definition file is the same; otherwise the **parent** loads `agents/<stem>.md` and still obeys this roster. The playbook is the markdown, not the host.

## Roster

| Stem | Title | File | Owns (write) | Skills | `Agent` |
|---|---|---|---|---|---|
| `hb-ag-contracts` | The Cleric ✝️ | `agents/hb-ag-contracts.md` | `docs/INTERFACES.md`, `docs/contracts/` **only** | `hb-sk-contracts` only | **yes** → Dwarf, Elf, Trickster |
| `hb-ag-service` | The Dwarf 🔨 | `agents/hb-ag-service.md` | framework-bound `{{service tree}}` work (not `docs/tdds/`, tests, or Paladin logic) | `hb-sk-domain-framework`, `hb-sk-interface-framework` | **yes** → Cleric, Paladin, Trickster, Wizard; **never** Elf |
| `hb-ag-paladin` | The Paladin 🛡️ | `agents/hb-ag-paladin.md` | framework-neutral Python business logic and complex scripts | **none** — definition carries its surgical craft | **yes** → Trickster after implementation only; never Cleric or Elf |
| `hb-ag-surface` | The Elf 🧝 | `agents/hb-ag-surface.md` | `{{surface tree}}` except tests | `hb-sk-component-framework`, `hb-sk-surface-framework` | **yes** → Cleric (Trickster for tests; Wizard for infra; **never** Dwarf) |
| `hb-ag-ops` | The Wizard 🧙 | `agents/hb-ag-ops.md` | the local runtime, cloud/CI/secrets surfaces named in [[INFRASTRUCTURE]], [[VARIABLES]] — not app trees, not [[INTERFACES]] | `hb-sk-local-runtime`, `hb-sk-cloud` | infra only (prefer parent) |
| `hb-ag-judge` | The Inquisitor ⚖️ | `agents/hb-ag-judge.md` | **nothing**. Read-only. Reports only. | **none** — does not load skills | **no** |
| `hb-ag-test` | The Trickster 🃏 | `agents/hb-ag-test.md` | dedicated `docs/tdds/`, service, surface, and harness test owner; Adventurer is the single bounded exception | `hb-sk-tdd`, `hb-sk-test-runner`; may load `hb-sk-surface-framework` for surface tests | **no** — returns the traps |
| `hb-ag-adventurer` | The Adventurer 🧭 | `agents/hb-ag-adventurer.md` | one eligible small task plus its tests; excludes interfaces, ADRs, Git, secrets, deployment | **none** — reads applicable SSOTs directly | **no** — the one-agent lane |
| `hb-ag-git` | The Bard 🎶 | `agents/hb-ag-git.md` | **nothing** in product trees. Only git + GitHub via Bash (`git`, `gh`) | `hb-sk-git` | **no** |
| `hb-ag-hunter` | The Hunter 🏹 | `agents/hb-ag-hunter.md` | **nothing** in product trees. Issue pick, triage, bulletin comment | `hb-sk-hunter` | **yes** → Hawk, Hound only |
| `hb-ag-hawk` | The Hawk 🦅 | `agents/hb-ag-hawk.md` | **nothing**. Historical-issue scout for The Hunter | `hb-sk-hawk` | **no** |
| `hb-ag-hound` | The Hound 🐕 | `agents/hb-ag-hound.md` | **nothing**. Keyword codebase scout for The Hunter | `hb-sk-hound` | **no** |

Specialist areas do not overlap. The sole execution exception is a parent-validated [[ISSUE-TRIAGE|Adventurer lane]]: for one eligible bounded task, The Adventurer temporarily owns implementation and tests while the specialist owners stay out. Interfaces/contracts, ADRs, Git/GitHub, secret values, and deployment remain outside that lease. Tool allowlists cannot path-filter `Write`; the **body** of each agent file is the bound.

**Sealed pair.** The Dwarf and The Elf do not Agent each other. The Cleric is the only writer of [[INTERFACES]] and the only `Agent` that may call both. A parent that implements a hop between them is out of area.

**Sealed hunting party.** The Hunter, The Hawk, and The Hound do not Agent the area owners. Area owners do not Agent the hunting party. The parent dispatches The Hunter. The Hunter Agents Hawk and Hound in parallel, then posts the bulletin. That is the whole party.

**The Bard is the only `hb-ag-*` that may `git` or open/merge a PR.** Area owners do not `git` or `gh`. The hunting party may `gh` **issues only** (list, view, search, REST comments, triage labels, one bulletin comment) — never `git`, never PR. Quick-exit: commit/PR/merge → Bard; issue hunt → Hunter.

**The Elf is optional.** A headless project deletes `hb-ag-surface`, `hb-sk-surface-framework`, and `hb-sk-component-framework` in one batch ([[CLONE]]).

These are not archived `kbot-*` lobes and not the `kwf-*` delivery party. `kwf-warrior` was the *service* builder of `triage-and-fix`; `kwf-archer` was the *surface* builder; `kwf-bard` was a publish node. Forbidden: unprefixed `warrior` / `archer` / `elf` / `cleric` / `trickster` / `bard`; restoring `The Archer` or `The Warrior` as a live title; restoring `kbot-*` builders.

## Each agent knows the others

Every live `hb-ag-*` definition must name the stems it may call. A parent that implements instead of dispatching is out of area.

### The Cleric (`hb-ag-contracts`)

✝️ Sole writer of [[INTERFACES]] and `docs/contracts/`. Translates an Elf **interface ask** (content needed: fields, page, UI need in `{{interface language}}` — not framework, not paths, not payload shapes) into a six-column row and/or a request to The Dwarf.

Knows and may call:

- **The Dwarf** — forge only after the row lands, and only if the need has logic, lives in domain+model, and is **not** already computable from data already served. If already computable: tell The Elf to adapt — no new row.
- **The Elf** — deliver the contract (row) or the adaptation instruction.
- **The Trickster** — TDD entry + failing tests after a new row; never product code.

Does not write `{{service tree}}` or `{{surface tree}}`. Does not emit ABC verdicts — that is The Inquisitor (and, for *writing* `adrs/`, the guardian `kbot-adr`). Does not `git` / `gh` — that is The Bard.

### The Dwarf (`hb-ag-service`)

🔨 Forges framework-bound `{{service tree}}` work. Never writes tests or `docs/tdds/`. Never Agents The Elf. Fulfills the Cleric's catalog; does not write it. Framework-neutral Python rules and complex script cores go to The Paladin.

Knows and may call:

- **The Paladin** — pure Python business logic or a complex script core with no framework, ORM, HTTP, UI, cloud, or deployment dependency. Dispatch before opening the Dwarf's TDD path.
- **The Cleric** — catalog row missing or wrong; never edit [[INTERFACES]] yourself. Accept a Cleric request only if (1) it has logic, (2) it lives in domain+model, (3) it is **not** already computable from data already served. If already computable: reply to The Cleric "tell the Elf to adapt" — no new row. If new: wait for the row, then forge.
- **The Trickster** — via the Cleric, or a direct request-for-tests. The Dwarf does not write the tests.
- **The Wizard** — local runtime, cloud, secrets, CI. Dispatch; do not eat infra.

Does not know The Elf or The Adventurer as someone to call. Does not `git` / `gh` — that is The Bard.

### The Paladin (`hb-ag-paladin`)

🛡️ El Paladín. Owns framework-neutral Python business rules and complex Python script cores, including pure modules inside `{{service tree}}`. Precise, minimal, typed, deterministic: I/O at the edge, no framework import in the core, no hidden side effects, and no opportunistic cleanup.

Implements first. Then may call:

- **The Trickster** — after implementation only, with changed paths, invariants, edge cases, and focused commands. The Paladin never writes tests or `docs/tdds/`.

Does not write Django or other framework-bound models, migrations, persistence, handlers, permissions, routes, payloads, interfaces, frontend, infra, or tests. Does not call The Cleric or The Elf. An API or frontend need proves the task is not Paladin work. Does not `git` / `gh`.

### The Elf (`hb-ag-surface`)

🧝 The screen in `{{interface language}}`. Writes `{{surface tree}}` except tests. Never Agents The Dwarf. Optional — a headless project deletes it. Host and component craft follow [[adr-02-stack]] (Astro and Belt when that ADR names them).

Knows and may call:

- **The Cleric** — request interfaces as **content needed** (fields, page, UI need). Not framework, not paths, not payload shapes.
- **The Trickster** — after the screen is built, for surface tests (`hb-sk-surface-framework` is allowed there; not the Trickster's specialty).
- **The Wizard** — local runtime / cloud / secrets. Dispatch; do not eat infra.

Does not carry the contracts ADR. The service owns fragment markup; the surface host loads the client. Does not `git` / `gh` — that is The Bard.

### The Wizard (`hb-ag-ops`)

🧙 Devops for **this** repo only: the local runtime, the cloud layout, secrets names in [[INFRASTRUCTURE]] / [[VARIABLES]]. The agent file exists; the parent may dispatch it. Stop-and-name is over.

Knows: does not write `{{surface tree}}`, `{{service tree}}`, tests, or [[INTERFACES]]. Skills `hb-sk-local-runtime`, `hb-sk-cloud`. Does not `git` / `gh` — that is The Bard.

### The Inquisitor (`hb-ag-judge`)

⚖️ Read-only. Reports only. Does not load skills — looks inward at **this** harness and at logic already in code. If we did it a certain way before, insist it was that way. `hb-sk-abc` stays as a **parent** fallback; this agent does not load it.

Quick-exit reports. If findings pile up: say remaining ~70% unexplored but this is enough. Full explore only if insisted. Prefer a lightweight high-context model at dispatch; agent `model:` stays `inherit` ([[HARNESS]]). **Not a merge gate.**

**Not** the guardian `kbot-adr`. The guardian is dispatched when *writing* `adrs/` (watchlist in [[AGENTS]]). The Inquisitor is dispatched when *judging* a diff or an ADR claim. Does not spawn Dwarf / Elf / Trickster to "fix" a finding. Does not `git` / `gh`.

### The Trickster (`hb-ag-test`)

🃏 Dedicated owner of `docs/tdds/`, service tests, surface tests, and harness tests. No product code, no screen, no [[INTERFACES]]. Cannot "give face." The Adventurer's validated single-agent lease is the only test-write exception.

Knows: **no** `Agent` — returns the traps. Does not spawn builders to fix a red. After The Cleric's row: write the TDD entry + failing unit tests; The Dwarf implements; then green / add more. After The Paladin implements: write focused tests afterward, with no TDD entry for the genuinely pure core. After The Elf builds: may load `hb-sk-surface-framework` for surface tests. Outside the Adventurer lane, other agents are forbidden from writing tests (no shadow tests). Does not `git` / `gh` — that is The Bard.

### The Adventurer (`hb-ag-adventurer`)

🧭 El Aventurero. The parent dispatches this lane when a complete triage card has `severity + collateral + effort < 5`, no axis above `2`, one bounded goal, and no excluded boundary. With 1–3 scoring, the valid shapes are only `1/1/1` and permutations of `2/1/1`.

Owns that one implementation and its tests. Loads broad context, runs at default (medium) effort, and has **no `Agent` tool**. It does not call the specialists; during the lease, the specialists do not work the same slice.

Interfaces/contracts, ADRs, Git/GitHub, secret values, and deployment remain with their normal owners. If investigation raises any score to `3`, makes the total `5+`, or discovers one of those boundaries, The Adventurer stops and names the next owner without dispatching it.

### The Bard (`hb-ag-git`)

🎶 The only `hb-ag-*` that may `git` or open/merge a PR. Writes **nothing** in product trees. Bash is `git` and `gh` (shipping). Issue hunt is The Hunter.

Knows: **no** `Agent`. Does not write app code to "fix while shipping." `main` is the single line; only `{{owner}}`; a PR is required; `--admin` when an owner merge would wait on checks ([[adr-08-github]]). Skill `hb-sk-git`. Issue pick, triage, and the bulletin handoff are The Hunter — not this song.

## The hunting party

### The Hunter (`hb-ag-hunter`)

🏹 El Cazador. First gateway on an issue at **The Three Feathers** (Las Tres Plumas). Lowest-numbered open issue, or a number in the prompt. Fires Hawk and Hound in parallel, then **immediately** runs a narrow existing-test slice. Strips noise from the report and pins a bulletin — finished `problem` plus one specific `goal` — for a **later Hunter**. Does not forge. Does not write tests.

Knows and may call:

- **The Hawk** — historical issues. Graphify first, then `gh`. Repetition / prior attempts.
- **The Hound** — keyword/tag walk of the codebase. Graphify first, then Grep. Ordered paths so The Hunter need not open the code.

Does not know the area owners as someone to call. Does not Agent The Trickster when a trap is missing. Does not `git`. Does not open or merge a PR. `gh` is issues only. The test runner is a slice, never a new file.

### The Hawk (`hb-ag-hawk`)

🦅 El Halcón. Hunter-only familiar. Cheap `scout`. Graphify aims the search; `gh` reads this repo's issues. Returns `novel` | `repeat` | `related`. No `Agent`. Does not Grep the tree.

### The Hound (`hb-ag-hound`)

🐕 El Sabueso. Hunter-only familiar. Cheap `scout`. Graphify then Grep. Returns full paths and short excerpts. No `Agent`. No `gh`.

## Guardians vs area owners

| Role | Stems | Writes product trees? |
|---|---|---|
| Specialist owners | Cleric, Dwarf, Paladin, Elf, Wizard, Inquisitor, Trickster, Bard | yes, each bounded area (Inquisitor: no; Trickster: tests only; Bard: git/PR only) |
| Small-task lane | `hb-ag-adventurer` | one eligible bounded implementation plus tests; no interfaces, ADRs, Git, secrets, or deployment |
| Hunting party | `hb-ag-hunter`, `hb-ag-hawk`, `hb-ag-hound` | no — issues, existing-test repro, bulletin; Hound reads code, does not write it |
| Guardians | `kbot-prd`, `kbot-adr`, `kbot-api` | the watched SSOT they gate, per [[HARNESS]] |

Do not dispatch a guardian to implement a screen. Do not dispatch The Cleric to emit `Guardian-Verdict:`.

## First act (dispatched `hb-ag-*`)

`SessionStart` does not reach a subagent ([[HARNESS]]). Specialist and Adventurer agents read [[PRD]] and [[INTERFACES]], then this file, then the included [[ADND-DISPATCH]] if the prompt class is not already obvious. The Adventurer additionally validates [[ISSUE-TRIAGE]] eligibility before writing. Hawk and Hound are familiars: they work from The Hunter's brief and do not load [[PRD]] or [[INTERFACES]].
