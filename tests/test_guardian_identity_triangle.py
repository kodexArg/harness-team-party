
from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS_DIR = ROOT / "agents"
WATCHLISTS_MODULE = ROOT / "scripts" / "guardian_watchlists.py"

# A guardian def is discovered by shape, never by a hardcoded project name
# (issue #130): its frontmatter `description:` names it a guardian.
GUARDIAN_MARKER = re.compile(r"\bguardian\b", re.IGNORECASE)
FRONTMATTER_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s?(.*)$")
# Sibling notify prose, e.g. "- **→ kbot-adr** when ...".
NOTIFY_LINE = re.compile(r"^-\s+\*\*→\s*([A-Za-z0-9_-]+)\*\*", re.MULTILINE)


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def parse_frontmatter(text: str, label: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(f"{label}: does not open with a '---' frontmatter fence")
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        fail(f"{label}: frontmatter fence never closes")
    data: dict[str, str] = {}
    for line in lines[1:end]:
        m = FRONTMATTER_KEY.match(line)
        if m:
            key, val = m.group(1), m.group(2).strip()
            data.setdefault(key, val.strip('"').strip("'"))
    return data


def discover_guardian_defs() -> dict[str, dict[str, str]]:
    """filename stem -> frontmatter, for every agents/*.md whose
    frontmatter description names it a guardian. Generic: no literal
    project-specific guardian name is ever hardcoded here."""
    found: dict[str, dict[str, str]] = {}
    for path in sorted(AGENTS_DIR.glob("*.md")):
        fm = parse_frontmatter(path.read_text(encoding="utf-8"), path.name)
        if GUARDIAN_MARKER.search(fm.get("description", "")):
            found[path.stem] = fm
    return found


def extract_watchlist_keys() -> list[str]:
    """Statically pull WATCHLISTS' dict keys via AST — never import the
    hook module, which may carry PostToolUse side effects."""
    if not WATCHLISTS_MODULE.is_file():
        fail(f"missing {WATCHLISTS_MODULE.relative_to(ROOT)}")
    tree = ast.parse(WATCHLISTS_MODULE.read_text(encoding="utf-8"), filename=str(WATCHLISTS_MODULE))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
            target_names = [t.id for t in node.targets if isinstance(t, ast.Name)]
            if "WATCHLISTS" not in target_names:
                continue
            keys: list[str] = []
            for k in node.value.keys:
                if isinstance(k, ast.Constant) and isinstance(k.value, str):
                    keys.append(k.value)
                else:
                    fail(
                        "WATCHLISTS has a non-string-literal key; cannot "
                        "statically verify it via AST"
                    )
            return keys
    fail(f"no WATCHLISTS dict assignment found in {WATCHLISTS_MODULE.relative_to(ROOT)}")
    return []  # unreachable — fail() raises


def test_identity_triangle() -> None:
    guardians = discover_guardian_defs()
    if not guardians:
        ok("no guardian defs under agents/ — skip identity triangle")
        return

    watchlist_keys = extract_watchlist_keys()
    if len(watchlist_keys) != len(set(watchlist_keys)):
        fail(f"WATCHLISTS has duplicate keys: {watchlist_keys}")
    watchlist_set = set(watchlist_keys)

    stems = set(guardians)
    names = set()
    for stem, fm in guardians.items():
        name = fm.get("name")
        if not name:
            fail(f"agents/{stem}.md: frontmatter has no name: field")
        names.add(name)
        if name != stem:
            fail(
                f"agents/{stem}.md: filename stem {stem!r} != frontmatter "
                f"name {name!r}"
            )
        if name not in watchlist_set:
            fail(
                f"agents/{stem}.md: name {name!r} has no matching key in "
                f"WATCHLISTS ({WATCHLISTS_MODULE.relative_to(ROOT)}) — the "
                "watchlist will never name this guardian"
            )

    extra = watchlist_set - stems
    if extra:
        fail(
            "WATCHLISTS has key(s) with no matching guardian def under "
            f"agents/: {sorted(extra)} — the watchlist names a "
            "subagent_type that resolves to nothing"
        )

    if stems != names or stems != watchlist_set:
        fail(
            "guardian identity triangle mismatch: "
            f"filenames={sorted(stems)} names={sorted(names)} "
            f"watchlist_keys={sorted(watchlist_set)}"
        )

    ok(f"identity triangle (filename == name == WATCHLISTS key) for {sorted(stems)}")


def test_notify_prose_resolves() -> None:
    guardians = discover_guardian_defs()
    stems = set(guardians)
    checked = 0
    for stem in sorted(guardians):
        text = (AGENTS_DIR / f"{stem}.md").read_text(encoding="utf-8")
        for target in NOTIFY_LINE.findall(text):
            checked += 1
            if target == stem:
                fail(f"agents/{stem}.md: notify prose lists itself ({target!r})")
            if target not in stems:
                fail(
                    f"agents/{stem}.md: notify prose references {target!r}, "
                    "which is not an existing guardian filename/frontmatter name"
                )
    if checked == 0:
        ok("no guardian notify prose — skip")
        return
    ok(f"{checked} cross-guardian notify reference(s) resolve to real guardian defs")


def main() -> int:
    tests = [test_identity_triangle, test_notify_prose_resolves]
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
