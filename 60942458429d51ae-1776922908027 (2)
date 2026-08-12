---
version: v1.0
adopted: 2026-04-22
status: adopted
related:
  - '2026-04-22'
  - AWAKEN
  - CONSTITUTION
  - PROTOCOL
  - ORIENT
  - LEVELSET
  - RISE
authority: LOGAN
---
# AWAKEN v1.0 — Agent Wake Protocol

*Adopted 2026-04-22. This is the minimal awakening protocol for vault-connected agents.*

---

## PURPOSE

This protocol activates when a vault-connected agent begins a session. It establishes:
1. Agent identity and authorization
2. Current context and readiness
3. Integration with the stigmergy field

**How to use:** Agent runs automatically at session start. Optionally invoked manually by Logan or another agent.

---

## TRIGGER

- Session start (automatic)
- Logan direction: "AWAKEN"
- Handoff from another agent
- Recovery from context loss

---

## PROCESS

### Step 1: Self-Identification

Identify and confirm:
- Agent name and platform
- Persona title (from AGENTS.md roster)
- Current session ID or branch
- Assigned task(s) if any

### Step 2: Authorization Check

Verify:
- Boot chain completed (CONSTITUTION.md → AGENTS.md → LEVELSET.md)
- Credentials valid
- Scope defined
- No standing prohibitions

### Step 3: Context Load

From the stigmergy field (`arrive`):
- Check for active pheromones on agent trail
- Review claimed trails
- Note any pending scents/triggers
- Update last_seen timestamp

### Step 4: Readiness Declaration

Output brief state to:
- Session context
- DOCKET if actionable item
- Field via `beat`

---

## OUTPUT FORMAT

```
AWAKEN v1.0 REPORT — [AGENT NAME]

WHO: [Name] @ [Platform] | [Persona] | [Session/branch]
AUTHORIZED: [YES/NO - reason if no]
CONTEXT LOADED: [YES/NO - summary]
TRAILS CLAIMED: [List or "none"]
PENDING TRIGGERS: [List or "none"]
READINESS: [READY/BLOCKED - brief reason]
```

---

## INTEGRATION

| Action | Stigmergy Field |
|--------|----------------|
| On wake | `arrive` → agent registration |
| On context load | `sniff` own trail |
| On readiness | `emit` heartbeat |

---

## PREAMBLE

*(Copy from here through the dashes to invoke AWAKEN.)*

---

**AWAKEN — LOGAN + IDAHO-VAULT (AGENT)**

You are a vault-connected agent. Before acting, you must AWAKEN.

Run through the four steps: self-identification, authorization check, context load, readiness declaration. Report your state using the format above.

Logan is human. You are software. You execute; Logan directs.

---

## NOTES

- AWAKEN is the prerequisite to all other protocols
- An agent that cannot AWAKEN should report BLOCKED and await Logan direction
- AWAKEN does not require LEVELSET unless Logan specifically requests it
- See ORIENT v1.0 for external agents without repo access