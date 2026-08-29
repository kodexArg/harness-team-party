---
name: hb-sk-interface-framework
title: Interface framework handler contract — knowledge contract
type: skill
status: active
version: v0.1.0
tags: [skill, interface-framework, dwarf]
description: >
  The interface framework contract as this repo programs it: explicit
  handlers plus declared paths, split read/write payload shapes, and the
  permission-class pattern. Load when writing or changing a handler,
  payload shape, permission class, or route declaration under the
  service tree — even if unnamed. Owner: The Dwarf (hb-ag-service).
  No catalog writes. No tests (The Trickster, hb-sk-tdd).
applies_when:
  - When authoring a {{interface framework}} handler, payload shape, permission class, or path declaration
  - When choosing a read payload shape vs a write payload shape
related_adrs:
  - adr-02-stack
---

# hb-sk-interface-framework

Knowledge contract for **The Dwarf**. Teach this project's {{interface framework}}, then stop.

## Load

1. Read the stack SSOT for this layer ([[SERVICES]]).
2. Confirm the path is a row in [[INTERFACES]] (read). Missing row → dispatch The Cleric (`hb-ag-contracts`); do not edit the catalog.
3. Wait for the Trickster's failing TDD (`hb-ag-test`, `hb-sk-tdd`) before forging the handler. Do not write tests.
4. Pins live in [[REQUIREMENTS]].

## This project

Explicit handlers and declared paths — no magic routing. Split read and
write payload shapes where the IO differs. Authorization is the project's
permission-class pattern, never an ad-hoc check; open access only where
[[INTERFACES]] names it. Instantiation records the concrete spellings:

- Handler + path idiom: `{{handler idiom}}`
- Read/write payload split: `{{payload split pattern}}`
- Permission-class pattern: `{{permission pattern}}`

## Do not

- Add routing conveniences the project has not sanctioned.
- Put business logic in the payload layer — that is the domain services' home (`hb-sk-domain-framework`).
- Write `docs/INTERFACES.md`, `docs/contracts/`, `docs/tdds/`, or tests.
- Load Elf / Cleric / Trickster / Wizard / Inquisitor skills.

## Instantiation

This is a template skill: replace every `{{placeholder}}`, then rename the
folder to `{{prefix}}-sk-{{technology}}` (e.g. the interface framework's
name). See [[ONBOARDING]] and [[CLONE]].
