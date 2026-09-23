# Testing Strategy & Guidelines

> Guidelines for automated testing, regression prevention, and software reliability.

## 1. Principles

- **Behavior & Contract Focused:** Tests verify expected outcomes and public contracts defined in [`docs/INTERFACES.md`](docs/INTERFACES.md) and [`docs/PRD.md`](docs/PRD.md).
- **Fast & Isolated:** Unit and integration tests must run deterministically and fast without relying on flaky external state.
- **Freedom of Technique:** Test-driven development (TDD), test-after, and property testing are all valid techniques. What matters is the outcome: high test confidence, good coverage of edge cases, and zero regressions.
- **No Document Bureaucracy:** Tests are authored directly in code (under `tests/` or alongside services), without requiring intermediate markdown paperwork or status-tracking notes.

## 2. Test Organization

- **Unit Tests:** Verify pure domain logic, computations, validations, and state machines in isolation.
- **Integration Tests:** Verify database queries, external integrations (using adapters or testcontainers), and contract serialization.
- **Contract / API Tests:** Validate route payloads, HTTP status codes, headers, and permission boundaries matching [`docs/INTERFACES.md`](docs/INTERFACES.md).

## 3. Running Tests

```bash
# Run test suite
uv run --with pytest pytest tests/ -q
```
