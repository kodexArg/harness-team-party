"""3-row micro-solid block font. Glyphs are █ and space only."""

from __future__ import annotations

GLYPHS: dict[str, tuple[str, str, str]] = {
    "A": ("███", "███", "█ █"),
    "B": ("██ ", "███", "███"),
    "C": ("███", "█  ", "███"),
    "D": ("██ ", "█ █", "██ "),
    "E": ("███", "██ ", "███"),
    "F": ("███", "██ ", "█  "),
    "G": ("███", "█ █", "███"),
    "H": ("█ █", "███", "█ █"),
    "I": ("█", "█", "█"),
    "J": ("  █", "  █", "██ "),
    "K": ("█ █", "██ ", "█ █"),
    "L": ("█  ", "█  ", "███"),
    "M": ("█   █", "██ ██", "█ █ █"),
    "N": ("██ ", "█ █", "█ █"),
    "O": (" █ ", "█ █", " █ "),
    "P": ("███", "███", "█  "),
    "Q": ("███", "█ █", " ██"),
    "R": ("███", "██ ", "█ █"),
    "S": (" ██", " █ ", "██ "),
    "T": ("███", " █ ", " █ "),
    "U": ("█ █", "█ █", "███"),
    "V": ("█ █", "█ █", " █ "),
    "W": ("█ █ █", "█ █ █", " █ █ "),
    "X": ("█ █", " █ ", "█ █"),
    "Y": ("█ █", " █ ", " █ "),
    "Z": ("███", " █ ", "███"),
    "!": ("█", " ", "█"),
    " ": ("  ", "  ", "  "),
}

MISSING = ("   ", "   ", "   ")


def _pad(rows: tuple[str, str, str]) -> tuple[str, str, str]:
    width = max(len(row) for row in rows)
    return (rows[0].ljust(width), rows[1].ljust(width), rows[2].ljust(width))


def glyph(ch: str) -> tuple[str, str, str]:
    if len(ch) != 1:
        raise ValueError(f"glyph expects one character, got {ch!r}")
    return _pad(GLYPHS.get(ch.upper(), MISSING))


def render(text: str, gap: str = " ") -> str:
    """Compose `text` as three rows. Unknown characters become a 3-wide blank."""
    rows = ["", "", ""]
    for ch in text.upper():
        g = glyph(ch)
        for i in range(3):
            rows[i] += g[i] + gap
    return "\n".join(row.rstrip() for row in rows)
