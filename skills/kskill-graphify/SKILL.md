---
name: kskill-graphify
description: >
  First exploration mechanism when the graph is present (adr-35-graphify).
  Query, path, explain against the docs+harness graph; ensure the CLI
  and graph.json after clone; extract or update it; upgrade the CLI;
  fetch the upstream skill snapshot. Triggers: graphify, graph.json,
  first mechanism, GRAPHIFY, kskill-graphify. Slash /kskill-graphify.
  Ruled by adr-35-graphify.
tools:
  - query_graph
  - get_neighbors
  - get_node
  - shortest_path
  - Read
  - Glob
  - Grep
  - Bash
---

# kskill-graphify

Procedure for [[adr-35-graphify]] over [[GRAPHIFY]]. Where this file
and that doc disagree, the doc wins ([[HARNESS]]).

Trim of Graphify-Labs `graphify/skill.md` (Apache 2.0). Upstream
snapshot: `skills/kskill-graphify/upstream/`. This copy keeps query,
path, explain, extract, and update. MCP is declared in `mcp/mcp.json`,
not vendored here. It drops Neo4j, Whisper, `graphify add <url>`,
GitHub clone, wiki, Obsidian, and pip/npx install.

Graph files live in the harness:
`skills/kskill-graphify/graphify-out/`. Repo-root `graphify-out`
is a symlink to that directory. `graph.json` and `manifest.json`
are tracked; `cache/` is not.

## Do this

1. Facts: read [[GRAPHIFY]]. Do not restate them here.
2. **Present?** `skills/kskill-graphify/graphify-out/graph.json`
   (or the `graphify-out` symlink).
3. **Present:** Graphify MCP (`query_graph`, `get_neighbors`, `get_node`,
   `shortest_path`) before Glob or Read ([[adr-35-graphify]] rule 1).
4. **Absent:** run `skills/kskill-graphify/bin/ensure`. If it still cannot produce a graph, Grep/Glob/Read
   ([[adr-35-graphify]] rule 5).
5. **Rebuild / refresh / upgrade** — real scripts, repo root:

   ```
   skills/kskill-graphify/bin/ensure           # CLI + code-only graph if missing
   skills/kskill-graphify/bin/extract          # semantic docs+harness (LLM key)
   skills/kskill-graphify/bin/update-graph     # incremental AST --code-only
   skills/kskill-graphify/bin/upgrade-cli      # uv tool install --upgrade graphifyy
   skills/kskill-graphify/bin/fetch-upstream   # snapshot official SKILL.md
   ```

   `GRAPHIFY_UPSTREAM_REF` (default `v8`) selects the GitHub ref
   for fetch-upstream.
6. [[CODEMAP]] is a different graph. This skill does not write `docs/`.

## Return shape

```
topic: <query | path | explain | ensure | extract | update | upgrade | fetch-upstream>
graph: present | absent
quote: <one GRAPHIFY sentence or empty>
file: docs/GRAPHIFY.md
```

## Do not

- Run `npx skills add` or `npm` (unprefixed `graphify/` skill,
  npm prohibited).
- Run `graphify add <url>` (historical SSRF).
- Run `graphify claude|codex|opencode install` (rewrites AGENTS).
- Vendor `upstream/SKILL.md` onto this file.
- Commit `graphify-out/cache/`.
- Load the full [[HARNESS]] file to answer one row.
- Replace [[CODEMAP]].
- Block clone or session start on an LLM API key.
