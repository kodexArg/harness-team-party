#!/bin/bash
# Cloud environment setup script for a cloud agent session.
#
# Paste this one line into the environment's "Setup script" field:
#
#     bash scripts/cloud_setup.sh
#
# Everything else stays versioned here. The script runs once per environment,
# before the agent launches; the platform snapshots the filesystem afterwards, so
# later sessions start with the work already on disk. Keep it well under the
# ~5 minute budget or the snapshot never builds and every session pays the cost.
set -euo pipefail

# Graphify CLI + graph.json. Non-fatal: a missing graphify is Grep-first
# per AGENTS.md, not a broken snapshot. Isolated uv tool, not a project dependency.
if timeout 120 skills/kskill-graphify/bin/ensure; then
    echo "[cloud_setup] graphify ensured — CLI on PATH, graph.json present or built --code-only"
else
    echo "[cloud_setup] WARNING: graphify ensure failed or timed out" >&2
fi

# Instantiation ([[CLONE]]): pre-warm the product trees' dependencies here
# (e.g. the service toolchain's install, the surface toolchain's install) so a
# cloud session can build, not only propose the change. Keep every prewarm
# NON-FATAL — a proxy failure must never abort the snapshot.
