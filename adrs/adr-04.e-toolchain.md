---
title: adr-04.e-toolchain
type: adr
status: active
version: v0.1.2
tags: [toolchain, surface]
description: "One surface toolchain and lockfile; pins in REQUIREMENTS; three verification layers."
applies_when:
  - When installing or pinning a surface dependency.
  - When running surface check, build, or smoke.
related_agents:
  - hb-ag-surface
  - hb-ag-test
---

# ADR-04.e — toolchain

> One package manager and lockfile keep local and CI on the same tree.

Instantiation: `{{surface toolchain}}` is the decision ([[adr-02-stack]]). Substitute managers are not the path. Rewrite the three layers to this host's real commands.

1. **Toolchain.** `{{surface toolchain}}` owns install, scripts, tests, and the lockfile. A second JS/Python package manager for the same tree is not the architecture.

2. **Verification layers** (rename to match this host):
   - Layer 1: static check (`check` / types).
   - Layer 2: production build.
   - Layer 3: interactive browser smoke — operator-run, never an unattended CI gate ([[HARNESS]]).

3. **Pins.** New surface packages land a [[REQUIREMENTS]] row first.
