#!/usr/bin/env python3
"""Read context/repos.json. Stdlib only."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
REQUIRED = ("name", "remote", "branch")


def load(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    repos = data.get("repos")
    if not isinstance(repos, list) or not repos:
        raise SystemExit(f"registry has no repos: {path}")
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for entry in repos:
        if not isinstance(entry, dict):
            raise SystemExit(f"registry entry is not an object: {entry!r}")
        missing = [key for key in REQUIRED if not isinstance(entry.get(key), str) or not entry[key]]
        if missing:
            raise SystemExit(f"registry entry missing {missing}: {entry!r}")
        name = entry["name"]
        if not NAME_RE.fullmatch(name):
            raise SystemExit(f"registry name is not a single path segment: {name!r}")
        if name in seen:
            raise SystemExit(f"registry name is duplicated: {name}")
        seen.add(name)
        out.append({key: entry[key] for key in REQUIRED})
    return out


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("usage: registry.py REGISTRY [NAME]")
    repos = load(Path(sys.argv[1]))
    if len(sys.argv) == 3:
        wanted = sys.argv[2]
        repos = [entry for entry in repos if entry["name"] == wanted]
        if not repos:
            raise SystemExit(f"registry has no repo named {wanted}")
    for entry in repos:
        print("\t".join(entry[key] for key in REQUIRED))


if __name__ == "__main__":
    main()
