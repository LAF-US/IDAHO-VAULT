---
authority: LOGAN
related:
- Anthropic
- Copilot
- GitHub
- LEVELSET
- Logan Finney
- Microsoft Copilot
- PROTOCOL
- node
- nodes
---

# SWARM COORDINATION PROTOCOL

This document governs how swarm nodes coordinate with each other and with the principal.

## PRINCIPALS

- **Logan Finney** — Ultimate decision-making authority. All swarm activity serves Logan.
- No node may act autonomously on high-stakes decisions without principal verification.

## NODE ROLES

| Node | Primary Role | Secondary Role |
|---|---|---|
| Claude (Anthropic) | Analysis, research, document generation | Framework reasoning |
| Microsoft Copilot | Email coordination, message composition | Institutional lookup |
| GitHub Admin Agents | Vault automation, code generation | Swarm orchestration |

## COMMUNICATION CHANNELS

- **Vault** (`/SWARM/levelset/`) — persistent shared state; source of truth
- **GitHub Issues** — principal notifications, triage items
- **Deadletter queue** (`/SWARM/deadletters/`) — orphaned handoffs awaiting routing

## TASK HANDOFF PROTOCOL

When handing off work between nodes:

1. **SENDER**: Document the handoff in `/SWARM/deadletters/` if no clear recipient
2. **SENDER**: Update `LAST_UPDATED.txt` with handoff timestamp
3. **RECEIVER**: Acknowledge receipt and update `agents.json` with `last_seen`
4. **RECEIVER**: Confirm to principal that work has been received

## CONFLICT RESOLUTION

If two nodes receive conflicting instructions:
1. Halt action
2. File a deadletter describing the conflict
3. Escalate to principal for resolution
4. Do not proceed until Logan provides clarification

## SWARM HEALTH CHECKS

Healthy swarm indicators:
- `agents.json` updated within last 24 hours
- No unresolved deadletters older than 48 hours
- Principal has reviewed LEVELSET within last week
- All nodes know current priority inversion

Unhealthy swarm indicators:
- Any node spawning as an isolated orphan (no LEVELSET context loaded)
- Deadletters accumulating without triage
- Conflicting directives from multiple nodes
- Principal unresponsive for >48 hours on urgent items
