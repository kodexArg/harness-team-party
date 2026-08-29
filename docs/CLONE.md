---
title: Instantiation guide — a new project from harness-team-party
type: reference
status: active
version: v0.1.2
tags: [harness, clone, instantiation, template]
description: "Operator steps to instantiate harness-team-party: copy, fill via ONBOARDING, prefix rename, stack decision, trees, first commit."
applies_when:
  - When creating a new project from the harness-team-party template.
  - When auditing whether an instantiation left placeholders behind.
related_adrs:
  - adr-02-stack
  - adr-05-after-versioning
  - adr-03-backend
  - adr-04-frontend
---
# CLONE — instantiating harness-team-party

harness-team-party is the stack-agnostic project harness template, successor of
`harness-base` / `harness-default`, born from the evolution of `alvs-financial-gateway` (a
Django/Astro/AWS treasury product) into a reusable, product-free harness. Where
that lineage shows through as an example — a Kotlin service, a flat site — it
is illustration, never prescription.

Operator steps for a new project from this template. Order matters where
noted.

## 1. Copy the template

Copy the tree, not the git history:

```bash
cp -r /path/to/harness-team-party /path/to/my-project
cd /path/to/my-project
git init
```

## 2. Fill every placeholder

An incoming agent (or operator) fills every live double-curly slot from the
map in [[ONBOARDING]] — token, files, and expected load. `AGENTS.md` is the
runtime index: substitute its slots; do not rewrite the harness procedure
around them. Install Graphify if the host can ([[ONBOARDING]] §0, [[GRAPHIFY]]).

```bash
grep -rn "{{" --exclude-dir=.git --exclude-dir=skills/kskill-report \
  --exclude-dir=skills/diagram-design --exclude=docs/ONBOARDING.md \
  --exclude=docs/CLONE.md .
```

## 3. Batch-rename the `hb-` prefix

`hb-` is the template's own product prefix. Pick the project's prefix (short,
lowercase, ending in a dash) and rename every `hb-sk-*` and `hb-ag-*` artifact
and every reference to them — skills, agents, docs, tests, and the roster
tables move in the same batch ([[HARNESS]]: a rename of an artifact moves every
reference in the same batch):

```bash
grep -rl "hb-sk-\|hb-ag-" --exclude-dir=.git . | xargs sed -i 's/hb-sk-/abc-sk-/g; s/hb-ag-/abc-ag-/g'
```

Then rename the directories: `git mv skills/hb-sk-contracts skills/abc-sk-contracts`,
`git mv agents/hb-ag-service.md agents/abc-ag-service.md`, and so on. Run
`python3 -m pytest tests/ -q` (or `python3 tests/test_<x>.py` per file) — the
roster guard (`tests/test_hb_ag_roster.py`, renamed alongside) asserts the new
stems.

## 4. Make the stack decision

Fill `adrs/adr-02-stack.md` — it ships as the placeholder shape of the
decision, not the decision. Fill the [[adr-03-backend]] and [[adr-04-frontend]]
families the same way: keep the parent, rewrite slots, **delete subs this
project does not use**. Choose the service stack, the surface stack (or
delete that section and the adr-04 family), infrastructure, and the
development variant. Record the pins in [[REQUIREMENTS]].

## 5. Create the stack trees

Create `{{service tree}}` and (unless headless) `{{surface tree}}`. Then:

- Wire the trees into `scripts/ci_select.py` (`SERVICE_PREFIXES` /
  `SURFACE_PREFIXES`) and `scripts/guardian_watchlists.py` (route-surface
  globs for `kbot-api`).
- Fill [[SERVICES]], [[INFRASTRUCTURE]], [[DB]], [[AUTH]], [[VARIABLES]],
  [[REQUIREMENTS]], [[ROADMAP]] — they ship as placeholders that say what they
  must contain.
- Write the first real row of [[INTERFACES]] before the first route.

## 6. Instantiate the stack-skill templates

Each `hb-sk-*` template (after the prefix rename, `abc-sk-*`) holds the
contract shape with `{{placeholders}}` for the chosen technology. Fill each
one, then rename the folder to name the technology: `abc-sk-domain-framework`
→ `abc-sk-django`, `abc-sk-test-runner` → `abc-sk-pytest`, and so on. Update
the skill names in each agent definition's body and in [[HARNESS]]'s required
skills table in the same batch.

## 7. Delete the surface agent if headless

A headless project deletes, in one batch: `agents/hb-ag-surface.md`,
`skills/hb-sk-surface-framework/`, `skills/hb-sk-component-framework/`,
`.cursor/rules/section-articles.mdc`, the [[adr-04-frontend]] family (parent
and every `adr-04.*` sub), and every roster/dispatch row that names The Elf
([[ADND-AGENTS]], [[ADND-DISPATCH]], [[HARNESS]], `AGENTS.md`,
`tests/test_hb_ag_roster.py`). The Cleric then mediates between the caller and
The Dwarf directly.

## 8. First commit and remote

```bash
git add -A
git commit -m "chore(harness): instantiate harness-team-party as {{project name}}"
gh repo create {{owner}}/{{repo}} --private --source . --push
```

Then apply the branch ruleset (`scripts/apply_main_ruleset.py`, after filling
its `{{owner}}`/`{{repo}}` and ruleset id), fill [[PRD]] and [[CLAUDE-TEAM]],
and open the first issue. The development loop ([[DEVELOPMENT-LOOP]]) takes
over from there.

## Done when

The leftover scan in step 2 shows no live product slots, no `hb-` prefix
remains, [[adr-02-stack]] names a real stack, the trees exist, Graphify is
installed or the gap is recorded, and `python3 -m pytest tests/ -q` is green.
The token inventory lives in [[ONBOARDING]]; this file keeps operator steps.
