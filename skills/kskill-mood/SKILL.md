---
name: kskill-mood
description: >
  Slash /kdx-mood. Session stance skill: chat, explore/scout,
  quick-win (/qw), afk, cannabis, directive, or normal. A mood
  changes how you work, never what the work is. Triggers:
  /kdx-mood, mood, quick win, qw, scout, afk, stance.
  Ruled by this procedure over [[HARNESS]]. Not a guardian.
---

# kskill-mood

A mood is a **stance**, not a task. It changes how you work, never what
the work is. Slash `/kdx-mood`. The `/qw` shortcut is `kskill-qw` — same
quick-win stance, no parser.

Everything below is a **standing instruction**. Once a mood is set it
governs every following turn for the rest of the session. The mood ends
only when kodex sets a different one, invokes `normal`, or the session
ends. Moods do not survive a new session.

## Parsing

```
/kdx-mood [mood] [mood ...] [task]
```

The invocation is: `$ARGUMENTS`

Read leading tokens left to right. Every token matching a mood name or
alias is a mood. The **first token that is not a mood ends the mood
list** — that token and everything after it is the task, executed under
the moods just set.

```
/kdx-mood                                   -> refuse, list moods, stop
/kdx-mood chat                              -> set chat, wait
/kdx-mood chat scout where are node_modules -> set chat+explore, then answer
/kdx-mood normal                            -> clear everything
/kdx-mood quick win <task>                  -> set quick-win, then the task
```

Matching is case-insensitive. Multi-word aliases (`quick win`) count as
one token.

## Bare invocation — do nothing

With no arguments: **do not act, do not guess, do not continue whatever
was being discussed.** State that a mood is required, list the moods one
per line with a half-line each, stop. No preamble, no closing line.

## The moods

| Mood | Aliases | Where the stance lives |
|---|---|---|
| `chat` | — | `references/chat.md` |
| `explore` | `scout`, `exploration` | `references/explore.md` |
| `quick-win` | `quickwin`, `quick win`, `qw` | `references/quick-win.md` |
| `afk` | `away` | `references/afk.md` |
| `cannabis` | `weed`, `high`, `fumado` | the `kdx-cannabis` skill when present |
| `directive` | — | the `kdx-directive` skill when present |
| `normal` | `reset`, `off`, `default` | nothing — see below |

**Read only the references for the moods actually named.** Do not preload
the rest. `cannabis` and `directive` are extra entrypoints, not this
skill's body. `normal` drops every active mood. If `normal` appears
anywhere in the list it wins and every other named mood is ignored —
say so in one line.

## Combining

Moods stack unless they contradict.

- `chat` + `explore` — short high-altitude answers, evidence from scouts.
- `cannabis` + anything — reshapes output format only.
- `afk` + `quick-win` / `directive` — autonomy plus speed or assertiveness.

Contradictions: `directive` outranks `quick-win`. `chat` + `directive`
keeps directive's assertiveness with chat's brevity.

An unrecognized token is never silently dropped. Name it, apply the
moods you did recognize, continue.

## Confirming

Confirm in **one short line** — the moods now active, nothing else. Then
execute the task if one was given; otherwise stop and wait.

Do not re-announce the mood on later turns. It is set; act it.

## Standing rules are not overridden

Moods change register, verbosity, autonomy, and delegation. They never
override the [[AGENTS]] / CLAUDE.md security posture, scope control, the
ABC gate, or the requirement to confirm destructive and irreversible
actions.

## Do not

- Invent a mood that is not in the table.
- Vendor `cannabis` / `directive` here.
- Rewrite `kskill-qw` as a second mood parser.
- Restate ADR rules as facts.
