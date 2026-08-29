# CHANGELOG

Every change landing on `main` records an entry here in the same batch
([[adr-05-after-versioning]]). Version format: `vA.B.C`.

## v1.2.0 — 2026-08-29

Add The Liturgist (`hb-ag-liturgy`) as a non-dispatchable authoring mock:
entity contract and hardcoded English/Spanish example phrases for every
live `hb-ag-*` agent. Literary voice without Area/stack glosses. Each of
the fourteen live agent files carries its own `## Liturgy`. The Liturgist
is not a fifteenth worker and is never dispatched. The root README is now
a literary inn-sign (Party as characters; The Three Feathers; `main` as
the single line).

## v1.1.0 — 2026-08-29

Add The Owl (`hb-ag-owl`) and The Crow (`hb-ag-crow`) as universally callable
web scouts, with `hb-sk-owl`, `hb-sk-crow`, and `docs/OWL-INDEX.md`.

- The Owl reads the per-requirement official documentation index and fetches
  only listed vendor URLs. Cheap `scout`. Index miss names The Crow.
- The Crow runs one kamikaze unofficial public-web pass for hard-to-find or
  precise facts, with source-trust labels. Not crime.
- Neither writes product trees or git. Neither is a Hunter familiar.

## v1.0.0 — 2026-08-29

Initial release of **harness-team-party**: the stack- and infrastructure-agnostic project harness and agent coordination framework.

- **AD&D Agent Roster** (`agents/`): Complete area owners and specialized archetypes:
  - The Hunter (`hb-ag-hunter`), The Hawk (`hb-ag-hawk`), and The Hound (`hb-ag-hound`) at The Three Feathers (Las Tres Plumas) for issue triage and scouting.
  - The Adventurer (`hb-ag-adventurer`) for bounded end-to-end task execution.
  - The Paladin (`hb-ag-paladin`) for pure Python business logic and complex script kernels.
  - The Cleric (`hb-ag-contracts`), The Dwarf (`hb-ag-service`), The Elf (`hb-ag-surface`), The Trickster (`hb-ag-test`), The Wizard (`hb-ag-ops`), The Inquisitor (`hb-ag-judge`), and The Bard (`hb-ag-git`).
- **Harness Skills** (`skills/`): Product-skill templates (`hb-sk-*`) and harness utilities (`kskill-*`, `diagram-design`).
- **Doctrine & Architecture** (`adrs/`): Core doctrine ADRs (00/01 series, 05, 07, 08, 35) and stack-agnostic templates (`adr-02`, `adr-03.*`, `adr-04.*`).
- **Documentation & Workflows** (`docs/`): PRD constitution, interface contracts (`INTERFACES.md`), onboarding fill-in playbook (`ONBOARDING.md`), clone guide (`CLONE.md`), development loop, TDD guidelines, and glossary.
- **Harness Self-Testing & Automation**: Full suite of guards in `tests/`, Cursor session hooks, and Graphify MCP integration.
