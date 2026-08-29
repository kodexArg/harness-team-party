#!/usr/bin/env python3
"""Guard: every agent definition binds model: inherit only.

Harness model roles (thinker / builder / scout) live in workflow scripts and
dispatch contracts — never as vendor product names in agent frontmatter.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
BANNED_MODEL_TOKENS = re.compile(
    r"\b(sonnet|haiku|opus|fable|composer)\b", re.IGNORECASE
)

failures = 0


def fail(msg: str) -> None:
    global failures
    failures += 1
    print(f"FAIL: {msg}", file=sys.stderr)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def main() -> int:
    if not AGENTS.is_dir():
        fail(f"{AGENTS.relative_to(ROOT)} is missing")
        return 1

    definitions = sorted(AGENTS.glob("*.md"))
    for path in definitions:
        rel = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")
        fm = frontmatter(text)
        model_match = re.search(r"^model:\s*(\S+)", fm, re.MULTILINE)
        if not model_match:
            fail(f"{rel} omits model:")
            continue
        model = model_match.group(1)
        if model != "inherit":
            fail(f"{rel} has model: {model} — only inherit is allowed")

        body = text[text.find("\n---", 3) + 4 :] if text.startswith("---") else text
        if BANNED_MODEL_TOKENS.search(body):
            fail(
                f"{rel} body names a vendor model or composer product — "
                "use harness role slugs (thinker / builder / scout) in prose instead"
            )

    if not failures:
        ok(f"{len(definitions)} agent definitions, all model: inherit")
        ok("no vendor model names in agent bodies")

    if failures:
        print(f"\n{failures} test(s) failed", file=sys.stderr)
        return 1
    print("\nall 2 test(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
