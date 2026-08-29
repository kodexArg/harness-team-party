---
title: adr-00-adr-doctrine
type: adr
status: active
version: v0.1.0
tags: [adr, doctrine, harness, rules]
description: "Establishes the core ADR doctrine, deterministic rule authority, positive definitions, and sub-ADR decomposition."
applies_when:
  - When entering the repository without prior architectural context.
  - When evaluating the deterministic authority of ADR rules over implementation code.
  - When checking which foundational documentation files must exist in the root.
sub_adrs:
  - adr-00.a-adr-frontmatter
  - adr-00.b-adr-crud
  - adr-00.c-adr-template
related_agents:
  - hb-ag-judge
---

# ADR-00 — the ADR doctrine

> Architecture Decision Records define the settled structural invariants of the project. They express what the system is as deterministic assertions, guiding implementation.

1. **Rule authority.** ADRs carry binding rule-level authority across the entire codebase, asserting architectural boundaries across every operation.

2. **Deterministic nature.** ADRs establish the deterministic structural invariants of this repository, fixing settled system realities rather than fluid preferences.

3. **Positive definition over prohibition.** ADRs define valid states, target architectures, and standard paths by the positive, avoiding restrictive phrasing whenever affirmative guidance suffices.

4. **Concise assertions.** ADRs maintain concise, high-signal phrasing for instant comprehension, keeping rules lightweight, direct, and generic.

5. **Sub-ADR decomposition.** Complex domains decompose into cohesive sub-ADRs (`adr-NN.x-*`). Sub-ADRs are always referenced by their parent ADR; for all practical purposes, a parent ADR and its sub-ADRs constitute the same single ADR.

6. **Fast interpretation.** Triage an ADR in seconds: inspect `description` and `applies_when` for trigger alignment, read the opening quote for intent and context, and apply the numbered assertions directly.

7. **Immediate knowledge over information repository.** ADRs contain only immediate, high-signal architectural rules, not extensive technical documentation. Detailed specifications, data models, and schemas reside in `docs/` and connect via wikilinks.

8. **Expected codebase structure.** This harness expects:
   - `adrs/` containing the architecture decision records.
   - `PRD.md` (or `docs/PRD.md` / `constitution/PRD.md`) defining the project's specific objective and core scope.
   - Indispensable first-class documentation files that must always exist: `INTERFACES.md`, `CODEMAP.md`, `INFRASTRUCTURE.md`, `GITHUB.md`, `GLOSSARY.md`, and `HARNESS.md`.
