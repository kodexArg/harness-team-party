#!/usr/bin/env python3
"""The PUT payload for `main is live` must not require status checks (#768)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "scripts" / "main_is_live_ruleset.json"


def main() -> int:
    data = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    types = [rule["type"] for rule in data["rules"]]
    if "required_status_checks" in types:
        print("FAIL: payload still requires status checks", file=sys.stderr)
        return 1
    for needed in ("deletion", "non_fast_forward", "pull_request"):
        if needed not in types:
            print(f"FAIL: payload dropped {needed}", file=sys.stderr)
            return 1
    actors = data.get("bypass_actors") or []
    if not any(
        a.get("actor_type") == "RepositoryRole" and a.get("bypass_mode") == "always"
        for a in actors
    ):
        print("FAIL: payload has no admin always-bypass", file=sys.stderr)
        return 1
    print("OK: main is live payload has no required status checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
