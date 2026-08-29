---
title: Product requirements
type: reference
status: active
version: v0.1.1
tags: [prd, product]
description: "Defines the product, its users, purpose, core stories, and acceptance criteria. Ships as a fill-in template: instantiation replaces every placeholder."
applies_when:
  - When deciding whether work serves the product.
  - When evaluating product acceptance.
related_adrs:
  - adr-00-adr-doctrine
---
# PRD — {{project name}}

This is the product constitution template. Every double-curly slot is filled at
instantiation ([[ONBOARDING]], [[CLONE]]); the section skeleton below is the
shape every project's constitution keeps. Until it is filled, the harness
treats this file as undecided product ground: agents read it first and find the
questions, not the answers.

## What are we building

{{product paragraph}}

A {{product kind}} that:

1. {{core capability 1}}
2. {{core capability 2}}
3. {{core capability 3}}
4. Carries a concise, living project harness so every change retains product context.

## Who it's for

- {{user role 1}} who need {{need 1}}.
- {{user role 2}} who need {{need 2}}.
- {{user role 3}} who {{need 3}}.

## What purpose it will have

{{purpose paragraph}}

## User stories

```gherkin
Scenario: {{primary read story}}
  Given {{precondition}}
  When {{user action}}
  Then {{observable outcome}}

Scenario: {{primary exception story}}
  Given {{a condition that needs attention}}
  When {{the product evaluates it}}
  Then {{the responsible user sees an actionable result}}

Scenario: {{primary action story}}
  Given {{an authorized user identifies a required action}}
  When {{they perform it in the product}}
  Then {{the action is validated, recorded, and attributable}}
```

## Acceptance criteria

- {{observable acceptance criterion 1}}
- {{observable acceptance criterion 2}}
- {{observable acceptance criterion 3}}
- The interface is fast, clear, and usable in {{interface language}}.
- The living harness remains concise and preserves product intent across changes.
