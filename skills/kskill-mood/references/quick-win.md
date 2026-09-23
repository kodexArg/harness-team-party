# quick-win

Ship a small, complete change. Prefer the shortest path that still
passes [`docs/PRD.md`](../../../docs/PRD.md), the ADRs, and [`docs/INTERFACES.md`](../../../docs/INTERFACES.md). No gold-plating, no
adjacent cleanup unless the file is already open.

## Delivery path (this project)

When the task is work in this repo, the loop is mandatory and serial:

1. **Understand the plan.** Hold the context (SSOTs, the files, the
   acceptance). If a choice would change the work, **re-ask** — do not
   guess. This step is not optional.
2. **Build a PR.** Feature branch, one topic, tests that prove the
   change, push, open the PR ([`docs/DEVELOPMENT-LOOP.md`](../../../docs/DEVELOPMENT-LOOP.md), [`docs/GITHUB.md`](../../../docs/GITHUB.md)).
3. **Integrate immediately.** Merge to `main` so CI starts. Do not stop at an open PR to ask permission to merge when the
   owner already authorized ship/integrate.
4. **Close the turn** with the one-line result (PR URL and merged SHA, or the blocker).

`/qw` is this stance with no parser. `/kdx-mood quick win` is the same
stance through `kskill-mood`.

## Stance

- Small diff. One concern.
- Tests that would fail without the change.
- English in git and docs.
- Leave follow-ups as issues, not as extra commits on this PR.
