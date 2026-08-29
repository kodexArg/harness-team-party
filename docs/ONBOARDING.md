---
title: Incoming-agent fill-in map for harness-team-party
type: reference
status: active
version: v0.1.4
tags: [harness, onboarding, instantiation, placeholders]
description: "Playbook for another model entering this template: how to fill every slot without confusing AGENTS.md, plus the full placeholder inventory."
applies_when:
  - When an agent first enters an unfilled harness-team-party clone.
  - When filling or auditing double-curly placeholders.
  - When deciding whether a remaining brace span is a live slot.
related_adrs:
  - adr-02-stack
  - adr-05-after-versioning
  - adr-35-graphify
  - adr-03-backend
  - adr-04-frontend
---
# ONBOARDING — fill this template

This file is the **fill-in map**. It is not the session index.

| File | What it is | What you do with it |
|---|---|---|
| **This file** (`docs/ONBOARDING.md`) | How to instantiate, and the inventory of every live slot | Follow it until no live slots remain |
| **`AGENTS.md`** (same bytes as `CLAUDE.md`) | Runtime index: how agents work *after* the product exists | **Fill its slots. Do not rewrite its harness procedure.** The useful parts (Graphify, ABC, roster, routing) already belong to the harness |
| **`docs/CLONE.md`** | Operator copy, `hb-` prefix rename, trees, first commit | Do those steps; do not treat it as a second inventory |
| **`docs/PRD.md`** | Product constitution skeleton | Write the product here; every other file borrows names from it |

If you open `AGENTS.md` first and see `{{project name}}` mixed with Graphify and dispatch rules, that is expected. The braces are empty product fields. The surrounding sentences are already in force.

## 0 · Graphify — install it if you can

This harness wants Graphify. Treat a missing graph as a **bootstrap gap**, not as permission to live in Grep.

When the host can install tools (especially `uv`):

1. Run `skills/kskill-graphify/bin/ensure` from the repo root. That installs `graphifyy[mcp]` and makes sure `graphify-out/graph.json` exists. A **code-only** graph does **not** need an LLM key.
2. Enable the project MCP server in `.mcp.json` → `mcp/mcp.json` (the `graphify` server). Worktree chats do not inherit the parent clone's MCP approval — turn Graphify on in **this** worktree's MCP panel, or point a user-level server at an **absolute** `graph.json` path ([[GRAPHIFY]]).
3. Query first (`query_graph`, `get_node`, `get_neighbors`, `shortest_path`), then Read the files the graph named.
4. If the operator can spare an LLM key, `skills/kskill-graphify/bin/extract` builds the richer docs+harness graph. Nice; not a gate on filling slots.

If `ensure` cannot run (no `uv`, no network, locked-down sandbox), say so, then Grep. Do not skip Graphify out of habit when install is available.

Facts and commands: [[GRAPHIFY]]. Force: [[adr-35-graphify]].

## 1 · Orient, then fill

1. Hold [[PRD]] and [[INTERFACES]] — they are still skeletons; that is fine.
2. Use Graphify (section 0).
3. Build a **value ledger** (section 3): one concrete string per shared token, reused everywhere that token appears.
4. Global-replace shared tokens (`{{project name}}`, `{{service tree}}`, …) in **every** file they appear, including `AGENTS.md` / `CLAUDE.md`.
5. Write **one-shot** content in place (PRD stories, INTERFACES rows, GLOSSARY project terms, ROADMAP stages, VARIABLES rows). Do not invent a second catalog.
6. Then [[CLONE]] steps 3–8: `hb-` → `{{prefix}}`, stack decision, **backend/frontend ADR families** ([[adr-03-backend]], [[adr-04-frontend]] — fill slots, delete unused subs), trees, skill-folder rename, headless deletions, first commit.

Keep code and docs in English. Screen copy later uses `{{interface language}}`.

## 2 · Slot syntax

Live instantiation slots look like `{{english words}}` — lowercase, spaces allowed, **no** `$` before the braces.

**Replace the same token with the same value everywhere.** `{{project name}}` in the PRD title, `AGENTS.md`, `.env.example`, and the glossary is one string.

**Do not replace:**

