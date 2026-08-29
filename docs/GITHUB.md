---
title: GitHub repository conventions, branching, and issue workflows
type: reference
status: active
version: v0.1.3
tags: [harness, github, git, workflow, pr]
description: "Establishes single-line main integration, branch naming, PR conventions, and GitHub CLI usage."
applies_when:
  - When creating git branches for issue development.
  - When authoring or merging pull requests to main.
  - When executing GitHub commands using the gh CLI.
  - When tagging issues and milestones.
related_adrs:
  - adr-07-git
  - adr-08-github
---
# GITHUB — GitHub + git for this project

> Owner `{{owner}}`, SSH protocol, `gh` CLI. `main` is the single line — integration and production both. Force: [[adr-07-git]], [[adr-08-github]].

Owner: **`{{owner}}`**. Repo: **`{{repo}}`**. Repo protocol: SSH. CLI: `gh` (used directly). Force: [[adr-07-git]], [[adr-08-github]]. Issue scoring vocabulary: [[ISSUE-TRIAGE]].

## Branches

> `main` is the single line. Integration and production both — a merged PR is shipped. No second branch exists between a merge and production.

| Branch | Role |
|---|---|
| **`main`** | The single line. Integration *and* production: every PR merges here, and every push here ships. |
| **`feat/*`, `fix/*`, `refactor/*`, `docs/*`** | Human / workflow ephemeral branches cut from `main`, deleted upon merge. |
| **`cursor/*`, `claude/*`, `agy/*`, `grok/*`, `kbot/*`, `kwf/*`** | Agent / IDE-generated ephemeral branches cut from `main`, subject to the same lifecycle and retention rule. |

**`main` is live.** There is no second branch between a merge and production — a merged PR is shipped. No `prod` branch exists, and recreating one is prohibited ([[adr-07-git]] rule 2). Forbidden branch name for default: `master` ([[GLOSSARY]]).

An *environment* named `prod` is a different thing from a `prod` *branch*: environment names, secret paths, and resource tags stand on their own and are untouched by the branch rule.

### Branch retention — 14 days, then promoted or deleted

**A remote branch that is unmerged, has no pull request, and has not moved in 14 days is either promoted to an issue or deleted. There is no third state.** All ephemeral branches—whether human (`feat/*`, `fix/*`) or agent-spawned (`cursor/*`, `claude/*`, `agy/*`, `grok/*`)—share this constraint.

Left unstated, the default is dead branches that read as pending work that does not exist, while genuine defects sit unnoticed on branches nobody lists.

| | |
|---|---|
| **Window** | 14 days without a PR, measured from the branch's last commit |
| **Promote** | the branch holds work worth keeping → open the issue, open the PR ([[DEVELOPMENT-LOOP]]) |
| **Delete** | `git push origin --delete <branch>` |
| **Report** | `python3 scripts/check_branch_retention.py` — lists what is past the window and prints the deletion commands |
| **See it earlier** | `python3 scripts/check_branch_retention.py` |

Two exemptions, both deliberate and both needing a stated reason: a branch **held for a recorded decision** (its PR closed by owner decision, the reason on record) and a branch whose PR is open, which is by definition not unclaimed.

`check_branch_retention.py` prints the deletion command and stops — it never deletes. Deleting somebody's unreviewed work is an operator decision. The script is also not a CI gate — a branch aging out is not a reason to fail an unrelated pull request.

## Who may push

> Direct push to `main` is `{{owner}}` only. Everyone else uses branches + PRs.

- **Direct push to `main`:** account **`{{owner}}` only**.
- Everyone else (agents, collaborators): **branches + PRs**. No direct push to protected lines.

`{{owner}}` is the git identity, not the roster. The people of record behind this project — who they are and what each owns — are listed in [[CLAUDE-TEAM]]; commits and PRs reach GitHub through the single `{{owner}}` account regardless of which of them the work belongs to.

## Cursor Cloud `gh` credential

> Cursor injects a `ghs_` App token that can clone and push but cannot read Issues or bypass the `main` ruleset. The operator PAT lives as a Cursor secret; source `scripts/cursor_cloud_gh_auth.sh` at session start.

Cursor Cloud always injects a GitHub App installation token (`ghs_…`) at VM boot. That token is enough to clone and push a branch. It is **not** enough to list, read, or create Issues — `gh issue create` / `gh api …/issues` return `403 Resource not accessible by integration`.

