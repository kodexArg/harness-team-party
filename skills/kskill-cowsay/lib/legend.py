"""Legend art: micro-solid font replacing the cowsay animal.

Glyphs stay in kskill-micro-solid-font. This module only composes
a thought-stem plus those three rows. Closed token set matches
kskill-cowsay.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from lib.art import measure_art_width
from lib.dialog import balloon, default_wrap_cols, wrap_lines

_FONT_PATH = (
    Path(__file__).resolve().parents[2] / "kskill-micro-solid-font" / "font.py"
)
_SPEC = importlib.util.spec_from_file_location("kskill_micro_solid_font", _FONT_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise ImportError(f"cannot load micro-solid font from {_FONT_PATH}")
_FONT = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_FONT)

ALIASES = {
    "QUICK WIN": "QUICK WIN",
    "QUICKWIN": "QUICK WIN",
    "QUICK-WIN": "QUICK WIN",
    "GH ISSUE": "GH ISSUE",
    "GHISSUE": "GH ISSUE",
    "GH-ISSUE": "GH ISSUE",
    "GH REPO": "GH REPO",
    "GHREPO": "GH REPO",
    "GH-REPO": "GH REPO",
    "EPIC DONE!": "EPIC DONE!",
    "EPIC DONE": "EPIC DONE!",
    "EPICDONE": "EPIC DONE!",
    "EPIC-DONE": "EPIC DONE!",
}

CLOSED = ("QUICK WIN", "GH ISSUE", "GH REPO", "EPIC DONE!")


def normalize_legend(raw: str | None) -> str | None:
    if raw is None or not raw.strip():
        return None
    key = " ".join(raw.strip().upper().replace("_", " ").split())
    folded = key.replace(" ", "").replace("-", "")
    if key in ALIASES:
        return ALIASES[key]
    if folded in ALIASES:
        return ALIASES[folded]
    return None


def figure_for(token: str, thoughts: str = "\\") -> str | None:
    name = normalize_legend(token)
    if name is None:
        return None
    body = _FONT.render(name)
    return f"        {thoughts}\n{body}\n"


def say(message: str, legend: str, width: int | None = None, think: bool = False) -> str | None:
    thoughts = "o" if think else "\\"
    art = figure_for(legend, thoughts)
    if art is None:
        return None
    if width is None:
        width = default_wrap_cols()
    width = max(1, width)
    lines = wrap_lines((message or "done").rstrip("\n"), width, False)
    min_content = max(0, measure_art_width(art) - 4)
    box, _ = balloon(lines, think, min_content_w=min_content)
    return "\n".join(box) + "\n" + art
