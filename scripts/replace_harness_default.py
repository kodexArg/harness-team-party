#!/usr/bin/env python3
"""
Deterministic script to replace all occurrences of 'harness-default'
with 'harness-team-party' across all text files in the repository.
"""
from __future__ import annotations

import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EXCLUDE_DIRS = {".git", ".venv", "__pycache__", "node_modules", "dist", ".obsidian"}

OLD_TERM = "harness-default"
NEW_TERM = "harness-team-party"


def is_text_file(filepath: Path) -> bool:
    try:
        with open(filepath, "rb") as f:
            chunk = f.read(1024)
            if b"\x00" in chunk:
                return False
        return True
    except Exception:
        return False


def run_replacement() -> dict[str, int]:
    modifications: dict[str, int] = {}
    self_path = Path(__file__).resolve()

    for root, dirs, files in os.walk(REPO_ROOT):
        # Prune excluded directories in-place deterministically
        dirs[:] = sorted([d for d in dirs if d not in EXCLUDE_DIRS])

        for fname in sorted(files):
            fpath = Path(root) / fname
            if not fpath.is_file() or fpath.is_symlink() or fpath.resolve() == self_path:
                continue

            if not is_text_file(fpath):
                continue

            try:
                content = fpath.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            if OLD_TERM in content:
                count = content.count(OLD_TERM)
                new_content = content.replace(OLD_TERM, NEW_TERM)
                fpath.write_text(new_content, encoding="utf-8")
                relpath = str(fpath.relative_to(REPO_ROOT))
                modifications[relpath] = count

    return modifications


def main() -> None:
    print(f"Scanning repository at: {REPO_ROOT}")
    print(f"Replacing '{OLD_TERM}' -> '{NEW_TERM}' deterministically...\n")

    mods = run_replacement()

    if not mods:
        print(f"No occurrences of '{OLD_TERM}' found.")
    else:
        print("Replacements applied:")
        total = 0
        for path, count in sorted(mods.items()):
            print(f"  - {path}: {count} replacement(s)")
            total += count
        print(f"\nTotal replacements: {total} in {len(mods)} file(s).")


if __name__ == "__main__":
    main()
