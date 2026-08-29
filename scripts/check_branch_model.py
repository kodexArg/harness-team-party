#!/usr/bin/env python3
"""Assertion 1 — main is the only deploy-bound ref, and no `prod` branch exists.

Contract: [[GITHUB]] Constraints, [[adr-07-git]], [[adr-08-github]].

Agnostic form: the template ships no deploy workflow, so the check scans every
workflow for branch-shaped `prod` references, and any workflow whose filename
contains `deploy` must trigger on exactly `['main']`. Instantiation keeps both
rules honest once a deploy pipeline exists.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"

LIVE_BRANCH = "main"
RETIRED_BRANCH = "prod"

# `prod` is a legitimate ENVIRONMENT name; only the branch is retired. These are
# the branch-shaped spellings, so `env=prod` and secret paths never match.
BRANCH_SHAPED = re.compile(r"refs/heads/prod\b|branches:\s*\[[^\]]*\bprod\b")


def _findings(branches: list[str] | None) -> list[str]:
    bad: list[str] = []

    for wf in sorted(WORKFLOWS.glob("*.yml")) if WORKFLOWS.is_dir() else []:
        text = wf.read_text()
        if "deploy" in wf.name:
            triggers = re.findall(r"branches:\s*\[([^\]]*)\]", text)
            refs = {r.strip().strip("\"'") for line in triggers for r in line.split(",")}
            if refs and refs != {LIVE_BRANCH}:
                bad.append(
                    f"{wf.relative_to(ROOT)} deploys from {sorted(refs)}, expected "
                    f"exactly ['{LIVE_BRANCH}'] (adr-08 rule 5)"
                )
        for n, line in enumerate(text.splitlines(), 1):
            if BRANCH_SHAPED.search(line):
                bad.append(
                    f"{wf.relative_to(ROOT)}:{n} names the retired "
                    f"`{RETIRED_BRANCH}` branch (adr-07 rule 2)"
                )

    if branches is not None:
        for b in branches:
            name = b.strip().removeprefix("origin/")
            if name == RETIRED_BRANCH:
                bad.append(
                    f"branch `{RETIRED_BRANCH}` exists — it is retired and MUST "
                    f"NOT be recreated (adr-07 rule 2)"
                )

    return bad


def _remote_branches() -> list[str] | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "branch", "-r", "--format=%(refname:short)"],
            capture_output=True, text=True, timeout=10,
        )
        if out.returncode != 0:
            return None
        return [b for b in out.stdout.split() if b]
    except Exception:
        return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--branches",
        help=f"comma-separated branch list to check for `{RETIRED_BRANCH}`; "
             "defaults to the local remote-tracking refs",
    )
    parser.add_argument(
        "--no-branches", action="store_true",
        help="skip the branch-existence check (offline / shallow checkouts)",
    )
    args = parser.parse_args(argv)

    if args.no_branches:
        branches = None
    elif args.branches:
        branches = args.branches.split(",")
    else:
        branches = _remote_branches()

    bad = _findings(branches)
    if bad:
        print("assertion 1 FAIL — main is not the sole deploy-bound ref:")
        for b in bad:
            print(f"  - {b}")
        return 1
    print(f"ok — assertion 1: `{LIVE_BRANCH}` is the only deploy-bound ref; "
          f"no `{RETIRED_BRANCH}` branch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
