---
version: v1.0
approved: 2026-04-22
status: approved
authority: LOGAN
related:
  - AGENTS
  - CONSTITUTION
  - DECISIONS
  - FLAG
  - LEVELSET
  - LOGAN
  - PROTOCOL
  - CONVENE
  - CONFERENCE
  - XKCD
  - agent
  - coordination
  - multi-agent
  - sync
---
# CONFERENCE CALL v1.0 — Multi-Agent Synchronized Work Session

*Approved 2026-04-22. Proposed by GitHub Copilot (The Clerk), 2026-04-06. Pending formal ratification.*

---

## I. PURPOSE

CONFERENCE CALL governs how Logan **formally convenes multiple agents** for a synchronized, agenda-driven working session.

A CONFERENCE CALL is declared when Logan needs more than one agent to act together on a shared topic.

---

## II. SCOPE

CONFERENCE CALL applies to:
- Multi-agent planning sessions
- Field-capture processing sessions
- Cross-tier vault operations
- Emergency synchronization
- Any session Logan marks with the CONFERENCE CALL signal

CONFERENCE CALL does **not** replace:
- LEVELSET (agent orientation)
- XKCD (message routing)

---

## III. CORE PRINCIPLES

1. **Logan Chairs** — No agent self-convenes or self-promotes to Chair
2. **Quorum is What Logan Says It Is** — Logan names participants
3. **One Agenda, One Record** — Every CONFERENCE produces one durable CONFERENCE RECORD
4. **Lanes Persist** — Lane boundaries remain during CONFERENCE
5. **Vault Over Chat** — Outputs are vault artifacts; chat is ephemeral

---

## IV. CONFERENCE STRUCTURE

| Phase | Name | Actor | Description |
|---|---|---|---|
| 1 | **CALL** | Logan | Declares the CONFERENCE, names participants, sets agenda |
| 2 | **CONVENE** | Agents | Each acknowledges, runs LEVELSET, declares readiness |
| 3 | **CONFERENCE** | Chair-directed | Agenda items worked in order |
| 4 | **RECORD** | Recording Agent | Outputs consolidated into CONFERENCE RECORD |
| 5 | **DISMISS** | Logan | Chair formally closes; agents return to lanes |

---

## V. ROLES

### Chair (Logan)
- Opens and closes the CONFERENCE
- Sets and owns the agenda
- Directs agent action
- Resolves disputes
- Signs off on the CONFERENCE RECORD

### Participants
- Acknowledge CALL, declare readiness (CONVENE)
- Work assigned agenda items
- Surface FLAGs immediately

### Recording Agent
- Designated by Logan
- Writes and commits CONFERENCE RECORD
- Does not editorialize

---

## VI. INVOCATION

### The CALL Signal

```
CONFERENCE CALL
DATE: YYYY-MM-DD
CHAIR: Logan
PARTICIPANTS: [list]
AGENDA:
  1. [Item]
RECORDING AGENT: [agent]
```

### The CONVENE Acknowledgment

Each invited agent responds:

```
CONVENE ACK
AGENT: [Name + persona]
LEVELSET: [brief summary]
READY: YES / NO
```

---

## VII. RUNNING THE CONFERENCE

1. Chair introduces item
2. Designated agent(s) act
3. FLAGs raised immediately if blocking
4. Output confirmed by Chair
5. NEXT ITEM or HOLD

---

## VIII. THE CONFERENCE RECORD

Location: `!/CONFERENCE-RECORD-[YYYY-MM-DD]-[TOPIC-SLUG].md`

Structure:
```yaml
---
type: conference-record
date: YYYY-MM-DD
chair: Logan
participants: [...]
recording-agent: [agent]
status: open | closed | partial
---
```

### RECORD Sections
- Agenda
- Item outcomes (COMPLETE / HOLD / DEFERRED)
- FLAGs Raised
- Decisions Made
- Action Items
- DISMISSED (sign-off)

---

## IX. CLOSURE

Logan closes:

```
CONFERENCE CLOSED
DATE: YYYY-MM-DD
RECORD: [file path]
DISMISSED: [agents]
```

---

## X. FAILURE MODES

| Failure | Mitigation |
|---|---|
| Quorum not reached | Chair decides: delay, substitute, or proceed |
| Scope explosion | Reject additions; log as proposed follow-up |
| Lane conflict | Chair arbitrates |
| Recording agent fails | Any participant may draft; Chair signs |

---

## XI. OPEN QUESTIONS FOR LOGAN

1. Record location: `!/` or `!/!/`?
2. Async CONFERENCE supported?
3. Automated trigger for scheduled work?
4. Numbered records (CONF-001) or dated slugs?
5. Minimum quorum (1 agent + Logan, or 2+)?

---

###### [["The world is quiet here."]]