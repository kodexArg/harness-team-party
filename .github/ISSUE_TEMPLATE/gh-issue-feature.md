---
name: Feature
about: A user-facing feature with Requires and references
title: "feat: "
labels: feat
assignees: {{owner}}
---

<!--
 Language: English for structure; keep verbatim user quotes in their original language.
 Links: Obsidian [[wikilinks]] and repo-root-relative paths.
 Every change: this issue → PR ([[DEVELOPMENT-LOOP]] §0.5).
 ENFORCEMENT: a feature issue without Story + Acceptance is incomplete —
 agents must rewrite it into this shape before building ([[GITHUB]]).
-->

## Story

**As a** <role>
**I want** <goal>
**so that** <value>

<!-- Optional: the real request, verbatim (any language). -->
> "<the user's ask, verbatim>"

## Acceptance criteria

- <observable, testable condition 1>
- <observable, testable condition 2>
- Guardian verdicts pass (AGENTS.md "Agents" section) when in scope

## Requires

<!--
 Issue-on-issue dependency SSOT ([[GITHUB]] — Requires).
 List every issue that MUST be CLOSED before this one is planned or built.
 Leave the empty marker when there is no predecessor.
 Do NOT use the `blocked` label for "waiting on another issue".
-->

- none

<!-- Examples when dependent:
- #314
- #360 · #361
-->

## References

<!--
 ⛔ Star section. Issues die orphaned for want of a link graph.
 Link LIBERALLY. Use [[wikilinks]]; code as repo-root-relative paths.
-->

**Governing ADRs** — which decisions constrain this work
- [[adr-NN-slug]]

**Specs & docs** — the SSOTs this touches
- [[TDD]] · [[INTERFACES]] · [[SERVICES]] · [[PRD]] · <trim>

**Code** — files/dirs the change lives in (repo-root-relative)
- [[{{surface tree}}/.../Thing.ext]]
- [[{{service tree}}/.../handlers.ext]]

**Related work** — issues, PRs, handoffs, prior art
- #<issue> · #<pr>

## Notes / out of scope

<!-- Anything a fresh agent must NOT assume. Environment gotchas, decisions deferred. -->
