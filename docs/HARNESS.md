---
title: Harness inventory, vendored skills, and agent contracts
type: reference
status: active
version: v1.2.0
tags: [harness, skills, agents, ssot]
description: "Complete inventory of vendored skills, kind prefixes, MCP policies, and agent definition contracts."
applies_when:
  - When authoring or invoking harness skills and hooks.
  - When defining agent contracts and tool grants.
  - When verifying harness directory layout and symlink structures.
related_adrs:
  - adr-05-after-versioning
---
# HARNESS — the skills and agents this project requires

**The harness is the support of the objective, not the objective** ([[PRD]] — that document's own words): the documentation system, the guardian and orchestrator agents, and the **skills** vendored into the repo. This file is the harness-team-party template's own inventory; a project instantiated from it ([[CLONE]]) keeps this file and re-points its product rows.

## Vendoring rule

> Every skill, hook, and agent this project requires is a real copy in the repo — never assumed present on the host. A fresh clone runs the harness without external setup.

Every skill, hook, and agent this project requires is vendored into the repo — a real copy under `skills/`, `hooks/`, `agents/` — never assumed present on the host. A fresh clone runs the harness without external setup.

## Layout and kind-prefix

> Artifacts are named by kind prefix and live in four trees at repo root, each linked into the runtime paths. The stem after the prefix names the role.

Kind prefixes: [[GLOSSARY]].

Every harness artifact name starts with its kind:

| Kind | Prefix |
|---|---|
| skill (reusable) | `kskill-` |
| skill (this product) | `hb-sk-` |
| hook | `khook-` |
| agent (guardian/lobe) | `kbot-` |
| agent (this product) | `hb-ag-` |
| delivery-party node | `kwf-` |

The stem after the prefix names the role. Product knowledge skills use `hb-sk-` + contract (`hb-sk-contracts`). Product agents use `hb-ag-` + area or role (`hb-ag-service`, title **The Dwarf**; `hb-ag-adventurer`, title **The Adventurer**). Reusable harness skills keep `kskill-`. A stem that *is* the role may name a technology (`kskill-cowsay`). Canonical and forbidden forms: [[GLOSSARY]] (`harness kind prefix`, `harness name stem`).

`hb-` is this template's own product prefix. Instantiation batch-renames it to the new project's prefix ([[CLONE]]).

One real copy, at the repo root:

| Tree | Real copy | Link paths |
|---|---|---|
| skills | `skills/` | `.claude/skills`, `.agents/skills` |
| hooks | `hooks/` | `.claude/hooks`, `.agents/hooks` |
| agents | `agents/` | `.claude/agents`, `.agents/agents` |
| ADRs | `adrs/` | `.claude/rules`, `.agents/rules` |

These trees are reached by path (Grep/Read). They stay outside the vault index — skill and agent filenames collide with the basename uniqueness the vault graph needs. Canonical trees: [[GLOSSARY]] (`harness SSOT trees`).

A rename of an artifact moves every reference in the same batch: hooks, workflow scripts, tests, the merge gate, agent definitions, ADRs.

## Harness docs frontmatter

> Every harness doc at `docs/*.md` carries a closed set of frontmatter keys in a fixed order, stamped against the current [[CHANGELOG]] version. An untouched file is not restamped.

Force: [[adr-05-after-versioning]].

The harness documentation set carries exactly these keys, in this order:

| Key | Shape | Notes |
|---|---|---|
| `title` | English phrase, at most ten words | Descriptive title; not the filename stem alone. |
| `type` | `reference` \| `note` \| `index` | `reference` for SSOT docs, `note` for registers, `index` for root portals. |
| `status` | `active` \| `draft` \| `superseded` | Presence under `docs/` is `active`; inactive docs are deleted. |
| `version` | `vA.B.C` | Equals the CHANGELOG version current at that revision. `A` initial milestone, `B` functional milestone, `C` granular commit iteration incremented generously. |
| `tags` | flow list `[a, b]` | Open vocabulary. |
| `description` | prose of what the file contains | Concise catalogue; the body does not repeat this opener. |
| `applies_when` | list of 2-4 trigger conditions | Clear context criteria when the document applies. |
| `related_adrs` | list of ADR slugs | ADRs governing this file, plus [[adr-05-after-versioning]]. `[]` when no other ADR governs it. |

A file that is not current is deleted in the same batch. An untouched file is not restamped.

[[CHANGELOG]] records every change that lands on `main`. This heading owns the `version` stamp on the docs.

## Boy-scout

> Applies only while a file is already under edit for another reason. Bare deletion leaves no trace — no tombstone, no residue, no renumbering prose.

Comment necessity: [[CODE-COMMENTS]].

Applies only while a file is already under edit for another reason. This heading never opens a file.

Bare deletion of one rule from `adrs/*.md` or from this file:

| Leave behind | Allowed |
|---|---|
| nothing in the hole | silent renumber if the document's own convention needs sequential numbers |
| a true unrecorded fact, relocated to the doc that owns it, then deleted here | — |

| Residue | Status |
|---|---|
| tombstone ("this rule was removed") | forbidden |
| "removed" / "retired" marker | forbidden |
| renumbering prose | forbidden |
| historical note in the hole | forbidden |

After the edit, a reader who never saw the prior revision must not be able to tell a rule is missing.

This heading does not cover adding a rule or changing what a rule requires or forbids.

## Required skills

> Skills this project requires. Sibling-owned skills (`hb-sk-tdd`, `hb-sk-test-runner`, `hb-sk-git`) are listed here even if their folders land in the same batch.

| Skill | Why this project requires it | Primary consumers |
|---|---|---|
| `hb-sk-component-framework` | `{{component framework}}` contract for the components the surface host renders. | The Elf (`hb-ag-surface`) |
| `hb-sk-surface-framework` | `{{surface framework}}` host contract: rendering mode, hydration, pages. The surface toolchain only. | The Elf (`hb-ag-surface`); The Trickster (`hb-ag-test`) may load for surface tests |
| `hb-sk-interface-framework` | `{{interface framework}}`: explicit handlers + declared paths, split payload shapes, permission classes. | The Dwarf (`hb-ag-service`) |
| `hb-sk-domain-framework` | `{{domain framework}}`: models, settings, adapters, the Paladin pure-compute boundary, and service toolchain. | The Dwarf (`hb-ag-service`) |
| `hb-sk-contracts` | Six-column [[INTERFACES]] catalog + `docs/contracts/`. | The Cleric (`hb-ag-contracts`) only |
| `hb-sk-tdd` | `docs/tdds/` specification lifecycle (red → green). | The Trickster (`hb-ag-test`) |
| `hb-sk-test-runner` | Service/harness test contract (`{{test runner}}` shape). | The Trickster (`hb-ag-test`) |
| `hb-sk-local-runtime` | Root `{{local runtime}}` orchestration. | The Wizard (`hb-ag-ops`) |
| `hb-sk-cloud` | `{{deploy target}}` layout on `{{cloud provider}}`. | The Wizard (`hb-ag-ops`) |
| `hb-sk-git` | Git + GitHub shipping (`git`, PR, merge) for this repo: `main`, `{{owner}}`, PR-required, `--admin` on owner merge wait. | The Bard (`hb-ag-git`) **only** |
| `hb-sk-hunter` | Issue hunt at The Three Feathers: noise-stripped `problem`, one imperative `goal` for a later Hunter, existing-test repro, bulletin comment. | The Hunter (`hb-ag-hunter`) only |
| `hb-sk-hawk` | Historical-issue scout: Graphify first, then `gh`. | The Hawk (`hb-ag-hawk`) only — Hunter familiar |
| `hb-sk-hound` | Keyword codebase scout: Graphify first, then Grep. | The Hound (`hb-ag-hound`) only — Hunter familiar |
| `hb-sk-owl` | Official-docs scout: [[OWL-INDEX]] first, listed URLs only, markdown findings. | The Owl (`hb-ag-owl`) only — universal web scout |
| `hb-sk-crow` | Kamikaze unofficial public-web scout: one intensive pass, source-trust labels. | The Crow (`hb-ag-crow`) only — universal web scout |
| `hb-sk-abc` | ABC checklist: PR vs [[PRD]], ADRs, [[INTERFACES]]. | **Parent fallback** — The Inquisitor does not load skills |
| `kskill-graphify` | First exploration mechanism when the graph is present ([[adr-35-graphify]], [[GRAPHIFY]]). Query/path/explain; `bin/ensure` after clone; extract and update; MCP in `mcp/mcp.json`. | exploration, `/kskill-graphify` |
| `kskill-mood` | Session stance (`/kdx-mood`). | main loop |
| `kskill-qw` | Slash `/qw` — Quick Win. | `/qw` close-out |
| `kskill-cowsay` | Slash `/cowsay`. | Stop brief, `/qw` close-out |
| `kskill-micro-solid-font` | 3-row block font for `/cowsay` legends. | `kskill-cowsay` |
| `kskill-report` | Structured run/status reporting. | main loop |
| `kskill-send-to-telegram` | Owner notification channel. | run notifications |
| `diagram-design` | Branded diagrams. | docs / architecture drawings |

## Vendored MCP servers

> No MCP server is vendored. `graphify` is declared in `mcp/mcp.json` and resolved by `uvx`; `chrome-devtools` by `bunx`.

This project vendors no MCP server. `mcp/mcp.json` (linked as `.mcp.json`) declares `graphify` (resolved by `uvx`, graph at `graphify-out/graph.json`) and `chrome-devtools` (resolved by `bunx`, pin in [[REQUIREMENTS]]).

`docs/` is read with Grep, Glob and Read, like every other file in the tree.

## Not vendored (intentionally)

> Services and convenience skills that are declared or available but not carried in the repo tree, with the rationale for each.

- **`chrome-devtools`** — the sanctioned real-browser path for interactive smoke checks. It **is** declared in `mcp/mcp.json` (pin in [[REQUIREMENTS]]), resolved on demand by `bunx` — but it is **not vendored**: it drives a browser the operating system provides, on a display, at `127.0.0.1:9222`, a declared-but-not-vendored server no different in kind from any other MCP a clone reaches without a local copy. A clone carries the declaration, never the browser. Away from a machine with that browser the server simply has nothing to attach to, so treat it as a local verification accelerator and never as a build dependency — which is also why no CI job may reach for it ([[AGENTS]]: smoke tests are prohibited as a gate, and the sanctioned runs are interactive and operator-run).
  - **It attaches, it never launches.** The declared invocation passes `--browserUrl http://127.0.0.1:9222`, binding it to the browser the operator already started with a remote-debugging port. Letting it start its own browser would give it a second, profile-less browser that is not the one under test.
- The global convenience skills of the operator's machines (handoff, diagram, and stance helpers, …) are available when present but are **not required** for this project to build, test, and deploy — so they are not vendored. Session stance (`kskill-mood` / `/kdx-mood`), the `/qw` shortcut, `/cowsay`, and the micro-solid font **are** required and sit in the inventory table above.

## Enforcement hooks

> The `hooks/` tree is empty. Cursor `sessionStart` loads SSOTs and bootstraps Graphify.

The `hooks/` tree is empty (`.gitkeep` only) — no agent hooks, no git pre-push installer. Guardian watchlists live in `scripts/guardian_watchlists.py`.

Cursor project hooks live in `.cursor/hooks.json`. `sessionStart` runs, in order:

1. `.cursor/hooks/load-hook.py` — injects [[PRD]], then `adrs/`, then `docs/` into additional context.
2. `.cursor/hooks/graphify-ensure.py` — `skills/kskill-graphify/bin/ensure` fail-open so a clone has the CLI and `graph.json` without an LLM key ([[GRAPHIFY]], [[adr-35-graphify]]).

## Where the harness runs — three surfaces, not two

> The harness runs on three surfaces: the owner's workstation, a cloud sandbox session, and a GitHub Actions runner. The runner is the only surface with no human in the session.

The harness was written for the owner's workstation and adapts to a cloud sandbox session. A GitHub Actions runner is the third surface, and the only one with **no human in the session** (an unattended GitHub Actions runner). What is specific to the runner:

- **No agent hooks.** `.claude/settings.json` carries no `hooks` key.
- **No cloud credential and no `id-token: write` by default.** The harness reaches GitHub here and nothing else, unless the project's deploy workflow declares otherwise ([[adr-08-github]] rule 5).

## Guardian & orchestrator agents

> Agents are the other half of the harness. Guardians gate [[PRD]], the ADRs, and [[INTERFACES]]; `kbot-*` agents are the orchestrator fan-out and project-resident lobes; `kwf-*` are workflow nodes resolved by script.

Agents are the other half of the harness. Their SSOT is `agents/`, reached as `.claude/agents/` and `.agents/agents/`. Product specialists, the Adventurer lane, and the hunting party are the `hb-ag-*` family. Roster and graphs: [[ADND-AGENTS]], [[ADND-DISPATCH]]. Where a host runtime exposes a native subagent type for a stem, the definition file is the same; otherwise the **parent** loads `agents/<stem>.md` and still obeys the roster. The playbook is the markdown, not the host.

### The agent definition contract — the fields

Every file under `agents/` declares the same closed set of frontmatter keys, in one shape. This section is the record of those fields ([[adr-00.a-adr-frontmatter]] rule 2a). Docs and ADRs use a different closed set; do not mix the two.

| Key | What it declares |
|---|---|
| `name` | The exact filename stem, kind-prefixed (Layout and kind-prefix, above). |
| `description` | The dispatch surface, 25–60 words: what it does, when to dispatch, one boundary it will not cross. Agents fire on description match. |
| `model` | Always `inherit`. The harness binds a vendor model at dispatch time; agent definitions never pin a product name. |
| `tools` | A YAML block sequence, one tool per line, an allowlist that excludes everything it does not name. Graphify MCP (`query_graph`, `get_neighbors`, `get_node`, `shortest_path`) is listed first, before `Read` and `Glob`. `tools: []` when the agent is granted none. |
| `related_adrs` | The ADRs whose force the agent carries. `[]` when it carries none — never omitted. |
| `color` | Cosmetic only. Carries no contract force; the one sanctioned key outside the set. |

**Agent `model` is always `inherit`.** Every file under `agents/` declares `model: inherit` and nothing else. Effort (`low` / default / `high`) stays in the dispatch contract and is orthogonal to which vendor model the harness picks.

**Harness model roles** — when a workflow script or dispatcher must name the *kind* of model to bind, it uses one of three role slugs. The runtime maps each slug to whatever vendor model the operator's harness provides; no vendor product name appears in agent definitions or in these docs:

| Role slug | Meaning | Typical cast |
|---|---|---|
| `thinker` | planner/thinker — judgment, planning, doctrine gates | guardians, the Inquisitor, plan-time judges |
| `builder` | builder — implementation, worktree diffs, publish | Paladin, Dwarf, Elf, Adventurer, Bard (`kwf-warrior` / `kwf-archer` / `kwf-bard` were the archived delivery-party builders) |
| `scout` | fast/scout — cheap parallel reads, familiars, pattern scans, official-docs Owl, kamikaze Crow | The Hawk, The Hound, The Owl, The Crow, read-only familiars and sweep nodes |

Admitting or retiring a role slug is an edit to this table, not to an ADR.

**The ADR-to-agent edge is a pair.** An ADR lists the agents that carry it in `related_agents` ([[adr-00.a-adr-frontmatter]]); each of those agents lists that ADR in `related_adrs`. Both ends move in the same batch, and a one-sided edge is a defect in both files.

**Entity and liturgy** live in `agents/hb-ag-liturgy.md` (The Liturgist): how an `hb-ag-*` is given personality without extra powers, with bilingual example phrases. The Liturgist is a **mock**. Never dispatch it for product, hunt, ship, or research. Mechanical fields stay in this section; each live agent carries a copy of its liturgy block.

### The product `hb-ag-*` family

Specialists own non-overlapping areas. The one exception is a parent-validated Adventurer lease: one eligible low-score task temporarily gives The Adventurer its bounded implementation and tests while specialists stay out. Interfaces/contracts, ADRs, Git/GitHub, secret values, and deployment never enter that lease. The filename stem is the harness name; the fantasy title is personality (opening quote + voice). `hb-ag-contracts` is the **writer** of the catalog, not a merge-verdict bot. Do not restore archived `kbot-*` builders.

`hb-sk-*` consumers are named in the inventory; most skills have one owner. `hb-sk-surface-framework` is Elf-owned (Trickster may load for surface tests). `hb-sk-abc` is a parent fallback (Inquisitor loads none). `hb-sk-git` is Bard-only. `hb-sk-hunter` / `hb-sk-hawk` / `hb-sk-hound` are the hunting party at The Three Feathers. `hb-sk-owl` / `hb-sk-crow` are the universal web scouts.

| Stem | Title | Owns (may write) | Must not write | `Agent` tool |
|---|---|---|---|---|
| `hb-ag-contracts` | The Cleric ✝️ | `docs/INTERFACES.md`, `docs/contracts/` only | `{{surface tree}}`, `{{service tree}}`, tests, infra, git | **yes** → Dwarf, Elf, Trickster |
| `hb-ag-service` | The Dwarf 🔨 | framework-bound `{{service tree}}` work | `INTERFACES.md`, pure Paladin logic, `{{surface tree}}`, `docs/tdds/`, tests, infra, git | **yes** → Cleric, Paladin, Trickster, Wizard; **never** Elf |
| `hb-ag-paladin` | The Paladin 🛡️ | framework-neutral Python business logic and complex scripts | frameworks, interfaces, frontend, infra, tests, git | **yes** → Trickster after implementation only; never Cleric or Elf |
| `hb-ag-surface` | The Elf 🧝 | `{{surface tree}}` except tests | `INTERFACES.md`, `contracts/`, `{{service tree}}`, tests, infra, git | **yes** → Cleric (Trickster for tests; Wizard for infra; **never** Dwarf) |
| `hb-ag-ops` | The Wizard 🧙 | local runtime, cloud/CI/secrets named in [[INFRASTRUCTURE]] / [[VARIABLES]] | app trees, `INTERFACES.md`, tests, git | infra only (prefer parent) |
| `hb-ag-judge` | The Inquisitor ⚖️ | **nothing**. Read-only. Reports only. | product trees, tests, git | **no** |
| `hb-ag-test` | The Trickster 🃏 | dedicated `docs/tdds/`, service/surface/harness tests | product code, screen, `INTERFACES.md`, git | **no** — returns traps; Adventurer is the bounded write exception |
| `hb-ag-adventurer` | The Adventurer 🧭 | one eligible low-score task plus its tests | interfaces/contracts, ADRs, Git/GitHub, secrets, deployment | **no** — complete or stop |
| `hb-ag-git` | The Bard 🎶 | git + PR shipping via Bash (`git`, `gh`) | product trees, app code "while shipping", issue-hunt bulletin | **no** |
| `hb-ag-hunter` | The Hunter 🏹 | issue bulletin comment at The Three Feathers | product trees, tests, git, PR | **yes** → Hawk, Hound only |
| `hb-ag-hawk` | The Hawk 🦅 | **nothing**. Historical-issue scout | product trees, tests, git, the bulletin | **no** |
| `hb-ag-hound` | The Hound 🐕 | **nothing**. Keyword codebase scout | product trees, tests, `gh` | **no** |
| `hb-ag-owl` | The Owl 🦉 | **nothing**. Official-docs scout | product trees, tests, git, [[OWL-INDEX]] writes | **no** |
| `hb-ag-crow` | The Crow 🐦‍⬛ | **nothing**. Kamikaze unofficial web scout | product trees, tests, git | **no** |

Tool allowlists cannot path-filter `Write`. The **body** is the bound: specialists hold `Write`/`Edit` for their area, while The Adventurer holds it only for a validated task lease. Need a new row → dispatch `hb-ag-contracts`. Do not edit the catalog. Need a commit or PR → dispatch `hb-ag-git`. Issue hunt and the notice board → `hb-ag-hunter`. Official docs → `hb-ag-owl`. Unofficial or hard-to-find public facts → `hb-ag-crow`. Product implementers do not `git` or `gh`. The hunting party may `gh` issues only.

Titles live in a different family from the archived `kwf-*` cast: `kwf-warrior` was the *service* builder; `kwf-archer` was the *surface* builder; `kwf-bard` was a publish node. Forbidden: dispatching `kwf-warrior` when you mean The Dwarf; dispatching `kwf-archer` when you mean The Elf; using `warrior` / `archer` / `elf` / `cleric` / `trickster` / `bard` unprefixed; restoring `The Archer` or `The Warrior` as a live title ([[GLOSSARY]]).

Each live definition opens with a one-line quote, then "You are **The X** (`hb-ag-…`)". Voice stays short. Depth of entity (traits, EN/ES phrases) lives under `## Liturgy`, authored against The Liturgist (`hb-ag-liturgy`); that file is not a fifteenth worker.

- **The Cleric** ✝️ — one rite, one row. Holds the scroll ([[INTERFACES]]). Agents Dwarf, Elf, Trickster. Never walks into the melee.
- **The Dwarf** 🔨 — forges framework-bound `{{service tree}}` work. Fulfills the Cleric's row; does not write it. Pure Python rules go to The Paladin. Never writes tests or Agents The Elf.
- **The Paladin** 🛡️ — El Paladín. Surgical framework-neutral Python business logic and complex scripts. Implements first, then Agents The Trickster for tests. Never Cleric or Elf.
- **The Elf** 🧝 — the face the user meets (the screen in `{{interface language}}`). Works only on `{{surface tree}}` (not tests). Calls the Cleric for interfaces. Never Agents The Dwarf. Optional: a headless project deletes it.
- **The Wizard** 🧙 — environment is the spell: the local runtime, [[INFRASTRUCTURE]], [[VARIABLES]], CI. Live; the parent may dispatch it. Does not write app code or `INTERFACES.md`.
- **The Inquisitor** ⚖️ — interrogates this harness and logic already in code. Read-only; quick-exit. Loads **no** skill. Not a merge gate.
- **The Trickster** 🃏 — dedicated test owner. Dwarf red-first; Paladin tests afterward. The Adventurer lane is the sole bounded exception. Returns the traps.
- **The Adventurer** 🧭 — El Aventurero. One eligible task, implementation plus tests, broad context, default effort, no `Agent`; no governed-boundary bypass.
- **The Bard** 🎶 — the only voice Git hears for shipping. `git` / PR / merge. Does not fix the song while singing it. Issue hunt is The Hunter.
- **The Hunter** 🏹 — El Cazador. Issue gateway at The Three Feathers. Pins a noise-stripped bulletin (`problem` + one `goal`) for a later Hunter.
- **The Hawk** 🦅 — El Halcón. Cheap `scout`. Old issues, Graphify then `gh`. Hunter only.
- **The Hound** 🐕 — El Sabueso. Cheap `scout`. Keywords in the tree. Hunter only.
- **The Owl** 🦉 — El Búho. Cheap `scout`. [[OWL-INDEX]] then listed official URLs. Universal.
- **The Crow** 🐦‍⬛ — El Cuervo. Expensive `scout`. One unofficial kamikaze pass. Universal.

### Invocation shape — every agent is a subagent

**Standing decision: every agent under `agents/` is written to run as a dispatched subagent; no definition declares itself a teammate.**

- **product specialists** — The Cleric holds `Agent` (Dwarf, Elf, Trickster) and is the sole surface↔service hop. The Dwarf may call The Paladin for a pure Python core, plus The Cleric, The Trickster, and The Wizard — never The Elf. The Paladin may call The Trickster after implementation only, never The Cleric or The Elf. The Elf retains its existing sealed path. Trickster, Inquisitor, and Bard do not spawn builders. Wizard Agent is infra-only; prefer the parent.
- **single-agent lane** — The Adventurer has no `Agent`. The parent dispatches it only for a complete [[ISSUE-TRIAGE]] card totaling less than 5 with no axis above 2 and no excluded boundary.
- **hunting party** — The Hunter holds `Agent` (Hawk, Hound only). Hawk and Hound do not spawn. The party does not Agent area owners. Dispatch Hawk/Hound as `scout`.
- **universal web scouts** — The Owl and The Crow have no `Agent`. Any specialist or parent may dispatch them as `scout`. They do not write trees.

What is enforceable, and is enforced by `tests/test_agents_are_subagents.py`: no definition under `agents/` declares itself a teammate or carries teammate-only frontmatter. If a host runtime still hands a definition to a teammate mechanism, the decision above constrains how the agents are *written*, not how a given machine chooses to run them.
