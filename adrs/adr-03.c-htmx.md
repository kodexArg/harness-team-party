---
title: adr-03.c-htmx
type: adr
status: active
version: v0.1.2
tags: [fragments, hypermedia]
description: "HTML-fragment / hypermedia producer lives in the service, if the project has one."
applies_when:
  - When authoring HTML partials or hypermedia swaps from the service.
  - When declaring a fragment route in INTERFACES.
related_agents:
  - hb-ag-service
---

# ADR-03.c — HTMX fragments

> One producer of fragment HTML keeps the surface from inventing a second copy of the same markup.

Instantiation: **keep, rewrite, or delete.** The filename says HTMX because that is a common choice — it is not a stack lock. Set `{{html fragment technology}}` (HTMX, Hotwire, datastar, …) or delete this whole sub if the service never returns HTML fragments. Rename the slug in the same batch if the name would mislead.

1. **Service as fragment engine.** `{{html fragment technology}}` fragments are produced in `{{service tree}}`. The surface host does not ship a parallel fragment tree for the same swap.

2. **Catalog row.** Every fragment route is an [[INTERFACES]] row with payload `—` and a description of the swap.

3. **Mutations.** Fragment POST/PUT/PATCH/DELETE use the project's session and CSRF (or equivalent) rules in [[AUTH]].

4. **Dedicated handling.** Fragment responses are explicit (dedicated handler or a documented request-header branch), with the headers that technology requires.
