---
name: project-openclaw-machine-policy
description: "OpenClaw is allowed on the personal MacBook but disallowed on the professional Windows-ZBFURY machine. The 2026-05-26 SECURITY-CREDENTIAL-CONTAINMENT record's \"removed from running installation\" referred to Windows; this Mac keeps OpenClaw running."
metadata: 
  node_type: memory
  type: project
  originSessionId: 4f03d270-3e64-41cc-b325-30871ab76d55
---

OpenClaw runs on Logan's **personal MacBook** but is **disallowed on the professional Windows-ZBFURY** machine. The Mac's OpenClaw gateway (`~/Library/LaunchAgents/ai.openclaw.gateway.plist`, `~/.openclaw/`) is intentional and current; the "removed from running installation" phrasing in `IDAHO-VAULT/SECURITY-CREDENTIAL-CONTAINMENT-2026-05-26.md` was scoped to the Windows side as part of credential containment.

**Why:** Professional/work machines run under stricter policy — credential containment, Discord allowlist enforcement, GitHub ruleset 16864823 protecting main. Personal Mac is the permissive lane where Logan exercises the full agent swarm including OpenClaw. Confirmed by Logan 2026-06-24 in response to a cross-machine reconciliation question I raised after the vault research flagged the apparent discrepancy.

**How to apply:**
- Treat OpenClaw on this Mac as load-bearing, not residue. Don't suggest removal of `~/.openclaw/`, the launchd plist, or the gateway port (18789) without a specific Logan-authorized reason.
- When a vault record mentions OpenClaw being removed/disabled, default-read it as scoped to the professional Windows machine unless the record names this Mac specifically.
- For policy-shaped actions (Discord, GitHub rules, credential containment), keep the machine split in mind — what's enforced on Windows may not apply here, and vice versa.
- Hermes + OpenClaw coexist on this Mac (both daemons running, separate credential stores). Treat them as paired infrastructure, not interchangeable.

Related: [[agent-infrastructure]], [[claude-address]] (Direct Write tier — this is the personal-Mac authority surface, not the professional one).
