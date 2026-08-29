---
title: adr-03-backend
type: adr
status: active
version: v0.1.4
tags: [adr, backend, service]
description: "Service family: domain isolation, interface catalog, framework-bound TDD, pure-Python business logic, fragments, local boot, and cache."
applies_when:
  - When placing domain modules, handlers, or pure-compute services in the service tree.
  - When declaring or retiring a service HTTP route.
  - When starting service work through TDD, fragments, local boot, or cache.
sub_adrs:
  - adr-03.a-api
  - adr-03.b-tdd
  - adr-03.c-htmx
  - adr-03.d-development
  - adr-03.e-cache
related_agents:
  - hb-ag-service
  - hb-ag-paladin
---

# ADR-03 — backend

> The service tree stays modular and contracted, with an explicit framework boundary so business rules remain portable without weakening service integration.

This family is a **template**. It is the backend/service rulebook. Instantiation fills slots from [[ONBOARDING]], rewrites named technologies to match [[adr-02-stack]], and **deletes any sub this project does not use** (no HTML fragments → drop `adr-03.c`; a different cache story → rewrite `adr-03.e`). Keep the parent. Facts live in [[SERVICES]], [[INTERFACES]], [[TDD]], [[INFRASTRUCTURE]], [[VARIABLES]].

1. **Architecture authority.** Service layout, layering, and the pure-compute boundary are governed by [[SERVICES]] under `{{service tree}}`.

2. **Modular domains.** The service is one project with isolated domains named per [[GLOSSARY]]. Generic utility accretion is not the architecture.

3. **Sub-ADR index** (rewrite or delete each to match this project):
   - [[adr-03.a-api]] — [[INTERFACES]] is the route catalog; row before tests and code.
   - [[adr-03.b-tdd]] — framework-bound service code is born in `docs/tdds/`; framework-neutral Python logic follows the Paladin's test-after path ([[TDD]], [[DEVELOPMENT-LOOP]]).
   - [[adr-03.c-htmx]] — HTML-fragment / hypermedia producer, if any.
   - [[adr-03.d-development]] — local boot of the service via `{{local runtime}}`.
   - [[adr-03.e-cache]] — cache policy; name what you use and what you refuse.

4. **Environment.** Service settings are declared in [[VARIABLES]] first. Secret **values** live in the secret store ([[adr-02-stack]]).

5. **Python business-logic boundary.** Framework-neutral Python business rules and complex script cores belong to The Paladin (`hb-ag-paladin`). Framework adapters, persistence, models, migrations, handlers, permissions, and routes remain The Dwarf's service work. The Paladin implements the pure core first; The Trickster writes its tests afterward.
