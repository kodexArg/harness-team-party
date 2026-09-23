"""kskill-context clones, fast-forwards, and refuses a dirty tree."""

from __future__ import annotations

import json
import os
import stat
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_BIN = ROOT / "skills" / "kskill-context" / "bin"
REGISTRY = ROOT / "context" / "repos.json"


def _run(cmd: list[str], *, cwd: Path | None = None, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(cmd, cwd=cwd, env=merged, capture_output=True, text=True, check=False)


def _git(repo: Path, *args: str) -> None:
    result = _run(["git", "-C", str(repo), *args])
    if result.returncode != 0:
        raise AssertionError(result.stderr or result.stdout)


def _fixture(tmp_path: Path) -> tuple[Path, dict[str, str]]:
    bare = tmp_path / "origin.git"
    seed = tmp_path / "seed"
    seed.mkdir()
    _run(["git", "init", "-b", "main", str(seed)], cwd=tmp_path)
    _git(seed, "config", "user.email", "test@example.com")
    _git(seed, "config", "user.name", "test")
    (seed / "README.md").write_text("one\n", encoding="utf-8")
    _git(seed, "add", "README.md")
    _git(seed, "commit", "-m", "one")
    _run(["git", "clone", "--bare", str(seed), str(bare)])
    context = tmp_path / "context"
    context.mkdir()
    registry = context / "repos.json"
    registry.write_text(
        json.dumps(
            {
                "repos": [
                    {"name": "sample", "remote": str(bare), "branch": "main"},
                ]
            }
        ),
        encoding="utf-8",
    )
    stub_dir = tmp_path / "stub-bin"
    stub_dir.mkdir()
    stub = stub_dir / "graphify"
    stub.write_text(
        "#!/bin/sh\n"
        "out=\n"
        "while [ $# -gt 0 ]; do\n"
        "  if [ \"$1\" = \"--out\" ]; then out=$2; shift 2; else shift; fi\n"
        "done\n"
        "mkdir -p \"$out/graphify-out\"\n"
        "printf '%s\\n' '{\"nodes\":[{\"id\":\"stub\"}]}' > \"$out/graphify-out/graph.json\"\n",
        encoding="utf-8",
    )
    stub.chmod(stub.stat().st_mode | stat.S_IXUSR)
    env = {
        "CONTEXT_DIR": str(context),
        "CONTEXT_REGISTRY": str(registry),
        "PATH": f"{stub_dir}:{os.environ.get('PATH', '')}",
        "GIT_AUTHOR_NAME": "test",
        "GIT_AUTHOR_EMAIL": "test@example.com",
        "GIT_COMMITTER_NAME": "test",
        "GIT_COMMITTER_EMAIL": "test@example.com",
    }
    return bare, env


def test_registry_is_tracked_and_valid() -> None:
    assert (ROOT / "context" / ".gitignore").is_file()
    assert REGISTRY.is_file()
    ignore = (ROOT / ".graphifyignore").read_text(encoding="utf-8")
    assert "context/" in ignore
    repos = json.loads(REGISTRY.read_text(encoding="utf-8"))["repos"]
    assert repos
    for entry in repos:
        assert entry["name"] and entry["remote"] and entry["branch"]
    interfaces = (ROOT / "docs" / "INTERFACES.md").read_text(encoding="utf-8")
    for script in ("bin/on-loop", "bin/list", "bin/sync", "bin/index"):
        path = SKILL_BIN / script.split("/")[-1]
        assert path.is_file()
        assert path.stat().st_mode & stat.S_IXUSR
        assert f"skills/kskill-context/{script}" in interfaces


def test_sync_clones_fast_forwards_and_refuses_dirty(tmp_path: Path) -> None:
    bare, env = _fixture(tmp_path)
    context = Path(env["CONTEXT_DIR"])
    sync = SKILL_BIN / "sync"
    first = _run([str(sync), "sample"], env=env)
    assert first.returncode == 0, first.stderr
    assert "check: sample missing" in first.stdout
    assert "inform: repo=sample action=clone" in first.stdout
    clone = context / "sample"
    assert (clone / ".git").exists()
    assert (context / ".graphs" / "sample" / "graphify-out" / "graph.json").is_file()

    work = tmp_path / "work"
    _run(["git", "clone", str(bare), str(work)])
    _git(work, "config", "user.email", "test@example.com")
    _git(work, "config", "user.name", "test")
    (work / "README.md").write_text("two\n", encoding="utf-8")
    _git(work, "add", "README.md")
    _git(work, "commit", "-m", "two")
    _git(work, "push", "origin", "main")

    second = _run([str(sync), "sample"], env=env)
    assert second.returncode == 0, second.stderr
    assert "check: sample present" in second.stdout
    assert "inform: repo=sample action=pull" in second.stdout
    head = _run(["git", "-C", str(clone), "log", "-1", "--format=%s"])
    assert head.stdout.strip() == "two"

    (clone / "README.md").write_text("dirty\n", encoding="utf-8")
    third = _run([str(sync), "sample"], env=env)
    assert third.returncode != 0
    assert "dirty" in third.stderr
