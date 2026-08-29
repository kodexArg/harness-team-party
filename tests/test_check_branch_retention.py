"""GITHUB.md assertion 2 — the branch retention window (#597).

The rule is only worth stating if the window it names and the window the script
applies are the same number, and if an unreachable API reads `unknown` rather
than an empty `everything is tidy`.
"""

from __future__ import annotations

import importlib.util
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_branch_retention.py"
GH = ROOT / "docs" / "GITHUB.md"

NOW = datetime(2026, 8, 16, tzinfo=timezone.utc)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def load():
    spec = importlib.util.spec_from_file_location("check_branch_retention", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stub(module, *, listing: str, merged: str, with_pr: set) -> None:
    module._git = lambda *args: listing if "for-each-ref" in args else merged
    module._branches_with_a_pr = lambda: with_pr


def iso(days_ago: int) -> str:
    return (NOW - timedelta(days=days_ago)).isoformat()


def test_window_matches_the_stated_rule() -> None:
    module = load()
    stated = re.search(r"unmerged, has no pull request, and has not moved in (\d+) days", GH.read_text(encoding="utf-8"))
    if not stated:
        fail("docs/GITHUB.md no longer states the retention window in the rule sentence.")
    if int(stated.group(1)) != module.RETENTION_DAYS:
        fail(
            f"GITHUB.md states {stated.group(1)} days, the script applies "
            f"{module.RETENTION_DAYS}. A rule and its tool must name one number."
        )
    ok(f"GITHUB.md and the script agree on a {module.RETENTION_DAYS}-day window")


def test_only_unclaimed_branches_past_the_window_are_named() -> None:
    module = load()
    stub(
        module,
        listing="\n".join([
            f"origin/main\t{iso(0)}",
            f"origin/fresh-work\t{iso(3)}",           # inside the window
            f"origin/has-a-pr\t{iso(60)}",            # claimed by a PR
            f"origin/already-merged\t{iso(60)}",      # content is on main
            f"origin/forgotten\t{iso(30)}",           # the case the rule is for
        ]),
        merged="origin/main origin/already-merged",
        with_pr={"has-a-pr"},
    )
    stale = module.stale_branches(now=NOW)
    if [b["branch"] for b in stale] != ["forgotten"]:
        fail(f"expected only ['forgotten']; got {stale}")
    if stale[0]["age_days"] != 30:
        fail(f"age must be reported from the last commit; got {stale[0]}")
    ok("fresh, PR-claimed and merged branches are all left alone; the forgotten one is named")


def test_an_unreachable_api_reads_unknown() -> None:
    module = load()
    stub(module, listing="", merged="", with_pr=set())
    module._branches_with_a_pr = lambda: None
    if module.stale_branches(now=NOW) is not None:
        fail("an unreachable gh must return None, never an empty `nothing is stale`.")
    ok("an unreachable gh reads unknown, never a false all-clear")


def main() -> int:
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    failed = 0
    for fn in tests:
        try:
            fn()
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
