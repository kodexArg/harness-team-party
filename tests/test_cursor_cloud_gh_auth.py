#!/usr/bin/env python3
"""Cursor Cloud `gh` auth helper — PAT wins, App token is dropped."""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "cursor_cloud_gh_auth.sh"

EXCLUDE_DIR_NAMES = {".git", "node_modules", "dist", ".venv", "__pycache__"}

_failures: list[str] = []


def fail(msg: str) -> None:
    _failures.append(msg)
    print(f"FAIL  {msg}", file=sys.stderr)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def sourced_token(env: dict[str, str]) -> str:
    merged = os.environ.copy()
    merged.pop("GH_TOKEN", None)
    merged.pop("GITHUB_PAT", None)
    merged.pop("GH_PROJECT_PAT", None)
    merged.update(env)
    probe = (
        f". {SCRIPT} && "
        'if [ -n "${GH_TOKEN+x}" ]; then printf "SET:%s" "$GH_TOKEN"; '
        'else printf UNSET; fi'
    )
    result = subprocess.run(
        ["bash", "-c", probe],
        check=False,
        capture_output=True,
        text=True,
        env=merged,
    )
    if result.returncode != 0:
        fail(f"script exited {result.returncode}: {result.stderr.strip()}")
        return ""
    return result.stdout.strip()


def test_pat_becomes_gh_token() -> None:
    out = sourced_token({"GITHUB_PAT": "github_pat_testvalue"})
    if out == "SET:github_pat_testvalue":
        ok("operator PAT is exported as GH_TOKEN")
    else:
        fail(f"expected SET:github_pat_testvalue, got {out!r}")


def test_repo_named_pat_becomes_gh_token() -> None:
    out = sourced_token({"GH_PROJECT_PAT": "github_pat_reponame"})
    if out == "SET:github_pat_reponame":
        ok("repo-named operator PAT is exported as GH_TOKEN")
    else:
        fail(f"expected SET:github_pat_reponame, got {out!r}")


def test_github_pat_wins_over_repo_named() -> None:
    out = sourced_token(
        {
            "GITHUB_PAT": "github_pat_named",
            "GH_PROJECT_PAT": "github_pat_reponame",
        }
    )
    if out == "SET:github_pat_named":
        ok("GITHUB_PAT wins over the repo-named secret")
    else:
        fail(f"expected SET:github_pat_named, got {out!r}")


def test_classic_pat_becomes_gh_token() -> None:
    out = sourced_token({"GITHUB_PAT": "ghp_testvalue"})
    if out == "SET:ghp_testvalue":
        ok("classic PAT is exported as GH_TOKEN")
    else:
        fail(f"expected SET:ghp_testvalue, got {out!r}")


def test_app_token_is_dropped() -> None:
    out = sourced_token({"GH_TOKEN": "ghs_installation"})
    if out == "UNSET":
        ok("Cursor App token is unset so gh can fall back")
    else:
        fail(f"expected UNSET for ghs_ token, got {out!r}")


def test_pat_wins_over_app_token() -> None:
    out = sourced_token(
        {"GITHUB_PAT": "github_pat_wins", "GH_TOKEN": "ghs_installation"}
    )
    if out == "SET:github_pat_wins":
        ok("GITHUB_PAT wins over an injected App token")
    else:
        fail(f"expected SET:github_pat_wins, got {out!r}")


def test_empty_is_noop() -> None:
    out = sourced_token({})
    if out == "UNSET":
        ok("missing vars leave GH_TOKEN unset")
    else:
        fail(f"expected UNSET with empty env, got {out!r}")


def _tree_files() -> list[Path]:
    """git ls-files, falling back to an excludes-aware rglob on an
    uncommitted tree (a fresh template has no index)."""
    try:
        tracked = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files"],
            check=False, capture_output=True, text=True,
        ).stdout.split()
        if tracked:
            return [ROOT / rel for rel in tracked]
    except (OSError, subprocess.SubprocessError):
        pass
    return [
        p
        for p in ROOT.rglob("*")
        if p.is_file()
        and not any(part in EXCLUDE_DIR_NAMES for part in p.relative_to(ROOT).parts)
    ]


def test_no_token_value_is_in_the_tree() -> None:
    """The script resolves a name; the value lives outside the repo."""
    real = re.compile(r"\b(ghp_|ghs_|github_pat_)[A-Za-z0-9_]{20,}")
    hits = []
    for path in _tree_files():
        try:
            body = path.read_text(errors="ignore")
        except OSError:
            continue
        for match in real.finditer(body):
            hits.append(f"{path.relative_to(ROOT)}: {match.group(1)}…")
    if hits:
        fail(f"token-shaped literals in tree: {hits[:5]}")
    else:
        ok("no token-shaped literal is tracked anywhere in the repository")


def main() -> int:
    test_no_token_value_is_in_the_tree()
    test_pat_becomes_gh_token()
    test_repo_named_pat_becomes_gh_token()
    test_github_pat_wins_over_repo_named()
    test_classic_pat_becomes_gh_token()
    test_app_token_is_dropped()
    test_pat_wins_over_app_token()
    test_empty_is_noop()
    if _failures:
        print(f"{len(_failures)} failed", file=sys.stderr)
        return 1
    print("all passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
