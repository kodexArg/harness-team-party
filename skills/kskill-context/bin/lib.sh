#!/usr/bin/env bash
# Shared paths for kskill-context scripts. Source from other bin scripts.
set -euo pipefail

_THIS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$_THIS/.." && pwd)"
REPO_ROOT="$(cd "$SKILL_DIR/../.." && pwd)"
CONTEXT_DIR="${CONTEXT_DIR:-$REPO_ROOT/context}"
REGISTRY="${CONTEXT_REGISTRY:-$CONTEXT_DIR/repos.json}"
GRAPHS_DIR="$CONTEXT_DIR/.graphs"
REGISTRY_PY="$SKILL_DIR/bin/registry.py"

case ":${PATH}:" in
  *":${HOME}/.local/bin:"*) ;;
  *) PATH="${PATH}:${HOME}/.local/bin" ;;
esac
export PATH

require_cli() {
  if ! command -v graphify >/dev/null 2>&1; then
    echo "graphify CLI missing. Run: $REPO_ROOT/skills/kskill-graphify/bin/ensure" >&2
    exit 1
  fi
}

each_repo() {
  local name="${1:-}"
  if [[ -n "$name" ]]; then
    python3 "$REGISTRY_PY" "$REGISTRY" "$name"
  else
    python3 "$REGISTRY_PY" "$REGISTRY"
  fi
}