A dashboard secret named `GH_TOKEN` collides with that injection. This repo's operator PAT lives as Cursor secret **`GITHUB_PAT`**, optionally mirrored under a repo-named secret (`GH_PROJECT_PAT` by default — renamed to match this repo at instantiation, [[CLONE]]). Fine-grained scopes that actually merge and mutate the `main` ruleset: Issues read/write, Pull requests write, Contents **write**, Administration **write**. Contents-read-only cannot merge a PR (`contents=write`). Administration-read-only cannot PUT a ruleset (`administration=write`). Agents source `scripts/cursor_cloud_gh_auth.sh` at session start: a `GITHUB_PAT` or the repo-named variable that looks like `ghp_` / `github_pat_` is exported as `GH_TOKEN`; an injected `ghs_` `GH_TOKEN` is unset so `gh` can fall back to `~/.config/gh/hosts.yml` for git. The App token **cannot** bypass the ruleset (`current_user_can_bypass: never`). The owner with admin bypass can (`always`). The variable's row lives in [[VARIABLES]] under *Harness (local tooling)*, because that file is the only source of environment variables. The **value** lives in the Cursor dashboard and nowhere else.

## How we work

> Issues track work — open early, close with PR. PRs are required for every change landing on `main`. Agents open branches and PRs; they do not force-push `main`.

1. **Issues** for collaboration, planning, and tracking. Issues can be of any type (bug, feature, task, exploration, tech debt, question) without rigid form restrictions, and are not a mandatory blocker for opening a PR.
2. **PRs** for every change that lands on `main`. Because `main` is live, merging a PR ships it — the PR is the integration record, not a staging area. An owner merge order is not delayed for CI ([[adr-08-github]] rule 8).
3. Agents open branches / PRs; they do not force-push `main` as another identity.
4. Base of every PR: **`main`**. There is no promote PR and no release head.
5. **Scoped commit formatting:** Commits follow `type(scope): concise imperative subject [trailer]` per [[adr-07-git]]. Mandatory scopes: `harness` (skills, hooks, agents, MCP, automation), `adrs` (ADR updates), `service` / `<domain>` (the service tree), `surface` / `<surface>` (the surface tree), and `infra` (cloud, local runtime). Subject in English imperative present tense.

### The Three Feathers (Las Tres Plumas)

**The Three Feathers** is the inn: this repo's issues, pull requests, and the agents that work them ([[GLOSSARY]]). It is an arbitrary grouping for those harness elements, not a second GitHub.

The notice board is an issue comment. The Hunter (`hb-ag-hunter`) pins a **bulletin** there (`cursor-issue-triage`): noise stripped, a finished interpretation of the real problem, and one specific imperative `goal` for a **later Hunter**. Shape: `hb-sk-hunter`. Do not invent a second board.

### PR Merge Authorization Model

Merge authority into `origin/main` follows a deterministic 3-tier rule ([[adr-08-github]] rule 3):

| PR Source | Condition | Merge Authority |
|---|---|---|
| **Triaged Issue PR** | Linked issue is triaged per [[ISSUE-TRIAGE]] (one score on each axis plus a domain) | **Autonomous agent merge** to `origin/main` upon passing validation and diff checks. |
| **Untriaged Issue PR** | Linked issue is not triaged | **Supervised merge:** Waits for operator review and approval before landing. |
| **Orphan PR (No Issue)** | PR opened directly without a parent issue | **Supervised merge:** Explicit operator directive ("merge", "push", "ship") is required and sufficient to land on `main`. |

### Reading issue comments

`gh issue view <n>` (body only) is fine. `gh issue view <n> --comments` is not the way this repo reads a thread.

That flag still selects GraphQL `repository.issue.projectCards`. GitHub sunset Projects (classic); hosts shipping `gh` older than **2.80.0** fail on **every** issue with that deprecation as a hard error — the failure looks like "no comments", which is how triage loses a re-dispatch. Floor that dropped the field: 2.80.0. Pin: [[REQUIREMENTS]].

Agents fetch the body and the thread as two calls, the second over REST so a host shipping an older `gh` cannot quietly fail:

```
gh issue view <n>
gh api repos/{owner}/{repo}/issues/<n>/comments
```

`{owner}/{repo}` are `gh api` placeholders and resolve from the current repo. A comment written after the body is the later word; where they disagree, the comment wins.

### Requires (issue-on-issue dependency)

**Requires** is the only sanctioned way to say "this issue cannot start until that one is done."

