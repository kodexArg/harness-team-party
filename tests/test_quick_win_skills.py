"""kskill-qw, kskill-mood, and kskill-cowsay are vendored together.

[[HARNESS]]: a skill absent from docs/HARNESS.md is not in the
harness. The real copy is skills/kskill-*/; slash /qw and
/kdx-mood are invocations, not unprefixed directories.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT / "docs" / "HARNESS.md"
GLOSSARY = ROOT / "docs" / "GLOSSARY.md"
RENDER = ROOT / "skills" / "kskill-cowsay" / "render.py"

SKILLS = (
    ("kskill-mood", "kskill-mood"),
    ("kskill-qw", "kskill-qw"),
    ("kskill-cowsay", "kskill-cowsay"),
    ("kskill-micro-solid-font", "kskill-micro-solid-font"),
)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def test_skills_exist_and_link() -> None:
    for folder, name in SKILLS:
        real = ROOT / "skills" / folder / "SKILL.md"
        linked_claude = ROOT / ".claude" / "skills" / folder / "SKILL.md"
        linked_agents = ROOT / ".agents" / "skills" / folder / "SKILL.md"
        if not real.is_file():
            fail(f"skills/{folder}/SKILL.md is missing")
        if f"name: {name}" not in real.read_text(encoding="utf-8").split("\n---", 1)[0]:
            fail(f"{folder} frontmatter name is not {name!r}")
        if not linked_claude.is_file():
            fail(f".claude/skills/{folder}/SKILL.md does not resolve")
        if linked_claude.resolve() != real.resolve():
            fail(f"{folder} in .claude/skills is a second copy, not the skills/ link")
        if not linked_agents.is_file():
            fail(f".agents/skills/{folder}/SKILL.md does not resolve")
        if linked_agents.resolve() != real.resolve():
            fail(f"{folder} in .agents/skills is a second copy, not the skills/ link")
    ok("mood, qw, cowsay, and micro-solid-font skills exist on the skills links")


def test_qw_is_the_quick_win_shortcut() -> None:
    qw = (ROOT / "skills" / "kskill-qw" / "SKILL.md").read_text(encoding="utf-8")
    mood = (ROOT / "skills" / "kskill-mood" / "SKILL.md").read_text(encoding="utf-8")
    stance = (ROOT / "skills" / "kskill-mood" / "references" / "quick-win.md").read_text(
        encoding="utf-8"
    )
    if "/qw" not in qw or "quick win" not in qw.lower():
        fail("kskill-qw does not declare /qw as the quick-win shortcut")
    if "`quick-win`" not in mood or "`qw`" not in mood:
        fail("kskill-mood does not register the quick-win / qw aliases")
    if "kskill-cowsay" not in stance or "QUICK WIN" not in stance:
        fail("quick-win stance does not close with cowsay QUICK WIN")
    if "re-ask" not in stance.lower() and "re-ask" not in stance:
        fail("quick-win stance dropped the mandatory understand/re-ask step")
    ok("/qw is the kdx-mood quick-win shortcut")


def test_harness_and_glossary_rows() -> None:
    harness = HARNESS.read_text(encoding="utf-8")
    glossary = GLOSSARY.read_text(encoding="utf-8")
    for name in ("kskill-mood", "kskill-qw", "kskill-cowsay", "kskill-micro-solid-font"):
        row = next((line for line in harness.splitlines() if line.startswith(f"| `{name}`")), None)
        if row is None or row.count("|") < 4:
            fail(f"docs/HARNESS.md has no complete `{name}` row")
    for term in (
        "mood skill",
        "quick-win skill",
        "cowsay skill",
        "cowsay legend",
        "cowsay final hook",
        "micro-solid font skill",
        "micro-solid glyph",
    ):
        if f"| {term} |" not in glossary:
            fail(f"docs/GLOSSARY.md has no row for {term!r}")
    ok("HARNESS and GLOSSARY register the four skills")


def test_cowsay_legends_replace_the_animal() -> None:
    cow = subprocess.check_output(
        [sys.executable, str(RENDER), "--", "ship it"],
        text=True,
        cwd=ROOT,
    )
    if "(oo)" not in cow:
        fail("default cowsay lost the cow")
    if "QUICK WIN" in cow.split("\n", 3)[-1] and "___" in cow and "(oo)" in cow:
        fail("default print mixed a legend with the cow")
    for token in ("QUICK WIN", "GH ISSUE", "GH REPO", "EPIC DONE!"):
        out = subprocess.check_output(
            [sys.executable, str(RENDER), "--legend", token, "--", "done"],
            text=True,
            cwd=ROOT,
        )
        if "(oo)" in out:
            fail(f"legend {token!r} still prints the cow")
        if "done" not in out.split("\n")[1].lower() and "done" not in out:
            fail(f"legend {token!r} dropped the balloon text")
        if "█" not in out or "(oo)" in out:
            fail(f"legend {token!r} is not micro-solid (or still has the cow)")
        if out.count("\n") < 5:
            fail(f"legend {token!r} is shorter than balloon + 3 rows")
        if token == "QUICK WIN" and " ██ ███ █ ███ █ █" not in out:
            fail("QUICK WIN legend is not the micro-solid rendering")
    unknown = subprocess.check_output(
        [sys.executable, str(RENDER), "--legend", "NOPE", "--", "x"],
        text=True,
        cwd=ROOT,
    )
    if "(oo)" not in unknown:
        fail("unknown legend must fall back to the cow, not invent art")
    ok("cowsay legends replace the animal and unknown tokens keep the cow")


def main() -> int:
    tests = [
        test_skills_exist_and_link,
        test_qw_is_the_quick_win_shortcut,
        test_harness_and_glossary_rows,
        test_cowsay_legends_replace_the_animal,
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
