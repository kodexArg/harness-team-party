from __future__ import annotations

import inspect
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"


def test_guardians_declare_unavailable_status() -> None:
    """A guardian whose declared tools are absent returns unavailable, never a verdict."""
    guardians = ["kbot-prd.md", "kbot-adr.md", "kbot-api.md"]
    for g in guardians:
        path = AGENTS_DIR / g
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        assert "unavailable" in content, f"{g} must document status: unavailable"
        assert "TOOL UNAVAILABLE:" in content, f"{g} must specify cause starting with TOOL UNAVAILABLE:"


def test_familiars_declare_unavailable_status() -> None:
    """Familiars of kwf and kwf-cloud casts specify unavailable when their read tools are absent."""
    familiars = [
        "kwf-prd.md",
        "kwf-adr.md",
        "kwf-api.md",
        "kwf-cloud-prd.md",
        "kwf-cloud-adr.md",
        "kwf-cloud-api.md",
    ]
    for f in familiars:
        path = AGENTS_DIR / f
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        assert "unavailable" in content, f"{f} must document unavailable status"
        assert "TOOL UNAVAILABLE:" in content, f"{f} must specify cause starting with TOOL UNAVAILABLE:"


def test_unavailable_is_never_treated_as_a_verdict_by_gate() -> None:
    """The merge gate parser must treat unavailable as not run, never as pass or fail."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("check_merge_gate", ROOT / "scripts" / "check_merge_gate.py")
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)

    for g in ("kbot-prd", "kbot-adr", "kbot-api"):
        assert g not in gate.recorded_verdicts(f"Guardian-Verdict: {g}: unavailable\n")

    for ssot in ("prd", "adr", "api"):
        assert gate.SSOT_GUARDIAN[ssot] not in gate.recorded_verdicts(f"Plan-Verdict: {ssot}: unavailable\n")


def test_doctrine_judges_have_a_read_path_that_survives_the_mcp() -> None:
    """Every doctrine judge must hold Read: a judge that cannot open its SSOT and
    rules anyway returns a verdict shaped exactly like a real one (#598)."""
    judges = [
        "kbot-prd.md",
        "kbot-adr.md",
        "kbot-api.md",
        "kwf-prd.md",
        "kwf-adr.md",
        "kwf-api.md",
        "kwf-cloud-prd.md",
        "kwf-cloud-adr.md",
        "kwf-cloud-api.md",
    ]
    for name in judges:
        path = AGENTS_DIR / name
        if not path.is_file():
            continue
        tools = declared_tools(path)
        assert "Read" in tools, f"{name} has no Read: it cannot open its SSOT at all"


def declared_tools(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    block = re.search(r"^tools:\n((?:\s+- .+\n)+)", text, re.MULTILINE)
    assert block, f"{path.name} declares no block-sequence tools list"
    return [line.strip().lstrip("- ").strip() for line in block.group(1).splitlines()]


def main():
    """CI runs each test file as `python3 tests/test_<x>.py` (.github/workflows/ci.yml).
    Without this, the file defined its tests and ran none — green by not running (#597)."""
    import tempfile

    failed = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_"):
            continue
        params = inspect.signature(fn).parameters
        try:
            if "tmp_path" in params:
                with tempfile.TemporaryDirectory() as tmp:
                    fn(Path(tmp))
            else:
                fn()
        except Exception as exc:
            print(f"FAIL: {name}: {exc}", file=sys.stderr)
            failed += 1
        else:
            print(f"ok  {name}")

    if failed:
        print(f"\n{failed} test(s) failed", file=sys.stderr)
        return 1
    print("\nall test(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
