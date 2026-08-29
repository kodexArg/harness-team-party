---
title: adr-03.a-api
type: adr
status: active
version: v0.1.2
tags: [interfaces, routes]
description: "INTERFACES.md is the route catalog: six-column row before tests or handlers."
applies_when:
  - When declaring, changing, or retiring a service route or fragment route.
  - When checking handler, payload, or auth columns against the catalog.
related_agents:
  - hb-ag-contracts
---

# ADR-03.a — API contract

> One catalog of routes keeps undeclared handlers from becoming the interface.

Instantiation: keep this sub. Point it at [[INTERFACES]] (not a second catalog). Change column names only if the transport is not HTTP — then say so here.

1. **SSOT.** [[INTERFACES]] is the sole catalog of service routes under `{{api prefix}}`. An undeclared route is a defect.

2. **Six-column row.** Every route is one row: Method, Path (English, trailing slash), Handler, Payload (or `—`), Auth, Description. The Cleric writes the row (`hb-ag-contracts`).

3. **Pre-declaration.** An approved row exists before tests, handlers, or routing (`plan → [[INTERFACES]] → [[TDD]] → code`). The same change updates the row.

4. **Retire the row first.** Removing a route starts by deleting its catalog row.

5. **Fragment routes.** If this project serves HTML fragments, they are catalog rows with payload `—` ([[adr-03.c-htmx]]). If it does not, delete that sentence.
