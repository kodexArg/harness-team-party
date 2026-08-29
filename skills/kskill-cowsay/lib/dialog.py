"""
Dialog box only — no cow art knowledge.

Rounded Unicode balloon, text wrap, terminal width.
Widths are **terminal columns** (East Asian Width + combining), not codepoints.
Change cows without touching this module.
"""
from __future__ import annotations

import os
import shutil
import unicodedata


def normalize(text: str) -> str:
    return unicodedata.normalize(
        "NFC", text.expandtabs(8).replace("\r\n", "\n").replace("\r", "\n")
    )


def char_display_width(ch: str) -> int:
    """
    Terminal columns for one codepoint (stdlib approximation of wcwidth).
    Combining / format marks → 0; fullwidth / wide → 2; else → 1.
    """
    if not ch:
        return 0
    o = ord(ch)
    # Null, soft hyphen
    if o == 0 or o == 0xAD:
        return 0
    cat = unicodedata.category(ch)
    # Non-spacing marks, enclosing marks, most format (ZWJ, variation selectors…)
    if cat in ("Mn", "Me", "Cf"):
        return 0
    # Other controls — no advance
    if cat == "Cc":
        return 0
    eaw = unicodedata.east_asian_width(ch)
    if eaw in ("F", "W"):
        return 2
    # Ambiguous (A): treat as narrow (typical Western terminals / cowsay)
    return 1


def display_width(s: str) -> int:
    """Sum of terminal columns for s (after caller should NFC if desired)."""
    return sum(char_display_width(ch) for ch in s)


def pad_display(s: str, width: int) -> str:
    """Pad with spaces so display_width(result) == width (or leave if already wider)."""
    w = display_width(s)
    if w >= width:
        return s
    return s + (" " * (width - w))


def _break_long_token(token: str, width: int) -> list[str]:
    """Hard-split a single token that exceeds width (by display columns)."""
    width = max(1, width)
    lines: list[str] = []
    buf = ""
    for ch in token:
        cw = char_display_width(ch)
        # Always emit at least one codepoint even if cw > width (e.g. -W 1 + emoji)
        if buf and display_width(buf) + cw > width:
            lines.append(buf)
            buf = ch
        else:
            buf += ch
    if buf:
        lines.append(buf)
    return lines or [""]


def _wrap_para(para: str, width: int) -> list[str]:
    """Soft-wrap one paragraph to display width (prefer breaks at spaces)."""
    width = max(1, width)
    words = para.split()
    if not words:
        return [""]
    lines: list[str] = []
    current = ""
    for word in words:
        if display_width(word) > width:
            if current:
                lines.append(current)
                current = ""
            lines.extend(_break_long_token(word, width))
            continue
        candidate = word if not current else f"{current} {word}"
        if display_width(candidate) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def wrap_lines(text: str, width: int, hard: bool) -> list[str]:
    text = normalize(text)
    if hard:
        return text.split("\n") if text else [""]
    width = max(1, width)
    out: list[str] = []
    for para in text.split("\n"):
        if para == "":
            out.append("")
            continue
        out.extend(_wrap_para(para, width) or [""])
    return out or [""]


def balloon(
    lines: list[str],
    think: bool,
    *,
    min_content_w: int = 0,
) -> tuple[list[str], str]:
    """
    Rounded Unicode dialog.
    Min 3 text rows. Content width hugs text: display_width(line) + 1 blank,
    floored by min_content_w (e.g. cow silhouette). Does NOT stretch to -W.
    Padding uses terminal columns so wide chars do not break the box.
    Returns (box_lines, thought_stem) where thought_stem is '\\' or 'o'.
    """
    padded = list(lines)
    while len(padded) < 3:
        padded.append("")
    text_w = max(display_width(line) for line in padded)
    # One extra blank column before the right border; floor at min (cow tail, etc.).
    width = max(text_w + 1, max(0, min_content_w), 1)
    bar = "─" * (width + 2)
    top = f"╭{bar}╮"
    bot = f"╰{bar}╯"
    body = [f"│ {pad_display(line, width)} │" for line in padded]
    return [top, *body, bot], ("o" if think else "\\")


def terminal_columns() -> int:
    """COLUMNS → shutil.get_terminal_size → 80."""
    raw = os.environ.get("COLUMNS")
    if raw is not None and raw.strip().isdigit():
        return max(1, int(raw.strip()))
    try:
        return max(1, shutil.get_terminal_size(fallback=(80, 24)).columns)
    except OSError:
        return 80


def default_wrap_cols() -> int:
    """
    Default -W when omitted.
    COWSAY_WIDTH = explicit content width (tests/CI).
    Else terminal cols - 4 (room for │…│). Floor 8.
    """
    raw = os.environ.get("COWSAY_WIDTH")
    if raw is not None and raw.strip().isdigit():
        return max(1, int(raw.strip()))
    return max(8, terminal_columns() - 4)
