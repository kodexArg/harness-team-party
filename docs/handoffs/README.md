---
title: handoffs
type: reference
status: active
created: 2026-08-28
tags: [handoff, harness]
---

# docs/handoffs/

This folder holds session-to-session handoff documents: a note one agent session
writes for the session (or tier) that picks the work up next.

## Provenance

The format originates from machine-global handoff skills, which
[[HARNESS]] deliberately does not vendor: global convenience skills are available when
present but are **not required** for this project to build, test, and
deploy — so they are not vendored. This README is the in-repo owner of the
format, so a fresh clone can read and author entries with no dependency on
any global skill.

## File naming

`YYYY-MM-DD-kebab-slug.md`, English throughout
([[adr-01-nomenclature]]).

## Frontmatter contract

| Field | Meaning |
|---|---|
| `title` | One-line description of the handoff's subject. |
| `type: handoff` | Fixed value; marks the note as this schema. |
| `created` | ISO date the handoff was written. |
| `direction` | `lateral` \| `upscale` \| `downscale` — how the receiving tier relates to the writer. |
| `from_tier` / `to_tier` | Harness model roles on each end (`thinker`, `builder`, `scout`). |
| `status` | `open` \| `closed`. |
| `goal` | One sentence: what the receiver is meant to accomplish. |
| `receiver` | Who picks the handoff up (e.g. "next session on <project>"). |
| `return_to` | Wikilink back to the handoff itself, for citing it from elsewhere. |
| `scope` | What the receiver may and may not touch. |
| `context` | List of wikilinks the receiver must read before starting. |
| `tags` | Includes `handoff` and `handoff/<direction>`. |

## Body sections, in order

1. **Goal** — the objective, in full.
2. **State** — where the repo/branches/PRs stood when this was written.
3. **Done** — what was completed and verified.
4. **In-progress** — what was started but not finished or applied.
5. **Decisions (+why)** — choices made, each with its reasoning.
6. **Traps** — mistakes the receiver must not repeat.
7. **Next step** — the single unblocked action to take first.
8. **File map** — the files and paths the receiver will touch or consult.
9. **Open questions** — unresolved points, not raised or not settled.

## Authoring

An entry is a plain vault note; writing one needs no tool. Where a global
handoff skill is present on a machine it may generate one, but it is
never a dependency ([[HARNESS]]).

Author a new `YYYY-MM-DD-kebab-slug.md` note with the frontmatter and body
sections above when a session needs a cold-start for the next one. Completed
handoffs are deleted once their goal is on `main` — they are not permanent
vault content.