| Rule | Detail |
|---|---|
| **Where** | Issue body section `## Requires` (template-enforced). Not a label. Not an ADR. |
| **Shape** | Bullet list of issue numbers (`- #314`), or the single line `- none`. |
| **Semantics** | Every listed issue must be **CLOSED** before this issue may be planned for build. |
| **Agent duty** | Read `## Requires` first. If any target is still open → stop, comment which numbers remain, do **not** invent workarounds. |
| **Not for** | Owner decisions, missing secrets, CI red, "needs more design" with no predecessor issue — those are comments (and optionally `blocked`, see labels). |

Dependency, not paralysis: prefer a precise `#N` over a blanket `blocked` label. An issue with `- none` is free to start.

### Feature template structure

For complex user-facing features, `.github/ISSUE_TEMPLATE/gh-issue-feature.md` provides a structured guide (Story, Scenario(s), Acceptance checklist, Requires, References) to clarify requirements and edge cases.

## Constraints

> Standing git/GitHub constraints recorded as they are applied. The rules live in [[adr-07-git]] and [[adr-08-github]]; this table is the applied register — what actually enforces each one, and how far that enforcement reaches.

| | Constraint | Authority | Enforced by |
|---|---|---|---|
| **1** | **`main` is the only deploy-bound ref, and no `prod` branch exists** | [[adr-07-git]], [[adr-08-github]] | Harness: `scripts/check_branch_model.py` (+ `tests/test_check_branch_model.py`). GitHub: the `main` ruleset (below). |
| **2** | **Only `{{owner}}` pushes to `main` directly** | [[adr-08-github]] rule 2 | GitHub: the `main` ruleset (`{{owner}}` bypass). |
| **3** | **No branch or tag deletes on `main`** | [[adr-08-github]] | GitHub: the `main` ruleset (`deletion: true`). |
| **4** | **Release tags `v*` are mandatory for `vA.B` milestones and cut from `main` only** | [[adr-07-git]] rule 5, [[adr-05-after-versioning]] | Operator cadence. Granular `.C` iterations are optional. |
| **5** | **Deploy trust is `refs/heads/main` only** | [[adr-08-github]] rule 5 | The deploy credential's trust policy ([[INFRASTRUCTURE]]). |
| **6** | **No branch outlives the 14-day retention window unclaimed** | Stated in this table (no governing ADR) | Harness: `scripts/check_branch_retention.py` (+ `tests/test_check_branch_retention.py`), run by an operator. Nothing on GitHub enforces it. |

`check_branch_model.py` asserts; it does not prevent. What actually prevents a bad ref from reaching production is the `main` ruleset plus the deploy pipeline's own checks — not this script. Stating that limit is deliberate, not a formality.

### The `main` ruleset (GitHub repository ruleset)

Ruleset name: **`main-protection`** (target: default branch `refs/heads/main`, enforcement: `active`).

- `deletion: true` — nobody can delete `main`.
- `non_fast_forward: true` — nobody can force-push to `main`.
- `pull_request` — all changes must enter through a PR.

| Rule | Effect |
|---|---|
| `pull_request` | A PR is required to merge. Zero approvals required — self-merge stays valid. |
| `non_fast_forward` | Force-push to `main` is blocked. |
| `deletion` | `main` cannot be deleted. |
| `required_status_checks` | **Not doctrine.** Required status checks do not delay an owner merge. `scripts/apply_main_ruleset.py` PUTs the payload without them (`scripts/main_is_live_ruleset.json`). |

**Bypass: the repository `admin` role**, `bypass_mode: always`. The owner `current_user_can_bypass: always`. A GitHub App installation token `never`. An owner *merge* / *push* / *ship* uses the operator PAT and `gh pr merge --admin` if GitHub would still wait on checks or an out-of-date base. Never report "pending CI" or "I did not use `--admin`" as the end of the order ([[adr-08-github]] rule 8).

Ruleset PUT needs `Administration: write`. A `403` names the token's scopes, not "agent tokens as a class".

### Measuring how changes arrive on `main`

The question here is how a change *arrives* on `main`, not how many commits
it carries. Count first-parent commits, therefore, never `git log --format=%an`: the second counts
every commit inside a merged branch, so one PR of eight commits reads as eight bypasses. A merge
commit and a squash subject ending in `(#NNN)` are both arrivals by PR.

```bash
git log --first-parent --format=%s <since>..main | grep -vcE '\(#[0-9]+\)$'   # direct arrivals
```

## Labels (issues + PRs) — fixed set

> Create only these labels; do not invent free-form ones. Scoring vocabulary: [[ISSUE-TRIAGE]].

