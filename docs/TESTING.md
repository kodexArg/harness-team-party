# Testing

Tests check behavior that is already in the tree: the code graph, the Graphify skill scripts, and the session hooks.

## Principles

- A test fails when a declared entry point or tracked graph file is missing or mis-wired.
- Tests run locally and in CI without network secrets.
- Tests live in `tests/`. No extra status notes.

## Run

```bash
uv run --with pytest pytest tests/ -q
```
