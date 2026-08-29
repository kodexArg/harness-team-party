"""Anti-contamination guard for the harness-team-party template.

This template MUST NOT carry any string from the product it was generalized
from. The inverted hardcode guard: where the source project asserted its own
slug never hardcodes, this template asserts the source project's slugs never
appear at all.

Rules:
  (a) `README.md` and `docs/CLONE.md` may mention the lineage ("born from
      ...") — that is the sanctioned place for it;
  (b) this test file itself — it necessarily types the literals it searches
      for;
  (c) everything else — any match is contamination and fails the test.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()

TOKENS = ("afg", "alvs", "financial-gateway")

EXCLUDE_DIR_NAMES = {".git", "node_modules", "dist", ".venv", "__pycache__"}

# rule (a): lineage mentions live here and nowhere else.
EXEMPT_FILES = {"README.md", "docs/CLONE.md"}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def ok(msg: str) -> None:
    print(f"ok    {msg}")


def tracked_files() -> list[Path]:
    """Prefer `git ls-files`; fall back to an excludes-aware rglob when the
    tree is not yet committed (a fresh template has no index)."""
    try:
        proc = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        files = [ROOT / line for line in proc.stdout.splitlines() if line.strip()]
        if files:
            return files
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    out: list[Path] = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part in EXCLUDE_DIR_NAMES for part in p.relative_to(ROOT).parts):
            continue
        out.append(p)
    return out


def scan_file(path: Path) -> list[str]:
    if path.resolve() == SELF:
        return []  # rule (b)

    rel = path.relative_to(ROOT).as_posix()
    if rel in EXEMPT_FILES:
        return []  # rule (a)

    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []  # binary / unreadable — not a text contamination

    offenders: list[str] = []
    for lineno, line in enumerate(text.splitlines(), start=1):
        lowered = line.lower()
        for token in TOKENS:
            if token in lowered:
                offenders.append(f"{rel}:{lineno}: ({token}) {line.strip()[:120]}")
    return offenders


def test_no_source_product_contamination() -> None:
    offenders: list[str] = []
    for f in tracked_files():
        offenders.extend(scan_file(f))

    if offenders:
        detail = "\n  ".join(offenders)
        fail(
            f"{len(offenders)} contamination occurrence(s) of the source "
            f"product's slugs {TOKENS!r} outside the lineage exemption "
            "(README.md / docs/CLONE.md):\n  " + detail
        )
    ok(f"zero occurrences of {TOKENS!r} outside README.md / docs/CLONE.md")


def main() -> int:
    tests = [test_no_source_product_contamination]
    failed = 0
    for fn in tests:
        try:
            fn()
        except AssertionError:
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
