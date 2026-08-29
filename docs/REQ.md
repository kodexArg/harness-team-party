---
title: Requirement-identifier tracking register
type: note
status: active
version: v0.1.0
tags: [doc, note, audit, requirements]
description: "Non-binding tracking note for REQ-DOMAIN-NN identifiers, when an audit or planning pass produces them."
applies_when:
  - When referencing requirement IDs produced by an audit or planning pass.
related_adrs:
  - adr-05-after-versioning
---
# REQ — the requirement-id tracking note

This file records the `REQ-<DOMAIN>-<NN>` identifiers an audit or planning pass
produces and that issues cite. It **binds nothing**: it states no lifecycle
obligation, it claims nothing about the issue template ([[GITHUB]] owns that
shape), and an id may be cited without a row here. Read it as a snapshot of the
pass that produced the ids, never as authority.

An id shared across several issues means the pass read those issues as facets of
one requirement. [[REQUIREMENTS]] is the version-pin SSOT ([[adr-02-stack]]),
not this note — despite the name, no `REQ-*` id lives there.

## Ids

GitHub is the live state, always; the table below is a snapshot.

| REQ id | Requirement | Open facets | Closed facets |
|---|---|---|---|
| {{REQ-DOMAIN-NN}} | {{requirement summary}} | {{open issues}} | {{closed issues}} |
