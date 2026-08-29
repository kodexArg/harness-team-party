---
title: adr-01.a-glossary
type: adr
status: active
version: v0.1.0
tags: [glossary, naming]
description: "Defines GLOSSARY as the canonical naming SSOT and governs term registration and single-row triage."
applies_when:
  - When introducing a new domain noun, entity, or component name.
  - When querying canonical terms or forbidden synonyms via single-row lookup.
  - When updating GLOSSARY.md rows during term creation or retirement.
---

# ADR-01.a — glossary naming authority

> Centralizing canonical nomenclature in a single authoritative document eliminates semantic drift, prevents synonym sprawl, and ensures absolute clarity across the repository.

1. **SSOT location and purpose.** [[GLOSSARY|`docs/GLOSSARY.md`]] is the repository's single source of truth for canonical terms and forbidden forms. It locks definitions and bounds usage before identifiers enter code.

2. **Pre-registration requirement.** Any new term, entity, model, payload field, endpoint segment, UI component, variable token, or domain concept must be registered in [[GLOSSARY]] before its first use in code or documentation.

3. **Fast single-row lookup.** Query [[GLOSSARY]] via targeted single-row lookups (e.g. `grep`). Loading the entire glossary file into context to inspect a single identifier is prohibited.

4. **Interaction and maintenance.** Edit [[GLOSSARY]] directly in the same commit whenever an identifier is created, modified, or retired. Every entry defines its canonical form, exact scope, and explicit forbidden alternatives.
