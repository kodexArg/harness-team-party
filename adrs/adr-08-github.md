---
title: adr-08-github
type: adr
status: active
version: v0.1.3
tags: [adr, github, issues, pr, actions, labels]
description: "Governs GitHub collaboration, PR merge authorization (triaged autonomous vs untriaged/orphan supervised), Actions CI/CD, and deploy trust confinement."
applies_when:
  - When determining whether a PR is authorized for autonomous agent merge or requires operator approval.
  - When configuring GitHub Actions workflows, deploy trust, or applying PR labels.
related_agents:
  - hb-ag-git
  - hb-ag-hunter
  - hb-ag-hawk
---

# ADR-08 — GitHub

> GitHub serves as the centralized collaboration platform and CI/CD automation plane, binding all production changes to pull requests and deterministic merge authorization.

1. **Collaboration platform authority.** GitHub (`github.com/{{owner}}/{{repo}}`) is the official repository host. Remote and CLI operations default to `{{owner}}`.

2. **Pull Request integration invariant.** All changes landing on `main` must enter through a Pull Request as the formal integration and deployment record (except for authorized direct operations by `{{owner}}`).

3. **Issue classification and PR merge authorization:**
   - **Unrestricted Issues:** Any topic, task, defect, or idea may be filed as an issue without format restrictions, and issues are not a mandatory prerequisite for PRs.
   - **Triaged Issue PRs (Autonomous Merge):** A PR that resolves a triaged issue is automatically authorized for autonomous agent merge into `origin/main` upon passing validation. What counts as triaged is [[ISSUE-TRIAGE]], not this ADR.
   - **Untriaged Issue PRs (Supervised Merge):** A PR resolving an issue that is not triaged requires explicit operator approval before merging.
   - **Orphan PRs (Supervised Merge):** A PR opened without a parent issue requires explicit operator instruction ("merge", "ship", "push") to merge, which is sufficient authority to land on `main`.

4. **GitHub Actions CI/CD orchestration.** Automated validation and deployment run via GitHub Actions declared in `.github/workflows/` (`ci.yml` and its siblings).

5. **Deploy trust confinement.** Deployment credentials trust only `refs/heads/main`. No other ref or branch carries deploy trust.

6. **Canonical label taxonomy.** Issue and PR labels are only the fixed set in [[GITHUB]]. Arbitrary ad-hoc label invention is prohibited. Scoring vocabulary, when used, is [[ISSUE-TRIAGE]].

7. **Advisory review routine.** Automated review passes (`kbot-prd`, `kbot-adr`, `kbot-api`, `kbot-cleancode`) provide non-blocking advisory feedback and labels on open PRs.

8. **Operator administrative bypass.** When the repository owner explicitly orders a merge, push, or deploy, the operator PAT executes `gh pr merge --admin` without waiting on pending or paused CI checks.
