---
title: Soft dispatch graphs — prompt class to hb-ag-* handoff
type: reference
status: active
version: v0.1.4
tags: [harness, agents, dispatch]
description: "Soft, host-agnostic graphs: given a user prompt class, which hb-ag-* goes first and whom they call. Included from ADND-AGENTS."
applies_when:
  - When a user prompt could belong to more than one area owner.
  - When deciding between The Adventurer, The Paladin, or a specialist owner.
related_adrs:
  - adr-01-nomenclature
  - adr-02-stack
  - adr-07-git
  - adr-08-github
---

# ADND-DISPATCH — soft graphs

> Included from [[ADND-AGENTS]]. Roster, areas, and "who knows whom" live there. This file is only **how to proceed** from a class of user prompt.

**Soft:** a parent or subagent is expected to follow these graphs. It is not a hard `agentType` resolver. Do not hand-dispatch archived `kwf-*` nodes from here.

**Host-agnostic:** the node labels are stems (`hb-ag-contracts`, `hb-ag-service`, `hb-ag-paladin`, `hb-ag-surface`, `hb-ag-ops`, `hb-ag-judge`, `hb-ag-test`, `hb-ag-adventurer`, `hb-ag-git`, `hb-ag-hunter`, `hb-ag-hawk`, `hb-ag-hound`). Where the host has no native type for a stem, the parent loads `agents/<stem>.md` and still obeys the graph.

The development loop remains [[DEVELOPMENT-LOOP]]. These graphs name **which agent** walks each step, including the Paladin's implementation-first pure-Python path and the Adventurer's one-agent small-task lane.

## Recursion (always)

- **The Cleric** has `Agent` (Dwarf, Elf, Trickster). After the catalog hunk: call the next owner, or return the row / adaptation instruction.
- **The Paladin** has `Agent` (Trickster only, after implementation). Never Cleric or Elf.
- **The Adventurer** has no `Agent`. The parent dispatches it; it finishes or returns `ADVENTURER STOP`.
- **The Trickster** has no `Agent`. Returns the traps. Does not spawn Dwarf / Elf to "fix" a red.
- **The Inquisitor** has no product `Write` and does not spawn builders to "fix" a finding. Returns the named rule. Not a merge gate.
- **The Bard** has no `Agent`. Does not write app code while shipping. Does not spawn builders to "fix" a red on the way to `main`.
- **The Hunter** has `Agent` (Hawk, Hound only). Does not Agent area owners. Does not spawn a builder to "fix" the issue.
- **The Hawk** and **The Hound** have no `Agent`. They return a pack to The Hunter.
- Do not nest two Inquisitor calls.
- **Elf never Agents Dwarf. Dwarf never Agents Elf.** Only The Cleric carries messages both ways. The Paladin is not a third hop.
- **Dwarf may Agent Paladin** only for framework-neutral Python business logic or a complex script core, before the Dwarf's TDD path.
- One missing-row trip to The Cleric per need. Do not edit [[INTERFACES]] from Dwarf, Elf, or Trickster.
- **git / PR / merge → Bard.** No area owner may `git` or `gh`. The hunting party may `gh` issues only. Their Bash is not a loophole.
- **Issue hunt → Hunter.** Area owners do not Agent the hunting party. The hunting party does not Agent area owners.
- **Adventurer lane → parent only.** The Hunter records triage but does not call The Adventurer. No specialist calls The Adventurer, and The Adventurer calls nobody.

## Prompt class → first agent

Classify the **user's ask**, not the files you wish were in scope. First check whether the parent has a complete [[ISSUE-TRIAGE]] card. If all three scores total less than `5`, none exceeds `2`, the goal is bounded, and no interface/contract, ADR, Git/GitHub, secret, or deployment change is required, dispatch The Adventurer **instead of** the specialist graph. Otherwise follow the matching specialist row.

