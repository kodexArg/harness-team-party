"""adr-05-after-versioning and its lookup skill exist (issue after-versioning).

The closed ADR frontmatter contract is tests/test_adr_frontmatter.py.
This file only checks that the ADR, the skill, and the HARNESS heading
that owns the field table are present — it does not revive the deleted
test_adr_ssot_pass suite.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADR = ROOT / "adrs" / "adr-05-after-versioning.md"
SKILL = ROOT / "skills" / "kskill-after-versioning" / "SKILL.md"
HARNESS = ROOT / "docs" / "HARNESS.md"

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def frontmatter(path: Path) -> dict[str, str]:
    match = re.match(r"\A---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.DOTALL)
    if match is None:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def test_adr_05_exists_and_owns_changelog() -> None:
    if not ADR.is_file():
        fail("adrs/adr-05-after-versioning.md is missing")
        return
    text = ADR.read_text(encoding="utf-8")
    if "CHANGELOG.md" not in text:
        fail("adr-05 paths do not own CHANGELOG.md")
    if "related_adrs:" in text.split("---", 2)[1]:
        fail("adr-05 frontmatter carries related_adrs (forbidden on ADRs)")
    if "adr-40" in text:
        fail("adr-05 still names adr-40")


def test_after_versioning_skill_exists() -> None:
    if not SKILL.is_file():
        print("skip  kskill-after-versioning is not vendored")
        return
    fields = frontmatter(SKILL)
    if fields.get("name") != "kskill-after-versioning":
        fail("kskill-after-versioning frontmatter name is wrong")
    text = SKILL.read_text(encoding="utf-8")
    if "Rules it enforces" in text:
        fail("kskill-after-versioning restates ADR numbered rules as a Rules it enforces dump")
    if "adr-40" in text:
        fail("kskill-after-versioning still cites adr-40")
    if "adr-05-after-versioning" not in text:
        fail("kskill-after-versioning does not cite adr-05-after-versioning")


def test_harness_docs_frontmatter_heading() -> None:
    if not HARNESS.is_file():
        fail("docs/HARNESS.md is missing")
        return
    text = HARNESS.read_text(encoding="utf-8")
    if "## Harness docs frontmatter" not in text:
        fail("docs/HARNESS.md lacks the Harness docs frontmatter heading")
    if "adr-40" in text:
        fail("docs/HARNESS.md still cites adr-40")


def main() -> int:
    tests = [
        test_adr_05_exists_and_owns_changelog,
        test_after_versioning_skill_exists,
        test_harness_docs_frontmatter_heading,
    ]
    for test in tests:
        test()
    if failures:
        for message in failures:
            print(f"FAIL: {message}")
        print(f"\n{len(failures)} after-versioning check(s) failed")
        return 1
    print("ok  adr-05 and HARNESS heading exist")
    return 0


if __name__ == "__main__":
    sys.exit(main())
