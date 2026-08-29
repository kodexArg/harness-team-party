---
title: Official documentation index for The Owl
type: reference
status: active
version: v1.1.0
tags: [harness, owl, documentation, index]
description: "Per-requirement official documentation URLs The Owl may fetch. One row per REQUIREMENTS pin. Product rows ship as placeholders."
applies_when:
  - When The Owl looks up official vendor documentation for a project pin.
  - When a pin PR must keep the official-docs URL in the same batch.
  - When filling product stack documentation links at instantiation.
related_adrs:
  - adr-02-stack
  - adr-05-after-versioning
---
# OWL-INDEX — official documentation links

The Owl (`hb-ag-owl`) reads this file first. It may fetch **only** URLs listed
here (and paths on the same official host under that documentation root). It
does not write this file.

Every row in [[REQUIREMENTS]] has a matching row here. A pin PR that changes
[[REQUIREMENTS]] updates the matching row in the same batch. Product stack
rows are filled at instantiation ([[ONBOARDING]], [[CLONE]]).

## Harness tooling

| Pin | Official docs URL | Notes |
|---|---|---|
| gh | https://cli.github.com/manual/ | GitHub CLI manual |
| git | https://git-scm.com/docs | Git reference |
| uv | https://docs.astral.sh/uv/ | Astral uv documentation |
| graphifyy[mcp] | https://github.com/graphify-org/graphify | Graphify CLI and MCP extra |
| chrome-devtools-mcp | https://github.com/ChromeDevTools/chrome-devtools-mcp | Declared MCP; not a build dependency |

## Service stack

| Pin | Official docs URL | Notes |
|---|---|---|
| {{package}} | {{official docs url}} | {{why this pin}} |

## Surface stack

| Pin | Official docs URL | Notes |
|---|---|---|
| {{package}} | {{official docs url}} | {{why this pin}} |
