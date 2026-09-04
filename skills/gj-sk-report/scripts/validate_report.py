#!/usr/bin/env python3
"""Structural gate for gj-sk-report HTML artifacts.

Exit 0 = deliverable. Exit 1 = fix before save/send.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"\{\{[A-Z0-9_]+\}\}")
VIEWPORT_RE = re.compile(
    r'<meta[^>]+name=["\']viewport["\'][^>]*>', re.IGNORECASE
)
MERMAID_CDN_RE = re.compile(r"cdn\.jsdelivr\.net/npm/mermaid|mermaid\.min\.js", re.I)
TAKEAWAY_RE = re.compile(r'class=["\'][^"\']*takeaway', re.I)
SVG_RE = re.compile(r"<svg\b", re.I)
SVG_A11Y_RE = re.compile(r'<svg[^>]+role=["\']img["\']', re.I)


def check(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if not text.lstrip().lower().startswith("<!doctype html"):
        errors.append("missing <!doctype html>")
    if not VIEWPORT_RE.search(text):
        errors.append("missing viewport meta (mobile-first required)")

    leftovers = sorted(set(PLACEHOLDER_RE.findall(text)))
    if leftovers:
        errors.append(f"unfilled placeholders: {', '.join(leftovers)}")

    if MERMAID_CDN_RE.search(text):
        errors.append(
            "mermaid CDN found — prefer diagram-design SVG embed "
            "(see references/diagram-bridge.md)"
        )

    takeaways = TAKEAWAY_RE.findall(text)
    if len(takeaways) > 1:
        errors.append(f"more than one .takeaway ({len(takeaways)})")

    svg_count = len(SVG_RE.findall(text))
    a11y_count = len(SVG_A11Y_RE.findall(text))
    if svg_count and a11y_count < svg_count:
        errors.append(
            f"SVG accessibility: {svg_count} <svg> but {a11y_count} with role=img"
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="artifact .html path")
    args = parser.parse_args()

    if not args.html.is_file():
        print(f"FAIL: not a file: {args.html}", file=sys.stderr)
        return 1

    errors = check(args.html)
    if errors:
        print(f"FAIL {args.html}", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK {args.html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
