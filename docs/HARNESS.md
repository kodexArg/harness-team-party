# Repository layout

> Where the code, docs, and checks live.

## 1. Tree

- **`docs/`**: specifications for this repository.
  - `PRD.md`: purpose and acceptance.
  - `INTERFACES.md`: skills, scripts, and MCP entry points.
  - `ARCHITECTURE.md`: how the tree is put together.
  - `TESTING.md`: how tests are run.
  - `GITHUB.md`: branches, commits, and pull requests.
  - `SETUP.md`: clone and local setup.
- **`adrs/`**: settled technical decisions.
- **`skills/`**: procedures and the scripts they call.
- **`tests/`**: automated checks for this tree.
- **`mcp/`**: MCP server declarations.
- **`context/`**: configured clones (`kskill-context`). The registry is tracked; the clones are not.

## 2. Graph navigation

- **Graphify:** code graph used before grepping.
  - `skills/kskill-graphify/bin/ensure`: installs the CLI and builds `graph.json` when it is missing.
  - Project MCP server in `.mcp.json` exposes `query_graph`, `get_node`, and `get_neighbors`.

| Tool | Path | Description | Status |
|---|---|---|---|
| `kskill-graphify` | `skills/kskill-graphify` | Knowledge graph navigation skill | active |
| `kskill-context` | `skills/kskill-context` | On-demand clone and Graphify index of configured repos | active |

Run tests with `uv run --with pytest pytest tests/`.
