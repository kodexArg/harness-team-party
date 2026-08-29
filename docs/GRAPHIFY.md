---
title: Graphify code graph exploration and MCP toolchain
type: reference
status: active
version: v0.1.1
tags: [harness, graphify, mcp, ast, graph]
description: "Governs first-line codebase exploration using the on-device Graphify code graph via MCP."
applies_when:
  - When exploring repository symbols and file dependencies via MCP.
  - When running graph queries for code impact analysis.
  - When extracting or updating code graph JSON files.
related_adrs:
  - adr-35-graphify
---
# GRAPHIFY

> The on-device code graph for this repository. When present, Graphify MCP tools are the first exploration mechanism — query the graph over MCP before Glob, Grep, or Read.

The on-device code graph for this repository. Force: [[adr-35-graphify]].

The graph is **present** when `graphify-out/graph.json` exists. A clone should
carry that file. **Install Graphify when the host can** — this harness is meant
to be explored through it, not around it:

```
skills/kskill-graphify/bin/ensure
```

That installs `graphifyy[mcp]` (needs `uv`) and builds a `--code-only`
`graph.json` if it is missing. No LLM key. A semantic docs+harness extract
(`skills/kskill-graphify/bin/extract`) is better when an LLM key is available;
it is not required to start. Grep is only the path after `ensure` cannot run.

## MCP Integration

Graphify is served exclusively via MCP. The **project** declaration is `.mcp.json` → `mcp/mcp.json`. That is the portable contract for this repo:

```json
{
  "mcpServers": {
    "graphify": {
      "command": "uvx",
      "args": [
        "--from",
        "graphifyy[mcp]",
        "python3",
        "-m",
        "graphify.serve",
        "graphify-out/graph.json"
      ]
    }
  }
}
```

Upstream docs ([graphify.com/docs#mcp](https://graphify.com/docs#mcp)) show the same server as `"command": "python", "args": ["-m", "graphify.serve", "graphify-out/graph.json"]`. `graphify-mcp` is the uv-tool console script for that module; `--graph PATH` is the same as the positional path. This repo uses `uvx --from graphifyy[mcp]` so the `mcp` extra is present without depending on system Python.

Relative `graphify-out/graph.json` is valid **only** when the MCP process cwd is the repo root (project MCP). A **user** MCP config starts with cwd `$HOME`; the relative path then looks for `$HOME/graphify-out/graph.json` and exits. A user-level server must pass an **absolute** `--graph` to that workspace's `graph.json`.

Worktree agent sessions do not inherit the parent clone's approved project MCP. If `query_graph` is missing in a worktree chat: turn Graphify on in that worktree's MCP panel, or attach user MCP with an absolute graph path.

`uv tool install graphifyy` without `[mcp]` ships a `graphify-mcp` that cannot `import mcp`. `ensure` / `upgrade-cli` install `graphifyy[mcp]`. Never `graphify install` or `graphify claude|codex|opencode install`.

The server exposes ten tools. First-line for this repo: `query_graph`, `get_node`, `get_neighbors`, `shortest_path`. Also present: `get_community`, `god_nodes`, `graph_stats`, `list_prs`, `get_pr_impact`, `triage_prs`.

## Navigation & Tool Selection

- `query_graph(question=...)`: BFS semantic and keyword search across nodes and downstream dependency trees (*children*).
- `get_neighbors(label=...)`: Immediate incoming (*parents / callers*) and outgoing (*children / dependencies*) edges. When a downstream search lands on a leaf component, check incoming neighbors to identify the parent container before falling back to filesystem tools.
- `get_node(label=...)`: Retrieve node metadata, file location, and community.
- `shortest_path(source=..., target=...)`: Trace dependency or call chains between two specific symbols.

## Maintenance Scripts

| Script | Command | When |
|---|---|---|
| `scripts/graphify-update` | `uvx --from graphifyy graphify extract . --code-only` | Incremental AST refresh (`update-graph`). No LLM key. |
| `scripts/graphify-extract` | `uvx --from graphifyy graphify extract .` | Semantic rebuild of docs and harness (`extract`). Needs an LLM key (`GEMINI_API_KEY` or `OPENAI_API_KEY`). Product trees stay out (`.graphifyignore`). |
| `skills/kskill-graphify/bin/ensure` | `uv tool install 'graphifyy[mcp]'` / ensure `graph.json` | Clone / session start bootstrap (`ensure`). |
| `skills/kskill-graphify/bin/upgrade-cli` | `uv tool install --upgrade 'graphifyy[mcp]'` | Upgrade the host CLI (`upgrade-cli`). |
| `skills/kskill-graphify/bin/fetch-upstream` | curl GitHub raw `graphify/skill.md` | Snapshot official skill for reference (`fetch-upstream`). |

`graph.json` and `manifest.json` are tracked. `graphify-out/cache/` is gitignored. Never `graphify add <url>`.

When Graphify is installed and the graph is present, explore through the MCP
tools first. Then Glob, Grep, and Read the files returned by the graph. If it
is not installed, run `ensure` before falling back to Grep.

[[CODEMAP]] remains the generated doc→code inverse index.
