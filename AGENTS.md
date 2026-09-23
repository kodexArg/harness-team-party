# AGENTS

How to work in this repository.

## Instructions

1. Read [`docs/PRD.md`](docs/PRD.md) and [`docs/INTERFACES.md`](docs/INTERFACES.md) before changing behavior.
2. Explore with Graphify (`query_graph`, `get_node`, `get_neighbors`) when `graphify-out/graph.json` is present. Procedure: [`docs/GRAPHIFY.md`](docs/GRAPHIFY.md), [`adrs/adr-35-graphify.md`](adrs/adr-35-graphify.md).
3. Follow [`docs/DEVELOPMENT-LOOP.md`](docs/DEVELOPMENT-LOOP.md). Tests live in `tests/`. English in code and technical docs.
4. Ship through an ephemeral branch and a pull request into `main`: [`docs/GITHUB.md`](docs/GITHUB.md).

## References

- [`docs/GRAPHIFY.md`](docs/GRAPHIFY.md) — code graph and MCP.
- [`docs/SETUP.md`](docs/SETUP.md) — clone and local setup.
- [`docs/TESTING.md`](docs/TESTING.md) — how to run tests.
- [`docs/HARNESS.md`](docs/HARNESS.md) — repository layout.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — how the tree is put together.
