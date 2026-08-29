"""Guard: no agent is instructed to run `gh issue view --comments` (#920).

That flag still selects GraphQL `repository.issue.projectCards`. GitHub sunset
Projects (classic); hosts shipping gh older than 2.80.0 fail on every issue.
docs/GITHUB.md owns the two-call REST fetch. This test only watches the trees that
*instruct* a worker: agents/, skills/, workflows, and the parked hunt engine.

Mentions that prohibit the flag (`never`, `is not`) are allowed — those are
the documentation of the defect, not an instruction to run it.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TREES = (
    ROOT / "agents",
    ROOT / "skills",
    ROOT / ".claude" / "workflows",
    ROOT / ".github" / "workflows",
    ROOT / ".github" / "workflows-disabled",
)

INSTRUCTION = re.compile(r"gh issue view[^\n]*--comments", re.IGNORECASE)
PROHIBITION = re.compile(r"\bnever\b|\bis not\b|\bnot the\b", re.IGNORECASE)

SKIP_SUFFIXES = {".lock", ".png", ".jpg", ".webp"}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def watched_files() -> list[Path]:
    files: list[Path] = []
    for tree in TREES:
        if not tree.is_dir():
            continue
        for path in tree.rglob("*"):
            if not path.is_file() or path.suffix in SKIP_SUFFIXES:
                continue
            if path.is_symlink():
                continue
            files.append(path)
    return files


def test_no_worker_is_told_to_run_issue_view_comments() -> None:
    hits: list[str] = []
    for path in watched_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for i, line in enumerate(text.splitlines(), start=1):
            if not INSTRUCTION.search(line):
                continue
            if PROHIBITION.search(line):
                continue
            rel = path.relative_to(ROOT)
            hits.append(f"{rel}:{i}: {line.strip()}")
    if hits:
        fail(
            "workers are still instructed to run `gh issue view --comments` "
            "(use REST `gh api repos/{owner}/{repo}/issues/<n>/comments` per "
            f"docs/GITHUB.md): {hits}"
        )
    ok("no agent/skill/workflow instructs `gh issue view --comments`")


def test_gh_doc_owns_the_rest_fetch() -> None:
    text = (ROOT / "docs" / "GITHUB.md").read_text(encoding="utf-8")
    if "### Reading issue comments" not in text:
        fail("docs/GITHUB.md lost the Reading issue comments heading")
    if "gh api repos/{owner}/{repo}/issues/<n>/comments" not in text:
        fail("docs/GITHUB.md no longer names the REST comments path")
    ok("docs/GITHUB.md owns the REST comments fetch")


def test_requirements_pins_gh() -> None:
    text = (ROOT / "docs" / "REQUIREMENTS.md").read_text(encoding="utf-8")
    if not re.search(r"^\| gh \| 2\.\d+\.\d+ \|", text, re.M):
        fail("docs/REQUIREMENTS.md has no gh pin row")
    if "2.80.0" not in text:
        fail("docs/REQUIREMENTS.md does not record the 2.80.0 floor for --comments")
    ok("docs/REQUIREMENTS.md pins gh and records the 2.80.0 floor")


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
            pass
    if failed:
        print(f"\n{failed} test(s) failed", file=sys.stderr)
        return 1
    print("\nall test(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
