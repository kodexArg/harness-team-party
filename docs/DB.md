---
title: Database
type: reference
status: active
version: v0.1.0
tags: [database, data, ssot]
description: "Database engine, schema conventions, and data lifecycle rules. Ships as a placeholder."
applies_when:
  - When designing a model, migration, or data lifecycle rule.
  - When checking schema conventions.
related_adrs:
  - adr-02-stack
---
# DB

> This file is **expected** and currently a placeholder. Instantiation writes
> it with the first model ([[CLONE]]).

## What it must eventually contain

- **Engine** — `{{database}}`, local vs cloud instances.
- **Schema conventions** — naming, keys, and the model hygiene rules of [[adr-01-nomenclature]] applied to tables.
- **Migrations** — how schema changes ship (the service framework's migration tooling, per [[adr-02-stack]]).
- **Data lifecycle** — what is persisted, what is derived, what is never stored.
- **Seeds and fixtures** — how a developer gets a working dataset.
