# ADR-07 — Git & Branching Strategy

> Strict single-trunk git discipline and ephemeral working branches eliminate drift, ensure continuous deployability, and maintain clean history.

1. **Single-Trunk Invariant:** `main` is the primary integration and production branch.
2. **Ephemeral Working Branches:** All development occurs on short-lived branches (`feat/*`, `fix/*`, `chore/*`, `docs/*`, `refactor/*`) cut from `main` and deleted upon merge.
3. **Conventional Commits:** Commit messages follow conventional commit formatting: `type(scope): imperative subject`.
4. **Clean Integration:** Merge pull requests using squash or rebase to keep `main` history linear and legible.
