---
name: hb-sk-abc
title: ABC gate — PR vs PRD, ADRs, INTERFACES
type: skill
status: active
version: v0.1.0
tags: [skill, abc]
description: >
  ABC checklist: a change vs PRD, the ADRs, and INTERFACES.md. Load when
  judging a pull request, a plan, or a diff against those three
  gates — even if the skill is not named. Parent fallback only —
  The Inquisitor (hb-ag-judge) does not load this skill. Does not
  author the change. Review labels do not block merge. Screen in the
  interface language; undeclared route is a defect.
applies_when:
  - When judging a PR, plan, or diff against PRD, ADRs, or INTERFACES.md
  - When a review label is being read as a merge gate
related_adrs:
  - adr-00-adr-doctrine
---

# hb-sk-abc

Knowledge contract for the **parent** ABC fallback. The Inquisitor does not load this skill. Interrogate the change against the three gates. Do not write the product.

## Checklist

Copy and answer. Name the rule that failed; do not patch the tree.

```
ABC
- [ ] PRD — serves the product objective ([[PRD]]), or it does not belong
- [ ] ADRs — the numbered assertions that apply; no silent route-around
- [ ] INTERFACES — every service call is a row; undeclared route = defect
```

Also hold, because they fail reviews that would otherwise look green:

- Screen strings render in `{{interface language}}`; code and docs stay English ([[adr-01.b-localization]]).
- Toolchains are the ones [[adr-02-stack]] sanctions for this project — no substitutes.
- `prd-fail` / `adr-fail` / `api-fail` **report**. They do not block an owner merge. A `Guardian-Verdict:` line is not a review label.

## Do not

- Author `{{service tree}}`, `{{surface tree}}`, `docs/INTERFACES.md`, the local runtime, or cloud infrastructure.
- Invent a thirteenth verdict label.
- Load Cleric / Dwarf / Elf / Wizard / Trickster / Bard skills — those agents own the work; this skill owns the interrogation.

## Instantiation

This is a template skill: replace every `{{placeholder}}`, then rename the
folder to `{{prefix}}-sk-abc`. See [[ONBOARDING]] and [[CLONE]].
