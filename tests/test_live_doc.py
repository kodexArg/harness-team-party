"""Harness test for the live-doc linker ([[HARNESS]]).

Asserts the block invariants without re-implementing the linker: no drift, exactly
one block per matched file, wikilinks-only bodies, API cited by the route surface,
and CODEMAP.md in sync. Run: python3 tests/test_live_doc.py
"""
from __future__ import annotations

import ast
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / ".claude" / "skills" / "kskill-live-doc"
LINKER = SKILL / "link.py"
MANIFEST_PATH = SKILL / "manifest.json"
MANIFEST = (
    json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if MANIFEST_PATH.is_file()
    else None
)
START, END = "LIVE-DOC:START", "LIVE-DOC:END"
API_TRIGGERS = ("models.py", "views.py", "viewsets.py", "serializers.py",
                "urls.py", "api_urls.py", "permissions.py")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def block_body(text: str) -> list[str] | None:
    """Return the lines strictly between the START and END markers, or None."""
    lines = text.splitlines()
    s = e = None
    for i, ln in enumerate(lines):
        if START in ln and s is None:
            s = i
        elif END in ln and s is not None:
            e = i
            break
    if s is None or e is None:
        return None
    return lines[s + 1:e]


def matched_files() -> list[Path]:
    from fnmatch import fnmatch
    excl = set(MANIFEST["exclude_dirs"])
    out = []
    for root in MANIFEST["roots"]:
        p = ROOT / root
        cands = [p] if p.is_file() else [f for f in p.rglob("*") if f.is_file()]
        for f in cands:
            if any(part in excl for part in f.parts):
                continue
            if not f.stat().st_size or f.name.endswith(".d.ts"):
                continue
            rel = f.relative_to(ROOT).as_posix()
            if any(fnmatch(rel, r["glob"]) or fnmatch(rel, "**/" + r["glob"])
                   for r in MANIFEST["rules"]):
                out.append(f)
    return out


