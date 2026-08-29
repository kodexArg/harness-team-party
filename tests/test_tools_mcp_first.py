"""Any tools: allowlist lists Graphify MCP before Read and Glob."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP_FIRST = ["query_graph", "get_neighbors", "get_node", "shortest_path"]
TOOLS_BLOCK = re.compile(r"^tools:\n((?:\s+- .+\n)+)", re.MULTILINE)


def allowlists() -> list[tuple[Path, list[str]]]:
    paths = list((ROOT / "agents").glob("*.md"))
    paths.extend((ROOT / "skills").glob("*/SKILL.md"))
    found: list[tuple[Path, list[str]]] = []
    for path in sorted(paths):
        if path.name == ".gitkeep":
            continue
        text = path.read_text(encoding="utf-8")
        block = TOOLS_BLOCK.search(text)
        if not block:
            continue
        names = [line.strip().lstrip("- ").strip() for line in block.group(1).splitlines() if line.strip()]
        found.append((path, names))
    return found


def test_declared_tools_put_graphify_mcp_before_read_and_glob() -> None:
    rows = allowlists()
    assert rows, "no tools: allowlists found under agents/ or skills/"
    for path, names in rows:
        rel = path.relative_to(ROOT).as_posix()
        assert names[:4] == MCP_FIRST, f"{rel} tools: must start with Graphify MCP: {names[:8]}"
        if "Read" in names:
            assert names.index("Read") > 3, f"{rel} lists Read before Graphify MCP"
        if "Glob" in names:
            assert names.index("Glob") > 3, f"{rel} lists Glob before Graphify MCP"
            if "Read" in names:
                assert names.index("Glob") > names.index("Read"), f"{rel} lists Glob before Read"


def main() -> int:
    try:
        test_declared_tools_put_graphify_mcp_before_read_and_glob()
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1
    print("ok  Graphify MCP precedes Read and Glob on every tools: allowlist")
    return 0


if __name__ == "__main__":
    sys.exit(main())
