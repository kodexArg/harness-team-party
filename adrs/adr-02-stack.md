---
title: adr-02-stack
type: adr
status: active
version: v0.1.0
tags: [stack, toolchain]
description: "Toolchain for this repository: Python, uv, pytest, and Graphify."
applies_when:
  - When selecting a tool or runtime.
  - When checking that a dependency belongs in the tree.
related_adrs:
  - adr-35-graphify
---

# ADR-02 — stack

> The repository stays a skills-and-docs tree. Tool versions live in `docs/REQUIREMENTS.md`.

1. **Stack authority.** This ADR names the stack. Pins live in [`docs/REQUIREMENTS.md`](../docs/REQUIREMENTS.md).

2. **Runtime.** Python 3. Package resolution and one-off tools go through `uv`. No second package manager for Python.

3. **Code graph.** `graphifyy[mcp]`, installed by `skills/kskill-graphify/bin/ensure`, served from `mcp/mcp.json`.

4. **Tests.** pytest, via `uv run --with pytest pytest tests/`.

5. **Local model access.** OpenRouter. The key is `OPENROUTER_API_KEY` in gitignored `.env`. The model slug is `OPENROUTER_MODEL_ID`. Both names are in [`docs/VARIABLES.md`](../docs/VARIABLES.md).

6. **Absent on purpose.** No application server, database, or UI bundle in this repository. No committed secret values.