def load_linker():
    """Import link.py as a module so insert_py can be exercised directly."""
    spec = importlib.util.spec_from_file_location("kdx_live_doc_link", LINKER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


BODY = ["Governed by: [[adr-02-stack]]", "Docs: [[HARNESS]]"]

# name -> (source, carries a module docstring). Every combination of the two
# axes that constrain where the block may go: the docstring slot, which the
# author owns, and `from __future__`, which Python admits only right after it.
PY_FIXTURES: list[tuple[str, str, bool]] = [
    (
        "future import only",
        "from __future__ import annotations\n\nimport os\n",
        False,
    ),
    (
        "docstring only",
        '"""Module docstring."""\n\nimport os\n',
        True,
    ),
    (
        "docstring + future import",
        '"""Module docstring."""\nfrom __future__ import annotations\n\nimport os\n',
        True,
    ),
    (
        "shebang + coding + docstring + future import",
        "#!/usr/bin/env python3\n"
        "# -*- coding: utf-8 -*-\n"
        '"""Multi-line summary.\n\nSecond paragraph of the docstring.\n"""\n'
        "from __future__ import annotations\n\nimport os\n",
        True,
    ),
    ("plain file", "import os\n\nVALUE = 1\n", False),
]


def check_insert_py(link) -> None:
    """insert_py must never break the file it annotates, nor eat its docstring.

    Two defects this pins: a block spliced above `from __future__` is a
    SyntaxError, and a block shaped as a docstring pushes the real one down
    into an unreachable literal — silent, and survivable by a green suite,
    since only ast sees it.
    """
    for name, source, has_doc in PY_FIXTURES:
        expected_doc = ast.get_docstring(ast.parse(source))
        if has_doc and expected_doc is None:
            fail(f"{name}: fixture is meant to carry a docstring but does not")

        result = link.insert_py(source, BODY)

        try:
            tree = ast.parse(result)
        except SyntaxError as exc:
            fail(f"{name}: insert_py produced invalid Python ({exc}):\n{result}")
        if ast.get_docstring(tree) != expected_doc:
            fail(f"{name}: docstring did not survive intact:\n{result}")
        if result.count(START) != 1 or result.count(END) != 1:
            fail(f"{name}: expected exactly one block:\n{result}")
        if "__future__" in source and "__future__" not in result:
            fail(f"{name}: future import lost:\n{result}")
        if source.startswith("#!") and not result.startswith("#!"):
            fail(f"{name}: shebang must stay on line 1:\n{result}")
        if link.insert_py(result, BODY) != result:
            fail(f"{name}: insert_py is not idempotent:\n{result}")
    ok(f"insert_py: {len(PY_FIXTURES)} fixtures parse, keep their docstring, idempotent")


def check_repo_root() -> None:
    """The root resolves identically through skills/ and .claude/skills/."""
    for entry in (ROOT / "skills" / "kskill-live-doc" / "link.py", LINKER):
        module = load_module(entry)
        if module.REPO != ROOT:
            fail(f"{entry}: REPO resolved to {module.REPO}, expected {ROOT}")
    ok("repo root resolves to the repository from both skill paths")


def check_empty_scan_is_a_failure() -> None:
    """Scanning nothing must exit non-zero, never look like a clean tree."""
    module = load_module(LINKER)
    module.MANIFEST = {**module.MANIFEST, "roots": ["no-such-directory"]}
    argv = sys.argv
    sys.argv = [argv[0], "--check"]  # apply mode would rewrite CODEMAP from an empty index
    try:
        module.main()
    except SystemExit as exit_code:
        if exit_code.code:
            ok("a zero-file scan exits non-zero")
            return
    finally:
        sys.argv = argv
    fail("a zero-file scan exited 0, which is indistinguishable from clean")


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(f"linker_{path.parent.name}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    if MANIFEST is None or not LINKER.exists():
        print("skip  kskill-live-doc is not vendored")
        return
    ok("linker present")

    check_repo_root()
    check_empty_scan_is_a_failure()

    check_insert_py(load_linker())

    # 1. No drift — the committed tree matches what the linker would produce.
    r = subprocess.run([sys.executable, str(LINKER), "--check"],
                       capture_output=True, text=True, cwd=ROOT)
    if r.returncode != 0:
        fail(f"live-doc drift — run link.py to re-sync:\n{r.stdout}\n{r.stderr}")
    ok("no drift (link.py --check clean)")

    files = matched_files()
    assert files, "manifest matched zero files"
    ok(f"{len(files)} matched files")

    wikilink = re.compile(r"\[\[[^\]]+\]\]")
    prose_line = re.compile(r"^(Governed by:|Docs:|API:)")
    for f in files:
        text = f.read_text()
        # 2. exactly one block
        if text.count(START) != 1 or text.count(END) != 1:
            fail(f"{f}: expected exactly one live-doc block")
        body = block_body(text)
        # 3. wikilinks only — every body line is a known label line and holds a wikilink
        for ln in body:
            stripped = re.sub(r"^[\s#*/{}<>!-]+", "", ln).rstrip("#-} */>").strip()
            if not stripped:
                continue
            if not prose_line.match(stripped):
                fail(f"{f}: block carries non-link prose: {ln!r}")
            if not wikilink.search(stripped):
                fail(f"{f}: block line without a wikilink: {ln!r}")
        # 4. route surface cites API
        if f.name in API_TRIGGERS and f.as_posix().find("/backend/") != -1:
            if "[[API]]" not in text:
                fail(f"{f}: route-surface file must cite [[API]]")
    ok("every block is wikilinks-only; route surface cites [[API]]")

    # 5. CODEMAP exists and names its governing doc
    codemap = (ROOT / "docs" / "CODEMAP.md").read_text()
    assert "[[HARNESS]]" in codemap, "CODEMAP missing its governing-doc link"
    ok("CODEMAP.md present and linked")

    print("\nALL LIVE-DOC CHECKS PASSED")


if __name__ == "__main__":
    main()
