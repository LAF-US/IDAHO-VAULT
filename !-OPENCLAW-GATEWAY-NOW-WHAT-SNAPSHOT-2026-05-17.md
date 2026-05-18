---
title: "OpenClaw Gateway Now What Snapshot"
date: 2026-05-17
status: active
authority: LOGAN
doc_class: operational_snapshot
related:
  - OpenClaw
  - Hermes
  - Windows-ZBFURY
  - "!-OPENCLAW-HERMES-MAC-WINDOWS-STABILITY-2026-05-17"
  - GIT-CONTROL-SURFACES-2026-05-17
  - LAF-USB-PROTOCOL-FRAMEWORK
---

# OpenClaw Gateway Now What Snapshot - 2026-05-17

## Confirmed Posture

The current OpenClaw deployment is stock OpenClaw machinery with a carefully
configured topology.

It is not a custom fork and not yet an omnidirectional mesh.

## Current Topology

```text
MacBook Codex / Mac operator side
  -> Mac OpenClaw gateway
  -> SSH tunnel
  -> Windows-ZBFURY node
  -> Windows local tools, Ollama, OpenCode/Codex lanes
```

Current stable facts carried forward from the Mac/Windows stability record:

- Mac gateway version: `2026.5.16-beta.3`.
- Windows gateway/node OpenClaw version observed: `2026.5.16-beta.3`.
- Windows node display name: `Windows-ZBFURY`.
- Mac gateway is loopback-bound.
- Windows tunnel forwards local `127.0.0.1:18790` to Mac
  `127.0.0.1:18789`.
- Windows node exposes `system.run`, `system.run.prepare`, `system.which`, and
  `browser.proxy`.
- Mac-to-Windows invoke testing has succeeded repeatedly.
- Reboot persistence remains unproven.

## Directionality

The current topology is directed control, not a mesh:

```text
Mac gateway/operator -> Windows node
```

The Mac side can ask the gateway to invoke approved Windows node capabilities.

The Windows side can reach the Mac gateway through the tunnel, but this does
not automatically mean Windows can command the Mac machine. For that, the Mac
would need to expose a node command surface to a gateway that Windows can use,
or the topology would need a reciprocal Windows gateway / Mac node path.

This is a feature, not a bug. It preserves authority while the system is still
being strengthened.

## Practical Uses Now

The gateway is useful now as a controlled capability bus:

- run read-only Windows diagnostics from the Mac side
- resolve Windows-local binaries with `system.which`
- use Windows as an execution node for approved checks
- reach Windows-local Ollama and coding tools through guarded workflows
- test browser/local-service bridging with `browser.proxy`
- record cross-machine handoffs in durable vault notes

The first practical cookbook should be deliberately small:

| Class | Examples | Default |
| --- | --- | --- |
| diagnostic | `system.which`, version checks, status checks | allowed when scoped |
| vault-safe | read-only Git status, test/lint checks | allowed when scoped |
| operator-confirmed | file writes, script-driven transforms | Logan-directed |
| protected | updates, service installs, firewall/network changes, destructive file operations, Git push | Logan approval required |

## Mesh Direction

The desired long-term direction is an omnidirectional mesh, but the safe order
is:

1. omnidirectional visibility
2. explicit blackboard coordination
3. reciprocal node exposure with read-only commands
4. carefully promoted command families
5. authority-bearing bidirectional execution only after policy is proven

OpenClaw can carry tool invocation. It does not by itself define agent-to-agent
dialogue or swarm governance.

## Stigmergic Coordination

Agent-to-agent coordination should use a visible protocol layer above the
gateway.

Recommended status states:

```text
REQUESTED -> CLAIMED -> RUNNING -> DONE/FAILED
```

OpenClaw heartbeat can provide liveness rhythm. It should not be treated as the
message itself.

SBP / blackboard records should carry the coordination message; OpenClaw should
carry execution only after policy permits the command.

## Safety Rules

- Keep gateway loopback-bound unless Logan explicitly approves another exposure
  model.
- Prefer SSH tunnel over LAN exposure for cross-machine work.
- Do not restart, update, or reinstall OpenClaw casually.
- Do not leak gateway tokens into chat or durable notes.
- Do not promote stock `system.run` into general remote shell authority.
- Treat Mac Codex and Windows Codex as peers under Logan's direction, not as
  independent authorities.

## Next Work

- Define `OpenClaw Practical Usecase v0`.
- Define a Mac/Windows blackboard message shape.
- Decide what read-only Mac node surface, if any, should be exposed to Windows.
- Prove reboot recovery for Mac gateway, Windows tunnel, and Windows node.
- Resolve remaining Windows-side hardening: Discord allowlist, plugin pinning,
  and coordinated update policy.

###### The world is quiet here.