| Brace span | Why |
|---|---|
| `${{ github.* }}` in `.github/workflows/` | GitHub Actions syntax |
| `{{TITLE}}`, `{{HOOK}}`, `{{STAT_LABEL}}`, and other **UPPERCASE** slots under `skills/kskill-report/` and `skills/diagram-design/` | Fill-at-render inputs for those skills, not product instantiation |
| Mermaid `{{hexagon}}` documented inside `kskill-report` | Diagram node syntax |
| Instructional phrases that *talk about* slots | This file and [[CLONE]] describe tokens on purpose so a later agent can search for them |

After fill, leftover detection **excludes** this file, [[CLONE]], vendored-skill render templates, and GitHub Actions:

```bash
grep -rn "{{" --exclude-dir=.git --exclude-dir=skills/kskill-report --exclude-dir=skills/diagram-design \
  --exclude=docs/ONBOARDING.md --exclude=docs/CLONE.md .
```

You should then see only `${{` in workflows, or nothing product-shaped.

## 3 · Value ledger — fill once, reuse

Decide these **before** editing files. Copy the bound value into every path listed in the inventory (section 7).

### Identity

| Token | Load | Example |
|---|---|---|
| `{{project name}}` | Prose product name (English in git/docs) | `Acme Billing Console` |
| `{{company name}}` | Organization | `Acme` |
| `{{owner}}` | GitHub owner account | `acme-co` |
| `{{repo}}` | GitHub repository name | `acme-billing-console` |
| `{{project slug}}` | Slug for hosts, env seeds, names | `acme-billing` |
| `{{prefix}}` | Product kind prefix **including the trailing dash**; replaces `hb-` | `abc-` |
| `{{one-line product statement}}` | One sentence: what the product is | `Operator console for Acme invoices` |
| `{{product kind}}` | Kind of product | `SaaS workspace`, `CLI tool`, `Kotlin service` |

### Locale (screen only)

| Token | Load | Example |
|---|---|---|
| `{{interface language}}` | Human language of the UI | `Spanish (es-AR)` |
| `{{interface locale}}` | Locale tag | `es-AR` |
| `{{number format}}` | How numbers render on screen | `1.234.567,89` |
| `{{date format}}` | How dates render on screen | `DD/MM/YYYY` |
| `{{timezone}}` | Product timezone | `America/Argentina/Buenos_Aires` |

### Trees, flow, deploy

| Token | Load | Example |
|---|---|---|
| `{{service tree}}` | Service code root, trailing slash | `service/`, `backend/` |
| `{{surface tree}}` | Surface code root, trailing slash — or delete the surface (section 5) | `web/`, `frontend/` |
| `{{service responsibilities}}` | What the service owns, one phrase | `domain logic, routes, and persistence` |
| `{{surface responsibilities}}` | What the surface owns, one phrase — omit if headless | `pages, components, and browser behavior` |
| `{{main flow}}` | One-line data flow | `source → store → service → surface` |
| `{{deploy target}}` | How it ships | `two Fargate services`, `one VPS` |

### Stack (must match [[adr-02-stack]])

| Token | Load | Example |
|---|---|---|
| `{{domain framework}}` | Service domain framework | `Django`, `Ktor` |
| `{{interface framework}}` | Service HTTP/API framework | `DRF`, `Ktor Routing` |
| `{{surface framework}}` | Surface host | `Astro`, `Next.js` |
| `{{component framework}}` | UI components | `Belt`, `Svelte`, `React` |
| `{{service toolchain}}` | Service package/run tool — no substitutes later | `uv`, `gradle` |
| `{{surface toolchain}}` | Surface package/run tool | `bun`, `pnpm` |
| `{{test runner}}` | Service test runner | `pytest`, `JUnit` |
| `{{local runtime}}` | Root orchestration filename | `compose.yaml` |
| `{{local runtime profiles}}` | Profiles of that runtime | `db / service / surface / full` |
| `{{local ports}}` | Local ports | `5432 / 8000 / 4321` |
| `{{cloud provider}}` | Cloud | `AWS`, `Fly.io` |
| `{{region}}` | Deploy region | `us-east-1` |
| `{{host}}` | Public host | `billing.acme.com` |
| `{{database}}` | Engine | `PostgreSQL 17` |
| `{{data layer}}` | How the service talks to data | `Django ORM + Psycopg` |
| `{{secret store}}` | Where secret **values** live | `AWS Secrets Manager` |
| `{{secret naming}}` | Name scheme, never values | `acme/<env>/<project>/*` |
| `{{secret exceptions}}` | Bounded exceptions, or `none` | `none` |
| `{{infrastructure absences}}` | What you deliberately do not run | `no NAT, no cache server` |
| `{{baseline sizing}}` | Size baseline | `1 task, 256/512` |
| `{{service integrations}}` | External integrations | `S3, SES` |
| `{{surface styling}}` | CSS/styling stack | `Tailwind 4` |
| `{{surface rendering mode}}` | Host rendering | `SSR, standalone adapter` |
| `{{hydration default}}` | Default hydration | `none — static unless declared` |
| `{{api prefix}}` | Catalog path prefixes | `/api/`, `/admin/` |
| `{{handler idiom}}` | Handler + path idiom | `APIView + path()` |
| `{{payload split pattern}}` | Read vs write payloads | `ReadSerializer vs WriteSerializer` |
| `{{permission pattern}}` | Permission classes | `GroupBasedPermission subclasses` |
| `{{authorization pattern}}` | Where authz lives | `service-side permission classes` |
| `{{identity provider}}` | Who authenticates | `Cognito`, `session login` |
| `{{domain framework rules}}` | Framework rules this repo programs by | `CheckConstraint(condition=)` |
| `{{pure-compute boundary}}` | Pure-compute rule | `no framework imports in services/` |
| `{{component reactivity idiom}}` | Component reactivity | `runes`, `signals` |
| `{{component composition idiom}}` | Component composition | `snippets + render` |
| `{{component extension}}` | File extension **without** `*.` — the glob is `**/*.{{component extension}}` | `svelte`, `tsx` |

