"""Every ADR declares the closed frontmatter contract of adr-00.a.

The contract is `title`, `type`, `status`, `version`, `tags`,
`description`, `applies_when` — plus optional `sub_adrs` (parents) and
`related_agents` (ADRs an hb-ag-* agent carries). `related_adrs` belongs
on docs, skills, and agents, not on ADRs.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADRS = ROOT / "adrs"

REQUIRED = ("title", "type", "status", "version", "tags", "description", "applies_when")
OPTIONAL = ("sub_adrs", "related_agents")
ALLOWED = set(REQUIRED) | set(OPTIONAL)
RETIRED = ("created", "paths", "related_adrs")

failures: list[str] = []


def fail(message: str) -> None:
    failures.append(message)


def frontmatter(path: Path) -> str | None:
    match = re.match(r"\A---\n(.*?)\n---\n", path.read_text(encoding="utf-8"), re.DOTALL)
    return match.group(1) if match else None


def top_level_keys(fm: str) -> list[str]:
    return [m.group(1) for m in re.finditer(r"^([A-Za-z_][A-Za-z0-9_]*):", fm, re.MULTILINE)]


def adr_files() -> list[Path]:
    return sorted(ADRS.glob("adr-*.md"))


def test_every_adr_declares_the_closed_key_set() -> None:
    files = adr_files()
    assert files, "expected at least one ADR in adrs/"
    for path in files:
        fm = frontmatter(path)
        if fm is None:
            fail(f"adrs/{path.name}: no frontmatter block")
            continue
        keys = top_level_keys(fm)
        for key in REQUIRED:
            if key not in keys:
                fail(f"adrs/{path.name}: key `{key}` missing (adr-00.a)")
        for key in RETIRED:
            if key in keys:
                fail(f"adrs/{path.name}: key `{key}` is not part of the contract (adr-00.a)")
        for key in keys:
            if key not in ALLOWED:
                fail(f"adrs/{path.name}: key `{key}` is invented (adr-00.a)")


def test_title_matches_the_filename_stem() -> None:
    for path in adr_files():
        fm = frontmatter(path) or ""
        match = re.search(r"^title:\s*(.+)$", fm, re.MULTILINE)
        title = match.group(1).strip().strip("\"'") if match else ""
        if title != path.stem:
            fail(f"adrs/{path.name}: title `{title}` does not match the filename stem (adr-00.a)")


def test_version_format() -> None:
    for path in adr_files():
        fm = frontmatter(path) or ""
        match = re.search(r"^version:\s*(.+)$", fm, re.MULTILINE)
        version = match.group(1).strip() if match else ""
        if not re.match(r"^v\d+\.\d+\.\d+$", version):
            fail(
                f"adrs/{path.name}: version `{version}` does not match vX.Y.Z semver format (adr-00.a)"
            )


def test_status_is_active() -> None:
    for path in adr_files():
        fm = frontmatter(path) or ""
        match = re.search(r"^status:\s*(.+)$", fm, re.MULTILINE)
        status = match.group(1).strip() if match else ""
        if status != "active":
            fail(
                f"adrs/{path.name}: status is `{status}`; a rule that stops applying is "
                "deleted, not parked (adr-00.b)"
            )


def test_bodies_carry_no_provenance_prose() -> None:
    for path in adr_files():
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"[Pp]rovenance of|express consent given in conversation", line):
                fail(f"adrs/{path.name}:{number}: provenance prose — history is git's (adr-00.b)")


def main() -> int:
    tests = [value for name, value in sorted(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
    if failures:
        for message in failures:
            print(f"FAIL: {message}")
        print(f"\n{len(failures)} contract breach(es) across {len(adr_files())} ADRs")
        return 1
    print(f"ok  {len(adr_files())} ADRs carry the closed frontmatter contract")
    return 0


if __name__ == "__main__":
    sys.exit(main())
