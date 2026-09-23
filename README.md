# harness-team-party

Skills, the code graph, and the tests for this repository. Version **v0.1.0**.

## What is here

- **`skills/`** — `kskill-graphify`, `kskill-mood`, `kskill-qw`, and `diagram-design`.
- **`docs/`** and **`adrs/`** — product intent, interfaces, and the decisions the code follows.
- **`tests/`** — checks that the graph, the skills, and the session hooks stay wired.
- **`mcp/`** — Graphify MCP declaration.

## Quickstart

```bash
cp .env.example .env   # set OPENROUTER_API_KEY locally; .env stays gitignored
skills/kskill-graphify/bin/ensure
uv run --with pytest pytest tests/ -q
```

Setup detail is in [`docs/SETUP.md`](docs/SETUP.md).

## License

MIT
