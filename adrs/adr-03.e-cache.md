---
title: adr-03.e-cache
type: adr
status: active
version: v0.1.2
tags: [cache, backend]
description: "Names the service cache policy: what is used, what is refused, HTTP cache defaults."
applies_when:
  - When adding a cache backend, cache key, or Cache-Control header.
  - When someone proposes Redis or another cache server.
related_agents:
  - hb-ag-service
---

# ADR-03.e — cache

> An explicit cache policy stops a surprise cache server from becoming the architecture.

Instantiation: **rewrite this sub.** `{{cache policy}}` is the decision (examples: PostgreSQL DatabaseCache and no Redis; Redis required; HTTP headers only). Put the same choice in [[adr-02-stack]] (integrations or absences). Do not keep a zero-Redis rule if this project uses Redis.

1. **Named policy.** `{{cache policy}}`

2. **Shared cache.** Cross-instance shared cache, if any, is the mechanism named in that policy — not an undeclared sidecar.

3. **Process-local cache.** In-process caches are allowed only where staleness across tasks is acceptable.

4. **HTTP.** Authenticated API responses default to `Cache-Control: no-store` unless a row in [[INTERFACES]] says otherwise.
