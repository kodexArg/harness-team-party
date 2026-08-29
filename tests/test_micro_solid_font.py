"""3-row micro-solid font: locked examples and glyph rules."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FONT_PATH = ROOT / "skills" / "kskill-micro-solid-font" / "font.py"
SKILL = ROOT / "skills" / "kskill-micro-solid-font" / "SKILL.md"
HARNESS = ROOT / "docs" / "HARNESS.md"
GLOSSARY = ROOT / "docs" / "GLOSSARY.md"

GOLDENS = {
    "QUICK WIN": (
        "███ █ █ █ ███ █ █    █ █ █ █ ██\n"
        "█ █ █ █ █ █   ██     █ █ █ █ █ █\n"
        " ██ ███ █ ███ █ █     █ █  █ █ █"
    ),
    "GITHUB TASK": (
        "███ █ ███ █ █ █ █ ██     ███ ███  ██ █ █\n"
        "█ █ █  █  ███ █ █ ███     █  ███  █  ██\n"
        "███ █  █  █ █ ███ ███     █  █ █ ██  █ █"
    ),
    "GOAL!": (
        "███  █  ███ █   █\n"
        "█ █ █ █ ███ █\n"
        "███  █  █ █ ███ █"
    ),
}


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def load_font():
    spec = importlib.util.spec_from_file_location("kskill_micro_solid_font", FONT_PATH)
    if spec is None or spec.loader is None:
        fail(f"{FONT_PATH} is missing")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_skill_and_inventory() -> None:
    if not SKILL.is_file():
        fail("skills/kskill-micro-solid-font/SKILL.md is missing")
    linked = ROOT / ".claude" / "skills" / "kskill-micro-solid-font" / "SKILL.md"
    if not linked.is_file() or linked.resolve() != SKILL.resolve():
        fail("kskill-micro-solid-font is not on the skills/ link")
    if "| `kskill-micro-solid-font` |" not in HARNESS.read_text(encoding="utf-8"):
        fail("docs/HARNESS.md has no kskill-micro-solid-font row")
    glossary = GLOSSARY.read_text(encoding="utf-8")
    for term in ("micro-solid font skill", "micro-solid glyph"):
        if f"| {term} |" not in glossary:
            fail(f"docs/GLOSSARY.md has no row for {term!r}")
    ok("micro-solid font is vendored and registered")


def test_glyph_widths_and_distinctions() -> None:
    font = load_font()
    widths = {ch: len(font.glyph(ch)[0]) for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ! "}
    if widths["I"] != 1 or widths["!"] != 1:
        fail(f"I and ! must be 1-wide, got I={widths['I']} !={widths['!']}")
    if widths["M"] != 5 or widths["W"] != 5:
        fail(f"M and W must be 5-wide, got M={widths['M']} W={widths['W']}")
    if widths[" "] != 2:
        fail(f"space must be 2-wide, got {widths[' ']}")
    for ch, width in widths.items():
        if ch in "I! MW":
            continue
        if width != 3:
            fail(f"{ch!r} should be 3-wide, got {width}")
    if font.glyph("G") == font.glyph("O"):
        fail("G and O collided")
    if font.glyph("H") == font.glyph("M"):
        fail("H and M collided")
    for ch, rows in font.GLYPHS.items():
        if len(rows) != 3:
            fail(f"{ch!r} is not 3 rows")
        if len({len(row) for row in font.glyph(ch)}) != 1:
            fail(f"{ch!r} rows are uneven after pad")
        joined = "".join(rows)
        if set(joined) - {"█", " "}:
            fail(f"{ch!r} uses a cell that is not █ or space")
    ok("glyph widths and G/O H/M distinctions hold")


def test_locked_examples() -> None:
    font = load_font()
    for phrase, expected in GOLDENS.items():
        got = font.render(phrase)
        if got != expected:
            fail(f"{phrase!r} drifted:\n{got}\n--- expected ---\n{expected}")
    ok("QUICK WIN, GITHUB TASK, and GOAL! match the locked examples")


def main() -> int:
    tests = [
        test_skill_and_inventory,
        test_glyph_widths_and_distinctions,
        test_locked_examples,
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
