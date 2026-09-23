---
title: Interface catalog
type: reference
status: active
version: v0.1.0
tags: [interfaces, contracts, ssot]
description: "Entry points in this repository: skills, scripts, and MCP. There is no HTTP service."
applies_when:
  - When adding or calling a public entry point.
related_adrs:
  - adr-01-nomenclature
  - adr-02-stack
---
# INTERFACES

An entry point is valid when it has a row here. This repository has no HTTP service.

| Kind | Path | Entry | Input | Auth | Description |
|---|---|---|---|---|---|
| skill | `skills/kskill-graphify` | `SKILL.md` | graph question | local | Query the code graph over MCP |
| script | `skills/kskill-graphify/bin/ensure` | `ensure` | repo root | local | Install Graphify and build `graph.json` if missing |
| script | `scripts/graphify-update` | `graphify-update` | repo root | local | Refresh the AST graph (`--code-only`) |
| script | `scripts/graphify-extract` | `graphify-extract` | repo root | local | Semantic graph rebuild; needs an LLM key |
| skill | `skills/kskill-mood` | `SKILL.md` | `/kdx-mood` | local | Session stance |
| skill | `skills/kskill-qw` | `SKILL.md` | `/qw` | local | Quick-win stance |
| skill | `skills/diagram-design` | `SKILL.md` | diagram brief | local | Diagram procedure |
| mcp | `mcp/mcp.json` | `graphify.serve` | `graphify-out/graph.json` | local | Graphify MCP server |
| skill | `skills/kskill-context` | `SKILL.md` | repo name | local | Clone and index configured context repos |
| script | `skills/kskill-context/bin/list` | `list` | optional repo name | local | Print registry entries and local state |
| script | `skills/kskill-context/bin/sync` | `sync` | optional repo name | local | Clone or fast-forward, then index |
| script | `skills/kskill-context/bin/index` | `index` | repo name | local | Code-only Graphify graph for one clone |
| hook | `.cursor/hooks/load-hook.py` | `sessionStart` | Cursor hook payload | local | Load PRD, ADRs, and docs into context |
| hook | `.cursor/hooks/graphify-ensure.py` | `sessionStart` | Cursor hook payload | local | Ensure the graph exists |

Large payload shapes, if one is ever needed, go in `docs/contracts/`.
