#!/usr/bin/env bash
# Shared paths for kskill-graphify scripts. Source from other bin scripts.
set -euo pipefail

_THIS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$_THIS/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../.." && pwd)"
OUT_DIR="$SKILL_DIR/graphify-out"
GRAPH_JSON="$OUT_DIR/graph.json"
UPSTREAM_DIR="$SKILL_DIR/upstream"

export PATH="${HOME}/.local/bin:${PATH}"

require_cli() {
  if ! command -v graphify >/dev/null 2>&1; then
    echo "graphify CLI missing. Run: $SKILL_DIR/bin/ensure" >&2
    exit 1
  fi
}

cd_repo() {
  cd "$REPO_ROOT"
}
