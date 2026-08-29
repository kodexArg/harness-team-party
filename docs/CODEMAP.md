---
title: Generated inverse index from docs to code
type: reference
status: active
version: v0.1.0
tags: [harness, codemap, generated]
description: "Generated inverse index: each heading is a live-doc SSOT, and the list is every code file whose live-doc block declares that SSOT. Ships as a placeholder until the linker is vendored."
applies_when:
  - When mapping a doc or ADR to the code files it governs.
  - When checking live-doc coverage of a tree.
related_adrs:
  - adr-05-after-versioning
---

# CODEMAP — doc → code index

> This file is **expected** and currently a placeholder. It becomes the
> generated inverse index once the project vendors a live-doc linker and its
> manifest; until then it is hand-maintained or simply sparse. Ruled by
> [[HARNESS]].

Each heading is a live-doc SSOT; the list under it is every code file that
declares itself governed by that SSOT through its `LIVE-DOC:START …
LIVE-DOC:END` block ([[GLOSSARY]]: live-doc block).

## What it must eventually contain

- One `## [[<ssot>]]` heading per governing doc/ADR that code files cite.
- Under each, the repo-root-relative paths of the files carrying that block.

Generated indexes are never hand-edited; edit the linker manifest and re-run.