| Label | Use |
|---|---|
| `bug` | Defect |
| `feat` | New capability |
| `chore` | Tooling, deps, noise cleanup |
| `docs` | Documentation / harness docs |
| `harness` | Skills, hooks, ADRs, agent config |
| `infra` | Cloud, CI, deploy |
| `blocked` | **Owner decision only** — never "waiting on issue #N" (use **Requires**) |
| `complex` | **Triage only** — an automated pass judged this issue too large or too undecided to build in one PR. Never a verdict on the issue's merit, and never a reason not to do the work by hand. |

### Domain and triage labels

Stamped by hand or by an issue-triage pass; they answer *where* and *how big*, never *what kind*. Axis meanings: [[ISSUE-TRIAGE]].

| Label | Use |
|---|---|
| `service` | Service-tree surface |
| `surface` | Surface-tree surface |
| `infra-cicd` | Cloud, CI or deploy plumbing |
| `enhancement` | New capability or improvement |
| `performance` | Latency, payload or resource cost |
| `security` | Authorization, secrets or exposure |
| `tech-debt` | Cleanup or refactor debt |
| `needs-design` | Cannot start: the shape is undecided |
| `needs-repro` | Cannot start: the defect is not reproducible as filed |
| `cursor-issue-triage` | Carries an automated triage comment |
| `invalid` | Not actionable as filed |
| `📜 adr` | Governed by one or more ADRs |
| `adr-00` | Governed by `adr-00` — a label dies with the ADR it names |
| `adr-01` | Governed by `adr-01` — a label dies with the ADR it names |
| `adr-02` | Governed by `adr-02` — a label dies with the ADR it names |
| `adr-03` | Governed by `adr-03` — a label dies with the ADR it names |
| `adr-04` | Governed by `adr-04` — a label dies with the ADR it names |
| `adr-05` | Governed by `adr-05` — a label dies with the ADR it names |
| `adr-07` | Governed by `adr-07` — a label dies with the ADR it names |
| `adr-08` | Governed by `adr-08` — a label dies with the ADR it names |
| `adr-35` | Governed by `adr-35` — a label dies with the ADR it names |
| `🟢 severity:1` | Triage: cosmetic / nice-to-have |
| `🟠 severity:2` | Triage: degrades the operation |
| `🔴 severity:3` | Triage: breaks the operation |
| `📦 collateral:1` | Triage: isolated / new files only |
| `📦 collateral:2` | Triage: touches a shared surface |
| `📦 collateral:3` | Triage: wide blast radius |
| `⚙️ effort:1` | Triage: mechanical, one-pass fix |
| `⚙️ effort:2` | Triage: a session of work |
| `⚙️ effort:3` | Triage: multi-session |

One primary type label per issue/PR. Meta labels that may stack: `complex`, and `blocked` only when a human decision is the stop — **not** for dependency sequencing.

### Review verdict labels (pull requests only)

Stamped by the review routine — four agents, one label each, three states apiece. They are part of the fixed set above, so adding a thirteenth verdict label means amending this table first, exactly as rule 7 requires.

| Label | Use |
|---|---|
| `prd-approved` | PRD review: serves the objective / compliant / declared |
| `prd-observed` | PRD review: findings stand, not a breach |
| `prd-fail` | PRD review: breach — advisory, does not block the merge |
| `adr-approved` | ADR review: serves the objective / compliant / declared |
| `adr-observed` | ADR review: findings stand, not a breach |
| `adr-fail` | ADR review: breach — advisory, does not block the merge |
| `api-approved` | Interface review: serves the objective / compliant / declared |
| `api-observed` | Interface review: findings stand, not a breach |
| `api-fail` | Interface review: breach — advisory, does not block the merge |
| `clean-approved` | Clean-code review: clean on comments, duplication and naming |
| `clean-observed` | Clean-code review: findings stand, nothing safe to commit |
| `clean-applied` | Clean-code review: comment removals committed to this PR branch |

Prefix by agent: prd- is `kbot-prd`, adr- is `kbot-adr`, api- is `kbot-api`, clean- is `kbot-cleancode`.

`clean-applied` replaces a failure state: this agent acts rather than objects, so its third state records that it committed comment removals to the PR branch. Twelve labels in total.

These labels are **advisory and carry no gate force**. A `-fail` does not block a merge. An owner's merge order is not delayed by the `main` ruleset checks or by `pr-merge-gate` ([[adr-08-github]] rule 8). A verdict label is never a substitute for the `Guardian-Verdict:` line below, and the routine never writes that line: the label says an agent looked, the line says the owner process dispatched a guardian and recorded its answer.

