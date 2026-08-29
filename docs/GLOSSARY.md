---
title: Canonical naming authority, terms, and forbidden forms
type: reference
status: active
version: v0.1.4
tags: [harness, glossary, ssot]
description: "Canonical naming authority, terminology invariants, and forbidden forms across the codebase. Harness terms ship live; project terms are registered at instantiation."
applies_when:
  - When introducing variables, settings, or secret stems.
  - When checking forbidden synonyms or prohibited aliases.
  - When naming harness skills, hooks, workflows, or agent roles.
  - When registering a new project domain term.
related_adrs:
  - adr-01-nomenclature
---

# GLOSSARY — naming authority

Canonical form and forbidden forms. Force: [[adr-01-nomenclature]].

| Term | Canonical form | Applies to | Forbidden forms |
|---|---|---|---|
| product name | `{{project name}}` | the project's prose name — docs, PRs, README, rendered copy (the screen keeps the English product name) | inventing a prose name without a row here |
| project slug | `{{project slug}}` | this project's slug — names, hosts, env seeds | a hardcoded slug literal outside the sanctioned consumption points ([[VARIABLES]]) |
| the single line | `main` | git default, PR target for every change, **and** the production line — every push to it ships ([[GITHUB]], [[adr-07-git]]) | `master`; calling `main` "integration only"; any second branch presented as the live line |
| production branch | *(none)* | there is no production branch; `main` is the live line ([[adr-07-git]] rule 2, [[GITHUB]]) | recreating `prod`; `production`, `release`, `staging` as a new live line; confusing a retired branch with a `prod` **environment** name |
| development flow | `issue → worktree → PR` | the mandatory shape of every change ([[DEVELOPMENT-LOOP]]) | skipping the issue; a direct hand-commit to `main` |
| worktree | `worktree` — a git worktree, keyed to its issue; optional, and destroyed on integration ([[DEVELOPMENT-LOOP]]) | git isolation for a change | `checkout` (for this meaning); a worktree that outlives its PR |
| integration | `integration` — merge of a PR into `main`, performed only as the `{{owner}}` identity ([[GITHUB]]) | landing a change on `main` | calling a direct push to `main` "integration" |
| adr, tdd | lowercase in filenames (`adr-NN-slug.md`); uppercase only for the manual [[TDD]] | files, wikilinks | mixed-case filenames |
| defered | `defered` | ADR lifecycle status token ([[adr-00-adr-doctrine]]) | `deferred` — the token's spelling is intentional |
| interface | `interface` | any route declared in [[INTERFACES]] | `endpoint` drift in prose; `route` (in catalog context) |
| live-doc block | `live-doc block`, delimited `LIVE-DOC:START … LIVE-DOC:END` | the wikilinks-only region stamped at the top of every matched code file, linking it to the ADRs and docs that govern it ([[CODEMAP]], [[HARNESS]]); stamped only by the linker, never by hand | `docstring header`, `backlink header`, `doclink`, `frontmatter` (for this meaning); any block carrying prose instead of links |
| Graphify | `Graphify` — the on-device code graph; first exploration mechanism when present ([[GRAPHIFY]], [[adr-35-graphify]]) | agent exploration of code and docs | treating [[CODEMAP]] as that graph; committing `graphify-out/cache/`; Grep-first while the graph is present |
| Graphify skill | `kskill-graphify` | vendored procedure for [[adr-35-graphify]]: query/path/explain, ensure (CLI + code-only graph after clone), extract, CLI upgrade, upstream skill snapshot. Scripts under `skills/kskill-graphify/bin/` | `graphify/` unprefixed; `npx skills add`; `graphify add <url>` |
| guardian | `kbot-prd`, `kbot-adr`, `kbot-api` — SSOT-watching subagents | agent names, dispatch, docs | `watcher`, `checker`, ad-hoc renames without a row here |
| harness kind prefix | `kskill-` / `hb-sk-` / `khook-` / `kbot-` / `hb-ag-` / `kwf-` | the mandatory first segment of every harness artifact's name, saying **what it is** before what it does: a reusable skill (`kskill-`), a **product** knowledge skill (`hb-sk-`), a hook, a lobe/guardian agent (`kbot-`), a **product** area-owner agent (`hb-ag-`), a member of the delivery party ([[HARNESS]]) | an unprefixed harness name; `kdx-` as a kind prefix (it names the author, not the kind); prefixing by stack; `hb-` with no `sk`/`ag` infix as a new artifact |
| harness name stem | the segment after the kind prefix | names the **role** — `kbot-adr`, `hb-sk-contracts`, `hb-ag-service`. Reusable skills do not embed the project in the stem. Product artifacts put the project in the **prefix** (`hb-sk-` / `hb-ag-`), not the stem | embedding the deployment or the client in a stem |
| hb-sk skill | `hb-sk-<contract>` | product knowledge skill: one pinned contract, thin `SKILL.md`, SSOT pointer into the docs. Fourteen ship in the template: the original eleven (`component-framework`, `surface-framework`, `interface-framework`, `domain-framework`, `contracts`, `tdd`, `test-runner`, `local-runtime`, `cloud`, `git`, `abc`) plus the hunting party (`hunter`, `hawk`, `hound`). One owner each except `abc` (parent fallback; Inquisitor loads none) and `surface-framework` (Elf-owned; Trickster may load for surface tests) ([[HARNESS]]) | copying vendor docs into `skills/*/references/`; a product skill with no owner |
| hb-ag agent | `hb-ag-<area-or-role>` | product agent under `agents/`. Live tree party: `contracts` (The Cleric), `service` (The Dwarf), `paladin` (The Paladin), `surface` (The Elf), `ops` (The Wizard), `judge` (The Inquisitor), `test` (The Trickster), `adventurer` (The Adventurer), `git` (The Bard). Live hunting party: `hunter` (The Hunter), `hawk` (The Hawk), `hound` (The Hound). Stem + title in the body ([[HARNESS]]) | unprefixed `warrior` / `archer` / `elf` / `cleric` / `paladin` / `trickster` / `adventurer` / `bard` / `hunter` / `hawk` / `hound`; restoring `The Archer` or `The Warrior` as a live title; restoring `kbot-*` builders |
| sealed pair | The Dwarf (`hb-ag-service`) and The Elf (`hb-ag-surface`) | two area owners that must not Agent each other; The Cleric is the only hop and the only writer of [[INTERFACES]] | a third hop between them; the Dwarf writing the catalog; The Elf inventing a path |
| The Cleric | `hb-ag-contracts`, title **The Cleric** | sole writer of `docs/INTERFACES.md` and `docs/contracts/`; `Agent` → Dwarf, Elf, Trickster | `The Archer` as a live title; unprefixed `cleric`; `kwf-archer` (archived *surface* builder of `triage-and-fix`); walking into `{{service tree}}` or `{{surface tree}}` |
| The Dwarf | `hb-ag-service`, title **The Dwarf** | owns framework-bound work in `{{service tree}}`; `Agent` → Cleric, Paladin (pure Python logic), Trickster (tests), Wizard (infra); never Elf | writing `INTERFACES.md`, tests, `docs/tdds/`, pure business logic assigned to The Paladin, or the local runtime; `git` / `gh`; Agent The Elf; `kwf-warrior` (archived *service* builder) |
| The Paladin | `hb-ag-paladin`, title **The Paladin** (El Paladín) | framework-neutral Python business logic and complex Python scripts; implements first, then Agents The Trickster for tests | Django or other framework-bound service work; models, handlers, permissions, routes, interfaces, frontend, infra, tests, `git` / `gh`; Agent The Cleric or The Elf |
| The Elf | `hb-ag-surface`, title **The Elf** | owns `{{surface tree}}` except tests; `Agent` → Cleric (Trickster for tests; Wizard for infra; never Dwarf); the screen in `{{interface language}}`. Optional: a headless project deletes it | `kwf-archer` (archived *surface* builder); `kwf-warrior` (that was the service); writing `INTERFACES.md`; Agent The Dwarf; `git` / `gh`; restoring `The Warrior` as a live title |
| The Wizard | `hb-ag-ops`, title **The Wizard** | local runtime, cloud, CI, secrets named in [[INFRASTRUCTURE]] / [[VARIABLES]] — live; parent may dispatch | writing app trees or `INTERFACES.md`; eating infra into The Dwarf; `git` / `gh` |
| The Inquisitor | `hb-ag-judge`, title **The Inquisitor** | read-only reports; loads no skill; `hb-sk-abc` is parent fallback | authoring the change; a review label as a merge gate; loading skills; `git` / `gh` |
| The Trickster | `hb-ag-test`, title **The Trickster** | dedicated owner of `docs/tdds/` and tests; tests The Paladin's implementation afterward; no `Agent`; cannot give face. The Adventurer lane is the single test-write exception | writing product code or `INTERFACES.md`; unprefixed `trickster`; `git` / `gh` |
| The Adventurer | `hb-ag-adventurer`, title **The Adventurer** (El Aventurero) | one eligible small task, implementation and tests, with broad context and default (medium) effort; no `Agent` | incomplete or ineligible triage; interfaces/contracts, ADRs, git/GitHub, secret values, deployment, or calling another agent |
| The Bard | `hb-ag-git`, title **The Bard** | the only `hb-ag-*` that may `git` / open or merge a PR; no product-tree Write; no `Agent` | unprefixed `bard`; other agents running `git` or shipping `gh`; writing app code while shipping; `kwf-bard` as this agent |
| Adventurer lane | one score on each [[ISSUE-TRIAGE]] axis, `severity + collateral + effort < 5`; therefore only `1/1/1` or a permutation of `2/1/1` | mutually exclusive parent-dispatched implementation lane: The Adventurer owns the complete bounded change and its tests, while normal area-owner dispatch pauses for that slice | any axis at `3`; a total of `5+`; missing scores; using the lane to bypass interface, ADR, Git, secret, or deployment ownership; dispatching a second agent |
| The Three Feathers | `The Three Feathers` — Las Tres Plumas | the inn: GitHub issues, pull requests, and the agents that work them. An arbitrary grouping for those harness elements. The Hunter's notice board is an issue comment there ([[GITHUB]], `hb-sk-hunter`) | a second board (a docs file, a chat dump, a local handoff folder) as the hunt's notice; calling that pile only "GitHub" in hunt prose without this name |
| notice board | Hunter **bulletin** — structured issue comment at The Three Feathers | the handoff note The Hunter pins on an issue (`cursor-issue-triage`). Written for a **later Hunter**: cold-start, noise stripped, one `goal` | pasting the raw issue body as the bulletin; a session dump; a `goal` that is "investigate" or empty |
| The Hunter | `hb-ag-hunter`, title **The Hunter** (El Cazador) | issue gateway of the hunting party; fires The Hawk and The Hound, runs one existing-test slice, posts the bulletin at The Three Feathers | Agent-ing area owners; writing tests or product trees; `git` / PR; a bulletin without `problem` and `goal` |
| The Hawk | `hb-ag-hawk`, title **The Hawk** (El Halcón) | Hunter-only familiar; historical issues; Graphify then `gh`; cheap `scout` | searching the codebase as The Hound; Agent anyone; writing the bulletin |
| The Hound | `hb-ag-hound`, title **The Hound** (El Sabueso) | Hunter-only familiar; keyword/tag walk of the tree; Graphify then Grep; cheap `scout` | searching GitHub issues as The Hawk; Agent anyone; writing the bulletin |
| harness SSOT trees | `skills/` · `hooks/` · `agents/` · `adrs/` | the one real copy of every skill, hook, agent definition and ADR. `.claude/{skills,hooks,agents,rules}` and `.agents/{skills,hooks,agents,rules}` are **links** to them; a second real copy is a second authority that can drift ([[HARNESS]]). Reached by path | a second real directory at any of the link paths |
| agent definition contract | the closed frontmatter key set every file under `agents/` declares — `name`, `description`, `model`, `tools`, `related_adrs`, plus the cosmetic `color` ([[HARNESS]]) | authoring or reviewing any agent definition; `tests/test_hb_ag_roster.py`, `tests/test_agents_are_subagents.py`, `tests/test_agent_model_inherit.py` | an inline or flow `tools:` list (the block sequence is the one shape); an invented key; omitting `related_adrs` instead of declaring `[]` |
| ADR-to-agent edge | the pair `related_agents:` on the ADR side and `related_adrs:` on the agent side, naming each other ([[adr-00-adr-doctrine]] r3, [[HARNESS]]) | ADR frontmatter, agent frontmatter, the symmetry check | a one-sided edge; declaring the edge in prose only; repairing one end by rewriting the other |
| agent model binding | `model: inherit` — the only value in agent frontmatter; the harness binds a vendor model at dispatch via role slugs `thinker`, `builder`, or `scout` ([[HARNESS]]) | agent frontmatter | any value other than `inherit`; a vendor product name in an agent's `name` or `description` |
| harness model role | `thinker` \| `builder` \| `scout` — planner/thinker, builder, or fast/scout; workflow scripts use these slugs; the runtime maps each to a vendor model ([[HARNESS]]) | workflow dispatch contracts | a vendor product alias in harness prose |
| delivery party | the archived `kwf-*` cast — workflow nodes resolved by script, never dispatched by hand | historical references in harness prose | live `kwf-*` files; hand-dispatching a `kwf-*` node |
| plan-time doctrine gate | familiars judging **the plan**, before a line is written, each reading its SSOT by path; emits `Plan-Verdict: <ssot>: <status>` lines keyed by SSOT, never by guardian name ([[GITHUB]]) | unattended delivery runs | a `Plan-Verdict:` line naming a guardian; judging the diff at plan time |
| merge-gate verdict line | `Guardian-Verdict: <guardian>: <status>` when that guardian ran; `Plan-Verdict: <ssot>: <status>` when the doctrine review judged that SSOT, `<ssot>` ∈ `prd` \| `adr` \| `api` | PR bodies, the `pr-merge-gate` CI job ([[GITHUB]]) | prose that mentions a guardian without the exact line shape; an unattended routine writing the line |
| mood skill | `kskill-mood`, slash `/kdx-mood` | vendored session-stance skill: moods change how work is done, never what the work is. Real copy `skills/kskill-mood/` ([[HARNESS]]) | directory `kdx-mood/` as the real copy (`kdx-` is not a kind prefix); a mood that changes the task |
| quick-win skill | `kskill-qw`, slash `/qw` | Quick Win shortcut — identical to `/kdx-mood quick win`. Delivery: understand (re-ask if needed), PR, merge to `main`, `/cowsay` with legend `QUICK WIN` | a second mood parser; directory `qw/` as the real copy; stopping at an open PR when integrate was already authorized |
| cowsay skill | `kskill-cowsay`, slash `/cowsay` | balloon plus cow **or** a closed legend set in `kskill-micro-solid-font` that replaces the animal. Binary `skills/kskill-cowsay/bin/cowsay`. Stop brief uses Tux (`-f tux`) and an `{{interface language}}` balloon. | hand-drawn letters; a cow and a legend on the same print; a fifth legend; a second glyph table; `apt install cowsay` |
| cowsay legend | the closed set `QUICK WIN` · `GH ISSUE` · `GH REPO` · `EPIC DONE!` | the only phrases `/cowsay` may put under the balloon; each is rendered by `kskill-micro-solid-font`. `/qw` uses these. The Tux stop brief does not. | a new token; using a legend as a footer under the cow; figlet or a 5-row banner |
| cowsay final hook | the `/cowsay` render that closes a goal | the last dialog of a completed goal is printed through `skills/kskill-cowsay/bin/cowsay`, never freehanded — legend for a delivery, Tux for a stop brief | printing the summary as plain prose; drawing the box by hand; a second renderer |
| micro-solid font skill | `kskill-micro-solid-font` | 3-row variable-width solid block font. Glyphs live in `skills/kskill-micro-solid-font/font.py` — that file is the font. Locked examples: `QUICK WIN`, `GITHUB TASK`, `GOAL!` | hand-drawn `█` letters; a fourth row; copying the dictionary into cowsay or a prompt |
| micro-solid glyph | a 1-, 3-, or 5-column triple of `█` / space rows | one letter in `kskill-micro-solid-font`. `I` and `!` are 1-wide; `M` and `W` are 5-wide; space is 2-wide; the rest of A–Z is 3-wide. `O` is the diamond so it does not collide with `G` | a shaded cell; a serif; treating `G` and `O` as the same box |

## Project terms

`{{project terms}}` — the project's own domain nouns, entities, and component
names are registered here at instantiation and maintained forever after
([[adr-01.a-glossary]]): one row per term — canonical form, scope, forbidden
forms. The table starts empty on purpose; the harness rows above are the
worked example.

| Term | Canonical form | Applies to | Forbidden forms |
|---|---|---|---|
| {{example term}} | `{{canonical form}}` | {{term applies to}} | {{forbidden forms}} |
