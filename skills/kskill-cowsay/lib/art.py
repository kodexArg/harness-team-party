"""
ASCII art layer only — cowfiles, faces, COWPATH.

No dialog/balloon code. Swap or add cows/*.cow without editing dialog.py.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# package: lib/ → project root is parent
ROOT = Path(__file__).resolve().parent.parent
COWS = ROOT / "cows"
# Persistent active cow choice (one line: stem name). Skill / --set-cow writes this.
ACTIVE_COW_FILE = ROOT / ".active-cow"


def paths() -> list[Path]:
    """Search dirs for cowfiles. COWPATH entries first; bundled cows always last."""
    dirs: list[Path] = []
    raw = os.environ.get("COWPATH")
    if raw:
        dirs.extend(Path(p) for p in raw.split(os.pathsep) if p)
    try:
        default = COWS.resolve()
    except OSError:
        default = COWS
    if not any(_same_dir(d, default) for d in dirs):
        dirs.append(COWS)
    return dirs


def _same_dir(a: Path, b: Path) -> bool:
    try:
        return a.resolve() == b.resolve()
    except OSError:
        return a == b


def _resolve_path(path: Path) -> Path | None:
    try:
        return path.resolve(strict=True)
    except OSError:
        try:
            return path.resolve()
        except OSError:
            return None


def _under_root(real_file: Path, root: Path) -> bool:
    root_real = _resolve_path(root)
    if root_real is None or not root_real.is_dir():
        return False
    try:
        real_file.relative_to(root_real)
    except ValueError:
        return False
    return real_file != root_real


def accept_cowfile(path: Path) -> Path | None:
    """
    Accept only real .cow files under COWPATH / bundled cows.
    Blocks symlink escape (e.g. evil.cow → /etc/passwd).
    """
    real = _resolve_path(path)
    if real is None or not real.is_file():
        return None
    if real.suffix != ".cow":
        return None
    for directory in paths():
        if _under_root(real, directory):
            return real
    return None


def resolve_cow(name: str) -> Path:
    candidate = Path(name)
    pathlike = (
        candidate.is_absolute()
        or os.sep in name
        or (os.altsep is not None and os.altsep in name)
    )

    explicit = pathlike or (candidate.suffix == ".cow" and candidate.is_file())
    if explicit:
        if candidate.suffix != ".cow" and not name.endswith(".cow"):
            sys.stderr.write(f"cowsay: refusing non-.cow path: {name}\n")
            raise SystemExit(2)
        accepted = accept_cowfile(candidate)
        if accepted is not None:
            return accepted
        try:
            exists = candidate.is_file()
        except OSError:
            exists = False
        if exists:
            sys.stderr.write(f"cowsay: refusing cowfile outside COWPATH: {name}\n")
        else:
            sys.stderr.write(f"cowsay: cowfile not found: {name}\n")
        raise SystemExit(2)

    stem = name if name.endswith(".cow") else f"{name}.cow"
    for directory in paths():
        for hit in (directory / stem, directory / name):
            accepted = accept_cowfile(hit)
            if accepted is not None:
                return accepted
    sys.stderr.write(f"cowsay: cowfile not found: {name}\n")
    raise SystemExit(2)


def list_cow_names() -> list[str]:
    """Loaded cow stems (unique, sorted by discovery order then first-seen)."""
    names: list[str] = []
    for directory in paths():
        if not directory.is_dir():
            continue
        for p in sorted(directory.glob("*.cow")):
            if accept_cowfile(p) is not None:
                names.append(p.stem)
    return list(dict.fromkeys(names))


def list_cows() -> int:
    names = list_cow_names()
    if not names:
        sys.stderr.write("cowsay: no cowfiles\n")
        return 2
    sys.stdout.write(" ".join(names) + "\n")
    return 0


def get_active_cow() -> str:
    """
    Active art stem. Order: COWSAY_COW env → .active-cow file → "default".
    Invalid names fall back to "default" if present, else first listed.
    """
    candidates: list[str] = []
    env = os.environ.get("COWSAY_COW")
    if env and env.strip():
        candidates.append(env.strip())
    try:
        if ACTIVE_COW_FILE.is_file():
            line = ACTIVE_COW_FILE.read_text(encoding="utf-8").strip().splitlines()
            if line and line[0].strip():
                candidates.append(line[0].strip())
    except OSError:
        pass
    candidates.append("default")
    available = set(list_cow_names())
    for name in candidates:
        if name in available:
            return name
    names = list_cow_names()
    return names[0] if names else "default"


def set_active_cow(name: str) -> str:
    """
    Persist active cow to .active-cow. Returns resolved stem.
    Raises SystemExit(2) if name is not a loaded cow.
    """
    stem = name[:-4] if name.endswith(".cow") else name
    available = list_cow_names()
    if stem not in available:
        sys.stderr.write(
            f"cowsay: unknown cow {stem!r} (loaded: {' '.join(available) or 'none'})\n"
        )
        raise SystemExit(2)
    # Validate file is resolvable
    resolve_cow(stem)
    try:
        ACTIVE_COW_FILE.write_text(stem + "\n", encoding="utf-8")
    except OSError as exc:
        sys.stderr.write(f"cowsay: cannot write {ACTIVE_COW_FILE}: {exc}\n")
        raise SystemExit(2) from None
    return stem


def load_cow(path: Path, thoughts: str, eyes: str, tongue: str) -> str:
    """Load a .cow resource; substitute $thoughts / $eyes / $tongue only."""
    try:
        body = path.read_text(encoding="utf-8")
    except OSError as exc:
        sys.stderr.write(
            f"cowsay: cannot read cowfile: {path}: {exc.strerror or exc}\n"
        )
        raise SystemExit(2) from None
    except UnicodeDecodeError:
        sys.stderr.write(f"cowsay: invalid UTF-8 in cowfile: {path}\n")
        raise SystemExit(2) from None
    for key, val in (
        ("$thoughts", thoughts),
        ("$eyes", eyes),
        ("$tongue", tongue),
    ):
        body = body.replace(key, val)
    lines = [line.rstrip("\n") for line in body.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines) + "\n"


def measure_art_width(art: str) -> int:
    """Bounding terminal-column width of rendered art (dialog floor sizing)."""
    # Local import keeps art free of dialog balloon logic; width math is shared.
    from .dialog import display_width

    widths = [
        display_width(line.rstrip("\n"))
        for line in art.splitlines()
        if line.strip()
    ]
    return max(widths) if widths else 0


def face(eyes: str, tongue: str, flags: set[str]) -> tuple[str, str]:
    """Classic cowsay face flags → ($eyes, $tongue) pair, always 2 chars each."""
    e = (eyes + "  ")[:2]
    t = (tongue + "  ")[:2]
    if "b" in flags:
        e = "=="
    if "d" in flags:
        e, t = "xx", "U "
    if "g" in flags:
        e = "$$"
    if "p" in flags:
        e = "@@"
    if "s" in flags:
        e, t = "**", "U "
    if "t" in flags:
        e = "--"
    if "w" in flags:
        e = "OO"
    if "y" in flags:
        e = ".."
    return e, t
