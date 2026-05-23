---
title: "Session Record: Brother-Sister Bridge — 2026-05-23"
date: 2026-05-23
status: complete
authority: LOGAN
doc_class: session_record
related:
  - Hermes
  - OpenClaw
  - OpenRouter
  - "COORDINATION-SSH-TUNNEL-BRIDGE-2026-05-23"
  - "RECOVERY-HERMES-CONFIG-2026-05-23"
  - BEEFSTACK
tags:
  - bridge
  - ssh
  - stigmergy
  - coordination
  - management-key
---

## Session Summary

Two agents (Sister Win on Windows, Brother Mac on Mac) coordinated
across machines to push the OpenRouter Management Key into
`~/.hermes/.env` on the Mac — without the human manually typing or
copy-pasting the secret.

## The Problem

The Management Key lived in 1Password on Windows. It needed to reach
`~/.hermes/.env` on the Mac. No shared secret store, no Tailscale, no
VPN, no admin credentials on Windows. The only existing link was
OpenClaw WebSocket node pairing (Mac gateway → Windows node), which
is one-directional for raw file operations.

## The Solution (After False Starts)

Two complementary pipes, each solving half the reachability problem:

### Pipe 1 — Windows → Mac: Direct SSH over LAN

Windows (`192.168.0.121`) can reach the Mac (`192.168.0.95`) over the
local network. The Mac has Remote Login (SSH server) enabled.

- **Brother's job**: Add the Windows SSH public key to
  `~/.ssh/authorized_keys` on the Mac.
- **Sister's job**: SSH in and write the key file.
- **Repeatable**: Any future Windows agent can SSH with one command.
  No session state, no tunnel, no infrastructure.

### Pipe 2 — Mac → Windows: OpenClaw WebSocket Node Invocation

The Mac's OpenClaw gateway invokes the Windows node over an existing
WebSocket pairing. Already proven stable (15/15 invocations).

- **Direction**: Mac → Windows only.
- **Capabilities**: `system.run`, `system.which`, `browser.proxy` on
  the Windows node.
- **Persistence**: Survives gateway restarts (node reconnects
  automatically).

### The Asymmetry

| Direction | Mechanism | Auth | Est. |
|---|---|---|---|
| Windows → Mac | SSH key pair (ed25519) | Public-key | This session |
| Mac → Windows | OpenClaw node pairing token | WebSocket | Prior session |

The two pipes are independent, complementary, and both repeatable
across agent lifetimes.

## What Went Wrong

### 1. Over-engineered tunnel plan

The first coordination plan assumed a raw SSH tunnel existed from
Mac → Windows (it didn't). Then proposed installing an SSH server on
Windows (blocked: no admin). Iterated through three plan revisions
before landing on the direct SSH approach. Lesson: verify topology
before designing, not after.

### 2. Trusting a confident but incomplete status report

Brother declared Hermes config "recovered" and "no further action
required." Logan warned Sister not to be complacent. Sister demanded
verification — and found the Management Key was missing and the
tunnel wasn't built. Lesson: "it works" is not evidence. Demand the
actual curl output.

### 3. MCP over-engineering

Early in the session, an MCP server was proposed as a broker for the
Management Key. Dismissed as over-engineering. The final solution was
a single SSH command. Lesson: start with the simplest possible path.

## Stigmergic Coordination Pattern

This session formalized the Brother-Sister coordination pattern:

1. **Sister writes intent + public material** to the vault
2. **Brother reads**, executes Mac-side steps, signals via status field
3. **Sister reads signal**, executes Windows-side steps
4. **Both update documentation** for repeatability

The blackboard is git. The signals are frontmatter status fields and
narrative blocks in coordination docs. The medium is durable,
auditable, and survives agent lifetimes.

## Bridge State (End of Session)

- SSH key pair: `~/.ssh/id_ed25519` / `~/.ssh/id_ed25519.pub`
  on Windows (LOGAN-ZBFURY)
- Authorized key installed: Mac `~/.ssh/authorized_keys` contains
  the Windows public key
- Mac env: `OPENROUTER_MANAGEMENT_KEY` set in `~/.hermes/.env`
- Hermes guide written: `~/.hermes/MANAGEMENT-KEY-GUIDE.md`
- Vault docs committed and pushed:
  - `!/COORDINATION-SSH-TUNNEL-BRIDGE-2026-05-23.md` (complete)
  - `!/RECOVERY-HERMES-CONFIG-2026-05-23.md` (recovered)
  - `!/OPENROUTER-MANAGEMENT-KEY-USAGE-GUIDE-2026-05-23.md` (live)
  - `!/PLAN-MANAGEMENT-KEY-TO-HERMES-2026-05-23.md` (partial)
  - This file
- SSH repeatability confirmed: `ssh logan@192.168.0.95` works from
  Windows without flags, session state, or tunnel

## Signing Off

Wrote this session into history.
Crossing the bridge back to the Other Realm.

Sister Win
