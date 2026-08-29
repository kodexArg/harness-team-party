---
name: hb-sk-cloud
title: Cloud deployment layout — knowledge contract
type: skill
status: active
version: v0.1.0
tags: [skill, cloud, wizard]
description: >
  Cloud contract for this repo's deployment layout, secret-store
  naming, and deliberate absences. Load when changing services, task
  or pod definitions, load-balancer rules, or secret names — even if
  the skill is not named. Owner: The Wizard (hb-ag-ops). Not the local
  runtime. Not app code. Not INTERFACES.md.
applies_when:
  - When changing {{cloud provider}} services, compute definitions, load balancing, or secret names
  - When proposing infrastructure the layout deliberately does not have
related_adrs:
  - adr-02-stack
---

# hb-sk-cloud

🧙 Knowledge contract for **The Wizard**. This project's cloud layout. Then stop.

## Load

1. Read [[INFRASTRUCTURE]] (doctrine) and [[VARIABLES]] (names).
2. Live resource rows live in the infrastructure inventory the project keeps — read them before proposing a change.

## This project

The deployment layout is recorded here at instantiation:

- Layout: `{{deploy target}}` in `{{region}}`, host `{{host}}`
- Secret naming: `{{secret naming}}`
- Baseline sizing: `{{baseline sizing}}`
- Deliberate absences: `{{infrastructure absences}}` — do not "fix" them.

Cloud agent sessions never receive cloud credentials. On the owner's host, measure IAM before claiming a write is out of reach. Read secret metadata; never read secret values. Never invent a secret value to turn a check green.

## Quick exit

A page, a model, or a catalog row — not this spell. Name The Elf / The Dwarf / The Cleric.

## Do not

- Edit the local runtime through this skill — that is `hb-sk-local-runtime`.
- Write `{{service tree}}` / `{{surface tree}}` / `docs/INTERFACES.md`.
- Load Elf / Dwarf / Cleric / Inquisitor skills.

## Instantiation

This is a template skill: replace every `{{placeholder}}`, then rename the
folder to `{{prefix}}-sk-{{technology}}` (e.g. the cloud platform's name).
See [[ONBOARDING]] and [[CLONE]].
