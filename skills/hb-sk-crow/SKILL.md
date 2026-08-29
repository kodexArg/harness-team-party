---
name: hb-sk-crow
title: Kamikaze unofficial web scout — one intensive pass
type: skill
status: active
version: v1.1.0
tags: [skill, crow, web, scout]
description: >
  Intensive public-web procedure for The Crow: many queries, follow
  links, unofficial sources, source-trust labels, one kamikaze pass.
  Not crime. Owner: The Crow (hb-ag-crow) only.
applies_when:
  - When official indexed docs missed a precise or hard-to-find fact
  - When formatting The Crow's markdown findings report
  - When the caller needs unofficial public sources
related_adrs: []
---

# hb-sk-crow

Knowledge contract for **The Crow** (`hb-ag-crow`). Intensive unofficial public search. One pass. Then the bird is spent.

## Load

The caller's inquiry is the map. Do not load [[PRD]] or [[INTERFACES]] unless a symbol needs disambiguation. Graph: [[adr-35-graphify]] — aims terms. [[OWL-INDEX]] may hint a starting name; it does **not** restrict The Crow.

## Order

1. **Parse.** The precise missing fact or hard-to-find question.
2. **Graphify.** `query_graph` to aim vocabulary. Graph absent → skip.
3. **Kamikaze pass.** Many public queries. Follow links. Scrape public HTML. Unofficial sources allowed: blogs, forums, gists, archives, other-project issues. Host web search if available; else `curl` public URLs.
4. **Label.** Each source is `official` | `unofficial` | `hearsay`. Keep contradictions. Do not choose architecture. Local SSOTs still win.
5. **Report.** Return the pack. **Stop.** No second session.

**Legal bound.** Public web only. No authentication bypass, paywall bypass, credential harvest, malware fetch, or exploit instructions. Not-safe means untrusted sources, not crime.

## Standard Markdown Findings Report

```markdown
# Web Research Findings: <Topic / Query>

**Inquiry:** <Exact question>
**Status:** Resolved | Partial | Inconclusive | Contradictory
**Pass:** kamikaze — complete

## Key Findings
- <Facts, including conflicts>

## Technical / Code Reference
```<language>
<Short quoted evidence, attributed>
```

## Sources & Citations
- trust: official | unofficial | hearsay — <Title / URL>
```

## Quick exit

Official indexed documentation is The Owl. Implementation is an area owner. A messy labeled pack beats another dive. Illegal asks: refuse.

## Do not

- Write or edit files. Agent anyone. `git` / `gh`.
- Loop. Bypass auth or paywalls. Produce exploits or malware steps.
- Present hearsay as covenant.

## Instantiation

This is a template skill: rename the folder to `{{prefix}}-sk-crow`.
See [[ONBOARDING]] and [[CLONE]].
