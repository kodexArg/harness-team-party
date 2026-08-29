---
title: Environment variables, secret paths, and runtime configuration inventory
type: reference
status: active
version: v0.1.0
tags: [harness, variables, secrets, config, ssot]
description: "Single source of truth for all declared environment variables and secret-store mappings. Ships as a placeholder."
applies_when:
  - When declaring environment variables for any tree.
  - When configuring secret-store mappings.
  - When verifying public versus secret variable exposure.
related_adrs:
  - adr-02-stack
---
# VARIABLES

The environment-variable **SSOT**. Every variable any tree reads is declared here first.

**A variable used in code but not declared here does not exist.** Same doctrine as [[INTERFACES]].

**Every secret value lives in the project's secret store, always** ([[INFRASTRUCTURE]]). Never committed in `.env`, never plain env in compute definitions, never in the surface tree at all. The surface receives only explicitly public non-secret variables. Local `.env` (git-ignored) holds dev-only values mirroring the names declared here.

## Declaration format

> Each variable is one row. The row is added here first — before the variable is used anywhere.

## Declared variables

> Complete inventory of every variable the service, the surface, the harness, and the local orchestrator read. Extended per feature; never pruned blindly.

### Harness (local tooling)

Read by harness tooling and agent sessions. Non-secret identity values; the PAT **values** live in the operator's secret store / dashboard, never in the repo.

| Name | Scope | Envs | Secret? | Source | Description |
|---|---|---|---|---|---|
| `GITHUB_PAT` | harness | local/cloud | yes | operator dashboard secret | Operator PAT for `gh` Issues/PRs/merges on cloud sessions ([[GITHUB]] — Cursor Cloud `gh` credential) |
| `GH_PROJECT_PAT` | harness | local/cloud | yes | operator dashboard secret | Repo-named mirror of `GITHUB_PAT` (rename to match this repo at instantiation) |
| `PROJECT_SLUG` | service + CI | dev/prod/local | no | plain env; `.env` local | Project slug — the `{{project slug}}` in every resource name. Sanctioned consumption points are listed here at instantiation |

### Service

| Name | Scope | Envs | Secret? | Source | Description |
|---|---|---|---|---|---|
| {{VARIABLE_NAME}} | {{scope}} | {{envs}} | {{yes/no}} | {{source}} | {{description}} |

### Surface

| Name | Scope | Envs | Secret? | Source | Description |
|---|---|---|---|---|---|
| {{PUBLIC_VARIABLE_NAME}} | {{scope}} | {{envs}} | no | {{source}} | {{description}} — public, non-secret, the only kind the surface may read |
