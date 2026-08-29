---
title: adr-00.a-adr-frontmatter
type: adr
status: active
version: v0.1.4
tags: [frontmatter, schema]
description: "Defines the mandatory harness-wide frontmatter contract, with a distinct closed key set for agent definitions."
applies_when:
  - When authoring YAML frontmatter for an ADR or harness document.
  - When validating YAML frontmatter schema compliance.
  - When choosing the docs/ADR key set versus the agent definition key set.
---

# ADR-00.a — ADR frontmatter

> Structured YAML frontmatter provides deterministic metadata for agent routing, automated indexing, and precise trigger matching without loading entire document bodies into context.

1. **Harness-level frontmatter doctrine.** Structured YAML frontmatter is the universal metadata contract across the entire harness, governing ADRs (`adrs/`), vault documentation (`docs/`), skills (`skills/`), and agent definitions (`agents/`).

2. **Standard closed contract.** Every ADR and vault document under `adrs/` and `docs/` declares the standardized closed key set: `title`, `type`, `status`, `version`, `tags`, `description`, and `applies_when`, plus optional relationship keys (`sub_adrs` on parent ADRs; `related_agents` on ADRs an `hb-ag-*` agent carries; `related_adrs` on docs and skills). Skills under `skills/` use that same docs key set plus `name` as the host skill identity when the skill file requires it.

2a. **Agent definition contract.** Files under `agents/` do **not** use the docs/ADR key set. Their closed keys are exactly `name`, `description`, `model`, `color`, `tools`, and `related_adrs`, as recorded in [[HARNESS]]. Host runtimes dispatch on `name`/`description`/`model`/`tools`; stamping `title`/`type`/`status`/`version`/`applies_when` onto an agent file is a defect. `related_adrs` is required and may be `[]`.

3. **Field definitions and semantics:**
   - `title`: Exact filename stem (for ADRs) or concise English phrase (for docs/skills). Not an agent-file key.
   - `type`: Document category (`adr`, `reference`, `index`, `guide`, `skill`). Not an agent-file key.
   - `status`: Fixed value `active` for current rules and live docs.
   - `version`: Version identifier (`vX.Y.Z`) tracking [[CHANGELOG]] and git release tags.
   - `tags`: Canonical array of lowercase topic identifiers.
   - `description`: High-density declarative summary of the document's assertion or scope.
   - `applies_when`: A DRY, unique list of atomic situational triggers, decision forks (`X vs Y`), precedence questions (`A over B`), and operational entry points (`When entering...`).
   - `sub_adrs`: (Optional) Array of child sub-ADR stems declared on parent ADRs.
   - `related_agents`: (Optional, ADRs only) Array of `hb-ag-*` stems that carry this ADR. Pair with `related_adrs` on those agent files.
   - `related_adrs`: Array of governing ADR stems. Required on agent files (`[]` when none). Optional on docs and skills. Not on ADRs.

4. **Centrality of description.** `description` serves as the primary declarative summary for automated indexing and agent triage. It carries critical importance: it must state the core assertion or scope in one definitive sentence so agents can evaluate relevance instantly without loading the document body.

5. **Boy-scout versioning on edit.** The `version` field tracks when that specific document was authored or last modified. A global project release or version bump does NOT restamp untouched documents: only documents that are actively edited, restructured, or reviewed in a batch have their `version` updated to the current release version in [[CHANGELOG]]. Untouched documents retain their previous version to preserve accurate revision history and prevent artificial diff churn.

6. **Reduced frontmatter for sub-documents.** Sub-ADRs and subsidiary documents allocate minimal context resources: minimal description, lean tags (1-2), strictly 1-2 situational triggers in `applies_when`, and no `sub_adrs` field. Their frontmatter footprint is especially minimized to conserve tokens.

7. **Fast triage via frontmatter.** Agents and tools inspect `description` and `applies_when` across the harness index to filter relevant rules and documents in milliseconds, loading full document bodies only for active matches.

8. **Frontmatter template.** Complete frontmatter configuration:

```yaml
---
title: adr-NN-slug
type: adr
status: active
version: v0.1.0
tags: [tag1, tag2]
description: "High-density declarative summary of the architectural assertion."
applies_when:
  - When encountering specific situational triggers or initial context entries.
  - When resolving specific decision forks (choice A vs choice B).
  - When establishing architectural precedence (rule X over implementation Y).
sub_adrs:
  - adr-NN.a-child-slug
---
```
