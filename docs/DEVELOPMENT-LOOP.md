---
title: Canonical development loop, workflows, and gate checkpoints
type: reference
status: active
version: v0.1.4
tags: [harness, workflow, development-loop, tdd, interfaces]
description: "Engineering workflows for specialist delivery, Paladin test-after logic, Adventurer small tasks, and PR integration."
applies_when:
  - When initiating feature development workflows.
  - When entering the service development zone through interface declaration.
  - When verifying the interface checkpoint before returning to surface implementation.
  - When routing pure Python business logic or an eligible one-agent task.
related_adrs:
  - adr-02-stack
  - adr-05-after-versioning
  - adr-08-github
---
Open this before starting any code. It assumes [[PRD]] and [[INTERFACES]] are already held in memory (the standing requirement in [[AGENTS]]) and that the ABC gate has cleared.

## The canonical workflows — the definition

> A general definition, not a rigid script. Routed framework service enters through [[INTERFACES]]; pure Python business logic and eligible tiny tasks have explicit bounded paths.

**The development loop:**

`idea → Adventurer eligible? → one-agent lane | pure Python core? → Paladin | user-facing/service specialist path`

The routed, framework-bound service zone is entered only through [[INTERFACES]]. The surface requests **interfaces as content** (fields, page, UI need) via The Cleric (`hb-ag-contracts`) — not framework, not paths. Framework-neutral Python business rules and complex script cores go directly to The Paladin and require no interface unless an adapter must change. Tests are The Trickster (`hb-ag-test`) on specialist paths; The Paladin calls it **after** implementation. The Adventurer writes both sides of its eligible task. Ship (`git` / `gh`) remains The Bard (`hb-ag-git`).

1. Confirm the need cannot be met by the interfaces already declared in [[INTERFACES]].
2. If it cannot: The Cleric adds the row to [[INTERFACES]].
3. Enter the [[TDD]] flow — The Trickster writes the spec and failing tests (`hb-sk-tdd`, `hb-sk-test-runner`); The Dwarf implements.
4. **Checkpoint — does [[INTERFACES]] solve the need?** Yes → return to the surface track. No → loop back to 1.

The checkpoint is what defines the loop: the service zone is exited only when [[INTERFACES]] answers the feature's need.

**New service piece:**

`plan → The Cleric ([[INTERFACES]]) → The Trickster ([[TDD]]) → The Dwarf (models → handlers)`

**New framework-neutral Python business rule or complex script:**

`plan → The Paladin (implementation) → The Trickster (tests afterward)`

**Eligible small task:**

`complete triage card → parent validates total < 5 and no axis > 2 → The Adventurer (implementation + tests)`

**New user-facing feature:**

`The Elf (surface) → interfaces content via The Cleric → The Trickster (tests)`
`         → needs the service? → The Trickster then The Dwarf → …`

All paths are active: every gate binds wherever its subject exists. The sections below render each one step by step.

## 0 · Boot — orientation before any code

> Every use case shares this prefix: hold [[PRD]] and [[INTERFACES]] in memory, orient per [[GRAPHIFY]], then clear the ABC gate before touching any code.

Every use case shares this prefix. [[PRD]] and [[INTERFACES]] stay in memory. Orient per
[[GRAPHIFY]] ([[adr-35-graphify]]). Then the ABC gate ([[AGENTS]]).

```mermaid
flowchart TD
    S(["Session start / new task"]) --> MEM["Hold PRD + INTERFACES in memory"]
    MEM --> G["Orient per GRAPHIFY"]
    G --> ABC{"ABC gate:<br/>A follows PRD? · B complies with ADRs? · C modifies INTERFACES?"}
    ABC -->|clears| READY(["Ready — pick a use-case loop"])
    ABC -->|fails| STOP(["Fix or stop — no code until ABC clears"])
```

## 0.25 · The Adventurer gate — one small task, one agent

> Coordination is removed only when the scored work is smaller than the coordination and no governed boundary needs a specialist.

The parent checks a complete [[ISSUE-TRIAGE]] card before specialist dispatch. `severity + collateral + effort < 5`, with no axis above `2`, permits only `1/1/1` or a permutation of `2/1/1`. The task also needs one bounded goal and no unresolved decision.

```mermaid
flowchart LR
    CARD["Complete triage card"] --> SCORE{"total < 5<br/>and no axis > 2?"}
    SCORE -->|no| SPEC["Specialist dispatch"]
    SCORE -->|yes| BOUND{"Needs INTERFACES/contracts,<br/>ADR, Git, secrets, or deploy?"}
    BOUND -->|yes| SPEC
    BOUND -->|no| ADV["The Adventurer<br/>implementation + tests<br/>no Agent"]
    ADV --> VERIFY["Required checks"]
    VERIFY --> TAIL["PR tail — The Bard"]
```

