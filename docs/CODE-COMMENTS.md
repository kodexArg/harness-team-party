---
title: Comment necessity tests, length ceilings, and prohibitions
type: reference
status: active
version: v0.1.0
tags: [harness, ssot, code-style, comments]
description: "Defines the strict necessity test, brevity constraints, and prohibitions for code comments."
applies_when:
  - When deciding whether to write a code comment.
  - When applying comment length ceiling rules.
  - When deleting obsolete comments during code edits.
  - When auditing PR diffs for comment necessity.
related_adrs:
  - adr-05-after-versioning
---
# CODE-COMMENTS — whether a comment may exist, and how much it may say

Language is English, always ([[adr-01.b-localization]]) — this file governs *whether* and *how much*, never *which language*.

The failure this exists to stop: multi-paragraph comments that narrate rationale, restate ADRs, argue with alternatives, or justify a decision to a reader. They out-grow the code, drift from it silently, and become a second, unversioned SSOT — the same disease [[adr-00-adr-doctrine]] rule 1 forbids in an ADR and a live-doc block ([[CODEMAP]]) forbids by construction.

## The necessity test — apply first

> Before length, ask whether the comment may exist at all. A comment is necessary only when the code cannot carry the meaning **and** a competent reader of that code plus its linked docs would otherwise get it wrong.

The burden is on the comment. If you cannot name the specific wrong conclusion a reader
would reach without it, it is not necessary — delete it. "It might help someone" is not
necessity; neither is "it took me a while to work out" (that belongs in the PR body).

## The limits — apply second, to a comment that survived the test

| Kind | Limit | May say |
|---|---|---|
| Live-doc block | as the linker writes it | wikilinks only, never prose ([[CODEMAP]]) |
| File header | **≤ 3 lines** | what the file is, in one breath; a wikilink for the rest |
| Inline / block | **≤ 2 lines** | the non-obvious *why* of the line below it |
| Docstring on a symbol | **≤ 2 lines** per symbol | what the parameter or return *is* |

A comment over its limit is a defect, fixed by deleting it or by moving what it says
into the doc that owns the subject. Necessity is the floor and these are the ceiling: a
comment must pass both.

## What a comment must never do

1. **Restate the code.** If the line reads `if (redirect) return redirect(redirect)`,
   it needs no comment.
2. **Restate a rule.** Cite `[[adr-NN-slug]]` or the doc; never paraphrase what it
   requires. The doc wins, so a paraphrase can only ever be a stale second copy.
3. **Argue.** No "chosen because", no rejected-alternative survey, no "deliberately",
   no defense of the design against an imagined reviewer. That belongs in the PR, the
   issue, a [[TDD]] entry, or an ADR.
4. **Narrate history.** No "used to be X", no "changed in #NNN". Git owns that.
5. **Teach.** No explanation of how a framework, browser, or language feature works.

## Where the prose goes instead

Rationale is not lost, it is *relocated* — to the surface that is reviewed and
versioned as prose:

- a design decision → the ADR that rules it, or the doc that ADR points at
- a service unit's contract → its [[TDD]] entry
- the reason for one commit's shape → the commit message or the PR body ([[GITHUB]])

## The one-line test

Read the comment. If deleting it would lose nothing a reader of the code plus its
linked docs could recover, delete it. Most comments fail this test.
