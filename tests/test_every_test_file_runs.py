"""Every harness test file must actually run its tests when CI invokes it.

The `pr-harness` job runs each file as `python3 tests/test_<x>.py`
(`.github/workflows/ci.yml`). A file with no `__main__` runner defines its
tests, runs none, and exits 0 — green by not running. Three files were in that
state when this was written (#597), one of them the guardian-availability suite
that #598 depends on.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"


def harness_test_files() -> list[Path]:
    return sorted(TESTS.glob("test_*.py"))


def has_main_guard(path: Path) -> bool:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.If):
            continue
        for sub in ast.walk(node.test):
            if isinstance(sub, ast.Name) and sub.id == "__name__":
                return True
    return False


def test_every_test_file_has_a_runner() -> None:
    missing = [p.name for p in harness_test_files() if not has_main_guard(p)]
    assert not missing, (
        "these files run zero tests under the CI harness job, and pass by "
        f"not running: {', '.join(missing)}"
    )


def test_the_audit_covers_every_file_ci_runs() -> None:
    """CI must still invoke each test file as a script, which is what a missing
    `__main__` guard defeats. Which files it selects may change — `ci_select.py`
    narrows them by diff — but the invocation is what this audit depends on."""
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert 'python3 "$t"' in workflow, (
        "the harness job no longer runs each test file as a script; this audit "
        "is checking an invocation CI does not use"
    )
    assert harness_test_files(), "no harness test files found"


def main() -> int:
    failed = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_"):
            continue
        try:
            fn()
        except Exception as exc:
            print(f"FAIL: {name}: {exc}", file=sys.stderr)
            failed += 1
        else:
            print(f"ok  {name}")

    if failed:
        print(f"\n{failed} test(s) failed", file=sys.stderr)
        return 1
    print("\nall test(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