The Hunter may supply the card in its bulletin but never calls The Adventurer. A parent-scored direct request may dispatch the same lane without a GitHub issue; shipping is still a PR (an orphan PR is valid under [[adr-08-github]]). If investigation raises the true score or crosses an excluded boundary, The Adventurer stops and names the owner. It never recruits a second agent.

## 0.5 · The change wrapper — PR out; issue preferred

> Every use-case loop closes with a PR into `main`. A direct commit to `main` is never valid. A GitHub issue is the preferred claim and tracking wrapper; it is not a prerequisite for a PR ([[adr-08-github]]).

The usual loop opens with a `gh` issue and closes with a PR. The worktree is optional. The PR is not. An orphan PR (no parent issue) remains a valid supervised merge when the operator orders ship. A complete Adventurer triage card is enough to start the one-agent lane; The Bard still lands the change through a PR.

```mermaid
flowchart LR
    ISS(["Prefer gh issue<br/>orphan PR still valid"]) --> CLAIM["If an issue exists:<br/>claim it --add-assignee @me"]
    CLAIM --> WT{"Isolate?"}
    WT -->|optional| WK["git worktree<br/>keyed to the issue"]
    WT -->|plain| BR["feature branch"]
    WK --> WORK["…run the use-case loop (§1–§4)…"]
    BR --> WORK
    WORK --> PR["Open PR → main"]
    PR --> MERGE["Merge as the owner identity<br/>owner order is immediate"]
    MERGE --> CLEAN(["Delete worktree + branch<br/>— nothing outlives the PR"])
```

### The claim — the one step that is about the other sessions

**Assign the issue to yourself before you touch anything, and read the claims before you pick.** The assignee is the claim: it costs one `gh` call, needs no new machinery, and it is the only thing in this repo that says *someone is inside this work right now*.

| | |
|---|---|
| **Claim** | `gh issue edit <n> --add-assignee @me` — the moment you start, not when you finish |
| **Read** | `gh issue list --assignee @me` and `gh pr list` before you pick |
| **Release** | closing the issue, or `--remove-assignee @me` if you stop without finishing |

Skipping it is how two sessions find the same defect and repair it in parallel: one opens a PR and merges it, the other opens a second PR and throws both away. Neither could have known. A claim is not a lock and nothing enforces it. It is a signal, and it only works because the next session reads it before choosing what to open.

The tail `Open PR → gate → merge → delete worktree` is the close of every loop that follows; each §-loop renders only its own middle, entered after the issue and exited into the PR. SSOTs: [[adr-07-git]] · [[adr-08-github]] · [[GITHUB]] · guardians (`kbot-prd`/`-adr`/`-api`).

## 1 · Use case — a user-facing feature

> The master loop. The surface's own interactivity ladder decides between server-rendered and client-rich; the service excursion delegates to §2.

The master loop. Its ladder decision resolves through the surface architecture doc the project names at instantiation; its service excursion is §2.

Verify in order: the surface toolchain's **check** (typecheck, agent) → the surface toolchain's **build** (production bundle, agent, **headless, exit 0 required, before merge**) → browser smoke (operator-only, interactive). The build gate is neither smoke nor operator-only, and a green typecheck alone does not clear it.

```mermaid
flowchart TD
    I(["Idea"]) --> UF{"User-facing?"}
    UF -->|no| BE["Service zone — see §2"]
    UF -->|yes| LAD{"Interactivity ladder<br/>criteria in the surface doc"}
    LAD -->|server-owned state| FRAG["Server-rendered fragment"]
    LAD -->|rich client state| ISL["Interactive component — skill: hb-sk-surface-framework"]
    FRAG --> NB{"Needs the service?"}
    ISL --> NB
    NB -->|yes| BE
    NB -->|no| FE["Surface build<br/>hb-sk-surface-framework + component framework"]
    BE --> RET{"Checkpoint: INTERFACES solves the need?"}
    RET -->|yes| FE
    FE --> VER["Verify — 3 layers:<br/>surface check typecheck agent<br/>surface build prod bundle agent exit 0 required<br/>browser smoke operator-only"]
    VER --> LD["Stamp live-doc + CODEMAP"]
    LD --> GRD{"Touched PRD / ADR / INTERFACES surface?"}
    GRD -->|yes| GUARD["Engage guardian(s)"]
    GRD -->|no| PR["PR tail — §0.5:<br/>open PR → gate → merge → delete worktree"]
    GUARD --> PR
```

SSOTs per step: the surface architecture doc · [[INTERFACES]] · [[CODEMAP]] · guardians (`kbot-prd`/`-adr`/`-api`) · [[GITHUB]].

## 2 · Use case — a new service interface

> The interface-first sequence: declare the row in [[INTERFACES]] first, enter the TDD flow, then exit only when the checkpoint confirms [[INTERFACES]] answers the need.

