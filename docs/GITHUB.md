# GitHub & Git Workflow

> Trunk-based integration, ephemeral branch workflows, and PR standards.

## 1. Branching Model

`main` is the single source of truth and production integration line:

| Branch | Role |
|---|---|
| **`main`** | Protected line. All features and fixes integrate here via Pull Requests. |
| **`feat/*`, `fix/*`, `chore/*`, `docs/*`, `refactor/*`** | Ephemeral branches created from `main` and deleted upon merge. |

A remote branch that is unmerged, has no pull request, and has not moved in 14 days is promoted to an issue or deleted.

Direct pushes to `main` are restricted. All changes land through pull requests.

### Reading issue comments

To fetch comments safely without GraphQL deprecations:
```bash
gh api repos/{owner}/{repo}/issues/<n>/comments
```


## 2. Commit Standards

Commits should be focused, atomic, and follow standard conventional commit formatting:

```
<type>(<scope>): <imperative subject>
```

- **Types:** `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `perf`.
- **Scopes:** area of the tree (e.g. `skills`, `docs`, `graph`, `tests`).
- **Subject:** Imperative, present tense, concise summary (e.g. `add user authentication route`).

## 3. Pull Request Workflow

1. **Branch & Implement:** Branch off latest `main`, implement changes, and ensure tests pass.
2. **Open PR:** Provide a clear description of WHAT changed and WHY.
3. **Verify:** Automated CI checks and linting must pass.
4. **Merge:** Merge to `main` using squash or rebase merge to maintain a linear history.

## 4. Issues & Labels

Issues track user stories, bugs, and technical tasks:

- `bug`: Defect or regression.
- `enhancement`: New feature or improvement.
- `chore`: Tooling, dependencies, or infrastructure updates.
- `documentation`: Documentation or specification changes.
- `question`: Needs clarification or design discussion.
