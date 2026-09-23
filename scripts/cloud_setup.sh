#!/bin/bash
# Install Graphify before a cloud session snapshots the filesystem.
set -euo pipefail

if timeout 120 skills/kskill-graphify/bin/ensure; then
    echo "[cloud_setup] graphify ensured — CLI on PATH, graph.json present or built --code-only"
else
    echo "[cloud_setup] WARNING: graphify ensure failed or timed out" >&2
fi
