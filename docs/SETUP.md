# Setup

## 1. Clone

```bash
git clone git@github.com:kodexArg/harness-team-party.git
cd harness-team-party
```

## 2. Local environment

```bash
cp .env.example .env
```

Set `OPENROUTER_API_KEY` in `.env`. The file is gitignored. The name is declared in [`docs/VARIABLES.md`](docs/VARIABLES.md).

## 3. Code graph

```bash
skills/kskill-graphify/bin/ensure
```

When the editor supports project MCP, enable the server in `.mcp.json`.

## 4. Tests

```bash
uv run --with pytest pytest tests/ -q
```
