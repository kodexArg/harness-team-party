#!/usr/bin/env python3
"""Merge-time conformance-verdict gate, CI job `pr-merge-gate`.

Contract, both accepted line shapes and the rationale: [[GITHUB]].
"""

from __future__ import annotations

import argparse
import fnmatch
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WATCHLISTS_MODULE = ROOT / "scripts" / "guardian_watchlists.py"

# Each guardian name is a contiguous literal so tests/test_project_slug_hardcode.py
# rule (g) strips it before its slug scan. Vocabulary: [[GITHUB]].
VERDICT_RE = re.compile(
    r"^Guardian-Verdict:\s*(kbot-prd|kbot-adr|kbot-api):\s*"
    r"(pass|clear|compliant|valid|ok|drift)\s*$",
    re.IGNORECASE,
)

# The party's plan-time verdict: keyed by SSOT, because no guardian ran.
PLAN_VERDICT_RE = re.compile(
    r"^Plan-Verdict:\s*(prd|adr|api):\s*"
    r"(pass|clear|compliant|valid|ok|drift)\s*$",
    re.IGNORECASE,
)

# Mirrors SSOT_GUARDIAN in both .claude/workflows/*triage-and-fix.js.
SSOT_GUARDIAN = {
    "prd": "kbot-prd",
    "adr": "kbot-adr",
    "api": "kbot-api",
}


def load_watchlists() -> dict:
    """Imports scripts/guardian_watchlists.py WATCHLISTS — the one shared copy;
    see scripts/guardian_watchlists.py's own docstring for the no-third-copy
    discipline."""
    spec = importlib.util.spec_from_file_location("guardian_watchlists", WATCHLISTS_MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.WATCHLISTS


def guardians_for(rel: str, watchlists: dict) -> list[str]:
    """fnmatch against each pattern AND against pattern.rstrip('*') + '*'."""
    hits = []
    for agent, patterns in watchlists.items():
        for pattern in patterns:
            if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(rel, pattern.rstrip("*") + "*"):
                hits.append(agent)
                break
    return hits


def required_guardians(changed_files: list[str], watchlists: dict) -> dict[str, list[str]]:
    """guardian name -> the changed files that triggered it."""
    required: dict[str, list[str]] = {}
    for rel in changed_files:
        for agent in guardians_for(rel, watchlists):
            required.setdefault(agent, []).append(rel)
    return required


def changed_files_from_git(base: str) -> list[str]:
    out = subprocess.run(
        ["git", "diff", "--name-only", f"{base}...HEAD"],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
        check=True,
    ).stdout
    return [line.strip() for line in out.splitlines() if line.strip()]


def recorded_verdicts(body: str | None) -> set[str]:
    """Guardian names (lowercased) whose requirement the body satisfies —
    by a `Guardian-Verdict:` line naming that guardian, or by a
    `Plan-Verdict:` line for the SSOT it answers to."""
    if not body:
        return set()
    recorded = set()
    for raw in body.splitlines():
        line = raw.strip()
        match = VERDICT_RE.match(line)
        if match:
            recorded.add(match.group(1).lower())
            continue
        match = PLAN_VERDICT_RE.match(line)
        if match:
            recorded.add(SSOT_GUARDIAN[match.group(1).lower()])
    return recorded


def pr_body_from_event(event_path: str | None) -> str | None:
    if not event_path:
        return None
    try:
        payload = json.loads(Path(event_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return (payload.get("pull_request") or {}).get("body")


def default_base() -> str:
    base_ref = os.environ.get("GITHUB_BASE_REF")
    if base_ref:
        return f"origin/{base_ref}"
    return "origin/main"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        default=None,
        help="diff base (default: origin/<GITHUB_BASE_REF> if set, else origin/main)",
    )
    parser.add_argument(
        "--body-file",
        default=None,
        help="path to a file holding the PR body text (local/test runs; "
        "CI reads GITHUB_EVENT_PATH instead)",
    )
    args = parser.parse_args()

    base = args.base or default_base()
    changed = changed_files_from_git(base)

    watchlists = load_watchlists()
    required = required_guardians(changed, watchlists)

    if not required:
        print("merge-gate: no watched files changed — passing trivially")
        return 0

    if args.body_file:
        body = Path(args.body_file).read_text(encoding="utf-8")
    else:
        body = pr_body_from_event(os.environ.get("GITHUB_EVENT_PATH"))

    recorded = recorded_verdicts(body)

    for agent, files in sorted(required.items()):
        status = "recorded" if agent in recorded else "MISSING"
        print(f"merge-gate: {agent} required by {files} -> {status}")

    missing = sorted(set(required) - recorded)
    if missing:
        print(
            "\nmerge-gate: FAIL — missing recorded verdict(s). Either dispatch "
            "the guardian(s) below and record one line each, or record the "
            "party's plan-time verdict for the same SSOT:",
            file=sys.stderr,
        )
        ssot_of = {v: k for k, v in SSOT_GUARDIAN.items()}
        for agent in missing:
            print(f"  Guardian-Verdict: {agent}: pass", file=sys.stderr)
            if agent in ssot_of:
                print(f"    (or)  Plan-Verdict: {ssot_of[agent]}: pass", file=sys.stderr)
        return 1

    print("\nmerge-gate: PASS — every required guardian has a recorded verdict")
    return 0


if __name__ == "__main__":
    sys.exit(main())
