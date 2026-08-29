# harness-team-party

A stack- and infrastructure-agnostic **project harness template**: the
documentation system, agent roster, skills, hooks, ADRs, and delivery
discipline a serious project needs — with zero product content and zero stack
assumptions. A project built from it can be a Kotlin service, a flat site, a
CLI, anything.

harness-team-party is the successor of `harness-base` (and earlier `harness-default`), born from
`alvs-financial-gateway`'s evolution: that product's harness was generalized,
every product and stack string became a `{{placeholder}}`, and every
stack-specific skill became an instantiation template.

What ships inside:

- **Agent roster** (`agents/`) — seven area owners with ownership boundaries,
  a dispatch graph, and a definition contract: contracts, service, surface
  (optional), ops, test, judge, git.
- **Skills** (`skills/`) — eleven product-skill templates (`hb-sk-*`) plus
  reusable harness skills (`kskill-*`): graph exploration, session stance,
  quick wins, reporting, diagrams.
- **ADRs** (`adrs/`) — the doctrine set: ADR rules, nomenclature,
  localization, versioning, git, GitHub, graph exploration — plus
  `adr-02-stack`, the placeholder decision every project makes once.
- **Docs** (`docs/`) — the PRD constitution template, the harness inventory,
  the development loop, GitHub delivery contract, TDD manual, glossary, and
  placeholder SSOTs that say what they must contain.
- **Harness self-tests** (`tests/`) — the guards that keep the harness honest.

## Quick start

**[docs/ONBOARDING.md](docs/ONBOARDING.md)** — incoming-agent fill-in map:
every live slot, which file, what to load. Install Graphify if you can.
**[docs/CLONE.md](docs/CLONE.md)** — operator steps: copy the tree, prefix
rename, stack decision, trees, first commit.

The runtime index for agents (after slots are filled, and while filling
them) is [AGENTS.md](AGENTS.md). Do not confuse that index with the fill-in
map.

## Git

| Branch | Role |
|--------|------|
| `main` | **The single line** — default PR target *and* production. Every push to it ships. |

Every change enters through an issue and reaches `main` only through a PR
([docs/DEVELOPMENT-LOOP.md](docs/DEVELOPMENT-LOOP.md) §0.5). Labels, tags,
detail: [docs/GITHUB.md](docs/GITHUB.md) · [adr-08](adrs/adr-08-github.md).

Documentation lives in [`docs/`](docs/) — wikilinked, one source of truth per
topic, read with grep and Read like every other file. ADRs load as agent rules
from [`adrs/`](adrs/). MIT licensed.
