# ADR-35 — Graphify

> Graphify MCP is the primary codebase exploration mechanism when the knowledge graph is present.

1. When the graph is present, Graphify MCP tools (`query_graph`, `get_node`, `get_neighbors`, `shortest_path`) are the preferred first exploration mechanism.
2. File reading and targeted search (`Read`, grep) run after initial graph exploration on identified symbols and paths.
3. When `query_graph` lands on a leaf node or yields partial context, inspect callers and dependencies using `get_neighbors`.
4. When the graph is absent or unavailable, standard text search and file discovery apply.
5. `graph.json` and `manifest.json` are tracked. Ephemeral cache files under `graphify-out/cache/` are not committed.
6. Context repos listed in `context/repos.json` are indexed on demand under `context/.graphs/`. Those clones and graphs are never committed.
