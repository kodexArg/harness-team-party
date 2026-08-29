"""Guard for the repository's GitHub label set (issue #49).

docs/GITHUB.md owns the fixed label set, and adr-08-github rule 7 gives it
force: "Labels are only the fixed set in GH." The set drifted anyway — the repo
carried GitHub's creation-time defaults and lacked five sanctioned labels, so
`.github/ISSUE_TEMPLATE/gh-issue-feature.md`'s `labels: feat` frontmatter
was a silent no-op for every issue opened through it.

docs/GITHUB.md is the single source of truth here: this test PARSES its label table
rather than typing the set out, so the doc stays the only place the set is
edited. Adding a label means adding its row there; this test then requires it
live.

The live half needs a working, authenticated `gh` against the repo. Where that
is unavailable — offline, no credentials, a fresh clone — the live comparison
is SKIPPED, loudly, and the parse half still runs. That is deliberate: a
harness test must not fail for want of a network, and this file must never
become a merge gate that depends on one. Compare tests/test_aws_infra.py, whose
live checks carry the same caveat.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GH_DOC = REPO_ROOT / "docs" / "GITHUB.md"

# The heading that opens the label table in docs/GITHUB.md. Anchoring on it keeps a
# stray pipe-table elsewhere in the doc from being read as the label set.
TABLE_HEADING = "## Labels (issues + PRs) — fixed set"

# One unsanctioned label is tolerated, temporarily and by name (issue #49).
#
# `invalid` is applied to #27, #28 and #30, all closed. It is the only
# in-tracker record of how they were dispositioned, so deleting the label would
# destroy that record; it stays until #49 decides. The hazard register that
# used to contradict their closed state no longer exists (removed by owner
# directive, #469), so only the tracker's word stands.
#
# This carve-out is temporary. Resolving that contradiction means removing
# `invalid` from this set in the same batch — leaving it here afterwards would
# turn a deliberate exception into permanent, invisible drift.
TEMPORARY_EXCEPTIONS = {"invalid"}


def parse_fixed_set():
    """Return {label: description} from the label table in docs/GITHUB.md."""
    text = GH_DOC.read_text(encoding="utf-8")
    if TABLE_HEADING not in text:
        raise AssertionError(
            f"{GH_DOC.relative_to(REPO_ROOT)} no longer contains the heading "
            f"{TABLE_HEADING!r}. This test parses the table under it; if the "
            f"heading was renamed, update TABLE_HEADING here in the same batch."
        )

    section = text.split(TABLE_HEADING, 1)[1]
    # Stop at the next h2 so a later table cannot leak into the set.
    section = section.split("\n## ", 1)[0]

    labels = {}
    for line in section.splitlines():
        # Rows look like: | `bug` | Defect |
        match = re.match(r"^\|\s*`([^`]+)`\s*\|\s*(.+?)\s*\|\s*$", line)
        if match:
            labels[match.group(1)] = match.group(2)
    return labels


def live_labels():
    """Return {label: description} from the live repo, or None if unavailable."""
    try:
        proc = subprocess.run(
            ["gh", "label", "list", "--limit", "200", "--json", "name,description"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    try:
        return {row["name"]: row.get("description") or "" for row in json.loads(proc.stdout)}
    except (json.JSONDecodeError, TypeError, KeyError):
        return None


def test_fixed_set_is_parseable():
    """docs/GITHUB.md must declare a non-empty, well-formed label table."""
    fixed = parse_fixed_set()
    assert fixed, (
        f"parsed no labels from the table under {TABLE_HEADING!r} in "
        f"{GH_DOC.relative_to(REPO_ROOT)} — the table is missing or its row "
        f"format changed (expected: | `name` | description |)"
    )
    print(f"  docs/GITHUB.md declares {len(fixed)} labels: {', '.join(sorted(fixed))}")


def test_live_set_matches_fixed_set():
    """The live repo must carry exactly the labels docs/GITHUB.md declares."""
    fixed = parse_fixed_set()
    live = live_labels()

    if live is None:
        print(
            "  SKIPPED (live): `gh label list` unavailable — no gh, no auth, or "
            "no network. The live half of this guard did NOT run."
        )
        return

    missing = sorted(set(fixed) - set(live))
    unsanctioned = sorted(set(live) - set(fixed) - TEMPORARY_EXCEPTIONS)

    for name in sorted(TEMPORARY_EXCEPTIONS & set(live)):
        print(f"  TOLERATED (temporary, issue #49): {name!r} is present live and not in docs/GITHUB.md")

    problems = []
    if missing:
        problems.append(
            "missing from the live repo (declared in docs/GITHUB.md): "
            + ", ".join(missing)
        )
    if unsanctioned:
        problems.append(
            "present live but not in docs/GITHUB.md: " + ", ".join(unsanctioned)
        )

    assert not problems, (
        "the repository label set has drifted from docs/GITHUB.md "
        "(adr-08-github rule 7):\n    - " + "\n    - ".join(problems)
    )
    print(f"  live label set matches docs/GITHUB.md ({len(fixed)} labels)")


def main():
    tests = [test_fixed_set_is_parseable, test_live_set_matches_fixed_set]
    failed = 0
    for fn in tests:
        print(f"{fn.__name__}:")
        try:
            fn()
        except AssertionError as exc:
            print(f"FAIL: {fn.__name__}: {exc}", file=sys.stderr)
            failed += 1
        except Exception as exc:
            print(f"FAIL: {fn.__name__}: {exc}", file=sys.stderr)
            failed += 1

    if failed:
        print(f"\n{failed} test(s) failed", file=sys.stderr)
        return 1
    print(f"\nall {len(tests)} test(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
