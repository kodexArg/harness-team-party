#!/usr/bin/env python3
"""Assertion 1's check, exercised on behaviour rather than source text.

A check that silently matches nothing passes every repository, so each case
asserts a real verdict against a real tree state.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "check_branch_model.py"

_failures: list[str] = []


def fail(msg: str) -> None:
    _failures.append(msg)
    print(f"FAIL  {msg}", file=sys.stderr)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def load_module():
    spec = importlib.util.spec_from_file_location("check_branch_model", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_this_repo_passes() -> None:
    mod = load_module()
    bad = mod._findings(None)
    if bad:
        fail(f"this repo must satisfy assertion 1, got: {bad}")
        return
    ok("this repository satisfies assertion 1")


def test_a_prod_branch_is_caught() -> None:
    mod = load_module()
    bad = mod._findings(["main", "origin/prod", "feat/x"])
    if not any("retired" in b and "MUST NOT be recreated" in b for b in bad):
        fail(f"a recreated `prod` branch must be caught, got: {bad}")
        return
    ok("a recreated `prod` branch is caught")


def test_ordinary_branches_pass() -> None:
    mod = load_module()
    bad = mod._findings(["main", "origin/feat/prod-ingestion", "chore/prod-docs"])
    if bad:
        fail(f"branch names merely containing 'prod' must pass, got: {bad}")
        return
    ok("branch names containing 'prod' as a substring pass")


def test_the_environment_sense_is_not_flagged() -> None:
    """The decisive case: `prod` the environment must never trip this check."""
    mod = load_module()
    for sample in (
        "  ENV_NAME: prod",
        "  CLUSTER: acme-prod",
        "SECRET_DB: arn:example:secretsmanager:...:secret:acme/prod/x/db-Ekm3yb",
        '            taskdef="${name}-prod"',
    ):
        if mod.BRANCH_SHAPED.search(sample):
            fail(f"environment-sense line wrongly flagged: {sample!r}")
            return
    ok("environment-sense `prod` is never flagged")


def test_branch_sense_spellings_are_flagged() -> None:
    mod = load_module()
    for sample in (
        "        sub: repo:owner/x:ref:refs/heads/prod",
        "    branches: [prod]",
        "    branches: [main, prod]",
    ):
        if not mod.BRANCH_SHAPED.search(sample):
            fail(f"branch-sense line not flagged: {sample!r}")
            return
    ok("branch-sense `prod` spellings are flagged")


def main() -> int:
    for fn in (
        test_this_repo_passes,
        test_a_prod_branch_is_caught,
        test_ordinary_branches_pass,
        test_the_environment_sense_is_not_flagged,
        test_branch_sense_spellings_are_flagged,
    ):
        fn()
    print()
    if _failures:
        print(f"{len(_failures)} test(s) FAILED")
        return 1
    print("all 5 test(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
