# CHANGELOG

Every change landing on `main` records an entry here in the same batch
([[adr-05-after-versioning]]). Version format: `vA.B.C`.

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
