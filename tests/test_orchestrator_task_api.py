from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "kskill-orchestrator" / "SKILL.md"
TEAMS = ROOT / "skills" / "kskill-orchestrator" / "references" / "agent-teams.md"
LOW = ROOT / "agents" / "kbot-low.md"

try:
    import pytest
except ImportError:  # script mode — main() carries the skip
    pytest = None


def _require_vendored() -> None:
    """The skip contract of main(), honored under pytest collection too: a
    skill that is not vendored skips, it never fails for its absence."""
    if not SKILL.is_file() and pytest is not None:
        pytest.skip("kskill-orchestrator is not vendored")


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    raise AssertionError(msg)


def ok(msg: str) -> None:
    print(f"ok  {msg}")


def forming_the_team(text: str) -> str:
    match = re.search(
        r"## Forming the Team.*?(?=\n## )",
        text,
        re.S,
    )
    if not match:
        fail("SKILL.md has no Forming the Team heading")
    return match.group(0)


def test_forming_the_team_opens_with_spawn_not_taskcreate() -> None:
    _require_vendored()
    section = forming_the_team(SKILL.read_text(encoding="utf-8"))
    first = re.search(r"^1\.\s+\*\*([^*]+)\*\*", section, re.M)
    if not first:
        fail("Forming the Team has no numbered step 1")
    step = first.group(1)
    if "TaskCreate" in step:
        fail(f"Forming the Team still opens with TaskCreate: {step}")
    if "Spawn" not in step:
        fail(f"Forming the Team step 1 is not a spawn: {step}")
    ok("Forming the Team opens with spawn, not TaskCreate")


def test_taskcreate_is_a_capability_check() -> None:
    _require_vendored()
    text = SKILL.read_text(encoding="utf-8")
    if not re.search(r"if `TaskCreate` exists,\s*prefer it", text):
        fail("SKILL.md lost the TaskCreate capability-check (same shape as TeamCreate)")
    if "do NOT exist in this harness" not in text:
        fail("SKILL.md no longer says TaskCreate does not exist in this harness")
    ok("TaskCreate is a capability check, not a mandatory first step")


def test_agent_teams_does_not_promise_a_shared_task_list() -> None:
    _require_vendored()
    text = TEAMS.read_text(encoding="utf-8")
    if "This still gives peer messaging and a shared" in text:
        fail("agent-teams.md still promises a shared task list")
    if "there is no shared task list" not in text:
        fail("agent-teams.md does not state that there is no shared task list")
    if "lead sequences" not in text and "Sequence waves on the lead side" not in text:
        fail("agent-teams.md lost lead-side sequencing")
    if "agentId" not in text:
        fail("agent-teams.md does not tell the lead to capture agentId")
    ok("agent-teams.md sequences on the lead side and addresses agentId")


def test_kbot_low_has_no_shell() -> None:
    _require_vendored()
    skill = SKILL.read_text(encoding="utf-8")
    if "**No Bash**" not in skill:
        fail("SKILL.md tier table does not say kbot-low has no Bash")
    if "kbot-medium" not in skill or "shell" not in skill.lower():
        fail("SKILL.md does not route shell-needing reads to kbot-medium")
    low = LOW.read_text(encoding="utf-8")
    tools = re.search(r"^tools:\n((?:  - .+\n)+)", low, re.M)
    if not tools:
        fail("agents/kbot-low.md has no tools block")
    names = {line.strip()[2:] for line in tools.group(1).splitlines() if line.strip()}
    if "Bash" in names:
        fail("agents/kbot-low.md lists Bash")
    if "No Bash" not in low:
        fail("agents/kbot-low.md body does not say No Bash")
    ok("kbot-low has no Bash; shell-needing reads go to kbot-medium")


def main() -> int:
    if not SKILL.is_file():
        print("skip  kskill-orchestrator is not vendored")
        return 0
    failed = 0
    for name, fn in sorted(globals().items()):
        if not name.startswith("test_"):
            continue
        try:
            fn()
        except Exception as exc:
            print(f"FAIL: {name}: {exc}", file=sys.stderr)
            failed += 1
    if failed:
        print(f"\n{failed} test(s) failed", file=sys.stderr)
        return 1
    print("\nall test(s) passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
