#!/usr/bin/env python3
"""Guard The Owl and The Crow web-scout contracts and OWL-INDEX coverage."""

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
FORBIDDEN_TOOLS = ("Agent", "Write", "Edit")


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


def assert_closed_frontmatter(stem: str, frontmatter: str) -> list[str]:
    keys = re.findall(
        r"^([a-z][a-z0-9_]*):(?:\s|$)",
        frontmatter,
        re.MULTILINE,
    )
    assert len(keys) == len(AGENT_KEYS) and set(keys) == AGENT_KEYS, (
        f"{stem} frontmatter keys must be exactly {sorted(AGENT_KEYS)}, got {keys}"
    )
    assert re.search(rf"^name:\s*{re.escape(stem)}\s*$", frontmatter, re.MULTILINE)
    assert re.search(r"^model:\s*inherit\s*$", frontmatter, re.MULTILINE)

    tools = frontmatter_tools(frontmatter)
    assert tools[:4] == list(GRAPHIFY_FIRST), (
        f"{stem} must list Graphify first, got {tools[:4]}"
    )
    assert tools.index("Read") > 3
    assert tools.index("Glob") > tools.index("Read")
    for forbidden in FORBIDDEN_TOOLS:
        assert forbidden not in tools, f"{stem} must not have the {forbidden} tool"
    return tools


def requirements_pin_names() -> list[str]:
    text = (ROOT / "docs" / "REQUIREMENTS.md").read_text(encoding="utf-8")
    names: list[str] = []
    for match in re.finditer(
        r"^\| ([^|]+) \| [^|]+ \|",
        text,
        re.MULTILINE,
    ):
        cell = match.group(1).strip()
        if cell in {"Tool", "Package", "Pin"}:
            continue
        if cell.startswith("-") or set(cell) <= {"-", " "}:
            continue
        names.append(cell)
    return names


def test_owl_frontmatter_and_tools() -> None:
    frontmatter, body = agent_parts("hb-ag-owl")
    assert_closed_frontmatter("hb-ag-owl", frontmatter)
    assert "You are **The Owl** (`hb-ag-owl`)" in body
    assert "OWL-INDEX" in body


def test_crow_frontmatter_and_tools() -> None:
    frontmatter, body = agent_parts("hb-ag-crow")
    assert_closed_frontmatter("hb-ag-crow", frontmatter)
    assert "You are **The Crow** (`hb-ag-crow`)" in body
    assert "kamikaze" in body.lower()


def test_owl_skill_contract() -> None:
    skill_path = ROOT / "skills" / "hb-sk-owl" / "SKILL.md"
    assert skill_path.is_file(), "skills/hb-sk-owl/SKILL.md is missing"
    text = skill_path.read_text(encoding="utf-8")
    assert "OWL-INDEX" in text
    assert "index-first" in text.lower() or "Index first" in text
    assert "Markdown Findings Report" in text
    assert "Sources & Citations" in text
    assert "Key Findings" in text
    assert "Index miss" in text


def test_crow_skill_contract() -> None:
    skill_path = ROOT / "skills" / "hb-sk-crow" / "SKILL.md"
    assert skill_path.is_file(), "skills/hb-sk-crow/SKILL.md is missing"
    text = skill_path.read_text(encoding="utf-8")
    assert "kamikaze" in text.lower()
    assert "unofficial" in text.lower()
    assert "hearsay" in text.lower() or "source-trust" in text.lower() or "trust:" in text
    assert "Markdown Findings Report" in text
    assert "Sources & Citations" in text
    assert "Key Findings" in text
    assert "paywall" in text.lower() or "authentication" in text.lower()


def test_owl_index_covers_requirements_pins() -> None:
    index = (ROOT / "docs" / "OWL-INDEX.md").read_text(encoding="utf-8")
    pins = requirements_pin_names()
    assert pins, "REQUIREMENTS.md has no pin rows"
    missing = [name for name in pins if f"| {name} |" not in index]
    assert not missing, f"OWL-INDEX.md missing REQUIREMENTS pins: {missing}"


def main() -> int:
    test_owl_frontmatter_and_tools()
    test_crow_frontmatter_and_tools()
    test_owl_skill_contract()
    test_crow_skill_contract()
    test_owl_index_covers_requirements_pins()
    print("all 5 Owl/Crow contract test(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
