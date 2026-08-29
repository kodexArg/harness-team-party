---
title: adr-35-graphify
type: adr
status: active
version: v0.1.0
tags: [adr, harness, graphify, exploration, mcp]
description: "Graphify MCP is the first exploration mechanism when the graph is present. Governs bidirectional navigation (downstream children and upstream parents), tool selection, transition to file reading, and cache tracking."
applies_when:
  - When exploring code or docs or answering an architecture question.
  - When deciding whether to Grep first or navigating parent/child dependencies.
---

# ADR-35 — Graphify

Rules only; content lives in [[GRAPHIFY]].

1. When the graph is present, Graphify MCP tools are the first exploration mechanism.
2. Grep, Glob, and direct file reading run after it, exclusively on the files and symbols identified by the graph.
3. When a downstream (children) query via `query_graph` yields incomplete context or lands on a leaf component, inspect upstream (parents / callers) with `get_neighbors` before exiting the graph.
4. Tool selection follows the query intent:
   - `query_graph(question=...)` for broad semantic discovery and downstream dependency trees.
   - `get_neighbors(label=...)` to inspect incoming callers/importers and outgoing dependencies of a known node.
   - `get_node(label=...)` to retrieve node metadata, file location, and community.
   - `shortest_path(source=..., target=...)` to trace the dependency or call chain between two symbols.
5. When the graph is absent, Grep, Glob, and Read are the path.
6. Graphify does not replace [[CODEMAP]].
7. `graph.json` and `manifest.json` are tracked. The generated cache under `graphify-out/` is never committed.
