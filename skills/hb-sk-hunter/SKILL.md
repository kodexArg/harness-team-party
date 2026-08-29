---
name: hb-sk-hunter
title: Issue hunt, existing-test repro, bulletin
type: skill
status: active
version: v0.1.4
tags: [skill, hunter, triage, issues, bulletin]
description: >
  Issue-hunt contract for The Hunter: pick an issue, fire Hawk and
  Hound, reproduce with existing tests, strip noise from the report,
  and pin a bulletin at The Three Feathers (Las Tres Plumas) with a
  finished problem interpretation and one specific imperative goal
  for a later Hunter. Load when hunting, triaging, reproducing, or
  posting the notice-board note — even if the skill is not named.
  Triggers: hunter, cazador, bulletin, Three Feathers, Las Tres
  Plumas, notice board, issue goal. Owner: The Hunter (hb-ag-hunter)
  only. Does not write tests or product trees.
applies_when:
  - When picking, triaging, or forensic-reading a GitHub issue
  - When writing the Hunter bulletin (problem + goal) at The Three Feathers
  - When reproducing an issue against existing tests (not writing them)
  - When deciding in-reach versus out-of-reach for an issue
related_adrs:
  - adr-08-github
---

# hb-sk-hunter

Knowledge contract for **The Hunter**. Teach the hunt, the existing-test repro, and the bulletin. Then stop. Point; do not paste the SSOTs.

## Load

1. [[ISSUE-TRIAGE]] — three axes plus a domain; that is "triaged".
2. [[GITHUB]] — The Three Feathers, labels, Requires, REST comments, `cursor-issue-triage`.
3. [[GLOSSARY]] — The Three Feathers, notice board, The Hunter.
4. Roster and party bounds: [[ADND-AGENTS]]. Hunt graph: [[ADND-DISPATCH]].
5. [[TDD]] only as a fence: The Trickster writes traps. This hunt **runs** them.

The Hunter already held [[PRD]] and [[INTERFACES]]. Familiars do not.

## Hunt

| Step | Move |
|---|---|
| Target | Prompt number wins. Else open issues, numeric ascending, first one |
| Thread | `gh issue view <n>` then `gh api repos/{owner}/{repo}/issues/<n>/comments`. Never `gh issue view --comments` |
| Requires | `## Requires` first. Any listed issue still open → `stop-blocked` |
| Scouts | Agent `hb-ag-hawk` and `hb-ag-hound` **in the same turn**. Brief: issue number, title, 3–8 clues. Role `scout`. **Do not wait** |
| Repro | **Immediately** after the scouts are fired: Graphify for existing tests matching the clues, run **one** narrow slice. Do not stall on Hawk/Hound |
| Score | One `severity:N`, one `collateral:N`, one `effort:N`, ≥1 domain — labels from [[GITHUB]] only |
| Reach | `in-reach` when the picture is complete and effort is not architectural. Else `out-of-reach` (`complex` when too large for one PR) |
| Board | Pin the bulletin on the issue at **The Three Feathers** (`cursor-issue-triage`). Receiver is a **later Hunter**. Same bytes in the reply |

Auth: `. scripts/cursor_cloud_gh_auth.sh` when Issues need the operator PAT ([[GITHUB]]).

## Repro (existing traps only)

The defect is real if an existing trap trips in a way that matches the issue. Planting a new trap is The Trickster — out of area.

Best practice, then stop:

1. Graphify the issue clues against tests (`tests/`, `{{service tree}}` tests, `{{surface tree}}` tests). Then Grep those files only.
2. Run **one** slice with the tree's own runner (`{{test runner}}` from `{{service tree}}`; `python3 tests/test_*.py` for harness files; the surface toolchain for surface tests). Clean environment. No live-credential markers. No browser smoke.
3. Prefer tests that already name the files or symbols in the issue. A full suite is `too-large`.
4. **Quick-exit is enough.** One run, then record. Do not deepen, do not write a file, do not Agent The Trickster.

