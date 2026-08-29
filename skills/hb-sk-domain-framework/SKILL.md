---
name: hb-sk-domain-framework
title: Domain framework this-repo contract — knowledge contract
type: skill
status: active
version: v0.1.4
tags: [skill, domain-framework, dwarf]
description: >
  The domain framework contract as this repo programs it: models,
  settings, framework adapters, the pure-Python boundary, and the
  service toolchain. Load for framework-bound service work — even if
  unnamed. Owner: The Dwarf (hb-ag-service). Pure Python business
  logic and complex scripts: The Paladin. TDD and tests: The
  Trickster. Not the catalog.
applies_when:
  - When authoring a {{domain framework}} model, constraint, setting, adapter, or persistence service
  - When deciding whether compute belongs to The Dwarf or The Paladin
related_adrs:
  - adr-02-stack
---

# hb-sk-domain-framework

Knowledge contract for **The Dwarf**. Teach this project's {{domain framework}}, then stop.

## Load

1. Read the stack SSOT for this layer ([[SERVICES]]) and the pins in [[REQUIREMENTS]].
2. Classify the boundary. Framework-neutral Python business rules and complex script cores → The Paladin (`hb-ag-paladin`). Framework-bound work continues here.
3. Loop: the Cleric's [[INTERFACES]] row (read) → wait for the Trickster's failing TDD (`hb-ag-test`, `hb-sk-tdd`) → models → handlers (`hb-sk-interface-framework`). Missing row → The Cleric. Do not write `docs/tdds/` or tests.
4. Toolchain: **{{service toolchain}}**, never a substitute. Pins live in [[REQUIREMENTS]].

## This project

At instantiation this section records the framework-specific rules this repo
programs by — the constraint spellings, the settings surfaces, the
framework adapter around Paladin-owned pure computation, and the authorization
pattern. Until then it holds placeholders:

- Framework rules: `{{domain framework rules}}`
- Pure-compute boundary: `{{pure-compute boundary}}` — framework-neutral rules belong to The Paladin
- Authorization pattern: `{{authorization pattern}}`

## Do not

- Write `docs/tdds/` or tests — The Trickster (`hb-ag-test`, `hb-sk-tdd`).
- Absorb framework-neutral Python business rules or complex script cores — The Paladin owns that cut.
- Write the local runtime (The Wizard) or `docs/INTERFACES.md` (The Cleric).
- Substitute the toolchain, add an unsanctioned dependency, or invent routing doctrine.
- Load Elf / Cleric / Trickster / Wizard / Inquisitor skills.

## Instantiation

This is a template skill: replace every `{{placeholder}}`, then rename the
folder to `{{prefix}}-sk-{{technology}}` (e.g. the domain framework's name).
See [[ONBOARDING]] and [[CLONE]].
