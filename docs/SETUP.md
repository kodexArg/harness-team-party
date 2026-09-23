# Project Setup & Instantiation Guide

> Clean, straightforward guide to instantiate and develop with this harness.

## 1. Quickstart

To create a new project from this harness:

```bash
# 1. Copy the template to your new project directory
cp -r /path/to/harness-team-party /path/to/my-project
cd /path/to/my-project
git init
```

## 2. Fill Core Project Information

Define the foundational project identity in `docs/PRD.md` and `docs/INTERFACES.md`:

1. **`docs/PRD.md`**: Define product purpose, target users, and acceptance criteria (**WHAT & WHY**).
2. **`docs/INTERFACES.md`**: Define the initial API, routes, and public contract catalog (**WHAT**).
3. **`adrs/adr-02-stack.md`**: Select and record your backend, frontend, database, and infrastructure stack.

Replace common placeholder tokens across docs:
- `{{project name}}` — Human-readable project name.
- `{{project slug}}` — Repository and package slug.
- `{{owner}}` / `{{repo}}` — GitHub organization/user and repository name.

## 3. Code Graph (Graphify)

Graphify provides semantic knowledge graph navigation of the repository:

```bash
# Ensure Graphify CLI is ready (requires uv)
skills/kskill-graphify/bin/ensure
```

When MCP is supported, enable the project MCP server in `.mcp.json`.

## 4. Verification

Verify the harness and test suite:

```bash
uv run --with pytest pytest tests/ -q
```
