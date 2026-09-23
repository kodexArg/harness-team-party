# Architecture

> How this repository is put together.

## 1. Layout

- **`skills/`** holds procedures and the scripts they run.
- **`docs/`** and **`adrs/`** hold intent and settled decisions. `.cursor/hooks/load-hook.py` reads them at session start.
- **`tests/`** checks that those files stay linked.
- **`mcp/mcp.json`** declares the Graphify server. `.mcp.json` points at it.
- **`context/`** holds on-demand clones of configured repos. `context/repos.json` is tracked. Clones and `context/.graphs/` are not.

There is no service process, database, or UI bundle in this tree.

## 2. Code graph

`graphify-out` is a symlink to `skills/kskill-graphify/graphify-out`. `graph.json` and `manifest.json` are tracked. `cache/` is not.

## 3. Secrets

Model credentials are `OPENROUTER_API_KEY` in a gitignored `.env`. Names are listed in [`docs/VARIABLES.md`](docs/VARIABLES.md). Values are not committed.

## 4. Runtime

Python 3 and `uv` on the workstation. Tests run with pytest. Graphify is installed with `uv tool` by `skills/kskill-graphify/bin/ensure`, not as a project dependency.
