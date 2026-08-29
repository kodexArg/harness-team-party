---
title: tdd-00-template
type: tdd
status: draft
created: 2026-08-28
api: []
tags: [tdd, template]
---

# tdd-00 — template

A project copies this file to `tdd-NN-slug.md` (sequential `NN`, kebab-case slug) and fills it. The `-00-` file is never implemented and never leaves `draft`. The flow, the frontmatter contract, and the status transitions are owned by [[TDD]] — read it before starting. This template ships no concrete `tdd-NN` entries of its own — it is scaffolding for the projects built from it.

## Context

Why this piece exists: the [[INTERFACES]] row(s) it covers, the GitHub issue it
closes, what need it serves. An entry with no route lists `api: []` and says so.

## Design

The chosen shape and the reasons — placement ([[SERVICES]]), variables read
([[VARIABLES]]), and why alternatives were rejected.

## Tests (`{{service tree}}/<area>/test_<subject>.*`)

The failing tests this entry writes first, listed one by one. They run against
real routed handlers and the real database — not mocks.

## Status

`draft → red → green → done` ([[TDD]]). Record here how red became green.
