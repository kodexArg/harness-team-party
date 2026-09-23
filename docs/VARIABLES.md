---
title: Environment variables
type: reference
status: active
version: v0.1.0
tags: [variables, secrets, config]
description: "Declared environment variables. A name used in code or in .env and missing here does not exist."
applies_when:
  - When declaring an environment variable.
  - When checking whether a value may be committed.
related_adrs:
  - adr-02-stack
---
# VARIABLES

Every variable this repository reads is declared here first.

Secret values live in gitignored `.env` on the workstation. They are never committed.

| Name | Scope | Envs | Secret? | Source | Description |
|---|---|---|---|---|---|
| `OPENROUTER_API_KEY` | local | local | yes | `.env` | OpenRouter API key for local model calls |
| `OPENROUTER_MODEL_ID` | local | local | no | `.env` | OpenRouter model slug (`org/model`). Default in `.env.example`: `z-ai/glm-5.3-flash` |
