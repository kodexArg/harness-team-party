#!/usr/bin/env python3
"""Guard the Paladin test-after path and Adventurer's bounded lease."""

from __future__ import annotations

import re
import sys
from itertools import product
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
    return tools


def body_section(body: str, heading: str, next_heading: str) -> str:
    match = re.search(
        rf"^{re.escape(heading)}\n(.*?)(?=^{re.escape(next_heading)}\n)",
        body,
        re.MULTILINE | re.DOTALL,
    )
    assert match, f"missing section {heading}"
    return match.group(1)


def test_paladin_frontmatter_is_closed_and_graphify_first() -> None:
    frontmatter, _ = agent_parts("hb-ag-paladin")
    tools = assert_closed_frontmatter("hb-ag-paladin", frontmatter)
    assert tools.count("Agent") == 1, "Paladin needs exactly one Agent capability"


def test_paladin_scope_and_test_after_handoff() -> None:
    _, body = agent_parts("hb-ag-paladin")
    area = body_section(body, "## Area", "## Does")
    does = body_section(body, "## Does", "## Does not")

    assert "framework-neutral Python business rules and complex Python scripts" in area
    for forbidden_dependency in (
        "Django",
        "web framework",
        "ORM",
        "HTTP",
        "UI code",
        "cloud clients",
        "deployment state",
    ):
        assert forbidden_dependency in area

    targets = re.findall(r"\*\*May Agent:\*\*\s*`([^`]+)`", area)
    assert targets == ["hb-ag-test"], f"Paladin Agent targets changed: {targets}"
    assert "after implementation only" in area
    assert "No other stem." in area
    assert "never Agent The Cleric or The Elf" in area
    assert "You do not write tests or `docs/tdds/`." in area
    assert "Implement first." in does
    assert "tests are written **after** the implementation" in does


def test_adventurer_frontmatter_is_closed_without_agent_tool() -> None:
    frontmatter, _ = agent_parts("hb-ag-adventurer")
    tools = assert_closed_frontmatter("hb-ag-adventurer", frontmatter)
    assert "Agent" not in tools, "Adventurer must remain a single-agent lane"


def test_adventurer_score_gate_allows_only_four_shapes() -> None:
    _, body = agent_parts("hb-ag-adventurer")
    area = body_section(body, "## Area", "## Does")

    score_range = re.search(
        r"`severity`, `collateral`, and `effort` each have exactly one "
        r"integer score from (\d)[–-](\d)",
        area,
    )
    assert score_range, "Adventurer needs one integer score on every named axis"
    gate = re.search(
        r"sum is \*\*less than (\d+)\*\* and no score exceeds \*\*(\d+)\*\*",
        area,
    )
    assert gate, "Adventurer score gate is missing its total or per-axis bound"

    low, high = map(int, score_range.groups())
    total_limit, axis_limit = map(int, gate.groups())
    eligible = {
        scores
        for scores in product(range(low, high + 1), repeat=3)
        if sum(scores) < total_limit and max(scores) <= axis_limit
    }
    expected = {
        (1, 1, 1),
        (2, 1, 1),
        (1, 2, 1),
        (1, 1, 2),
    }
    assert eligible == expected, f"Adventurer score shapes changed: {sorted(eligible)}"
    assert "`1/1/1`" in area
    assert "permutations of `2/1/1`" in area


def test_dwarf_carries_tdd_adr_with_paladin() -> None:
    dwarf_fm, _ = agent_parts("hb-ag-service")
    paladin_fm, _ = agent_parts("hb-ag-paladin")
    adr = (ROOT / "adrs" / "adr-03.b-tdd.md").read_text(encoding="utf-8")
    assert re.search(r"^  - adr-03\.b-tdd\s*$", dwarf_fm, re.MULTILINE)
    assert re.search(r"^  - adr-03\.b-tdd\s*$", paladin_fm, re.MULTILINE)
    assert "hb-ag-service" in adr
    assert "hb-ag-paladin" in adr


def test_agent_frontmatter_is_not_the_docs_key_set() -> None:
    adr = (ROOT / "adrs" / "adr-00.a-adr-frontmatter.md").read_text(
        encoding="utf-8"
    )
    assert "Agent definition contract" in adr
    assert (
        "`name`, `description`, `model`, `color`, `tools`, and `related_adrs`"
        in adr
    )
    loop = (ROOT / "docs" / "DEVELOPMENT-LOOP.md").read_text(encoding="utf-8")
    assert "orphan PR is valid under [[adr-08-github]]" in loop
    assert "it is not a prerequisite for a PR" in loop


def test_adventurer_lease_keeps_context_and_governed_boundaries() -> None:
    _, body = agent_parts("hb-ag-adventurer")
    first_act = body_section(body, "## First act", "## Area")
    area = body_section(body, "## Area", "## Does")

    assert "broadest practical context" in first_act
    assert "**default (medium) effort**" in first_act
    assert "production code, test code" in area
    assert "**one eligible task**" in area
    assert "temporary, mutually exclusive task lease" in area

    for excluded in (
        "`docs/INTERFACES.md`",
        "`docs/contracts/`",
        "`adrs/`",
        "Git/GitHub state",
        "secret values",
        "deployment state",
    ):
        assert excluded in area, f"Adventurer lease no longer excludes {excluded}"


def main() -> int:
    tests = (
        test_paladin_frontmatter_is_closed_and_graphify_first,
        test_paladin_scope_and_test_after_handoff,
        test_adventurer_frontmatter_is_closed_without_agent_tool,
        test_adventurer_score_gate_allows_only_four_shapes,
        test_dwarf_carries_tdd_adr_with_paladin,
        test_agent_frontmatter_is_not_the_docs_key_set,
        test_adventurer_lease_keeps_context_and_governed_boundaries,
    )
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as exc:
            print(f"FAIL: {test.__name__}: {exc}", file=sys.stderr)
            failed += 1
        else:
            print(f"ok  {test.__name__}")

    if failed:
        print(f"\n{failed} test(s) failed", file=sys.stderr)
        return 1
    print(f"\nall {len(tests)} test(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
