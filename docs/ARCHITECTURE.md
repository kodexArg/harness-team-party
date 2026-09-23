# Architecture

> Architectural overview: Service structure, Data layer, Authentication, and Infrastructure.

## 1. Service Layout & Patterns

- **Service Structure:** Top-level layout under `{{service tree}}` and/or `{{surface tree}}`.
- **Layering:** Clear separation of domain logic, persistence, and external presentation/API interfaces.
- **Contract Adherence:** All exposed endpoints and public actions must adhere to contracts defined in [`docs/INTERFACES.md`](docs/INTERFACES.md).

## 2. Data & Persistence

- **Database Engine:** `{{database}}` (e.g., PostgreSQL, SQLite, or managed service).
- **Schema & Migrations:** Framework-standard migrations versioned in code.
- **Data Lifecycle:** Clear boundaries between persistent records, ephemeral cache, and computed values.

## 3. Authentication & Authorization

- **Identity Provider:** `{{identity provider}}` (e.g., JWT, OAuth2, session-based).
- **Session Management:** Secure token or session transmission.
- **Authorization Pattern:** Declarative or middleware-based permission checks at the boundary.

## 4. Infrastructure & Runtime

- **Deployment Target:** `{{deploy target}}` on `{{cloud provider}}`.
- **Local Runtime:** Orchestrated locally via Docker Compose or equivalent runtime tooling.
- **Environment & Secrets:** Secret variables are injected via environment; names are recorded without committing secret values.
