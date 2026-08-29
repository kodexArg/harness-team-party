---
title: adr-00.c-adr-template
type: adr
status: active
version: v0.1.0
tags: [template, layout]
description: "Defines the standard structural body template and phrasing conventions for ADRs."
applies_when:
  - When creating a new ADR document.
  - When verifying that an existing ADR complies with the canonical physical layout.
---

# ADR-00.c — ADR template

> A uniform document structure ensures rapid scanning, unambiguous interpretation by LLMs and human operators, and consistent assertion quality across the repository.

1. **Single structural use case.** This template is consumed exclusively when creating a new ADR or verifying that an existing ADR complies with the canonical physical layout, irrespective of domain content.

2. **Heading convention.** The title follows `# ADR-NN — <slug description>` (or `# ADR-NN.x — <slug description>` for sub-ADRs).

3. **Context blockquote.** The first element under the title is a prose blockquote (`> `) of one or two sentences explaining the rationale and why the rule exists. The quote contains plain text without hyperlinks.

4. **Numbered assertions.** Core rules follow as sequential numbered items:
   - State the WHAT as definitive, positive assertions.
   - Keep each point compact, generic, and focused on architectural invariants.
   - Link domain facts, data tables, or external specifications to authoritative docs.

5. **Recommended size and brevity.** ADRs strive to remain compact, with a recommended target under 30 lines (~300–500 tokens). Broad contexts or expansive topics are partitioned into `docs/` or decomposed into sub-ADRs (`adr-NN.x-*`).

6. **Body template.** Standard ADR body layout:

```markdown
# ADR-NN — title-slug

> Concise prose context explaining the background and rationale for this decision.

1. **Core assertion.** Definitive statement of the architectural invariant formulated by the positive.
2. **Operational boundary.** Clear scope of application and integration criteria.
3. **Reference pointers.** Links to authoritative documentation for detailed domain context.
```
