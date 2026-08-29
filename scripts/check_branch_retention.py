#!/usr/bin/env python3
"""Assertion 2 — no remote branch outlives the retention window unclaimed.

Contract: [[GITHUB]] "Branch retention — 14 days, then promoted or deleted".

A branch with no PR is unclaimed and uncounted: nothing lists it, no guardian
sees it, and the only way to learn a fix already exists on it is to go looking.
The 2026-08-15 audit (#597) found ten such branches and five of them were
already dead — one superseded by a better refactor on main, so keeping it looked
like pending work that did not exist.

Reports; it does not delete. The deletion command is printed for an operator to
run, because deleting somebody's unreviewed work is not a thing a script decides.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# The window GITHUB.md states. A branch younger than this is simply work in progress.
RETENTION_DAYS = 14
PROTECTED = {"main"}


def _git(*args: str) -> str | None:
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), *args], capture_output=True, text=True, timeout=15
        )
        return out.stdout if out.returncode == 0 else None
    except Exception:
        return None


def _branches_with_a_pr() -> set[str] | None:
    try:
        out = subprocess.run(
            ["gh", "pr", "list", "--state", "all", "--limit", "200",
             "--json", "headRefName"],
            cwd=str(ROOT), capture_output=True, text=True, timeout=20,
        )
        if out.returncode != 0:
            return None
        return {pr["headRefName"] for pr in json.loads(out.stdout)}
    except Exception:
        return None


def stale_branches(days: int = RETENTION_DAYS, now: datetime | None = None) -> list[dict] | None:
    """Remote branches unmerged into main, with no PR, older than the window.

    Returns None when git or gh cannot answer — an unreachable API must read
    `unknown`, never an empty list that says everything is tidy.
    """
    now = now or datetime.now(timezone.utc)
    listing = _git("for-each-ref", "--format=%(refname:short)%09%(committerdate:iso-strict)",
                   "refs/remotes/origin")
    merged = _git("branch", "-r", "--merged", "origin/main", "--format=%(refname:short)")
    with_pr = _branches_with_a_pr()
    if listing is None or merged is None or with_pr is None:
        return None

    merged_set = set(merged.split())
    stale = []
    for row in listing.splitlines():
        if "\t" not in row:
            continue
        ref, when = row.split("\t", 1)
        name = ref.removeprefix("origin/")
        if ref in merged_set or name in PROTECTED or ref.endswith("/HEAD"):
            continue
        if name in with_pr:
            continue
        try:
            age = (now - datetime.fromisoformat(when.strip())).days
        except ValueError:
            continue
        if age >= days:
            stale.append({"branch": name, "age_days": age})
    return sorted(stale, key=lambda b: -b["age_days"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--days", type=int, default=RETENTION_DAYS,
        help=f"retention window in days (default {RETENTION_DAYS}, the GITHUB.md rule)",
    )
    args = parser.parse_args(argv)

    stale = stale_branches(days=args.days)
    if stale is None:
        print("branch retention: UNKNOWN — git or gh could not answer.")
        return 0
    if not stale:
        print(f"branch retention: ok — no unmerged branch without a PR is older than {args.days} days.")
        return 0

    print(f"branch retention: {len(stale)} branch(es) past the {args.days}-day window, no PR, not merged:")
    for row in stale:
        print(f"  {row['branch']}  ({row['age_days']}d)")
    print("\nEach one is promoted to an issue or deleted — GITHUB.md, Branch retention. To delete:")
    for row in stale:
        print(f"  git push origin --delete {row['branch']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
