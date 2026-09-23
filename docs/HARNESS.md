# Harness Overview

> Architecture, tooling, and organization of this agentic development harness.

## 1. Repository Structure

- **`docs/`**: Core specifications, architecture, and developer documentation.
  - `PRD.md`: Product constitution, user requirements, and acceptance criteria (**WHAT & WHY**).
  - `INTERFACES.md`: Explicit API and route catalog (**WHAT**).
  - `ARCHITECTURE.md`: Technical architecture across services, persistence, auth, and infrastructure.
  - `TESTING.md`: Automated test guidelines and quality standards.
  - `GITHUB.md`: Git branching, commit guidelines, and PR workflow.
  - `SETUP.md`: Quickstart and project instantiation.
- **`adrs/`**: Architectural Decision Records documenting significant technical choices.
- **`skills/`**: Specialized procedures and tools.
- **`agents/`**: Agent role definitions and tool configurations.
- **`tests/`**: Automated test suite for the harness and product.

## 2. Tools & Graph Navigation

- **Graphify:** Repository knowledge graph for structural navigation before grepping code.
  - `skills/kskill-graphify/bin/ensure`: Ensures Graphify CLI and graph state.
  - Project MCP server in `.mcp.json` provides graph query tools (`query_graph`, `get_node`, `get_neighbors`).

| Tool | Path | Description | Status |
|---|---|---|---|
| `kskill-graphify` | `skills/kskill-graphify` | Knowledge graph navigation skill | active |

- **Tests & Verification:**

  - Fast test execution via standard runners: `uv run --with pytest pytest tests/`.