| Prompt class | First agent | Then if |
|---|---|---|
| Eligible triage: `severity + collateral + effort < 5`, no axis `>2`, no excluded boundary | The Adventurer | One agent writes implementation + tests and verifies. Scope grows → stop and name owner; **never** Agent |
| Framework-neutral Python business rule, calculation, policy, transformation, algorithm, or complex script core | The Paladin | Implement first → Trickster writes tests afterward. No API/frontend. Never Cleric or Elf |
| New/changed page, component, tokens, surface UI | The Elf | Interface content needed → Cleric (not framework, not paths). Tests → Trickster. **Never** Dwarf. ABC/ADR claim → Inquisitor |
| New/changed framework model, persistence, handler, permission, route, or adapter | The Dwarf | Pure core → Paladin before TDD. Row missing → Cleric. Tests / `docs/tdds/` → Trickster. **Never** Elf. ABC/ADR claim → Inquisitor |
| Add/change/retire an interface **row** or `docs/contracts/` | The Cleric | Translate to a six-column row and/or request Dwarf; return the contract or "adapt" to Elf |
| Elf asks for **interfaces** (fields, page, UI need) | The Cleric | If already computable from served data: tell Elf to adapt (no row). If new: row, then Trickster (TDD) then Dwarf |
| `docs/tdds/`, service tests, surface tests, harness tests | The Trickster | Write the traps; return. Paladin tests are after implementation. Adventurer writes its own eligible-task tests. Trickster does not spawn builders |
| Local orchestration file, profiles, bind-mounts, ports | The Wizard | Dispatch. Not The Dwarf |
| Cloud services, load balancing, secret-store names | The Wizard | Dispatch. Not The Dwarf. Do not invent infrastructure the layout lacks |
| "Does this PR / plan / diff comply with PRD, ADRs, or INTERFACES?" | The Inquisitor | Quick-exit report. Do not author a fix. Parent may load `hb-sk-abc`; Inquisitor does not |
| "Does this comply with adr-NN?" / about to assert ADR compliance | The Inquisitor | Area owner must **call**. Do not self-certify |
| Writing `adrs/` itself | guardian `kbot-adr` | Not The Inquisitor. Watchlist in [[AGENTS]] |
| `git`, `gh`, commit, push, PR, merge | The Bard | Quick-exit. No area owner. Bard does not patch product trees while shipping. Issue hunt is not this row |
| Lowest-numbered issue, issue triage, issue forensics, hunter bulletin | The Hunter | Parallel Hawk + Hound (`scout`). Immediate existing-test repro (quick-exit). Bulletin. **Never** an area owner |
| Ambiguous (screen + new interface + infra) | Parent splits | Catalog first (Cleric), tests (Trickster), then Dwarf, then Elf; infra last (Wizard). Surface↔service only through Cleric. Ship via Bard. Inquisitor after the product hunk if ABC is in question |

Undeclared route in code is a defect ([[INTERFACES]]). Inventing a path on the surface is the same defect.

## Graph — user-facing page

```mermaid
flowchart TD
  p[Prompt: page or component]
  e[The Elf]
  c[The Cleric]
  t[The Trickster]
  j[The Inquisitor]
  p --> e
  e -->|"interfaces: content needed"| c
  c -->|contract or adapt| e
  e -->|"screen built, need tests"| t
  t -->|traps returned| e
  e -->|"ABC or ADR claim"| j
  j -->|finding, not a merge gate| e
```

A page binds to a **declared** row in [[INTERFACES]]. The surface toolchain only. Screen copy in `{{interface language}}` ([[adr-01.b-localization]]). The Elf does not Agent The Dwarf.

## Graph — interface request (Elf → Cleric → Dwarf)

```mermaid
flowchart TD
  e[The Elf]
  c[The Cleric]
  d[The Dwarf]
  e -->|"interfaces as CONTENT NEEDED<br/>fields, page, UI need — not framework, not paths"| c
  c -->|"already computable from served data"| adapt[tell Elf to adapt — no new row]
  c -->|"has logic, domain+model, not already served"| row[six-column INTERFACES.md row]
  row --> d
  d -->|forge the service tree| done[implemented]
  adapt --> e
```

The Cleric is the sole write on [[INTERFACES]]. The Dwarf waits for the row, then forges. If the need is already computable: no new row.

## Graph — TDD (Cleric → Trickster → Dwarf)

```mermaid
flowchart TD
  c[The Cleric]
  t[The Trickster]
  d[The Dwarf]
  c -->|new approved row| t
  t -->|TDD entry + failing unit tests| d
  d -->|implements the service tree — never tests| t
  t -->|greens / adds more| done[green]
```

The Dwarf never writes tests or TDD entries. The Trickster is the dedicated test writer; a validated Adventurer lease is the sole exception. The Trickster cannot give face (no UI, not the product). Surface tests: after The Elf builds, The Trickster may use `hb-sk-surface-framework`.

## Graph — Paladin (implementation, then tests)

```mermaid
flowchart TD
  p[Prompt: pure Python business logic or complex script]
  pal[The Paladin]
  t[The Trickster]
  p --> pal
  pal -->|implement surgical pure core| done[implementation]
  done -->|"afterward: paths + invariants + edge cases"| t
  t -->|focused tests| green[verified]
```

The Paladin owns only framework-neutral Python logic. A framework, ORM, HTTP, UI, cloud, or deployment dependency returns the work to the parent. No TDD entry is backfilled. The Paladin may Agent The Trickster after implementation; never The Cleric or The Elf.

## Graph — Adventurer (one-agent lane)

