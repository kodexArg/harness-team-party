# harness-team-party

> A clean, agile, and high-performance development harness for autonomous AI agents and pair programming.

## Overview

`harness-team-party` provides a pragmatic structure for software development with autonomous agents:
- **Contract-first architecture:** Explicit interfaces in [`docs/INTERFACES.md`](docs/INTERFACES.md) act as the source of truth between system boundaries.
- **Product focus:** [`docs/PRD.md`](docs/PRD.md) sets product purpose and acceptance criteria (**WHAT & WHY**), leaving execution and design creativity to the agent (**HOW**).
- **Knowledge graph navigation:** On-device semantic codebase graphs via Graphify for fast, high-context exploration.
- **Trunk-based delivery:** Ephemeral branches and pull requests into `main` for clean, verifiable integration.

## Quickstart

Follow [`docs/SETUP.md`](docs/SETUP.md) to instantiate a new project:

```bash
# 1. Fill docs/PRD.md with product requirements
# 2. Select stack in adrs/adr-02-stack.md
# 3. Define initial contracts in docs/INTERFACES.md
# 4. Verify test suite
uv run --with pytest pytest tests/ -q
```

## Directory Structure

```
├── docs/           # Product constitution (PRD), Interfaces, Architecture, Testing, Git
├── adrs/           # Architectural Decision Records
├── skills/         # Specialized tool procedures
├── agents/         # Agent role definitions
├── tests/          # Automated test suite
└── mcp/            # MCP server declarations (Graphify, etc.)
```

## License

MIT