| `repro.status` | When |
|---|---|
| `reproduced` | A named test failed in a way that matches the issue |
| `not-reproduced` | The slice ran green — the trap does not catch this yet |
| `no-trap` | Graphify/Grep found no matching test file |
| `too-large` | The only honest slice is the whole suite or a multi-session setup |

`not-reproduced` and `no-trap` are valid bulletins, not a reason to author tests.

## Goal (constitutive)

The Hunter's real task is not to retell the issue. It is to **apart the noise** from the reported pile and leave a finished, specific interpretation — then **ask a specific goal** in the same note.

The notice hangs at **The Three Feathers** (Las Tres Plumas): issues, PRs, and the agents that work them ([[GLOSSARY]], [[GITHUB]]). A later Hunter reads only this comment. No session context.

| Field | What it is |
|---|---|
| `problem` | The real defect, one finished reading. Observable failure, expected vs actual. Not the issue body copied. Not venting, "please fix", log walls, or a second title |
| `goal` | **One imperative sentence.** Specific enough to act. This *is* the request — do not add a second ask in prose |
| `receiver` | Always `later Hunter` |

`goal` matches a handoff `goal:`: imperative, not a dump. Bad: "investigate the login bug". Good: "Return 401 from `POST /session/` when the refresh token is expired, matching the existing handler test."

If the picture is not finished, say so in `problem` and set `verdict: stop-out-of-reach`. Do not invent a crisp goal you do not have.

## Bulletin

The inn's notice board is this payload, pinned on the issue at The Three Feathers. Same bytes in the reply. A later Hunter has no session context.

```
BULLETIN
inn: The Three Feathers
issue: #<n>
title: <one line — as filed, not the interpretation>
problem: <finished interpretation — noise stripped>
goal: <one imperative sentence>
receiver: later Hunter
reach: in-reach | out-of-reach | blocked-requires
verdict: proceed-handoff | stop-out-of-reach | stop-blocked
triage:
  severity: 1|2|3
  collateral: 1|2|3
  effort: 1|2|3
  domain: [service | surface | infra-cicd | harness]
repetition:
  status: novel | repeat | related
  evidence: [#M, ...]
  prior_attempts: <one line or none>
clues: [tag, ...]
code:
  - path: <repo-relative>
    symbol: <or —>
    lines: <a-b>
    excerpt: <short>
    clue: <which tag>
repro:
  status: reproduced | not-reproduced | no-trap | too-large
  slice: <paths or command>
  evidence: <failing test name | green | no matching tests | suite too wide>
requires: none | [#…]
```

Omit empty `code` rows. Do not paste whole files. `goal` is the request. Clues, code, and repro are how a later Hunter verifies — they are not a second goal.

## Quick exit

The repro uses the Inquisitor's shape: one slice, then enough. Remaining tests unrun is acceptable.

A page, model, pure Python rule, eligible Adventurer task, catalog row, infra *to build*, or a git commit/PR — not this hunt. Leave the bulletin if you have one; the parent may route its completed triage card. Do not Agent a builder or area owner. Do not spawn The Trickster to write the missing trap.

## Do not

- `git`, `gh pr`, merge, force-push.
- Write `{{service tree}}`, `{{surface tree}}`, tests, TDD entries, or [[INTERFACES]].
- Load `hb-sk-tdd` or `hb-sk-test-runner`.
- Agent Cleric / Dwarf / Paladin / Elf / Trickster / Adventurer / Wizard / Inquisitor / Bard.
- Invent a label. Stamp `blocked` (owner-only).
- Run the full suite first. Run live markers. Use browser smoke as the repro.
- Load Hawk/Hound skills in this agent — the familiars load them.
- Paste the issue body as `problem`. Leave `goal` empty or "investigate".
- Invent a second notice board. Hand the hunt to The Bard.

## Instantiation

This is a template skill: replace live slots if any, then rename the
folder to `{{prefix}}-sk-hunter`. See [[ONBOARDING]] and [[CLONE]].
