"""kodexArg cowsay library: dialog (balloon) + art (cowfiles) stay separate."""

from .art import (
    face,
    get_active_cow,
    list_cow_names,
    list_cows,
    load_cow,
    measure_art_width,
    resolve_cow,
    set_active_cow,
)
from .dialog import (
    balloon,
    default_wrap_cols,
    display_width,
    pad_display,
    wrap_lines,
)

__all__ = [
    "balloon",
    "default_wrap_cols",
    "display_width",
    "face",
    "get_active_cow",
    "list_cow_names",
    "list_cows",
    "load_cow",
    "measure_art_width",
    "pad_display",
    "resolve_cow",
    "set_active_cow",
    "wrap_lines",
]
