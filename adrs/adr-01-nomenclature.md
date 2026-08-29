---
title: adr-01-nomenclature
type: adr
status: active
version: v0.1.0
tags: [adr, nomenclature, glossary, localization]
description: "Establishes nomenclature authority, canonical naming in GLOSSARY, and codebase vs screen language boundaries."
applies_when:
  - When establishing naming conventions across the codebase.
  - When determining technical English versus rendered interface-language boundaries.
  - When preventing redundant fields or semantic duplication in data models.
sub_adrs:
  - adr-01.a-glossary
  - adr-01.b-localization
related_agents:
  - hb-ag-contracts
---

# ADR-01 — nomenclature

> Active nomenclature coherence and strict linguistic boundaries eliminate ambiguity, duplicate model state, and vocabulary drift across code, documentation, and user interfaces.

1. **Active nomenclature coherence.** Naming across all layers—models, database schemas, payload fields, interface paths, UI components, configuration tokens, and documentation—must maintain active, unbroken semantic consistency. Inventing ad-hoc synonyms or diverging terms across technical boundaries is prohibited.

2. **Model and entity hygiene.** Models, payload shapes, and data structures must never introduce redundant, duplicate, or nonsensical fields that mirror or overlap existing attributes, relationships, or derived values. Every field carries a single, distinct domain concept named strictly after its canonical definition.

3. **Universal English codebase.** English is the mandatory language for the entire technical repository: source code, identifiers, variable names, database tables and columns, interface paths, JSON payload keys, configurations, test suites, comments, commit messages, and technical documentation.

4. **Rendered screen exception.** The sole exception to English is human-facing UI output, where the screen renders natively in `{{interface language}}` as governed by [[adr-01.b-localization]]. All backing message IDs, catalog keys, and data variables remain strictly English.

5. **Sub-ADR decomposition:**
   - [[adr-01.a-glossary]]: Location of `docs/GLOSSARY.md`, lookup protocols, term pre-registration, and continuous maintenance.
   - [[adr-01.b-localization]]: Interface-language rendering and regional formatting standards.