```mermaid
flowchart TD
    N(["Service need"]) --> Q{"Already declared in INTERFACES?"}
    Q -->|yes| REUSE(["Reuse interface — no new row"])
    Q -->|no| ROW["The Cleric adds the INTERFACES.md row<br/>engage kbot-api"]
    ROW --> PLAN["The Trickster: TDD entry + failing tests<br/>hb-sk-tdd / hb-sk-test-runner"]
    PLAN --> MODELS["The Dwarf: models then handlers"]
    MODELS --> GREEN["The Trickster greens"]
    GREEN --> VARS{"Reads a new env var?"}
    VARS -->|yes| VDOC["Declare in VARIABLES<br/>secrets → the secret store only"]
    VARS -->|no| CHK{"Checkpoint: INTERFACES solves the need?"}
    VDOC --> CHK
    CHK -->|no| Q
    CHK -->|yes| GUARD["Guardians: api + adr"]
    GUARD --> PR(["PR tail — §0.5:<br/>The Bard: open PR → merge → delete worktree"])
```

SSOTs per step: [[INTERFACES]] · [[TDD]] · [[SERVICES]] · [[VARIABLES]] · [[CODEMAP]] · guardians (`kbot-prd`/`-adr`/`-api`).

## 3 · Use case — pure Python business logic or a complex script

> The Paladin changes the portable rule first; The Trickster tests that implementation afterward.

This path is only for framework-neutral Python. It may live as a pure module inside `{{service tree}}`, but it does not own models, migrations, persistence, handlers, permissions, routes, payloads, interfaces, frontend, infra, or deployment.

```mermaid
flowchart TD
    N(["Python rule or complex script need"]) --> B{"Framework / ORM / HTTP / UI / cloud dependency?"}
    B -->|yes| SPEC["Return to the applicable specialist path"]
    B -->|no| PAL["The Paladin: state invariants<br/>implement surgical pure core"]
    PAL --> CHECK["Static checks + existing test slice"]
    CHECK --> TEST["The Trickster: focused tests afterward<br/>no TDD entry"]
    TEST --> GREEN{"Tests expose a real defect?"}
    GREEN -->|yes| PAL
    GREEN -->|no| PR(["PR tail — The Bard"])
```

SSOTs per step: [[SERVICES]] · [[TDD]] · [[REQUIREMENTS]] · [[GLOSSARY]]. The Paladin may Agent The Trickster after implementation only. It never calls The Cleric or The Elf.

## 4 · Use case — a docs / doctrine change

> Docs are the product here. ADR rule changes run the supersession lifecycle; the matching guardian is engaged before the batch closes.

Here the docs *are* the product. An ADR rule change runs the supersession lifecycle ([[adr-00-adr-doctrine]]); prose is reached by path; the matching guardian is engaged before the batch closes.

```mermaid
flowchart TD
    D(["Doctrine / docs change"]) --> W{"What is touched?"}
    W -->|ADR rule| ADR["Supersession check, adr-00<br/>semantic → new ADR, defer old"]
    W -->|docs prose / wikilinks| PROSE["Edit by path"]
    W -->|PRD / AGENTS| PRDN["Edit PRD / AGENTS"]
    ADR --> GUARD{"Engage the matching guardian"}
    PROSE --> GUARD
    PRDN --> GUARD
    GUARD -->|ADR / governed file| GA["kbot-adr"]
    GUARD -->|PRD / goal| GP["kbot-prd"]
    GUARD -->|INTERFACES| GI["kbot-api"]
    GA --> NOTIFY["Honor each guardian's notify list"]
    GP --> NOTIFY
    GI --> NOTIFY
    NOTIFY --> PR(["PR tail — §0.5:<br/>open PR → gate → merge → delete worktree"])
```

SSOTs per step: [[adr-00-adr-doctrine]] · guardians (`kbot-prd`/`-adr`/`-api`) · [[GLOSSARY]] (a new name gets its row first) · [[GITHUB]].

## Variants

> Shorthand for the non-standard paths: surface-only, infra/cloud, smoke-test, and unattended runs.

- **Surface-only** change → the `Needs the service? = no` branch of §1; [[INTERFACES]] is never entered. The build gate still runs headless before merge: this branch carries the fewest gates, so the bundle is where a broken import or render error surfaces.
- **Eligible small task** → §0.25 replaces the specialist middle with The Adventurer; the Bard still owns the PR tail.
- **Pure Python business logic / complex script** → §3; implementation first by The Paladin, focused tests afterward by The Trickster.
- **Infra / cloud** change → The Wizard (`hb-ag-ops`, `hb-sk-cloud` / `hb-sk-local-runtime`) in place of [[INTERFACES]]/[[TDD]]; the resource lands in the project's infrastructure inventory ([[INFRASTRUCTURE]]). Ship via The Bard.
- **Smoke tests** are operator-only and interactive; an agent routine that reaches a smoke step stops and defers ([[AGENTS]]).
- **Automated** — the §0.5 wrapper walked by an unattended process instead of a person: issue in, PR out, never a merge.