### People, git, skills

| Token | Load | Example |
|---|---|---|
| `{{author name}}` / `{{author email}}` / `{{author role}}` | One author-of-record row; duplicate the row for more people | `Ada Lovelace` / `ada@acme.com` / `owner` |
| `{{ruleset id}}` | GitHub ruleset id for `scripts/apply_main_ruleset.py` | numeric id from the GitHub UI |
| `{{technology}}` | **Per skill folder**, the technology name that folder is renamed to — not a single global string | `django`, `pytest`, `astro` |

## 4 · One-shot slots — write the content, do not invent a global string

These mark **where** to write. Replace the slot with real prose, a table row, or delete the example row and add real ones.

### PRD (`docs/PRD.md`)

| Token | Load |
|---|---|
| `{{product paragraph}}` | Opening paragraph: what it is, what it reads, what it serves |
| `{{purpose paragraph}}` | What becomes shorter, safer, or possible; what it does not replace |
| `{{core capability 1}}` … `{{core capability 3}}` | Three capabilities (add more as numbered slots if needed) |
| `{{user role 1}}` … `{{user role 3}}` and `{{need 1}}` … `{{need 3}}` | Who it is for |
| `{{observable acceptance criterion 1}}` … `3` | Observable acceptance |
| `{{primary read story}}`, `{{precondition}}`, `{{user action}}`, `{{observable outcome}}` | Primary read scenario |
| `{{primary exception story}}`, `{{a condition that needs attention}}`, `{{the product evaluates it}}`, `{{the responsible user sees an actionable result}}` | Exception scenario |
| `{{primary action story}}`, `{{an authorized user identifies a required action}}`, `{{they perform it in the product}}`, `{{the action is validated, recorded, and attributable}}` | Action scenario |

### INTERFACES (`docs/INTERFACES.md`) — Cleric-owned

Replace the **example** row with the first real route (or leave the table header and add rows). Tokens on that example row:

| Token | Load |
|---|---|
| `{{http method}}` | Verb (`GET`, `POST`, …) — **not** the letters G-E-T as a magic word |
| `{{example path}}` | English path, trailing slash, under `{{api prefix}}` |
| `{{handler name}}` | Handler name per [[GLOSSARY]] |
| `{{payload shape}}` | Shape name, or `—` for fragments |
| `{{permission class}}` | Permission class that will exist |
| `{{route description}}` | What it serves; link `docs/contracts/` |

### GLOSSARY project table (`docs/GLOSSARY.md`)

Harness rows stay. The empty project table uses:

| Token | Load |
|---|---|
| `{{project terms}}` | Replace this paragraph with the project's domain nouns, or delete it once the table has real rows |
| `{{example term}}` | A real domain term (or delete the example row) |
| `{{canonical form}}` | Canonical spelling |
| `{{term applies to}}` | Scope of that term — **not** the VARIABLES column `{{scope}}` |
| `{{forbidden forms}}` | Forbidden synonyms |

