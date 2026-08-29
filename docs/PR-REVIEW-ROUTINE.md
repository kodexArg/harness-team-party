---
title: Four-agent advisory review pass and PR verdict labels
type: reference
status: active
version: v0.1.0
tags: [harness, pr, review, agents, labels]
description: "Details the unattended four-agent PR review routine, label semantics, and non-blocking advice."
applies_when:
  - When dispatching automated PR review agent passes.
  - When interpreting PR review verdict labels.
related_adrs:
  - adr-05-after-versioning
  - adr-08-github
---
# PR-REVIEW-ROUTINE — the four-agent review pass

On a schedule, an unattended cloud session reads every open pull request in this repository and leaves
four marks on it: one advisory label from each of four independent reviewers. This file states,
directly, the rules that pass must obey; the labels themselves belong
to the fixed set in [[GITHUB]].

The routine is a **reader that leaves marks**. It does not merge, does not push `main`, does not
open or close issues, and does not touch cloud infrastructure. One of its four agents may commit, and only comment
removals, and only to the branch of the PR it is reviewing.

## Why four agents and not one

A single reviewer asked to judge product alignment, rule compliance, interface declaration and code
cleanliness in one pass produces one blended opinion, and a blended opinion hides its weakest part.
Four dispatches against the same diff, none of them seeing the others' findings, produce four
readings that can disagree — and a disagreement is information. A PR that comes back
`prd-approved` + `adr-fail` is saying something precise: the change serves the goal and breaks a
rule, which is exactly the case that most needs a human. That signal does not survive being folded
into a single verdict, which is why the four stay separate labels, never folded into one.

## The four

| Agent | Reads | Asks |
|---|---|---|
| `kbot-prd` | [[PRD]] | does the change serve the objective, and does it stay inside the railguard? |
| `kbot-adr` | `adrs/` | does it comply with every active ADR? |
| `kbot-api` | [[INTERFACES]] | does it touch the route surface, and is every route declared? |
| `kbot-cleancode` | the diff | comment necessity ([[CODE-COMMENTS]]), duplication, naming |

The first three are the guardians. Being dispatched by this routine does not
change what they are, but it does change what their answer *counts as* — see "A label is not a
guardian verdict" below. The fourth is a worker, not a guardian: it owns no SSOT and gates nothing
([[GLOSSARY]]: guardian).

## The pass, step by step

1. **Orient.** Read `AGENTS.md`, [[PRD]] and [[INTERFACES]] — the two standing in-memory documents — then
   the label section of [[GITHUB]].
2. **Pick the work.** List open PRs. A PR needs a pass when it carries no verdict label at all, or
   when its head has moved since the last pass. Drafts are skipped.
3. **Review.** Check out the head, diff against `main`, and dispatch all four agents in one message
   so they run concurrently. Each gets the PR number, the diff, and the title and body.
4. **Map and stamp.** Translate each verdict to its label, remove that agent's previous label, apply
   the new one.
5. **Record.** One comment per pass, headed `## Review routine`, with a one-sentence reason per
   verdict and the line `Reviewed-SHA: <head sha>`.

That last line is the whole memory of the system. The routine holds no state between fires; it
learns whether a PR has already been judged, and at which commit, by reading its own last comment.
A pass whose `Reviewed-SHA` matches the current head is skipped, so a quiet PR is not re-reviewed
on every fire, and a PR that gets a new commit is re-reviewed on the next fire.

## What the tags mean

Twelve labels, three per agent. The table lives in [[GITHUB]]; this is what each state is *saying*.

**`-approved`** — that reviewer found nothing. For `kbot-api` this includes the common case of a
diff that touches no interface at all; silence about the route surface and approval of it are the
same label, deliberately, because a PR that changes no route has nothing for that guardian to
object to.

**`-observed`** — findings stand, but none of them is a breach. This is the most useful of the
three and the easiest to under-read. It means a human should look, not that anything is wrong.

**`-fail`** — a breach: outside the railguard, against an active rule, or an undeclared route. It
is a **report**, and it stops nothing. See below.