```mermaid
flowchart TD
  card[Complete triage card]
  gate{"sum < 5<br/>no axis > 2<br/>no excluded boundary"}
  adv[The Adventurer<br/>broad context · default effort]
  work[implementation + tests + verification]
  stop[ADVENTURER STOP<br/>name owner, call nobody]
  card --> gate
  gate -->|yes| adv
  gate -->|no| stop
  adv --> work
  work -->|"scope remains eligible"| done[return complete slice]
  work -->|"score rises or boundary appears"| stop
```

The parent alone opens this lane, including from a Hunter bulletin. The valid score shapes are `1/1/1` and permutations of `2/1/1`. The Adventurer has no `Agent`, does not use Git/GitHub, and cannot change interfaces/contracts, ADRs, secret values, or deployment state.

## Graph — catalog only

```mermaid
flowchart TD
  p[Prompt: interface row or contract]
  c[The Cleric]
  next[Dwarf and/or Elf and/or Trickster]
  p --> c
  c -->|six-column row, then Agent or return| next
```

The Cleric does not write routes or pages.

## Graph — service (no tests)

```mermaid
flowchart TD
  p[Prompt: service change]
  q{Framework-neutral<br/>Python core?}
  pal[The Paladin]
  d[The Dwarf]
  c[The Cleric]
  p --> q
  q -->|yes| pal
  q -->|no| d
  d -->|"row missing"| c
  c -->|return row or adapt| d
  d --> forge[models then handlers plus declared paths]
```

The service's own toolchain only. Pins in [[REQUIREMENTS]]. Dwarf tests are The Trickster's red-first graph. Paladin tests follow implementation in the Paladin graph.

## Graph — Wizard (live)

```mermaid
flowchart TD
  p[Prompt: local runtime or cloud or secrets]
  wiz[The Wizard]
  p --> wiz
  wiz --> work[orchestration file / cloud / CI / secret names]
```

The parent may dispatch The Wizard. Do not "fix" the layout's deliberate absences.

## Graph — Inquisitor (quick-exit)

```mermaid
flowchart TD
  p[Prompt: judge PR or ADR compliance]
  j[The Inquisitor]
  p --> j
  j --> q{enough to report?}
  q -->|yes| r[named rules; remaining ~70% unexplored is enough]
  q -->|insisted: full explore| full[continue, still read-only]
  r --> p
  full --> p
```

Area owners **call** this graph when they would otherwise write "this follows the ADRs" without an interrogation. The Inquisitor does not load `hb-sk-abc`; the **parent** may. Do not patch in that turn. Prefer a lightweight high-context model at dispatch; `model: inherit` in the agent file.

`prd-fail` / `adr-fail` / `api-fail` **report**. They do not block an owner merge. A `Guardian-Verdict:` line is not a review label and is not The Inquisitor's to write ([[AGENTS]], [[PR-REVIEW-ROUTINE]]).

## Graph — Bard (git / GitHub)

```mermaid
flowchart TD
  p[Prompt: git or gh or PR or merge]
  b[The Bard]
  p --> b
  b --> ship["git / gh only — no product-tree Write"]
```

`main` is the single line; `{{owner}}`; a PR is required; `--admin` when an owner merge would wait on checks ([[adr-08-github]]). The Bard does not write app code to "fix while shipping." Any area owner that hits git **returns**; the parent loads The Bard. Issue pick and triage are The Hunter.

## Graph — Hunter (issue hunt)

```mermaid
flowchart TD
  p[Prompt: issue N or lowest open]
  h[The Hunter]
  k[The Hawk]
  d[The Hound]
  r[Existing-test slice]
  b[Bulletin]
  p --> h
  h -->|"brief, parallel scout"| k
  h -->|"clues, parallel scout"| d
  h -->|"immediately, do not wait"| r
  k -->|HAWK pack| h
  d -->|HOUND catalog| h
  r -->|reproduced or quick-exit| h
  h --> b
```

The Hunter fires Hawk and Hound, then **immediately** runs one existing-test slice to reproduce. It strips noise from the report and pins a bulletin at **The Three Feathers** — finished `problem` plus one specific `goal` — for a later Hunter. Quick-exit on the repro is enough. It does not write tests and does not Agent The Trickster. Scout packs fold into the bulletin when they land. Hawk: Graphify first, then `gh`. Hound: Graphify first, then Grep. Neither familiar loads [[PRD]]. The party does not Agent area owners. The parent may use the bulletin's completed triage card to open the Adventurer lane.

## Parent session (any host)

1. Read [[ADND-AGENTS]] (this file is included there).
2. If a complete triage card exists, validate the Adventurer gate first. The Hunter supplies scores but never dispatches the builder.
3. Otherwise classify the prompt with the specialist table.
4. Dispatch or impersonate **one** first agent. Do not overlap an Adventurer lease with a specialist.
5. Follow `Then if` until the ask is done. Paladin → Trickster happens only after implementation. Surface ↔ service traffic goes through The Cleric. Ship through The Bard.
