#!/usr/bin/env python3
"""CLI for the 3-row micro-solid font."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from font import render


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render uppercase text in the 3-row micro-solid font")
    parser.add_argument("text", nargs="*", help="text to render")
    args = parser.parse_args(argv)
    sys.stdout.write(render(" ".join(args.text)))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
