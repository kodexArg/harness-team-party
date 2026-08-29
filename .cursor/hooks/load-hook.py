#!/usr/bin/env python3
"""sessionStart: load PRD, ADRs, then docs/ into context."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRD_REL = Path("docs") / "PRD.md"
ADRS_REL = Path("adrs")
DOCS_REL = Path("docs")
COWSAY = ROOT / "skills" / "kskill-cowsay" / "bin" / "cowsay"
COWSAY_MSG = "SSoT Loaded into context"


def iter_files(directory: Path) -> list[Path]:
    if not directory.is_dir():
        return []
    found = [p for p in directory.rglob("*") if p.is_file()]
    return sorted(found, key=lambda p: p.as_posix())


def ssot_files(root: Path) -> list[Path]:
    prd = root / PRD_REL
    ordered: list[Path] = []
    if prd.is_file():
        ordered.append(prd)
    ordered.extend(iter_files(root / ADRS_REL))
    skip = prd.resolve() if prd.is_file() else None
    for path in iter_files(root / DOCS_REL):
        if skip is not None and path.resolve() == skip:
            continue
        ordered.append(path)
    return ordered


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def render_cowsay() -> str:
    if not COWSAY.is_file():
        return COWSAY_MSG
    try:
        proc = subprocess.run(
            [sys.executable, str(COWSAY), COWSAY_MSG],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return COWSAY_MSG
    text = proc.stdout.strip()
    return text or COWSAY_MSG


def build_context(root: Path, banner: str | None = None) -> str:
    chunks: list[str] = [banner or render_cowsay(), ""]
    for path in ssot_files(root):
        rel = path.relative_to(root).as_posix()
        chunks.append(f"===== {rel} =====")
        chunks.append(read_text(path))
        chunks.append("")
    return "\n".join(chunks).rstrip() + "\n"


def main() -> None:
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError:
        pass
    banner = render_cowsay()
    sys.stderr.write(banner + "\n")
    print(json.dumps({"additional_context": build_context(ROOT, banner)}))


if __name__ == "__main__":
    main()
