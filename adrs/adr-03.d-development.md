---
title: adr-03.d-development
type: adr
status: active
version: v0.1.2
tags: [development, local-runtime]
description: "Local service boot: one root orchestrator, bind-mounts, documented start chain."
applies_when:
  - When starting the local service stack.
  - When changing local ports, bind-mounts, or the service boot sequence.
related_agents:
  - hb-ag-ops
  - hb-ag-service
---

# ADR-03.d — local development

> One documented local boot keeps workstations and cloud VMs on the same sequence.

Instantiation: fill the orchestrator and the boot chain. Compose, a Procfile, or another `{{local runtime}}` are all valid — name the one [[adr-02-stack]] chose. Rewrite the example chain; do not treat migrate/seed as mandatory if this stack has none.

1. **One orchestrator.** Local service development uses root `{{local runtime}}` ([[INFRASTRUCTURE]]). A second per-app compose file is not the architecture.

2. **Boot sequence.** Every local service start runs: `{{boot sequence}}` (example shape: migrate → seed → run with reload). Replace that list with this project's real commands.

3. **Reload and port.** The service listens on the port named in `{{local ports}}` with source bind-mounted as [[INFRASTRUCTURE]] says.

4. **Environment.** Local config is git-ignored `.env` mirroring [[VARIABLES]] names. Debug and auth-dev flags stay out of production defaults.
