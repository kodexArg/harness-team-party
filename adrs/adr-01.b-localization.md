---
title: adr-01.b-localization
type: adr
status: active
version: v0.1.0
tags: [localization, i18n]
description: "Governs English-only codebase language, interface-language screen rendering, and regional formatting standards."
applies_when:
  - When authoring code identifiers, comments, tests, commits, or documentation in English.
  - When formatting numbers, dates, or currencies for the screen.
  - When authoring UI translation catalog entries.
related_agents:
  - hb-ag-surface
---

# ADR-01.b — localization and regional formatting

> Strict linguistic segregation preserves English as the international standard for codebase maintainability while delivering a native, culturally precise user experience in the project's interface language.

1. **Codebase language invariant.** All code identifiers, interface paths, variable names, database schemas, tests, comments, git commit messages, PR descriptions, and technical documentation are strictly English.

2. **Screen localization.** User-facing UI elements, messages, labels, and notifications render exclusively in `{{interface language}}`. Keys, message IDs, and catalog identifiers remain English (`snake_case`).

3. **Regional formatting standards.** Number, date, currency, and timezone formats for the screen are the standards of the interface language's locale; APIs and databases exchange ISO formats. The concrete locale table is recorded here at instantiation:

   - Locale: `{{interface locale}}`
   - Numbers: `{{number format}}`
   - Dates: `{{date format}}` on screen; ISO `YYYY-MM-DD` on the wire
   - Timezone: `{{timezone}}`

4. **Translation catalogs.** Screen copy resides in the surface tree's translation catalogs through the project's message helper; service-side validation messages use the domain framework's i18n mechanism. The concrete paths are recorded at instantiation.
