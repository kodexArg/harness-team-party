---
title: adr-00.b-adr-crud
type: adr
status: active
version: v0.1.0
tags: [crud, lifecycle]
description: "Defines the creation criteria, WHAT and WHY scope, harness wiring, update lifecycle, and CRUD operations for ADRs."
applies_when:
  - When creating, updating, or deleting an ADR under operator instruction.
  - When distinguishing architectural invariants from procedural execution details.
---

# ADR-00.b — ADR CRUD and lifecycle

> Clear governance over when to introduce, modify, or retire rules prevents architectural drift while keeping the rulebook lean, relevant, and authoritative.

1. **Creation criteria (Create):**
   - **User authorization:** ADR creation strictly requires explicit human instruction. Agents never initiate new ADRs independently. *Objective: prevents autonomous rule sprawl, phantom constraints, and ungrounded architectural drift.*
   - **Scope (WHAT and WHY, never HOW):**
     - **WHAT:** The leading spirit of numbered rules, asserting settled structural invariants, boundaries, and contracts.
     - **WHY:** Expressed exclusively in the opening blockquote (`> ...`) as pure prose without hyperlinks.
     - **Never HOW:** Procedural execution belongs to skills, transient configs belong in `docs/`, and craft choices belong to the developer. *Objective: guarantees rules remain lightweight, enduring invariants without dictating transient implementation mechanics.*
   - **Storage and harness wiring:** ADRs reside in `adrs/` and are symlinked directly into the agent harness (`.claude/rules/`). *Objective: ensures zero-friction visibility to agents on every prompt while keeping source files in a clean dedicated repository tree.*
   - **Identifier convention:** Sequential numbering `adr-NN-slug.md` (and `adr-NN.x-slug.md` for sub-ADRs). *Objective: provides unambiguous, chronological, human-readable citations across all discussions and commits.*

2. **Consumption and triage (Read):**
   - Filter ADRs via frontmatter `description` and `applies_when` triggers before loading full document bodies.
   - Evaluate relevant rules during planning and verification loops.
   - *Objective: maximizes agent attention efficiency and conserves context tokens by preventing unneeded rule loading.*

3. **Active evolution (Update & boy-scout versioning):**
   - Update existing ADRs directly in place when architectural reality changes.
   - **Boy-scout rule:** Only the ADRs actively modified or specifically reviewed in a batch have their `version` field updated to the current release version in [[CHANGELOG]]. Untouched ADRs are never blindly restamped.
   - Retain positive phrasing, concise assertions, and frontmatter accuracy.
   - *Objective: ensures the rulebook reflects active system truth without artificial diff churn across untouched rules, preserving individual rule revision provenance.*

4. **Retirement (Delete):**
   - Completely delete ADRs that no longer apply to the system, leaving git history to preserve past records; retired numbers remain unassigned.
   - *Objective: keeps the active rulebook lean, zero-noise, and free from zombie or conflicting rules, while avoiding citation collisions.*

5. **Sub-ADR hierarchy:**
   - Complex domains decompose into cohesive sub-ADRs (`adr-NN.a-*`, `adr-NN.b-*`, etc.) carrying especially reduced frontmatter.
   - Parent ADRs register their sub-ADRs in the `sub_adrs:` frontmatter list.
   - Sub-ADRs are always referenced by their parent ADR; for all practical purposes, a parent ADR and its sub-ADRs constitute the same single ADR.
   - All external documents, code, and peer ADRs reference solely the parent ADR.
   - *Objective: isolates distinct facets of large domains into focused, compact files without fragmenting external architectural citations.*
