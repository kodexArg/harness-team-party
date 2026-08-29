#!/usr/bin/env python3
"""Idempotent CI slice picker: same path list → same jobs and files.

A GitHub Actions job always starts (required checks cannot be skipped), then
this script says whether that job has work. No network. No clock.

Agnostic form: the service and surface arms key off SERVICE_PREFIXES /
SURFACE_PREFIXES. Instantiation ([[CLONE]]) points them at the project's real
trees and names its contract suites in SURFACE_CONTRACT_TESTS.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS_DIR = ROOT / "tests"

# Instantiation: the project's real trees ([[CLONE]] §5).
SERVICE_PREFIXES = ("service/",)
SURFACE_PREFIXES = ("surface/",)

SERVICE_FORCE_ALL = frozenset(
    {
        "docs/INTERFACES.md",
    }
)
SERVICE_FORCE_PREFIX = ("docs/tdds/",)

# Contract suites that run on any surface-src change. Empty in the template;
# instantiation names them once the surface has contract tests.
SURFACE_CONTRACT_TESTS: tuple[str, ...] = ()

MERGE_GATE_PATHS = frozenset(
    {
        "docs/PRD.md",
        "docs/INTERFACES.md",
        "docs/VARIABLES.md",
        "scripts/check_merge_gate.py",
    }
)
MERGE_GATE_PREFIX = ("adrs/", "docs/tdds/")

# Harness tests that must never run in CI (need live credentials). Empty in
# the template; a project that adds live-credential guards lists them here.
HARNESS_ALWAYS_SKIP: frozenset[str] = frozenset()


@dataclass
class Selection:
    service: bool = False
    service_args: str = ""
    surface: bool = False
    surface_files: list[str] = field(default_factory=list)
    harness: bool = False
    harness_files: list[str] = field(default_factory=list)
    merge_gate: bool = False


def _norm(path: str) -> str:
    p = path.replace("\\", "/")
    while p.startswith("./"):
        p = p[2:]
    return p


def classify(paths: list[str]) -> Selection:
    files = sorted({_norm(p) for p in paths if _norm(p)})
    sel = Selection()
    sel.service, sel.service_args = _service(files)
    sel.surface, sel.surface_files = _surface(files)
    sel.harness, sel.harness_files = _harness(files)
    sel.merge_gate = _merge_gate(files)
    return sel


def _touches(files: list[str], prefixes: tuple[str, ...]) -> list[str]:
    return [p for p in files if any(p.startswith(pre) for pre in prefixes)]


def _service(files: list[str]) -> tuple[bool, str]:
    touched = _touches(files, SERVICE_PREFIXES)
    touched += [p for p in files if p in SERVICE_FORCE_ALL or p.startswith(SERVICE_FORCE_PREFIX)]
    if not touched:
        return False, ""
    if any(p in SERVICE_FORCE_ALL or p.startswith(SERVICE_FORCE_PREFIX) for p in touched):
        return True, ""
    areas: set[str] = set()
    for p in touched:
        parts = p.split("/")
        if len(parts) >= 3:
            areas.add("/".join(parts[:2]))
        else:
            return True, ""
    if not areas:
        return True, ""
    return True, " ".join(sorted(areas))


def _surface_tests_root() -> Path | None:
    for pre in SURFACE_PREFIXES:
        candidate = ROOT / pre / "tests"
        if candidate.is_dir():
            return candidate
    return None


@lru_cache(maxsize=1)
def _surface_test_corpus() -> tuple[tuple[str, str], ...]:
    root = _surface_tests_root()
    if root is None:
        return ()
    return tuple(
        (p.name, p.read_text(encoding="utf-8", errors="replace"))
        for p in sorted(root.rglob("*"))
        if p.is_file() and "test" in p.name
    )


def _tests_naming(path: str) -> set[str]:
    """Tests that name the changed file — the link is the mention inside the
    test, never the filename convention."""
    name = Path(path).name
    word = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(Path(path).stem)}(?![A-Za-z0-9_])")
    root = _surface_tests_root()
    if root is None:
        return set()
    base = root.relative_to(ROOT).as_posix()
    return {
        f"{base}/{test}"
        for test, text in _surface_test_corpus()
        if name in text or word.search(text)
    }


def _surface(files: list[str]) -> tuple[bool, list[str]]:
    touched = _touches(files, SURFACE_PREFIXES)
    if not touched:
        return False, []
    tests_root = next((f"{pre}tests/" for pre in SURFACE_PREFIXES), None)
    selected: set[str] = set()
    for p in touched:
        if tests_root and p.startswith(tests_root):
            selected.add(p)
            continue
        selected.update(c for c in SURFACE_CONTRACT_TESTS if (ROOT / c).is_file())
        selected.update(_tests_naming(p))
    return True, sorted(selected)


def _existing_harness(rel: str) -> bool:
    return rel not in HARNESS_ALWAYS_SKIP and (ROOT / rel).is_file()


def _harness(files: list[str]) -> tuple[bool, list[str]]:
    picked: set[str] = set()
    needs_all = False
    relevant = False
    for p in files:
        if p.startswith("tests/test_") and p.endswith(".py"):
            relevant = True
            if _existing_harness(p):
                picked.add(p)
            continue
        if p.startswith("agents/"):
            relevant = True
            for t in (
                "tests/test_agents_are_subagents.py",
                "tests/test_guardian_identity_triangle.py",
                "tests/test_hb_ag_roster.py",
                "tests/test_agent_model_inherit.py",
                "tests/test_tools_mcp_first.py",
            ):
                if _existing_harness(t):
                    picked.add(t)
            continue
        if p.startswith("adrs/"):
            relevant = True
            for t in (
                "tests/test_adr_frontmatter.py",
                "tests/test_live_doc.py",
                "tests/test_wikilink_targets.py",
            ):
                if _existing_harness(t):
                    picked.add(t)
            continue
        if p == "scripts/ci_select.py" or p == "tests/test_ci_select.py":
            relevant = True
            if _existing_harness("tests/test_ci_select.py"):
                picked.add("tests/test_ci_select.py")
            continue
        if p.startswith("scripts/check_merge_gate"):
            relevant = True
            if _existing_harness("tests/test_merge_gate.py"):
                picked.add("tests/test_merge_gate.py")
            continue
        if p.startswith("scripts/check_pr_tags"):
            relevant = True
            if _existing_harness("tests/test_pr_tags.py"):
                picked.add("tests/test_pr_tags.py")
            continue
        if p.startswith("scripts/"):
            relevant = True
            needs_all = True
            continue
        if p.startswith("skills/"):
            relevant = True
            if "kskill-graphify" in p:
                for t in ("tests/test_kskill_graphify.py", "tests/test_graphify.py"):
                    if _existing_harness(t):
                        picked.add(t)
            elif any(
                stem in p
                for stem in (
                    "kskill-qw",
                    "kskill-mood",
                    "kskill-cowsay",
                    "kskill-micro-solid-font",
                )
            ) and _existing_harness("tests/test_quick_win_skills.py"):
                picked.add("tests/test_quick_win_skills.py")
                if _existing_harness("tests/test_micro_solid_font.py"):
                    picked.add("tests/test_micro_solid_font.py")
            else:
                needs_all = True
            continue
        if p.startswith(".github/workflows/"):
            relevant = True
            mapped = False
            if "ci.yml" in p:
                for t in ("tests/test_ci_select.py", "tests/test_every_test_file_runs.py"):
                    if _existing_harness(t):
                        picked.add(t)
                        mapped = True
            if not mapped:
                # Silence is never a selector's answer; unmapped means the full
                # harness.
                needs_all = True
            continue
    if not relevant:
        return False, []
    if needs_all:
        all_files = sorted(
            f"tests/{p.name}"
            for p in HARNESS_DIR.glob("test_*.py")
            if _existing_harness(f"tests/{p.name}")
        )
        return True, all_files
    return True, sorted(picked)


def _merge_gate(files: list[str]) -> bool:
    return any(p in MERGE_GATE_PATHS or p.startswith(MERGE_GATE_PREFIX) for p in files)


def git_paths(base: str, head: str) -> list[str]:
    import subprocess

    out = subprocess.check_output(
        ["git", "diff", "--name-only", "-z", f"{base}...{head}"],
        cwd=ROOT,
        text=True,
    )
    return [p for p in out.split("\0") if p]


def emit(sel: Selection, job: str) -> None:
    if job == "service":
        print(f"run={'true' if sel.service else 'false'}")
        print(f"args={sel.service_args}")
    elif job == "surface":
        print(f"run={'true' if sel.surface else 'false'}")
        print(f"files={' '.join(sel.surface_files)}")
    elif job == "harness":
        print(f"run={'true' if sel.harness else 'false'}")
        print(f"files={' '.join(sel.harness_files)}")
    elif job == "merge-gate":
        print(f"run={'true' if sel.merge_gate else 'false'}")
    else:
        raise SystemExit(f"unknown job: {job}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job", required=True, choices=("service", "surface", "harness", "merge-gate"))
    parser.add_argument("--base", default="")
    parser.add_argument("--head", default="HEAD")
    parser.add_argument("--paths-file", default="")
    args = parser.parse_args(argv)

    if args.paths_file:
        raw = Path(args.paths_file).read_text(encoding="utf-8").splitlines()
        paths = [line.strip() for line in raw if line.strip()]
    elif args.base:
        paths = git_paths(args.base, args.head)
    else:
        parser.error("pass --base SHA or --paths-file")

    emit(classify(paths), args.job)
    return 0


if __name__ == "__main__":
    sys.exit(main())
