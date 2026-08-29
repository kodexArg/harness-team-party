#!/usr/bin/env python3
"""Read the review routine's signature off a pull request, CI job `pr-merge-gate`.

The four verdict labels are a signature, never a gate: this script always exits
0. Contract and semantics: [[GITHUB]], [[PR-REVIEW-ROUTINE]] (advisory, never a gate).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

PREFIXES = ("prd", "adr", "api", "clean")

STATES = ("approved", "observed", "fail", "applied")

REVIEWED_SHA_RE = re.compile(r"^Reviewed-SHA:\s*([0-9a-f]{7,40})\s*$", re.MULTILINE)

# The routine writes its findings under a heading of this shape, one per failing
# reviewer: "Under adr (fail):" followed by the quoted rule and the fix.
FINDING_RE = re.compile(
    r"^Under (\w+) \(fail\):\s*\n(.*?)(?=\n^Under \w+ \(fail\):|\n^Reviewed-SHA:|\Z)",
    re.MULTILINE | re.DOTALL,
)


def gh_pr(number: str, repo: str | None) -> dict:
    cmd = ["gh", "pr", "view", number, "--json", "labels,comments,headRefOid"]
    if repo:
        cmd += ["--repo", repo]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or "gh pr view failed")
    return json.loads(proc.stdout)


def signature(pr: dict) -> tuple[dict, str | None, str]:
    """Return (verdict per prefix, the reviewed SHA, the routine's comment body)."""
    labels = {label["name"] for label in pr.get("labels", [])}
    verdicts = {}
    for prefix in PREFIXES:
        for state in STATES:
            if f"{prefix}-{state}" in labels:
                verdicts[prefix] = state
                break
        else:
            verdicts[prefix] = None

    body = ""
    reviewed = None
    for comment in pr.get("comments", []):
        match = REVIEWED_SHA_RE.search(comment.get("body", ""))
        if match:
            reviewed = match.group(1)
            body = comment["body"]
    return verdicts, reviewed, body


def findings(body: str) -> dict:
    return {m.group(1): m.group(2).strip() for m in FINDING_RE.finditer(body)}


def covers_head(reviewed: str | None, head: str) -> bool:
    if not reviewed or not head:
        return False
    shortest = min(len(reviewed), len(head))
    return reviewed[:shortest] == head[:shortest]


def render(verdicts: dict, reviewed: str | None, head: str, found: dict) -> str:
    fresh = covers_head(reviewed, head)
    lines = ["## Review signature", ""]

    if not any(verdicts.values()):
        lines += [
            "No verdict label on this pull request. The review routine has not signed "
            "this diff — reviewing it is the agent's own job.",
            "",
        ]
        return "\n".join(lines)

    if not fresh:
        lines += [
            f"The signature was made against `{reviewed or 'an unrecorded commit'}`, "
            f"and the head is `{head[:7]}`. It does not cover this diff, so it counts "
            "for nothing — review this head as if unsigned.",
            "",
        ]

    lines += ["| Reviewer | Verdict |", "|---|---|"]
    for prefix in PREFIXES:
        state = verdicts[prefix]
        lines.append(f"| `{prefix}-` | {state or '— not signed'} |")
    lines.append("")

    if fresh:
        for prefix, text in found.items():
            lines += [f"### What `{prefix}-fail` reports", "", text, ""]

    lines += [
        "A verdict label is advisory and gates nothing ([[PR-REVIEW-ROUTINE]]). A `-fail` "
        "names work to do; it does not stop this merge.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pr", default=os.environ.get("PR_NUMBER"))
    parser.add_argument("--repo", default=os.environ.get("GH_REPO"))
    args = parser.parse_args()

    if not args.pr:
        print("no pull request number — pass --pr or set PR_NUMBER", file=sys.stderr)
        return 0

    try:
        pr = gh_pr(args.pr, args.repo)
    except (RuntimeError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        print(f"could not read the pull request ({exc}) — no signature available", file=sys.stderr)
        return 0

    verdicts, reviewed, body = signature(pr)
    summary = render(verdicts, reviewed, pr.get("headRefOid", ""), findings(body))
    print(summary)

    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
