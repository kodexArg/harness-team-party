#!/usr/bin/env python3
"""Guard The Liturgist mock: authoring contract, not a live worker."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENT_KEYS = {
    "name",
    "description",
    "model",
    "color",
    "tools",
    "related_adrs",
}
GRAPHIFY_FIRST = (
    "query_graph",
    "get_neighbors",
    "get_node",
    "shortest_path",
)
FORBIDDEN_TOOLS = ("Agent", "Write", "Edit", "Bash")
LIVE_STEMS = (
    "hb-ag-contracts",
    "hb-ag-service",
    "hb-ag-paladin",
    "hb-ag-surface",
    "hb-ag-ops",
    "hb-ag-judge",
    "hb-ag-test",
    "hb-ag-adventurer",
    "hb-ag-git",
    "hb-ag-hunter",
    "hb-ag-hawk",
    "hb-ag-hound",
    "hb-ag-owl",
    "hb-ag-crow",
)
ROSTER_TITLES = (
    "The Cleric",
    "The Dwarf",
    "The Paladin",
    "The Elf",
    "The Wizard",
    "The Inquisitor",
    "The Trickster",
    "The Adventurer",
    "The Bard",
    "The Hunter",
    "The Hawk",
    "The Hound",
    "The Owl",
    "The Crow",
)


def agent_parts(stem: str) -> tuple[str, str]:
    path = ROOT / "agents" / f"{stem}.md"
    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n"), f"{path.relative_to(ROOT)} has no frontmatter"
    end = text.find("\n---\n", 4)
    assert end != -1, f"{path.relative_to(ROOT)} has unclosed frontmatter"
    return text[4:end], text[end + 5 :]


def frontmatter_tools(frontmatter: str) -> list[str]:
    match = re.search(r"^tools:\n((?:  - .+\n?)+)", frontmatter, re.MULTILINE)
    assert match, "frontmatter has no tools block"
    return re.findall(r"^  - (\S+)\s*$", match.group(1), re.MULTILINE)


def test_liturgist_frontmatter_and_tools() -> None:
    frontmatter, body = agent_parts("hb-ag-liturgy")
    keys = re.findall(r"^([a-z][a-z0-9_]*):(?:\s|$)", frontmatter, re.MULTILINE)
    assert len(keys) == len(AGENT_KEYS) and set(keys) == AGENT_KEYS
    assert re.search(r"^name:\s*hb-ag-liturgy\s*$", frontmatter, re.MULTILINE)
    assert re.search(r"^model:\s*inherit\s*$", frontmatter, re.MULTILINE)
    tools = frontmatter_tools(frontmatter)
    assert tools[:4] == list(GRAPHIFY_FIRST)
    assert "Read" in tools and tools.index("Read") > 3
    for forbidden in FORBIDDEN_TOOLS:
        assert forbidden not in tools, f"Liturgist must not have {forbidden}"
    assert "You are **The Liturgist** (`hb-ag-liturgy`)" in body
    for heading in (
        "## First act",
        "## Area",
        "## Does",
        "## Does not",
        "## Quick exit",
        "## Liturgy",
    ):
        assert heading in body, f"missing {heading}"
    lower = body.lower()
    assert "never dispatch" in lower or "not a worker" in lower
    assert "mock" in lower
    assert "parenthetical" in lower or "gloss" in lower


def test_liturgy_covers_every_live_agent_bilingual() -> None:
    _, body = agent_parts("hb-ag-liturgy")
    for stem, title in zip(LIVE_STEMS, ROSTER_TITLES, strict=True):
        assert stem in body, f"liturgy missing stem {stem}"
        assert title in body, f"liturgy missing title {title}"
    assert body.count("**EN.**") >= 14
    assert body.count("**ES.**") >= 14
    assert "El Enano" in body
    assert "El Elfo" in body
    assert "El Cazador" in body


def test_liturgist_is_not_on_the_live_roster() -> None:
    roster = (ROOT / "tests" / "test_hb_ag_roster.py").read_text(encoding="utf-8")
    assert '("hb-ag-liturgy", "The Liturgist")' not in roster
    for path in (
        ROOT / "docs" / "ADND-AGENTS.md",
        ROOT / "docs" / "ADND-DISPATCH.md",
    ):
        text = path.read_text(encoding="utf-8")
        assert "hb-ag-liturgy" in text
        assert "never" in text.lower()


def main() -> int:
    test_liturgist_frontmatter_and_tools()
    test_liturgy_covers_every_live_agent_bilingual()
    test_liturgist_is_not_on_the_live_roster()
    print("all 3 Liturgist contract test(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
