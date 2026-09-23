---
title: Version pins and toolchain requirements
type: reference
status: active
version: v0.1.0
tags: [requirements, pins]
description: "Toolchain pins for this repository."
applies_when:
  - When adding or upgrading a tool.
  - When checking a sanctioned version.
related_adrs:
  - adr-02-stack
---
# REQUIREMENTS

A tool enters the repository by landing a row here first. The stack decision is [`adrs/adr-02-stack.md`](../adrs/adr-02-stack.md).

| Tool | Version | Notes |
|---|---|---|
| gh | 2.91.0 | GitHub CLI. Floor **2.80.0**. |
| git | any recent | — |
| uv | any recent | Resolves Graphify (`uvx --from graphifyy[mcp]`) and pytest |
| graphifyy[mcp] | 0.9.51 | Graphify CLI and MCP extra |
| pytest | current | Test runner, installed at CI and via `uv run --with pytest` |
| chrome-devtools-mcp | 1.6.0 | Declared in `mcp/mcp.json`, resolved by `bunx` |

## Re-pin policy

A pin moves in its own PR, with the date checked against the vendor's release notes. A version that cannot be stated is not adopted.
