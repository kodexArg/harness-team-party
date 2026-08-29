---
title: adr-04.f-client-api
type: adr
status: active
version: v0.1.2
tags: [client-api, surface]
description: "SSR calls use internal discovery; the browser sends session credentials; only PUBLIC_ vars in the bundle."
applies_when:
  - When the surface fetches a declared interface from server or browser.
  - When adding a surface environment variable.
related_agents:
  - hb-ag-surface
---

# ADR-04.f — client API

> Server-side discovery stays off the public edge; the browser never receives private secrets.

Instantiation: fill `{{client fetch rule}}`. CSRF headers, cookie names, and Cloud Map vs localhost are examples — replace with [[AUTH]] and [[INFRASTRUCTURE]] for this project.

1. **SSR fetch.** Server-side calls to the service use `{{client fetch rule}}` (example: internal DNS in cloud, compose service name locally) — not the public host — unless this project has no SSR.

2. **Browser.** Browser calls send the session credentials [[AUTH]] names. Unsafe methods send the CSRF (or equivalent) header that [[AUTH]] names.

3. **Public env only.** The surface bundle reads only `PUBLIC_*` names declared in [[VARIABLES]]. Private secrets never enter `{{surface tree}}`.
