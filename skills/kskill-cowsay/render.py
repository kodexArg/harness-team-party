#!/usr/bin/env python3
"""Project CLI: kodexArg cowsay balloon + optional micro-solid legend."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from lib.legend import say  # noqa: E402

BIN = ROOT / "bin" / "cowsay"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="cowsay with optional micro-solid legends")
    parser.add_argument("--legend", default=None, help="QUICK WIN | GH ISSUE | GH REPO | EPIC DONE!")
    parser.add_argument("-W", type=int, default=40)
    parser.add_argument("message", nargs="*", help="bubble text")
    args = parser.parse_args(argv)
    text = " ".join(args.message) if args.message else "done"
    if args.legend:
        out = say(text, args.legend, width=args.W)
        if out is not None:
            sys.stdout.write(out if out.endswith("\n") else out + "\n")
            return 0
    from subprocess import run

    proc = run(
        [str(BIN), "-W", str(args.W), "--", text],
        capture_output=True,
        text=True,
    )
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
