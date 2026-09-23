# ADR-08 — GitHub & Pull Request Integration

> GitHub serves as the primary collaboration platform and CI/CD automation plane, binding all production changes to pull requests.

1. **Pull Request Integration:** All changes landing on `main` enter through Pull Requests as the formal integration and review record.
2. **Automated CI/CD Validation:** Automated tests and linters execute via GitHub Actions workflows on pull requests.
3. **Deployment Trust Confinement:** Production deployments are triggered strictly from merges into `refs/heads/main`.
4. **Pragmatic Reviews:** Code reviews focus on correctness, security, architecture alignment with `docs/PRD.md`, and contract adherence with `docs/INTERFACES.md`.
