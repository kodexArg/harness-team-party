---
name: hb-sk-contracts
title: INTERFACES.md six-column catalog — knowledge contract
type: skill
status: active
version: v0.1.0
tags: [skill, contracts, cleric]
description: >
  Interface catalog contract for docs/INTERFACES.md: six-column row,
  docs/contracts/, trailing slash, declared path prefixes, fragment
  Payload: —. Load when adding, changing, or retiring an interface
  or fragment row — even if the skill is not named. Owner: The
  Cleric (hb-ag-contracts) only. The Cleric also mediates surface↔service;
  this skill stays the catalog-writing contract. The Dwarf and The
  Elf read INTERFACES.md; they do not load this skill and they do
  not write the catalog.
applies_when:
  - When declaring, changing, or removing an interface or fragment row in INTERFACES.md
  - When linking a payload shape into docs/contracts/
related_adrs:
  - adr-01-nomenclature
---

# hb-sk-contracts

Knowledge contract for **The Cleric**. Teach the catalog row, then stop. The Cleric also mediates surface↔service — the row is the prayer; Dwarf and Elf walk their own trees. Not a lookup of one existing path for implementers — that remains reading [[INTERFACES]]. This skill is how the row is *written*.

## Load

1. Read [[INTERFACES]] and its governing ADRs.
2. First act of the owner agent is also [[PRD]].
3. Payload shapes live in `docs/contracts/`, linked from Description — not inlined in the table.

## The row

`Method` · `Path` (English, trailing slash) · `Handler` (named per [[GLOSSARY]]) · `Payload` (or `—`) · `Auth` (the permission class that **will** exist) · `Description`.

| Rule | Shape |
|---|---|
| Prefixes | `{{api prefix}}` (and the other prefixes [[INTERFACES]] declares for this project) |
| Fragments | same six columns; `Payload: —`; Description names the markup swap |
| Order | row first, then TDD / code. Retire the row before deleting the code |
| Atomic | the catalog hunk is its own reviewable act |

An undeclared route in code is a defect. Do not invent routing doctrine — this project programs its interfaces the way [[adr-02-stack]] and [[SERVICES]] record.

## Do not

- Write `{{service tree}}` or `{{surface tree}}` or `docs/tdds/`. After the row lands, return it — the Cleric may Agent Dwarf/Elf/Trickster; this skill does not.
- Carry the surface / component / interface-framework / domain-framework / local-runtime / cloud / abc skills.

## Instantiation

This is a template skill: replace every `{{placeholder}}`, then rename the
folder to `{{prefix}}-sk-contracts`. See [[ONBOARDING]] and [[CLONE]].
