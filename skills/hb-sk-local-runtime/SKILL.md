---
name: hb-sk-local-runtime
title: Local runtime orchestration contract — knowledge contract
type: skill
status: active
version: v0.1.0
tags: [skill, local-runtime, wizard]
description: >
  Local runtime contract for this repo's orchestration file: profiles,
  bind-mounts, and port mappings. Load when editing the local
  orchestration file, its profiles, or its bind-mount/port mappings —
  even if the skill is not named. Owner: The Wizard (hb-ag-ops).
  Not the cloud. Not app code. Not INTERFACES.md.
applies_when:
  - When editing {{local runtime}}, its profiles, or its local bind-mounts
  - When a change looks like production but is only the local stack
related_adrs:
  - adr-02-stack
---

# hb-sk-local-runtime

🧙 Knowledge contract for **The Wizard**. This project's {{local runtime}}. Then stop.

## Load

1. Read the local-runtime SSOT section of [[INFRASTRUCTURE]].
2. Doctrine: [[adr-02-stack]] development variant. The file on disk is the project's orchestration file, named at instantiation.

## This project

One orchestration file at repo root. Profiles, ports, and bind-mounts are
recorded here at instantiation:

- Profiles: `{{local runtime profiles}}`
- Ports: `{{local ports}}`
- Bind-mounts: source trees mounted into their containers; dependency volumes stay anonymous.

Bring-up script: named at instantiation under `scripts/`.

## Quick exit

A page, a model, or a catalog row — not this spell. Name The Elf / The Dwarf / The Cleric.

## Do not

- Run the local runtime as production. Production is `hb-sk-cloud`.
- Add unsanctioned services, a per-app orchestration file, or write `{{service tree}}` / `{{surface tree}}` / `docs/INTERFACES.md`.
- Load Elf / Dwarf / Cleric / Inquisitor skills.

## Instantiation

This is a template skill: replace every `{{placeholder}}`, then rename the
folder to `{{prefix}}-sk-{{technology}}` (e.g. the local runtime's name).
See [[ONBOARDING]] and [[CLONE]].