### Reading the signature (CI job `pr-merge-gate`)

The verdict labels are a signature on a diff, and `scripts/check_pr_tags.py` reads it into the job summary on every pull request (same `pr-merge-gate` job as the recorded-verdict check below). It always exits 0 — a signature is evidence, never a gate.

Three states, and what each one means for whoever picks the change up:

- **Signed and clean.** A reviewer already read this diff, so that reading does not need doing again.
- **Signed `-fail`.** The routine's comment carries the rule it breached and usually the fix. That is the work; it is not a stop.
- **Unsigned.** No label, or a `Reviewed-SHA` that no longer matches the head — a signature covers the commit it was made against and nothing after it. Either way the routine has not read this diff, and reviewing it belongs to the agent doing the work.

## Merge-gate contract (CI job `pr-merge-gate`)

> The PR body must record a conformance pass for every guardian whose watchlist a changed file hits. `scripts/check_merge_gate.py` enforces this. The job does not delay an owner merge.

The PR body must record a conformance pass for every guardian whose watchlist a changed file hits. Enforced by `scripts/check_merge_gate.py`. This job verifies a **recorded** pass. It does not delay an owner merge ([[adr-08-github]] rule 7).

### Exact lines (machine-parsed)

One line per required guardian, unindented, outside any fence. **Two shapes satisfy a requirement**, and which one you use says who actually reviewed — that distinction is the point, not a formality:

```
Guardian-Verdict: <guardian>: <status>     # that guardian was dispatched and ran
Plan-Verdict: <ssot>: <status>           # the party judged the PLAN for that SSOT
```

| Field | Accepted values |
|---|---|
| `<guardian>` | `kbot-prd` · `kbot-adr` · `kbot-api` |
| `<ssot>` | `prd` · `adr` · `api` — each records the guardian it answers to |
| `<status>` | `pass` · `clear` · `compliant` · `valid` · `ok` · `drift` (case-insensitive), on either shape |

Examples that pass the gate:

```
Guardian-Verdict: kbot-adr: compliant
Guardian-Verdict: kbot-api: valid
Guardian-Verdict: kbot-prd: ok
```

```
Plan-Verdict: prd: ok
Plan-Verdict: adr: compliant
Plan-Verdict: api: valid
```

The second block is what a plan-time doctrine gate emits: familiars judge the **plan** — before a line is written — against the ADRs, [[PRD]] and this file ([[GLOSSARY]]: plan-time doctrine gate). A `Plan-Verdict:` line therefore says something narrower than a guardian's: it judged the plan, not the diff that followed. It **never** spells a guardian's agent name — no guardian ran, and claiming one did is the overstatement this file forbids; the gate rejects such a line outright. A guardian judging the diff itself remains a separate dispatch at the pull request.

Prose that *mentions* a guardian without that exact line shape does **not** count. Zero watched files → the job passes trivially.

### Frozen event payload

CI reads the PR body from `GITHUB_EVENT_PATH` — a snapshot frozen at the event that **started** the run. Editing the PR body and re-running the failed job alone **replays the old body** and fails identically. Recovery:

1. Put the exact `Guardian-Verdict:` lines in the PR body.
2. Push a new commit on the PR branch (empty is fine: `git commit --allow-empty -m "chore: re-trigger merge-gate"`) so a **new** `pull_request` event re-snapshots the body.

Do not rely on "Re-run failed jobs" after a body-only edit. Detail of the script: `scripts/check_merge_gate.py`; watchlist SSOT stays the guardian definitions + `scripts/guardian_watchlists.py`.

## Git tags (releases)

> `vMAJOR.MINOR.PATCH` semver, cut from `main` only, after the deploy that shipped them. A tag records what shipped; the push to `main` already deployed it.

- Format: **`vMAJOR.MINOR.PATCH`** (semver).
- Cut tags **from `main` only**, after the deploy that shipped them.
- Optional prerelease: `vX.Y.Z-rc.N`, also from `main`.
- A tag **records** what shipped. The push to `main` already deployed it.

## CI / deploy refs

- **Deploy trust**: `refs/heads/main` — the only trusted ref ([[adr-08-github]] rule 5).
- PR checks hold no deploy trust.
- Detail for cloud roles: [[INFRASTRUCTURE]].

**`main` is live — every push ships.** There is no cloud dev environment and no staging line unless [[INFRASTRUCTURE]] declares one: a merged PR is in production. The PR remains the integration record. An owner's merge order is not delayed for CI ([[adr-08-github]] rule 8).
