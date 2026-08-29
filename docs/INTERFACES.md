---
title: Interface catalog — the route authority
type: reference
status: active
version: v0.1.1
tags: [interfaces, contracts, ssot]
description: "The interface catalog: every route the service serves, one six-column row each. Ships as a placeholder; The Cleric owns it."
applies_when:
  - When checking whether a route is declared before writing or calling it.
  - When The Cleric adds, changes, or retires a catalog row.
related_adrs:
  - adr-01-nomenclature
  - adr-02-stack
---
# INTERFACES — the catalog

> This file is **expected** and currently a placeholder. It is the route
> authority for the instantiated project: an interface is valid if and only if
> it has a row here. An undeclared route in code is a defect.

Owner: **The Cleric** (`hb-ag-contracts`) — the sole writer. Everyone else
reads. Row-writing contract: `hb-sk-contracts`.

## What it must eventually contain

One six-column row per route the service serves:

| Method | Path | Handler | Payload | Auth | Description |
|---|---|---|---|---|---|
| {{http method}} | {{example path}} | {{handler name}} | {{payload shape}} | {{permission class}} | {{route description}} |

- **Method** — the HTTP verb (or the transport's equivalent).
- **Path** — English, trailing slash, under one of the declared prefixes: `{{api prefix}}`.
- **Handler** — the named handler, per [[GLOSSARY]] naming.
- **Payload** — the payload shape, or `—` for fragment rows; large shapes live in `docs/contracts/`.
- **Auth** — the permission class that **will** exist.
- **Description** — what it serves, linking the contract document.

Row first, then TDD, then code ([[DEVELOPMENT-LOOP]]). Retire the row before
deleting the code.
