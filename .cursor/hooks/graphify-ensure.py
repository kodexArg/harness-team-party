#!/usr/bin/env python3
"""sessionStart: ensure Graphify CLI + graph.json (fail-open)."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ENSURE = ROOT / "skills" / "kskill-graphify" / "bin" / "ensure"
GRAPH = ROOT / "skills" / "kskill-graphify" / "graphify-out" / "graph.json"


def _present() -> bool:
    return GRAPH.is_file()


def main() -> None:
    try:
        json.load(sys.stdin)
    except json.JSONDecodeError:
        pass
    try:
        subprocess.run(
            [str(ENSURE)],
            cwd=ROOT,
            timeout=120,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.TimeoutExpired):
        pass
    status = "present" if _present() else "absent"
    print(
        json.dumps(
            {
                "additional_context": (
                    f"Graphify graph: {status} at graphify-out/graph.json. "
                    "When present, query/path/explain before Grep. "
                    "Procedure: kskill-graphify. Bootstrap: skills/kskill-graphify/bin/ensure."
                )
            }
        )
    )


if __name__ == "__main__":
    main()
