---
title: Infrastructure and deployment
type: reference
status: active
version: v0.1.0
tags: [infrastructure, deploy, cloud, ssot]
description: "Cloud layout, deploy trust, local runtime, and the resource inventory. Ships as a placeholder."
applies_when:
  - When changing cloud resources, deploy wiring, or the local runtime.
  - When checking deploy trust or secret-store naming.
related_adrs:
  - adr-02-stack
  - adr-08-github
---
# INFRASTRUCTURE

> This file is **expected** and currently a placeholder. Instantiation writes
> it when the first environment exists ([[CLONE]]).

## What it must eventually contain

- **Cloud layout** — `{{deploy target}}` on `{{cloud provider}}`, region `{{region}}`, host `{{host}}`.
- **Deploy trust** — the credential that ships from `refs/heads/main` only ([[adr-08-github]] rule 5), and how it is federated.
- **Local runtime** — `{{local runtime}}` orchestration: profiles, ports `{{local ports}}`, bind-mounts.
- **Secrets** — the secret store and its naming scheme: `{{secret naming}}`. Names and metadata only, never values.
- **Resource inventory** — the live resource rows (names, ids, tags), kept authoritative and committed.
- **Deliberate absences** — the infrastructure this layout does not have: `{{infrastructure absences}}`.
