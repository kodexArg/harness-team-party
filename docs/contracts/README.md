---
title: Interface payload contracts
type: reference
status: active
version: v0.1.0
tags: [contracts, interfaces]
description: "Holds the payload-shape documents that docs/INTERFACES.md rows link from their Description column."
applies_when:
  - When a catalog row's payload is too large to inline in INTERFACES.md.
  - When The Cleric writes or retires a payload shape.
related_adrs:
  - adr-01-nomenclature
---

# docs/contracts/

Payload shapes live here, one document per contract cluster, linked from the
Description column of [[INTERFACES]] rows — never inlined into the catalog
table.

Expected content, written by The Cleric (`hb-ag-contracts`) at the first row
that needs it:

- Request and response payload shapes, field by field, English keys.
- Error shapes and status codes the row can return.
- Fragment markup contracts (`Payload: —` rows) when the swap's shape matters.

Naming: `contract-<cluster>.md`, kebab-case cluster names registered in
[[GLOSSARY]] before first use.
