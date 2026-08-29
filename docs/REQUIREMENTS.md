---
title: Version pins and toolchain requirements
type: reference
status: active
version: v0.1.1
tags: [harness, requirements, pins, ssot]
description: "Single source of truth for dependency pins, toolchain versions, and re-pin policy. Ships as a placeholder with the harness pins filled."
applies_when:
  - When adding or upgrading a dependency.
  - When checking the sanctioned version of a toolchain component.
related_adrs:
  - adr-02-stack
---
# REQUIREMENTS

The version-pin **SSOT** ([[adr-02-stack]] rule 1). A dependency enters the
project by landing a row here first; the stack decision itself is
[[adr-02-stack]].

> This file is **expected** and currently a placeholder: the harness tooling
> pins below ship filled; the product stack rows are written at instantiation
> ([[CLONE]]), when [[adr-02-stack]] is decided.

## Harness tooling

| Tool | Version | Notes |
|---|---|---|
| gh | 2.91.0 | GitHub CLI. Floor **2.80.0**: older releases select the sunset Projects-classic GraphQL field on `gh issue view --comments` and hard-fail ([[GITHUB]] — Reading issue comments) |
| git | any recent | — |
| uv | any recent | Resolves the Graphify MCP server (`uvx --from graphifyy[mcp]`, [[GRAPHIFY]]) |
| graphifyy[mcp] | 0.9.51 | Graphify CLI + MCP extra ([[GRAPHIFY]]) |
| chrome-devtools-mcp | 1.6.0 | Declared in `mcp/mcp.json`, resolved by `bunx`; never a build dependency ([[HARNESS]]) |

## Service stack

| Package | Version | Checked | Notes |
|---|---|---|---|
| {{package}} | {{pin version}} | {{pin date}} | {{why this pin}} |

## Surface stack

| Package | Version | Checked | Notes |
|---|---|---|---|
| {{package}} | {{pin version}} | {{pin date}} | {{why this pin}} |

## Re-pin policy

A pin moves in its own PR, with the date checked against the vendor's release
notes. A version that cannot be stated is not adopted.