### VARIABLES, REQUIREMENTS, REQ, ROADMAP, env

| Token | File | Load |
|---|---|---|
| `{{VARIABLE_NAME}}` | [[VARIABLES]] service table | Env var name |
| `{{PUBLIC_VARIABLE_NAME}}` | [[VARIABLES]] surface table | Public non-secret name |
| `{{scope}}` | [[VARIABLES]] only | `service`, `surface`, `harness`, … |
| `{{envs}}` | [[VARIABLES]] | `dev/prod/local` |
| `{{source}}` | [[VARIABLES]] | Where the value comes from |
| `{{description}}` | [[VARIABLES]] | What the variable is |
| `{{yes/no}}` | [[VARIABLES]] | Secret? `yes` or `no` |
| `{{package}}` | [[REQUIREMENTS]] | Package name |
| `{{pin version}}` | [[REQUIREMENTS]] | Pinned version — **not** the docs `version:` frontmatter |
| `{{pin date}}` | [[REQUIREMENTS]] | Date the pin was checked — **not** a changelog date |
| `{{why this pin}}` | [[REQUIREMENTS]] | Why this version |
| `{{REQ-DOMAIN-NN}}` | [[REQ]] | Optional tracking id |
| `{{requirement summary}}` / `{{open issues}}` / `{{closed issues}}` | [[REQ]] | Snapshot cells |
| `{{stage 1}}`, `{{stage 2}}`, `{{stage 3}}`, … | [[ROADMAP]] | Stage name + one-line exit; mark exactly one current |
| `{{dev secret seed}}` | `.env.example` | Local **non-production** seed for `SECRET_KEY` — never a real secret. Declare the name in [[VARIABLES]] first |

## 5 · Headless products

If there is no screen: delete in **one batch** The Elf, `skills/hb-sk-surface-framework/`, `skills/hb-sk-component-framework/`, `.cursor/rules/section-articles.mdc`, the whole [[adr-04-frontend]] family, and every roster row that names the surface ([[CLONE]] §7). Do not leave `{{surface tree}}` pointing at a missing tree. Surface stack tokens in [[adr-02-stack]] go away with that section.

## 6 · What `AGENTS.md` still is after fill

A filled `AGENTS.md` still says: read PRD then INTERFACES; Graphify first; English in git; dispatch `hb-ag-*` (then the new prefix); do not invent production state. You only substitute the slots. You do not turn that file into a second ONBOARDING.

## 7 · Inventory — token, files, expected load

Canonical paths only (ignore `.claude/skills` and `.agents/skills`; they are links). `AGENTS.md` and `CLAUDE.md` are the same document twice — edit both.

Shared tokens appear in many files so the product name cannot drift. **Load** is what to put in the slot.

