"""sessionStart load-hook injects PRD, then ADRs, then docs/ recursively."""

from __future__ import annotations

import importlib.util
import json
import stat
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOK = ROOT / ".cursor" / "hooks" / "load-hook.py"
HOOKS_JSON = ROOT / ".cursor" / "hooks.json"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def load_hook():
    spec = importlib.util.spec_from_file_location("load_hook", HOOK)
    if spec is None or spec.loader is None:
        fail("cannot load .cursor/hooks/load-hook.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_hook_is_registered_first() -> None:
    if not HOOK.is_file():
        fail(".cursor/hooks/load-hook.py is missing")
    if not (HOOK.stat().st_mode & stat.S_IXUSR):
        fail(".cursor/hooks/load-hook.py is not executable")
    payload = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
    start = payload.get("hooks", {}).get("sessionStart", [])
    commands = [item.get("command") for item in start]
    if not commands or commands[0] != ".cursor/hooks/load-hook.py":
        fail("load-hook.py is not first on sessionStart")
    ok("load-hook is first on sessionStart")


def test_paths_are_discovered_not_hardcoded() -> None:
    source = HOOK.read_text(encoding="utf-8")
    if "adr-07" in source or "GLOSSARY.md" in source or "API.md" in source:
        fail("load-hook hardcodes a discovered SSOT filename")
    if 'Path("docs") / "PRD.md"' not in source:
        fail("load-hook does not hardcode docs/PRD.md")
    if 'Path("adrs")' not in source or 'Path("docs")' not in source:
        fail("load-hook does not hardcode the adrs/ and docs/ roots")
    ok("only PRD.md, adrs/, and docs/ are hardcoded")


def test_order_on_a_synthetic_tree(tmp_path: Path) -> None:
    hook = load_hook()
    docs = tmp_path / "docs"
    adrs = tmp_path / "adrs"
    (docs / "nested").mkdir(parents=True)
    (adrs / "nested").mkdir(parents=True)
    (docs / "PRD.md").write_text("PRD-BODY\n", encoding="utf-8")
    (docs / "later.md").write_text("DOC-BODY\n", encoding="utf-8")
    (docs / "nested" / "deep.md").write_text("DEEP\n", encoding="utf-8")
    (adrs / "adr-99-example.md").write_text("ADR-BODY\n", encoding="utf-8")
    (adrs / "nested" / "extra.md").write_text("ADR-NEST\n", encoding="utf-8")
    rels = [p.relative_to(tmp_path).as_posix() for p in hook.ssot_files(tmp_path)]
    if rels[0] != "docs/PRD.md":
        fail(f"first file is {rels[0]!r}, not docs/PRD.md")
    adrs_rels = [r for r in rels if r.startswith("adrs/")]
    docs_rels = [r for r in rels if r.startswith("docs/") and r != "docs/PRD.md"]
    if rels[1 : 1 + len(adrs_rels)] != adrs_rels:
        fail("ADR files are not a contiguous block after PRD")
    if rels[1 + len(adrs_rels) :] != docs_rels:
        fail("docs/ files are not after the ADR block")
    if "docs/PRD.md" in docs_rels or rels.count("docs/PRD.md") != 1:
        fail("PRD.md is duplicated in the docs walk")
    if "adrs/nested/extra.md" not in rels or "docs/nested/deep.md" not in rels:
        fail("recursive files were not discovered")
    ok("order is PRD, then adrs/**, then docs/** without a second PRD")


def test_repo_payload_contains_cowsay_and_discovered_files() -> None:
    hook = load_hook()
    files = hook.ssot_files(ROOT)
    if not files or files[0] != ROOT / "docs" / "PRD.md":
        fail("repo walk does not start at docs/PRD.md")
    adrs = list((ROOT / "adrs").rglob("*"))
    adrs_files = sorted(p for p in adrs if p.is_file())
    docs_files = sorted(p for p in (ROOT / "docs").rglob("*") if p.is_file())
    expected = 1 + len(adrs_files) + (len(docs_files) - 1)
    if len(files) != expected:
        fail(f"walked {len(files)} files, expected {expected}")
    context = hook.build_context(ROOT)
    if "SSoT Loaded into context" not in context:
        fail("cowsay banner is missing from additional_context")
    prd = (ROOT / "docs" / "PRD.md").read_text(encoding="utf-8")
    if prd.strip() and prd.splitlines()[0] not in context:
        fail("PRD.md body is missing from additional_context")
    sample_adr = adrs_files[0]
    sample_doc = next(p for p in docs_files if p.name != "PRD.md")
    if f"===== {sample_adr.relative_to(ROOT).as_posix()} =====" not in context:
        fail("an ADR filename header is missing")
    if f"===== {sample_doc.relative_to(ROOT).as_posix()} =====" not in context:
        fail("a docs/ filename header is missing")
    ok("payload has cowsay, PRD, discovered ADRs, and discovered docs")


def main() -> int:
    import tempfile

    if not HOOK.is_file():
        print("skip  .cursor/hooks/load-hook.py is not in this worktree")
        return 0

    tests = [
        test_hook_is_registered_first,
        test_paths_are_discovered_not_hardcoded,
        test_repo_payload_contains_cowsay_and_discovered_files,
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
    try:
        with tempfile.TemporaryDirectory() as tmp:
            test_order_on_a_synthetic_tree(Path(tmp))
    except AssertionError:
        failed += 1
    except Exception as exc:
        print(f"FAIL: test_order_on_a_synthetic_tree: {exc}", file=sys.stderr)
        failed += 1
    else:
        pass
    total = len(tests) + 1
    if failed:
        print(f"\n{failed} test(s) failed", file=sys.stderr)
        return 1
    print(f"\nall {total} test(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
