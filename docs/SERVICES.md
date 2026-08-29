---
title: Service architecture
type: reference
status: active
version: v0.1.4
tags: [services, architecture, ssot]
description: "The service architecture: framework-bound integration, Paladin-owned pure Python logic, layering, and conventions."
applies_when:
  - When placing new code in the service tree.
  - When checking the service's layering and module conventions.
related_adrs:
  - adr-02-stack
  - adr-03-backend
---
# SERVICES — service architecture

> This file is **expected** and currently a placeholder. Instantiation writes
> it once `{{service tree}}` exists ([[CLONE]]).

## What it must eventually contain

- **Layout** — the service tree's top-level structure: `{{service tree}}` and its module/area convention.
- **Framework** — `{{domain framework}}` and `{{interface framework}}` as this repo programs them (the stack decision: [[adr-02-stack]]).
- **Layering** — where handlers, domain services, and data access live; the pure-compute boundary.
- **Ownership boundary** — The Dwarf owns framework adapters, models, persistence, handlers, permissions, and routes. The Paladin owns framework-neutral Python business rules and complex script cores, including pure modules under `{{service tree}}`.
- **Test order** — framework-bound service work is TDD-first. The Paladin implements pure logic first; The Trickster adds its focused tests afterward ([[TDD]]).
- **Authorization** — the permission-class pattern and where checks happen.
- **Toolchain** — `{{service toolchain}}` commands for run, check, and test; pins in [[REQUIREMENTS]].
- **Conventions** — naming, file placement, and the things this tree deliberately never does.