**`clean-applied`** — `kbot-cleancode`'s third state is not a failure, because that agent acts
instead of objecting. It means comment removals were committed to the PR's branch, in a commit
whose subject carries the literal token `[CLEANCODE]`. Its `clean-observed` means the opposite kind
of thing from the other three agents': findings exist that were **not safe to apply automatically**
— duplication or a misleading name — and were reported as text instead.

## A `-fail` does not block anything

This is the property most likely to be misread, so it is stated plainly: **no verdict label has
gate force**. An owner's merge order is not delayed by the `main` ruleset checks or by
`pr-merge-gate` ([[GITHUB]], [[adr-08-github]] rule 8), and a label is neither. A PR carrying
`adr-fail` can be merged by the owner at any moment, with no override and no ceremony.

That is a deliberate choice rather than an unfinished one. An advisory channel that quietly acquires
authority is worse than no channel at all, because people stop re-reading what they believe is
already enforced. If a verdict should one day block, that is a change to
`scripts/check_merge_gate.py` and a deliberate rewrite of this file's own rule — never a
quiet re-interpretation of what the label already meant.

## A label is not a guardian verdict

`pr-merge-gate` passes on the presence of a `Guardian-Verdict:` line in the PR body ([[GITHUB]]). The
routine is forbidden from writing that line, or any PR body, and the reason is worth stating
without euphemism: **an unattended process that can write its own gate token can unblock its own
merges.** On every fire, forever, with no human in the loop. The bar stated above — the routine may never write that line or any PR body — is the
containment that keeps the advisory channel advisory.

So the two marks say different things, and the difference is who made the claim:

- `prd-approved` (label, by the routine) — *this agent ran and found nothing.*
- `Guardian-Verdict: kbot-prd: ok` (line, by the owner process) — *the owner dispatched this
  guardian for this change and recorded its answer*, which is what a PR-time guardian dispatch
  requires and what the merge gate is checking for.

The routine can produce the first. Only the owner process can produce the second.

## When an agent fails, it says why

Failing has two shapes and both stop at the first cause. An agent that finds a breach stops looking
the moment it can prove one: it returns its `-fail` tag and a cause — what was breached, where, and
why — instead of a sweep of every other thing it might have found. An agent that cannot judge at all
returns `blocked` with a cause that starts `QUICK EXIT:`.

The routine carries the cause through. Beneath each verdict line in the `## Review routine` comment,
a failing or blocked reviewer gets its cause quoted verbatim, and a run marked `quick_exit: true` is
labelled as such — so a reader knows the reading stopped at the first cause and the diff may hold
more. A `-fail` with no cause is an incomplete record, not a terse one.

A `blocked` reviewer gets **no label**, and the comment names it as missing next to its cause.
Silence is never mapped to a pass. The cost of this is that a PR can carry three labels instead of
four; the cost of the alternative is a fabricated record, which is worse and is forbidden outright.

## What it may never do

Merge, approve, request changes, close a PR. Push to `main` or to any branch that is not the
reviewed PR's own. Edit a PR body or title. Write `Guardian-Verdict:` or `Plan-Verdict:`. Create,
rename or delete a label. Open or close an issue. Touch cloud infrastructure, secrets or `.env`. Run a smoke test —
prohibited outside an interactive session by the owner directive in `AGENTS.md`. Act on a `-fail`:
it reports what the agents found; it does not fix it.

## This is not an issue runner

An unattended issue-runner job is a different machine and the two are easy to confuse. A runner takes one
**issue**, may open a PR, and must publish its outcome.
This routine takes every open **pull request**, opens nothing, and publishes a label. Neither one's
bounds transfer to the other.

## Where it runs

A scheduled cloud routine, on its own checkout with its own credential — not on the owner's
machine and not with the owner's local `gh` login. Registration and schedule are held by the routine
service, not by this repository; nothing in the tree starts it. Its four agents are ordinary definitions under `agents/`
([[HARNESS]]), so a change to any of them changes the routine's behavior on its next fire with no
redeploy.
