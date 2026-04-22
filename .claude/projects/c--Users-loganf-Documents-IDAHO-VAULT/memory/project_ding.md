---
name: DING Protocol (v0.0)
description: Informal beta relay protocol introduced 2026-03-29 — do not hard-define
type: project
---

DING is an informal beta relay protocol, introduced 2026-03-29 at v0.0.

**Why:** Relay state signals between agents, branches, or sessions in a lightweight way. Not yet formalized — "do not hard define at this checkpoint" per Logan.

**First instance:** Comment posted on PR #109 (`claude/levelset-refresh-2026-03-29`) on 2026-03-29 by The Abhorsen:

```
DING (v0.0)

relay: claude/levelset-refresh-2026-03-29 → main
signal: LEVELSET refreshed 2026-03-29 — mesh slimmed, Sunday swarm wrapped, PRs current
from: The Abhorsen
```

**How to apply:** When Logan references DING, treat it as a relay signal/ping between swarm nodes. Keep responses loose — this is v0.0. Do not over-engineer or formalize unless Logan asks.

**Related:** PING/PONG is the broader pattern Logan uses for async confirmations (e.g., GCP build steps). DING may be a sub-pattern of that.
