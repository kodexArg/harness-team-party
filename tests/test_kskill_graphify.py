"""kskill-graphify is vendored with real update scripts.

docs/HARNESS.md is the SSOT of what the harness is:
a vendored skill absent from that table is not part of it. Scripts
are the update mechanism — not npx, not a second skill.
"""

from __future__ import annotations

import json
import os
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "kskill-graphify" / "SKILL.md"
LINKED = ROOT / ".claude" / "skills" / "kskill-graphify" / "SKILL.md"
BIN = ROOT / "skills" / "kskill-graphify" / "bin"
HARNESS = ROOT / "docs" / "HARNESS.md"
GLOSSARY = ROOT / "docs" / "GLOSSARY.md"
GRAPHIFY = ROOT / "docs" / "GRAPHIFY.md"
GRAPH_JSON = ROOT / "skills" / "kskill-graphify" / "graphify-out" / "graph.json"
HOOK = ROOT / ".cursor" / "hooks" / "graphify-ensure.py"
HOOKS_JSON = ROOT / ".cursor" / "hooks.json"
CLOUD_SETUP = ROOT / "scripts" / "cloud_setup.sh"
SCRIPTS = ("ensure", "extract", "update-graph", "upgrade-cli", "fetch-upstream")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def test_skill_exists_and_links() -> None:
    if not SKILL.is_file():
        fail("skills/kskill-graphify/SKILL.md is missing")
    head = SKILL.read_text(encoding="utf-8").split("\n---", 1)[0]
    if "name: kskill-graphify" not in head:
        fail("skill frontmatter name is not kskill-graphify")
    if not LINKED.is_file():
        fail(".claude/skills/kskill-graphify/SKILL.md does not resolve")
    if LINKED.resolve() != SKILL.resolve():
        fail("kskill-graphify is a second copy, not the skills/ link")
    ok("kskill-graphify exists on the skills link")


def test_scripts_are_real_and_executable() -> None:
    for name in SCRIPTS:
        path = BIN / name
        if not path.is_file():
            fail(f"missing script skills/kskill-graphify/bin/{name}")
        mode = path.stat().st_mode
        if not (mode & stat.S_IXUSR):
            fail(f"skills/kskill-graphify/bin/{name} is not executable")
    ensure = (BIN / "ensure").read_text(encoding="utf-8")
    extract = (BIN / "extract").read_text(encoding="utf-8")
    update = (BIN / "update-graph").read_text(encoding="utf-8")
    upgrade = (BIN / "upgrade-cli").read_text(encoding="utf-8")
    fetch = (BIN / "fetch-upstream").read_text(encoding="utf-8")
    if "uv tool install" not in ensure or "graphifyy" not in ensure:
        fail("ensure does not install graphifyy via uv")
    if "--code-only" not in ensure:
        fail("ensure does not extract --code-only when graph.json is missing")
    if "graphify extract" not in extract:
        fail("extract does not call graphify extract")
    if "bin/ensure" not in update:
        fail("update-graph does not fall back to ensure when the graph is missing")
    if "--code-only" not in update or "--out" not in update:
        fail("update-graph does not refresh with extract --code-only --out")
    if "uv tool install --upgrade" not in upgrade or "graphifyy" not in upgrade:
        fail("upgrade-cli does not upgrade graphifyy via uv")
    if "raw.githubusercontent.com/Graphify-Labs/graphify" not in fetch:
        fail("fetch-upstream does not curl the official skill")
    if "npx" in fetch:
        fail("fetch-upstream uses npx")
    ok("the five scripts are executable and call the real CLIs")


def test_skill_forbids_npx_and_add_url() -> None:
    text = SKILL.read_text(encoding="utf-8")
    if "npx skills add" not in text:
        fail("skill does not forbid npx skills add")
    if "graphify add <url>" not in text:
        fail("skill does not forbid graphify add <url>")
    if "Commit `graphify-out/cache/`" not in text:
        fail("skill does not forbid committing the cache")
    ok("skill forbids npx, graphify add, and cache commits")


def test_graph_is_tracked_cache_is_not() -> None:
    link = ROOT / "graphify-out"
    if not link.is_symlink():
        fail("repo-root graphify-out is not a symlink")
    if os.readlink(link) != "skills/kskill-graphify/graphify-out":
        fail(f"graphify-out symlink target is {os.readlink(link)!r}")
    gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    if "skills/kskill-graphify/graphify-out/*" not in gitignore:
        fail(".gitignore does not ignore graphify-out artifacts")
    if "!skills/kskill-graphify/graphify-out/graph.json" not in gitignore:
        fail(".gitignore does not un-ignore graph.json")
    if "!skills/kskill-graphify/graphify-out/manifest.json" not in gitignore:
        fail(".gitignore does not un-ignore manifest.json")
    ignore = (ROOT / ".graphifyignore").read_text(encoding="utf-8")
    if "node_modules/" not in ignore or ".venv/" not in ignore:
        fail(".graphifyignore does not exclude build/virtualenv artifacts")
    if not GRAPH_JSON.is_file():
        fail("tracked graph.json is missing")
    payload = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))
    if not payload.get("nodes"):
        fail("graph.json has no nodes")
    ok("graph.json is tracked; cache is ignored; build artifacts are out")


def test_session_start_and_cloud_setup_call_ensure() -> None:
    if not HOOK.is_file():
        fail(".cursor/hooks/graphify-ensure.py is missing")
    mode = HOOK.stat().st_mode
    if not (mode & stat.S_IXUSR):
        fail(".cursor/hooks/graphify-ensure.py is not executable")
    hook = HOOK.read_text(encoding="utf-8")
    if "bin/ensure" not in hook:
        fail("sessionStart hook does not call bin/ensure")
    hooks_json = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
    start = hooks_json.get("hooks", {}).get("sessionStart", [])
    commands = [item.get("command") for item in start]
    if ".cursor/hooks/graphify-ensure.py" not in commands:
        fail(".cursor/hooks.json does not register graphify-ensure.py on sessionStart")
    setup = CLOUD_SETUP.read_text(encoding="utf-8")
    if "skills/kskill-graphify/bin/ensure" not in setup:
        fail("cloud_setup.sh does not call bin/ensure")
    ok("sessionStart and cloud_setup call ensure")


def test_harness_glossary_graphify_rows() -> None:
    harness = HARNESS.read_text(encoding="utf-8")
    row = next((line for line in harness.splitlines() if line.startswith("| `kskill-graphify`")), None)
    if row is None or row.count("|") < 4:
        fail("docs/HARNESS.md has no complete kskill-graphify row")
    glossary = GLOSSARY.read_text(encoding="utf-8")
    if "| Graphify skill |" not in glossary:
        fail("docs/GLOSSARY.md has no Graphify skill row")
    facts = GRAPHIFY.read_text(encoding="utf-8")
    for name in SCRIPTS:
        if name not in facts:
            fail(f"docs/GRAPHIFY.md does not name {name}")
    ok("HARNESS, GLOSSARY, and GRAPHIFY name the skill and scripts")


def main() -> int:
    if not SKILL.is_file():
        print("skip  kskill-graphify is not vendored")
        return 0
    tests = [
        test_skill_exists_and_links,
        test_scripts_are_real_and_executable,
        test_skill_forbids_npx_and_add_url,
        test_graph_is_tracked_cache_is_not,
        test_session_start_and_cloud_setup_call_ensure,
        test_harness_glossary_graphify_rows,
    ]
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
