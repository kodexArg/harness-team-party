#!/usr/bin/env python3
"""Guard: relationship docs list the live 12-agent party, no retired titles."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ROSTER = (
    ("hb-ag-contracts", "The Cleric"),
    ("hb-ag-service", "The Dwarf"),
    ("hb-ag-paladin", "The Paladin"),
    ("hb-ag-surface", "The Elf"),
    ("hb-ag-ops", "The Wizard"),
    ("hb-ag-judge", "The Inquisitor"),
    ("hb-ag-test", "The Trickster"),
    ("hb-ag-adventurer", "The Adventurer"),
    ("hb-ag-git", "The Bard"),
    ("hb-ag-hunter", "The Hunter"),
    ("hb-ag-hawk", "The Hawk"),
    ("hb-ag-hound", "The Hound"),
)

DOC_PATHS = (
    ROOT / "docs" / "ADND-AGENTS.md",
    ROOT / "docs" / "ADND-DISPATCH.md",
    ROOT / "docs" / "HARNESS.md",
    ROOT / "AGENTS.md",
)

LIVE_ARCHER = re.compile(
    r"(\| The Archer \||title \*\*The Archer\*\*|You are \*\*The Archer\*\*|"
    r"`hb-ag-contracts` \(The Archer\)|Knows: Archer)"
)
LIVE_WARRIOR = re.compile(
    r"(\| The Warrior \||title \*\*The Warrior\*\*|You are \*\*The Warrior\*\*|"
    r"`hb-ag-surface` \(The Warrior\)|The Warrior 🗡️)"
)

REQUIRED_HEADINGS = (
    "## First act",
    "## Area",
    "## Does",
    "## Does not",
    "## Quick exit",
)

GRAPHIFY_FIRST = (
    "query_graph",
    "get_neighbors",
    "get_node",
    "shortest_path",
)

failures = 0


def fail(msg: str) -> None:
    global failures
    failures += 1
    print(f"FAIL: {msg}", file=sys.stderr)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def main() -> int:
    for path in DOC_PATHS:
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        if LIVE_ARCHER.search(text):
            fail(f"{rel} still treats The Archer as a live title")
        if LIVE_WARRIOR.search(text):
            fail(f"{rel} still treats The Warrior as a live title")
        for stem, title in ROSTER:
            if stem not in text:
                fail(f"{rel} is missing stem {stem}")
            if title not in text:
                fail(f"{rel} is missing title {title}")

    agents = ROOT / "agents"
    for stem, title in ROSTER:
        path = agents / f"{stem}.md"
        rel = path.relative_to(ROOT).as_posix()
        if not path.is_file():
            fail(f"{rel} is missing")
            continue
        text = path.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if re.search(r"teammate\s*:", fm):
            fail(f"{rel} declares itself a teammate")
        if not re.search(r"^model:\s*inherit\s*$", fm, re.MULTILINE):
            fail(f"{rel} does not bind model: inherit")
        if f"You are **{title}** (`{stem}`)" not in text:
            fail(f"{rel} does not open as You are **{title}** (`{stem}`)")
        if LIVE_ARCHER.search(text):
            fail(f"{rel} still treats The Archer as a live title")
        if LIVE_WARRIOR.search(text):
            fail(f"{rel} still treats The Warrior as a live title")
        for heading in REQUIRED_HEADINGS:
            if heading not in text:
                fail(f"{rel} is missing {heading}")
        tools_match = re.search(r"^tools:\n((?:  - .+\n)+)", fm, re.MULTILINE)
        tools = (
            re.findall(r"^  - (\S+)\s*$", tools_match.group(1), re.MULTILINE)
            if tools_match
            else []
        )
        if tools[:4] != list(GRAPHIFY_FIRST):
            fail(f"{rel} tools: must list Graphify four first, got {tools[:4]!r}")

    if not failures:
        ok("roster docs list twelve stems and titles; no live Archer or Warrior")
        ok("twelve agent files: inherit, You are The X, church headings, Graphify first")
        print("\nall 2 test(s) passed")
        return 0
    print(f"\n{failures} test(s) failed", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