| Token | Files | Expected load |
|---|---|---|
| `{{project name}}` | `AGENTS.md`, `CLAUDE.md`, `docs/PRD.md`, `docs/GLOSSARY.md`, `docs/CLAUDE-TEAM.md`, `.env.example` | Prose product name |
| `{{company name}}` | `docs/CLAUDE-TEAM.md` | Organization |
| `{{one-line product statement}}` | `AGENTS.md`, `CLAUDE.md` | One-line product |
| `{{main flow}}` | `AGENTS.md`, `CLAUDE.md` | One-line flow |
| `{{service responsibilities}}` | `AGENTS.md`, `CLAUDE.md` | Service owns … |
| `{{surface responsibilities}}` | `AGENTS.md`, `CLAUDE.md` | Surface owns … (or drop if headless) |
| `{{interface language}}` | `AGENTS.md`, `CLAUDE.md`, `docs/PRD.md`, `docs/HARNESS.md`, `docs/GLOSSARY.md`, `docs/ADND-AGENTS.md`, `docs/ADND-DISPATCH.md`, `adrs/adr-01-nomenclature.md`, `adrs/adr-01.b-localization.md`, `agents/hb-ag-contracts.md`, `agents/hb-ag-judge.md`, `agents/hb-ag-ops.md`, `agents/hb-ag-surface.md`, `agents/hb-ag-test.md`, `skills/hb-sk-abc/SKILL.md`, `skills/kskill-cowsay/SKILL.md`, `skills/kskill-mood/references/quick-win.md` | UI language |
| `{{interface locale}}` | `adrs/adr-01.b-localization.md` | Locale tag |
| `{{number format}}` | `adrs/adr-01.b-localization.md` | Screen numbers |
| `{{date format}}` | `adrs/adr-01.b-localization.md` | Screen dates |
| `{{timezone}}` | `adrs/adr-01.b-localization.md` | Timezone |
| `{{service tree}}` | `AGENTS.md`, `CLAUDE.md`, `docs/HARNESS.md`, `docs/GLOSSARY.md`, `docs/SERVICES.md`, `docs/ADND-AGENTS.md`, `docs/tdds/tdd-00-template.md`, `adrs/adr-07-git.md`, `agents/hb-ag-contracts.md`, `agents/hb-ag-git.md`, `agents/hb-ag-ops.md`, `agents/hb-ag-paladin.md`, `agents/hb-ag-service.md`, `agents/hb-ag-surface.md`, `agents/hb-ag-test.md`, `skills/hb-sk-abc/SKILL.md`, `skills/hb-sk-cloud/SKILL.md`, `skills/hb-sk-contracts/SKILL.md`, `skills/hb-sk-domain-framework/SKILL.md`, `skills/hb-sk-local-runtime/SKILL.md`, `skills/hb-sk-tdd/SKILL.md`, `skills/hb-sk-test-runner/SKILL.md` | Service root path |
| `{{surface tree}}` | `AGENTS.md`, `CLAUDE.md`, `docs/HARNESS.md`, `docs/GLOSSARY.md`, `docs/ADND-AGENTS.md`, `adrs/adr-07-git.md`, `agents/hb-ag-contracts.md`, `agents/hb-ag-git.md`, `agents/hb-ag-ops.md`, `agents/hb-ag-service.md`, `agents/hb-ag-surface.md`, `agents/hb-ag-test.md`, `skills/hb-sk-abc/SKILL.md`, `skills/hb-sk-cloud/SKILL.md`, `skills/hb-sk-contracts/SKILL.md`, `skills/hb-sk-local-runtime/SKILL.md` | Surface root path |
| `{{service toolchain}}` | `AGENTS.md`, `CLAUDE.md`, `docs/SERVICES.md`, `adrs/adr-02-stack.md`, `skills/hb-sk-domain-framework/SKILL.md` | Service toolchain |
| `{{surface toolchain}}` | `AGENTS.md`, `CLAUDE.md`, `adrs/adr-02-stack.md`, `skills/hb-sk-surface-framework/SKILL.md` | Surface toolchain |
| `{{local runtime}}` | `AGENTS.md`, `CLAUDE.md`, `docs/HARNESS.md`, `docs/INFRASTRUCTURE.md`, `adrs/adr-02-stack.md`, `skills/hb-sk-local-runtime/SKILL.md` | Orchestration file |
| `{{deploy target}}` | `AGENTS.md`, `CLAUDE.md`, `docs/HARNESS.md`, `docs/INFRASTRUCTURE.md`, `adrs/adr-02-stack.md`, `adrs/adr-07-git.md`, `skills/hb-sk-cloud/SKILL.md` | Deploy layout |
| `{{owner}}` | `docs/GITHUB.md`, `docs/GLOSSARY.md`, `docs/HARNESS.md`, `docs/CLAUDE-TEAM.md`, `docs/ADND-AGENTS.md`, `docs/ADND-DISPATCH.md`, `adrs/adr-08-github.md`, `scripts/apply_main_ruleset.py`, `skills/hb-sk-git/SKILL.md` | GitHub owner |
| `{{repo}}` | `docs/GITHUB.md`, `adrs/adr-08-github.md`, `scripts/apply_main_ruleset.py`, `skills/hb-sk-git/SKILL.md` | GitHub repo |
| `{{project slug}}` | `docs/GLOSSARY.md`, `docs/VARIABLES.md`, `.env.example` | Slug |
| `{{prefix}}` | every `skills/hb-sk-*/SKILL.md` Instantiation section | New kind prefix with dash |
| `{{technology}}` | stack-shaped `hb-sk-*` Instantiation sections (not abc/contracts/tdd/git/hunter/hawk/hound which keep their stem) | Folder rename target |
| `{{domain framework}}` | `docs/HARNESS.md`, `docs/SERVICES.md`, `adrs/adr-02-stack.md`, `skills/hb-sk-domain-framework/SKILL.md` | Domain framework |
| `{{interface framework}}` | `docs/HARNESS.md`, `docs/SERVICES.md`, `adrs/adr-02-stack.md`, `skills/hb-sk-interface-framework/SKILL.md` | Interface framework |
| `{{surface framework}}` | `docs/HARNESS.md`, `adrs/adr-02-stack.md`, `skills/hb-sk-surface-framework/SKILL.md` | Surface host |
| `{{component framework}}` | `docs/HARNESS.md`, `adrs/adr-02-stack.md`, `skills/hb-sk-component-framework/SKILL.md`, `skills/hb-sk-surface-framework/SKILL.md` | Components |
| `{{test runner}}` | `docs/HARNESS.md`, `adrs/adr-02-stack.md`, `skills/hb-sk-test-runner/SKILL.md` | Test runner |
| `{{cloud provider}}` | `docs/HARNESS.md`, `docs/INFRASTRUCTURE.md`, `adrs/adr-02-stack.md`, `skills/hb-sk-cloud/SKILL.md` | Cloud |
| `{{region}}` | `docs/INFRASTRUCTURE.md`, `adrs/adr-02-stack.md`, `agents/hb-ag-ops.md`, `skills/hb-sk-cloud/SKILL.md` | Region |
| `{{host}}` | `docs/INFRASTRUCTURE.md`, `skills/hb-sk-cloud/SKILL.md` | Public host |
| `{{database}}` | `docs/DB.md`, `adrs/adr-02-stack.md` | Database engine |
| `{{data layer}}` | `adrs/adr-02-stack.md` | Data access |
| `{{secret store}}` | `adrs/adr-02-stack.md` | Secret store |
| `{{secret naming}}` | `docs/INFRASTRUCTURE.md`, `skills/hb-sk-cloud/SKILL.md` | Secret name scheme |
| `{{secret exceptions}}` | `adrs/adr-02-stack.md` | Exceptions or `none` |
| `{{infrastructure absences}}` | `docs/INFRASTRUCTURE.md`, `adrs/adr-02-stack.md`, `skills/hb-sk-cloud/SKILL.md` | Deliberate absences |
| `{{baseline sizing}}` | `skills/hb-sk-cloud/SKILL.md` | Size baseline |
| `{{service integrations}}` | `adrs/adr-02-stack.md` | Integrations |
| `{{surface styling}}` | `adrs/adr-02-stack.md` | Styling |
| `{{surface rendering mode}}` | `skills/hb-sk-surface-framework/SKILL.md` | Rendering mode |
| `{{hydration default}}` | `skills/hb-sk-surface-framework/SKILL.md` | Hydration default |
| `{{local runtime profiles}}` | `skills/hb-sk-local-runtime/SKILL.md` | Profiles |
| `{{local ports}}` | `docs/INFRASTRUCTURE.md`, `skills/hb-sk-local-runtime/SKILL.md` | Ports |
| `{{api prefix}}` | `docs/INTERFACES.md`, `skills/hb-sk-contracts/SKILL.md` | Path prefixes |
| `{{handler idiom}}` | `skills/hb-sk-interface-framework/SKILL.md` | Handler idiom |
| `{{payload split pattern}}` | `skills/hb-sk-interface-framework/SKILL.md` | Payload split |
| `{{permission pattern}}` | `skills/hb-sk-interface-framework/SKILL.md` | Permission pattern |
| `{{authorization pattern}}` | `docs/AUTH.md`, `skills/hb-sk-domain-framework/SKILL.md` | Where authz lives |
| `{{identity provider}}` | `docs/AUTH.md` | Identity provider |
| `{{domain framework rules}}` | `skills/hb-sk-domain-framework/SKILL.md` | Framework rules |
| `{{pure-compute boundary}}` | `skills/hb-sk-domain-framework/SKILL.md` | Pure-compute rule |
| `{{component reactivity idiom}}` | `skills/hb-sk-component-framework/SKILL.md` | Reactivity |
| `{{component composition idiom}}` | `skills/hb-sk-component-framework/SKILL.md` | Composition |
| `{{component extension}}` | `.cursor/rules/section-articles.mdc` | Extension for the glob |
| `{{product kind}}` | `docs/PRD.md` | Product kind |
| `{{product paragraph}}` | `docs/PRD.md` | Opening paragraph |
| `{{purpose paragraph}}` | `docs/PRD.md` | Purpose paragraph |
| `{{core capability 1}}` `2` `3` | `docs/PRD.md` | Capabilities |
| `{{user role 1}}` `2` `3` | `docs/PRD.md` | User roles |
| `{{need 1}}` `2` `3` | `docs/PRD.md` | Needs |
| `{{observable acceptance criterion 1}}` `2` `3` | `docs/PRD.md` | Acceptance |
| `{{primary read story}}` and its Given/When/Then slots | `docs/PRD.md` | Read scenario |
| `{{primary exception story}}` and its Given/When/Then slots | `docs/PRD.md` | Exception scenario |
| `{{primary action story}}` and its Given/When/Then slots | `docs/PRD.md` | Action scenario |
| `{{http method}}` | `docs/INTERFACES.md` | HTTP verb on the example row |
| `{{example path}}` | `docs/INTERFACES.md` | Example path |
| `{{handler name}}` | `docs/INTERFACES.md` | Handler |
| `{{payload shape}}` | `docs/INTERFACES.md` | Payload or `—` |
| `{{permission class}}` | `docs/INTERFACES.md` | Auth column |
| `{{route description}}` | `docs/INTERFACES.md` | Description column |
| `{{project terms}}` | `docs/GLOSSARY.md` | Project glossary intro |
| `{{example term}}` / `{{canonical form}}` / `{{term applies to}}` / `{{forbidden forms}}` | `docs/GLOSSARY.md` | First project term row |
| `{{author name}}` / `{{author email}}` / `{{author role}}` | `docs/CLAUDE-TEAM.md` | Author row |
| `{{stage 1}}` `2` `3` | `docs/ROADMAP.md` | Stages |
| `{{package}}` / `{{pin version}}` / `{{pin date}}` / `{{why this pin}}` | `docs/REQUIREMENTS.md` | Stack pin rows |
| `{{VARIABLE_NAME}}` / `{{PUBLIC_VARIABLE_NAME}}` / `{{scope}}` / `{{envs}}` / `{{source}}` / `{{description}}` / `{{yes/no}}` | `docs/VARIABLES.md` | Variable rows |
| `{{REQ-DOMAIN-NN}}` / `{{requirement summary}}` / `{{open issues}}` / `{{closed issues}}` | `docs/REQ.md` | Optional REQ snapshot |
| `{{ruleset id}}` | `scripts/apply_main_ruleset.py` | GitHub ruleset id |
| `{{dev secret seed}}` | `.env.example` | Local secret seed (fake) |
| `{{html fragment technology}}` | `adrs/adr-03.c-htmx.md` | HTMX, Hotwire, … — or **delete that sub** |
| `{{boot sequence}}` | `adrs/adr-03.d-development.md` | Local service start chain |
| `{{cache policy}}` | `adrs/adr-03.e-cache.md` | What cache exists / is refused |
| `{{layout convention}}` | `adrs/adr-04.a-architecture.md` | Base/print (or this host's) layouts |
| `{{interactivity ladder}}` | `adrs/adr-04.a-architecture.md` | Rungs: static / fragments / islands |
| `{{token stylesheet}}` | `adrs/adr-04.b-design-system.md`, `adrs/adr-04.g-responsive.md` | Token CSS/path |
| `{{theme persistence}}` | `adrs/adr-04.c-theming.md` | How theme is stored — or **delete that sub** |
| `{{component catalog}}` | `adrs/adr-04.d-components.md` | Where existing components are listed |
| `{{client fetch rule}}` | `adrs/adr-04.f-client-api.md` | SSR internal URL vs public host |

The [[adr-03-backend]] parent and [[adr-04-frontend]] parent stay. Subs are invitations: rewrite them to the chosen stack or delete them in the same batch. Do not treat HTMX, Redis-or-not, or a three-rung ladder as locked — they are examples in those files.

`{{prefix}}` is a string replace **and** a directory rename (`skills/hb-sk-contracts` → `skills/abc-sk-contracts`). Same batch as [[CLONE]] §3.

## Done when

- Graphify is installed or you recorded why it could not be (`ensure` failed).
- Shared ledger values are consistent across `AGENTS.md` / `CLAUDE.md` and the docs.
- [[adr-02-stack]] names a real stack; [[adr-03-backend]] / [[adr-04-frontend]] are filled or their unused subs deleted.
- The leftover `grep` in section 2 shows no live product slots.
- `python3 -m pytest tests/ -q` is green.
- [[CLONE]] steps 3–8 are done (prefix, trees, skills, remote).

Then stop treating this file as a queue. `AGENTS.md` is the session entry. Keep this file as the map of what was bound.
