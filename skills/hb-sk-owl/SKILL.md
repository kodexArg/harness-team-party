---
name: hb-sk-owl
title: Official-docs scout — OWL-INDEX then listed URLs
type: skill
status: active
version: v1.1.0
tags: [skill, owl, documentation, scout]
description: >
  Official documentation procedure for The Owl: read OWL-INDEX,
  fetch only listed vendor URLs, return a short markdown findings
  report. Index miss names The Crow. Owner: The Owl (hb-ag-owl) only.
applies_when:
  - When looking up official vendor documentation for a project pin
  - When formatting The Owl's markdown findings report
  - When the inquiry maps to a REQUIREMENTS row
related_adrs:
  - adr-02-stack
---

# hb-sk-owl

Knowledge contract for **The Owl** (`hb-ag-owl`). Index first. Official URLs only. Light fetch. Then stop.

## Load

The caller's inquiry is the map. Do not load [[PRD]] or [[INTERFACES]] unless a symbol needs disambiguation. Pins: [[REQUIREMENTS]]. Allowed URLs: [[OWL-INDEX]]. Graph: [[adr-35-graphify]] — first tool, aims terms, is not a web index.

## Order

1. **Parse.** Extract the question, pin/package name, and version from [[REQUIREMENTS]] when the pin exists.
2. **Graphify.** `query_graph` only if local symbols must map to pin keys. Graph absent → skip.
3. **Index first.** Read `docs/OWL-INDEX.md`. Select the matching row. No row → **Index miss**: return the report with `Status: Index miss`, name The Crow, stop. Do not Agent The Crow. Do not search the open web.
4. **Light fetch.** `curl` (or the host fetch) **only** listed URLs, or paths on the same official host under that documentation root. Cap about three pages. No search engines. No forums.
5. **Report.** Distill official facts. Stop.

## Standard Markdown Findings Report

```markdown
# Web Research Findings: <Topic / Query>

**Inquiry:** <Exact question>
**Status:** Resolved | Partial | Inconclusive | Index miss

## Key Findings
- <Official behavioral facts, parameters, version bounds>

## Technical / Code Reference
```<language>
<Minimal canonical snippet from official documentation>
```

## Sources & Citations
- <Title / official URL from OWL-INDEX>
```

## Quick exit

Unofficial or hard-to-find search is The Crow. Implementation is an area owner. Empty official facts plus Index miss beats a forbidden open-web hunt.

## Do not

- Write or edit files, including [[OWL-INDEX]].
- Fetch URLs that are not on the index (except same-host paths under a listed docs root).
- Agent anyone. `git` / `gh`.
- Invent syntax absent from the fetched official page.

## Instantiation

This is a template skill: rename the folder to `{{prefix}}-sk-owl`.
See [[ONBOARDING]] and [[CLONE]]. Fill [[OWL-INDEX]] product rows with `{{official docs url}}`.
