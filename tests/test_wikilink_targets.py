"""ADR-shaped `[[wikilink]]`s must resolve to a real ADR file.

Dead links reproduce faster than they get boy-scouted: a contributor copies an
existing header verbatim and cites an ADR deleted the same day. This check is
scoped to `[[adr-NN-slug]]`-shaped targets, not every wikilink in the tree — a
full-resolution pass over the whole vault flags legitimate non-ADR cases
(literal placeholders like `[[adr-NN-slug]]` in templates, path-shaped
targets) that would need a sprawling allowlist to carry. `adr-`-shaped targets
have zero such cases, and an ADR citation is exactly the regression this
guards.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Captures the file half of `[[target]]`, `[[target|display]]` and
# `[[target#heading]]` alike — the display text and the anchor are never
# part of what must resolve to a file.
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
ADR_SHAPED = re.compile(r"^adr-\d+-", re.IGNORECASE)

# Renamed ADRs still cited in prose. Fail only on stems that never had a successor.
SUPERSEDED_ADR_STEMS: set[str] = set()

# Each exclusion is a category, not a per-file convenience:
EXCLUDED_FILES = {
    # Historical records — narrate past state, deliberately never swept
    # (project holds that history belongs to git, not to a live wikilink).
    "CHANGELOG.md": "history",
    # Literal placeholders — documentation OF the `[[adr-NN-slug]]` syntax,
    # not a use of it.
    ".github/ISSUE_TEMPLATE/gh-issue-feature.md": "placeholder",
    "docs/CODE-COMMENTS.md": "placeholder",
    "docs/GLOSSARY.md": "placeholder",
}

EXCLUDE_DIR_NAMES = {".git", "node_modules", "dist", ".venv", "__pycache__"}

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def tracked_markdown_files() -> list[str]:
    """Prefer `git ls-files`; fall back to an excludes-aware rglob when the
    tree is not yet committed (a fresh template has no index)."""
    try:
        out = subprocess.run(
            ["git", "ls-files"], capture_output=True, text=True, cwd=ROOT, check=True
        ).stdout
        files = [f for f in out.splitlines() if f.endswith(".md")]
        if files:
            return files
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return [
        p.relative_to(ROOT).as_posix()
        for p in ROOT.rglob("*.md")
        if p.is_file()
        and not any(part in EXCLUDE_DIR_NAMES for part in p.relative_to(ROOT).parts)
    ]


def adr_basename_index(files: list[str]) -> set[str]:
    """Basenames (lowercase, no extension) of markdown files under docs/**,
    adrs/**, and the repo root — where a `[[wikilink]]` target resolves in
    this vault."""
    index = set()
    for rel in files:
        if rel.startswith("docs/") or rel.startswith("adrs/") or "/" not in rel:
            index.add(Path(rel).stem.lower())
    return index


def test_every_adr_wikilink_resolves_to_a_real_file() -> None:
    files = tracked_markdown_files()
    assert files, "expected at least one tracked markdown file"
    index = adr_basename_index(files)
    assert "adr-00-adr-doctrine" in index, "sanity: the ADR index looks empty"

    for rel in files:
        if rel in EXCLUDED_FILES:
            continue
        if not (ROOT / rel).is_file():
            continue
        text = (ROOT / rel).read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            for match in WIKILINK.finditer(line):
                target = match.group(1).strip()
                if not ADR_SHAPED.match(target):
                    continue
                if target.lower() in SUPERSEDED_ADR_STEMS:
                    continue
                if target.lower() not in index:
                    fail(
                        f"{rel}:{lineno}: [[{target}]] has no matching "
                        f"adrs/{target}.md — dead ADR link"
                    )


def main() -> int:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    if failures:
        for message in failures:
            print(f"FAIL: {message}")
        print(f"\n{len(failures)} dead ADR-shaped wikilink(s)")
        return 1
    print("ok  every ADR-shaped wikilink resolves to a real ADR file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
