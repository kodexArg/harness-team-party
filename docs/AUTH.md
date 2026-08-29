---
title: Authentication and authorization
type: reference
status: active
version: v0.1.2
tags: [auth, security, ssot]
description: "Identity provider, session model, and the authorization pattern. Ships as a placeholder."
applies_when:
  - When wiring authentication or a permission check.
  - When choosing where an authorization decision lives.
related_adrs:
  - adr-02-stack
  - adr-03-backend
---
# AUTH

> This file is **expected** and currently a placeholder. Instantiation writes
> it when the first protected route exists ([[CLONE]]).

## What it must eventually contain

- **Identity** — `{{identity provider}}`: who authenticates, and the immutable user key.
- **Session model** — how a request carries identity, and for how long.
- **Authorization pattern** — `{{authorization pattern}}`: where permission classes live and how they compose.
- **Development mode** — how local development authenticates without the provider.
- **Boundaries** — what the identity provider is never asked to do (authorization stays in the service unless this file says otherwise).
