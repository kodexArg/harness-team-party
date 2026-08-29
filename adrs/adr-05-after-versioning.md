---
title: adr-05-after-versioning
type: adr
status: active
version: v0.1.0
tags: [adr, harness, docs, changelog, versioning]
description: "Governs CHANGELOG tracking on main, vA.B.C semantics, and Boy Scout documentation version stamping."
applies_when:
  - When recording a release entry in CHANGELOG.md.
  - When updating the version field on an edited harness document.
  - When deleting superseded documentation instead of leaving it in the vault.
---

# ADR-05 — after versioning

> Tracking release changes and updating documentation metadata on every commit guarantees traceability and prevents documentation drift.

1. **CHANGELOG tracking mandate.** Every change landing on `main` must record an entry in `CHANGELOG.md` in the same batch. Pushing to `main` without a corresponding changelog entry is prohibited.

2. **Version format law.** Version numbers must follow the three-tier format `vA.B.C`:
   - `A` designates the initial project release milestone and generational eras.
   - `B` designates functional milestones and architectural feature groupings. Cutting a git release tag (`vA.B.0`) is mandatory for each `vA.B` milestone.
   - `C` designates granular commit-level iterations, incremented generously on every batch without digit limits. Git tagging is optional for granular `.C` increments.

3. **Boy Scout version alignment.** Every edited or reviewed harness document must update its `version` property to match the current release version in the same batch. Untouched files preserve their stamped version.

4. **Obsolete documentation eviction.** Outdated or superseded documentation must be deleted in the same batch. Accumulating dead or inaccurate documentation in the vault is prohibited. There is no in-tree archive folder.

5. **Closed frontmatter schema mandate.** Harness documentation must carry the closed frontmatter schema: `title`, `type`, `status`, `version`, `tags`, `description`, `applies_when`, and `related_adrs`. Invented keys or missing required fields are prohibited.

6. **Body opener prohibition.** The `description` property is the sole catalogue of file contents. Document bodies must begin directly with content; introductory summaries explaining file contents are prohibited.
