#!/usr/bin/env python3
"""Guard: no agent definition declares itself a teammate (issue #193).

HARNESS.md carries a standing decision (2026-07-18, upstream issue #321):
every agent under `agents/` runs as a dispatched subagent, never an agent-team
teammate. For guardians the reason is doctrinal — the teammate mechanism's
direct inter-agent mailbox is a second sibling-notification conduit, which the
guardian-dispatch rule in AGENTS.md forbids.

The decision used to be written as "and CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS
is not set". That half was unenforceable and, when checked, false: the flag
lives in the operator's own ~/.claude/settings.json, outside this tree, and it
was set to "1" on the machine that read the claim. A document cannot assert
the state of a file the repository does not control.

So this guard covers the half that IS the repository's to hold — how the
agents are *written*:

  1. No definition declares itself a teammate.
  2. No definition carries `skills:` or `mcpServers:` frontmatter, which the
     teammate mechanism reads and the subagent path ignores. Their presence
     would be evidence a definition was authored for the other shape.

What it deliberately does NOT do is check the environment variable. That is
the failure this test exists because of: asserting something the repo cannot
observe produces a claim that rots silently. If the flag is on, the runtime
may still run these definitions as teammates — the decision constrains
authorship, not the operator's machine, and HARNESS.md now says so.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"

# Frontmatter keys the teammate mechanism reads and the subagent path ignores.
TEAMMATE_ONLY_KEYS = ("skills", "mcpServers")

# A definition declaring itself a teammate, in any of the shapes a frontmatter
# could plausibly use.
TEAMMATE_DECL = re.compile(
    r"^\s*(teammate|is_teammate|team|team_name)\s*:", re.MULTILINE
)

failures = 0


def fail(msg: str) -> None:
    global failures
    failures += 1
    print(f"FAIL: {msg}", file=sys.stderr)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def frontmatter(text: str) -> str:
    """The block between the opening and closing `---`, or "" if absent."""
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end != -1 else ""


def main() -> int:
    if not AGENTS.is_dir():
        fail(f"{AGENTS.relative_to(ROOT)} is missing — the agent SSOT")
        return 1

    definitions = sorted(AGENTS.glob("*.md"))
    if not definitions:
        fail(
            "no agent definitions found under agents/ — either the SSOT moved "
            "or this guard is looking in the wrong place; both are defects"
        )
        return 1

    for path in definitions:
        fm = frontmatter(path.read_text(encoding="utf-8"))
        rel = path.relative_to(ROOT)

        if TEAMMATE_DECL.search(fm):
            fail(
                f"{rel} declares itself a teammate. Every agent under agents/ "
                "is a dispatched subagent (HARNESS standing decision, upstream "
                "#321); for a guardian this also breaks the guardian-dispatch "
                "rule in AGENTS.md, since a teammate mailbox is a second "
                "sibling-notification conduit."
            )

        for key in TEAMMATE_ONLY_KEYS:
            if re.search(rf"^\s*{key}\s*:", fm, re.MULTILINE):
                fail(
                    f"{rel} carries `{key}:` frontmatter, which only the "
                    "teammate mechanism reads — the subagent path ignores it. "
                    "Either the definition was authored for the wrong shape, "
                    "or the key is dead weight implying a capability it does "
                    "not have."
                )

    if not failures:
        ok(f"{len(definitions)} agent definitions, none declares itself a teammate")
        ok("no definition carries teammate-only frontmatter (skills:, mcpServers:)")

    if failures:
        print(f"\n{failures} test(s) failed", file=sys.stderr)
        return 1
    print("\nall 2 test(s) passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
