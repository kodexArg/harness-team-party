#!/usr/bin/env python3
"""PUT the live `main is live` ruleset from scripts/main_is_live_ruleset.json.

Owner rule ([[adr-08-github]] rule 8): required status checks must not delay
merge. Needs Administration: write. A Contents-only PAT returns 403.

Instantiation ([[CLONE]]): fill RULESET_ID (created by the first GET/POST
against the repo's rulesets) and the {{owner}}/{{repo}} pair below.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "scripts" / "main_is_live_ruleset.json"
RULESET_ID = "{{ruleset id}}"
API = "repos/{{owner}}/{{repo}}/rulesets/" + RULESET_ID


def main() -> int:
    payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))
    if any(rule.get("type") == "required_status_checks" for rule in payload["rules"]):
        print("refusing to PUT a payload that still requires status checks", file=sys.stderr)
        return 2
    result = subprocess.run(
        ["gh", "api", "--method", "PUT", API, "--input", str(PAYLOAD)],
        check=False,
    )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
