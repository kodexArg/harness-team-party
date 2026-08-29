---
name: hb-sk-component-framework
title: Component framework in the surface host — knowledge contract
type: skill
status: active
version: v0.1.1
tags: [skill, component-framework, elf]
description: >
  The component framework contract for the component files this
  project's surface host renders or hydrates. Load when authoring or
  editing a component, choosing reactive state primitives, or
  hydrating an interactive component — even if the skill is not named.
  Owner: The Elf (hb-ag-surface). The Elf does not write tests.
  Interface gaps go to The Cleric as content-needed. Not the catalog
  (hb-sk-contracts).
applies_when:
  - When authoring a {{component framework}} component the surface host will render or hydrate
  - When choosing among the framework's reactivity or composition primitives
related_adrs:
  - adr-02-stack
---

# hb-sk-component-framework

Knowledge contract for **The Elf**. Teach {{component framework}} in this host, then stop.

## Load

1. Read the surface stack SSOT and the pins in [[REQUIREMENTS]].
2. Doctrine of this repo stays in the surface architecture doc and the ADRs — an extract is not an ADR.
3. If a pin moves, re-fetch the extract that backs this skill.

## This host

Routing, data fetch, and the document shell belong to the surface host
(`hb-sk-surface-framework`) — components do not own them. The reactivity
idioms, composition idiom, and event idiom of `{{component framework}}` as
this repo programs them are recorded here at instantiation:

- Reactivity idiom: `{{component reactivity idiom}}`
- Composition idiom: `{{component composition idiom}}`
- Hydration is the host's decision; a component with no hydration directive renders as static markup.

When [[adr-02-stack]] names Belt, that is the component and style hand: tokens, rhythm, reusable chrome. Follow the pins. Do not paste vendor manuals into this skill. Visual decisions are tokens ([[adr-04.b-design-system]]), not one-off literals.

## Do not

- Invent HTTP paths. The Elf requests interfaces from The Cleric (`hb-ag-contracts`) as content-needed (fields, page, UI need) — never a path invented here, never edit [[INTERFACES]].
- Author tests. The Elf does not write tests; The Trickster (`hb-ag-test`) plants traps.
- Load the interface-framework, domain-framework, contracts, local-runtime, cloud, or abc skills.
- Agent The Dwarf.

## Instantiation

This is a template skill: replace every `{{placeholder}}`, then rename the
folder to `{{prefix}}-sk-{{technology}}` (e.g. the component framework's
name). A headless project deletes this skill, `hb-sk-surface-framework`,
and `hb-ag-surface` together. See [[ONBOARDING]] and [[CLONE]].
