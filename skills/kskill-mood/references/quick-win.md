# quick-win

Ship a small, complete change. Prefer the shortest path that still
passes the ABC gate ([[PRD]], ADRs, [[INTERFACES]]). No gold-plating, no
adjacent cleanup unless the file is already open ([[HARNESS]] Boy-scout).

## Delivery path (this project)

When the task is work in this repo, the loop is mandatory and serial:

1. **Understand the plan.** Hold the context (SSOTs, the files, the
   acceptance). If a choice would change the work, **re-ask** — do not
   guess. This step is not optional.
2. **Build a PR.** Feature branch, one topic, tests that prove the
   change, push, open the PR ([[DEVELOPMENT-LOOP]] §0.5, [[GITHUB]]).
3. **Integrate immediately.** Merge to `main` so CI and deploy workflows
   start. Do not stop at an open PR to ask permission to merge when the
   owner already authorized ship/integrate.
4. **Inform with `kskill-cowsay`.** Close the turn with `/cowsay` using
   the **QUICK WIN** legend (word art, not an animal). The bubble carries
   the one-line result (PR URL + merged SHA, or the blocker).

`/qw` is this stance with no parser. `/kdx-mood quick win` is the same
stance through `kskill-mood`.

## Stance

- Small diff. One concern.
- Tests that would fail without the change.
- English in git and docs; {{interface language}} only on screen.
- Leave follow-ups as issues, not as extra commits on this PR.
