#!/usr/bin/env python3
"""Guard: The Three Feathers inn and the Hunter bulletin for a later Hunter."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

failures = 0


def fail(msg: str) -> None:
    global failures
    failures += 1
    print(f"FAIL: {msg}", file=sys.stderr)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def test_glossary_names_the_inn() -> None:
    text = (ROOT / "docs" / "GLOSSARY.md").read_text(encoding="utf-8")
    if "The Three Feathers" not in text or "Las Tres Plumas" not in text:
        fail("docs/GLOSSARY.md does not name The Three Feathers / Las Tres Plumas")
        return
    if "GitHub issues" not in text and "issues, pull requests" not in text:
        fail("docs/GLOSSARY.md does not say the inn is issues, PRs, and agents")
        return
    ok("glossary names The Three Feathers as the inn")


def test_github_notice_board_is_an_issue_comment() -> None:
    text = (ROOT / "docs" / "GITHUB.md").read_text(encoding="utf-8")
    if "### The Three Feathers (Las Tres Plumas)" not in text:
        fail("docs/GITHUB.md lacks The Three Feathers heading")
        return
    if "issue comment" not in text:
        fail("docs/GITHUB.md does not say the notice board is an issue comment")
        return
    if "later Hunter" not in text:
        fail("docs/GITHUB.md does not name a later Hunter as the bulletin receiver")
        return
    ok("GITHUB pins the notice board as an issue comment for a later Hunter")


def test_hunter_bulletin_is_problem_plus_goal() -> None:
    skill = (ROOT / "skills" / "hb-sk-hunter" / "SKILL.md").read_text(encoding="utf-8")
    agent = (ROOT / "agents" / "hb-ag-hunter.md").read_text(encoding="utf-8")
    for needle in (
        "inn: The Three Feathers",
        "problem:",
        "goal:",
        "receiver: later Hunter",
        "noise",
    ):
        if needle not in skill:
            fail(f"skills/hb-sk-hunter/SKILL.md is missing {needle!r}")
    if "Leave `goal` empty or \"investigate\"" not in skill:
        fail("skills/hb-sk-hunter/SKILL.md no longer forbids an empty or investigate goal")
    if "later Hunter" not in agent or "problem" not in agent:
        fail("agents/hb-ag-hunter.md does not charge the Hunter with problem + later Hunter")
    if not failures:
        ok("Hunter bulletin is a noise-stripped problem plus one imperative goal")


def test_runtime_index_routes_the_inn() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for needle in (
        "The Three Feathers",
        "Las Tres Plumas",
        "hb-ag-hunter",
        "The Hunter",
        "later Hunter",
    ):
        if needle not in text:
            fail(f"AGENTS.md is missing {needle!r}")
    if not failures:
        ok("AGENTS.md routes issue hunt to The Hunter at The Three Feathers")


def main() -> int:
    tests = (
        test_glossary_names_the_inn,
        test_github_notice_board_is_an_issue_comment,
        test_hunter_bulletin_is_problem_plus_goal,
        test_runtime_index_routes_the_inn,
    )
    for fn in tests:
        fn()
    if failures:
        print(f"\n{failures} test(s) failed", file=sys.stderr)
        return 1
    print("\nall 4 test(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
