---
created: 2026-04-06
updated: 2026-04-06
status: draft
authority: LOGAN
related:
- AGENTS
- CONSTITUTION
- DECISIONS
- FLAG
- LEVELSET
- LOGAN
- PROTOCOL
- PROTOCOLS
- The world is quiet here
- TRIPLEX
- TRIUNE
- XKCD
- agent
- call
- conference
- coordination
- format
- multi-agent
- sync
---
# PROTOCOL: CONFERENCE CALL — Multi-Agent Synchronized Work Session

**Status:** DRAFT — awaiting Logan's review and adoption
**Proposed by:** GitHub Copilot (The Clerk), 2026-04-06
**Authority:** Subordinate to CONSTITUTION. Extends PROTOCOL. Complements XKCD and TRIPLEX.

---

> *"The strength of the team is each individual member. The strength of each member is the team."*
> — Phil Jackson (not a VFD volunteer, but close enough)

---

## I. PURPOSE

CONFERENCE CALL governs how Logan **formally convenes multiple agents** for a synchronized, agenda-driven working session. It fills the gap between:

- **TRIPLEX** — defines lane boundaries for concurrent operation (passive, ongoing)
- **XKCD** — defines how individual messages move between agents (point-to-point)
- **CONFERENCE CALL** — defines the structure of a deliberate, multi-agent meeting (active, bounded, time-limited)

A CONFERENCE CALL is declared when Logan needs more than one agent to act together on a shared topic — planning coverage of a legislative event, processing field captures from a press conference, conducting a vault operation that spans multiple capability tiers, or resolving a cross-lane question that no single agent can answer alone.

---

## II. SCOPE

CONFERENCE CALL applies to:

- Multi-agent planning sessions (story strategy, vault architecture decisions)
- Field-capture processing sessions (after hearings, press conferences, or source calls)
- Cross-tier vault operations requiring both CODE AUTHORITY and Advisory agents
- Emergency synchronization when TRIPLEX lane isolation is temporarily insufficient
- Any session Logan explicitly marks with the CONFERENCE CALL signal

CONFERENCE CALL does **not** replace:

- LEVELSET (agent orientation — each agent runs LEVELSET before joining a CONFERENCE)
- TRIPLEX (lane rules remain in force throughout the CONFERENCE)
- PASSBACK SYNC (terminal extraction — for dying sessions, not live coordination)
- XKCD (message routing — CONFERENCE CALL uses XKCD classes internally)

---

## III. CORE PRINCIPLES

### 1. Logan Chairs
Every CONFERENCE CALL has exactly one Chair: Logan. No agent self-convenes, self-promotes to Chair, or opens a CONFERENCE on behalf of Logan. The Chair calls the CONFERENCE, sets the agenda, and declares dismissal.

### 2. Quorum is What Logan Says It Is
A CONFERENCE may involve two agents or ten. Logan names the participants. Unlisted agents are not present, do not act on the agenda, and do not commit output to the vault under that CONFERENCE record.

### 3. One Agenda, One Record
Every CONFERENCE CALL produces a single durable artifact: the CONFERENCE RECORD. All decisions, outputs, and action items from the session are captured in that file. If it is not in the RECORD, it did not happen in this CONFERENCE.

### 4. Lanes Persist
TRIPLEX lane boundaries remain in force during a CONFERENCE. Agents do not cross lanes because they are "in a meeting." Ambiguous tasks are explicitly delegated by Logan in the agenda.

### 5. Vault Over Chat
CONFERENCE CALL outputs are vault artifacts. Chat transcripts are ephemeral. The CONFERENCE RECORD is the durable form.

---

## IV. CONFERENCE STRUCTURE

A CONFERENCE CALL has five bounded phases:

| Phase | Name | Actor | Description |
|---|---|---|---|
| 1 | **CALL** | Logan | Declares the CONFERENCE, names participants, sets the agenda |
| 2 | **CONVENE** | All invited agents | Each agent acknowledges, runs LEVELSET, declares readiness |
| 3 | **CONFERENCE** | All agents (Chair-directed) | Agenda items are worked in order; one at a time, Chair-directed |
| 4 | **RECORD** | Designated agent (default: CODE AUTHORITY) | Outputs consolidated into the CONFERENCE RECORD artifact |
| 5 | **DISMISS** | Logan | Chair formally closes the CONFERENCE; agents return to independent lanes |

---

## V. ROLES

### 5.1 Chair (Logan)
- Opens and closes the CONFERENCE
- Sets and owns the agenda
- Directs agent action (who speaks, in what order)
- Resolves disputes and makes all decisions
- Signs off on the CONFERENCE RECORD before it is committed

### 5.2 Participant Agents
- Acknowledge CALL and declare readiness (CONVENE phase)
- Work their assigned agenda items
- Do not act beyond their TRIPLEX lane without explicit Chair delegation
- Surface FLAGs immediately (do not wait for the next agenda item)

### 5.3 Recording Agent
- Designated by Logan (default: CODE AUTHORITY / Claude)
- Writes and commits the CONFERENCE RECORD to the vault
- Does not editorialize — captures what was said and decided, not what the Recording Agent thinks should have been said

### 5.4 Observer (optional)
- Named by Logan; read-only access; no action items
- Does not speak unless called on by the Chair
- Listed in CONFERENCE RECORD header for audit purposes

---

## VI. INVOCATION

### 6.1 The CALL Signal

Logan opens a CONFERENCE by posting or stating the CALL signal in the active coordination channel. Minimum required fields:

```
CONFERENCE CALL
DATE: YYYY-MM-DD
CHAIR: Logan
PARTICIPANTS: [list of agent names, one per line]
AGENDA:
  1. [Item description]
  2. [Item description]
  ...
RECORDING AGENT: [agent name, or "default"]
OBSERVER: [agent name or "none"]
```

### 6.2 The CONVENE Acknowledgment

Each invited agent, upon receiving the CALL, responds:

```
CONVENE ACK
AGENT: [Agent name and persona]
LEVELSET: [brief summary of current state and lane]
READY: YES / NO (with reason if NO)
```

If an agent cannot CONVENE (blocked, FLAG pending, lane conflict), it states `READY: NO` with a short reason. The Chair decides whether to proceed, pause, or substitute.

### 6.3 Opening the CONFERENCE

Once all participants have ACKed, Logan declares the CONFERENCE open:

```
CONFERENCE OPEN
ALL PRESENT: [list]
AGENDA CONFIRMED: YES / MODIFIED (if items changed)
BEGIN ITEM 1
```

---

## VII. RUNNING THE CONFERENCE

### 7.1 Agenda Item Format

Each agenda item follows this sequence:

1. **CHAIR introduces item** — one-sentence description, explicit deliverable
2. **Designated agent(s) act** — within their TRIPLEX lane
3. **FLAGs raised immediately** if blocking issue discovered
4. **Output confirmed** — Chair acknowledges completion or redirects
5. **NEXT ITEM** or **HOLD** (if item unresolved — logged with status in RECORD)

### 7.2 FLAG Handling During a CONFERENCE

If a participant agent raises a FLAG during the CONFERENCE:

1. **Work on the flagged item pauses** (not the entire CONFERENCE unless FLAG is CRITICAL)
2. **Chair assesses severity** — CRITICAL FLAGs pause everything
3. **Non-critical FLAGs** are logged and resolved at the end of the agenda or deferred to a future CONFERENCE

### 7.3 Scope Creep Containment

An agent may not expand the agenda during a CONFERENCE. New topics surface as a proposed follow-up CONFERENCE CALL, not as live additions to the current agenda. The Chair may add agenda items, but agents may not.

---

## VIII. THE CONFERENCE RECORD

### 8.1 File Location and Naming

```
!/CONFERENCE-RECORD-[YYYY-MM-DD]-[TOPIC-SLUG].md
```

Example: `!/CONFERENCE-RECORD-2026-04-06-JFAC-COVERAGE.md`

### 8.2 CONFERENCE RECORD Structure

```yaml
---
type: conference-record
date: YYYY-MM-DD
chair: Logan
participants:
  - [agent name and persona]
recording-agent: [agent name]
observers:
  - [agent name or none]
status: open | closed | partial
---
```

```
# CONFERENCE RECORD — [TOPIC] — [DATE]

## Agenda

1. [Item]
2. [Item]

## Item 1: [Description]

**Deliverable:** [what was produced]
**Agent(s):** [who acted]
**Outcome:** COMPLETE / HOLD / DEFERRED
**Output location:** [file path or "none"]

## Item 2: [...]

## FLAGs Raised

| Severity | Description | Resolution |
|---|---|---|
| [level] | [description] | [resolved/deferred/Logan decision] |

## Decisions Made

| # | Decision | Authority |
|---|---|---|
| 1 | [decision text] | Logan |

## Action Items

| Owner | Action | Deadline |
|---|---|---|
| [agent] | [action] | [date or "next CONFERENCE"] |

## DISMISSED

**Time:** [timestamp or "n/a"]
**Chair sign-off:** Logan
**Record committed by:** [agent name]
```

---

## IX. CLOSURE

Logan closes the CONFERENCE by posting:

```
CONFERENCE CLOSED
DATE: YYYY-MM-DD
RECORD: [file path of committed CONFERENCE RECORD]
DISMISSED: [list of agents returning to independent lanes]
```

Agents do not close their own participation. They wait for DISMISSED, then return to their TRIPLEX lanes.

---

## X. FAILURE MODES & MITIGATIONS

| Failure | Symptom | Mitigation |
|---|---|---|
| Quorum not reached | Agent cannot CONVENE | Chair decides: delay, substitute, or proceed with partial quorum; log absent agents in RECORD |
| Scope explosion | Agenda grows during session | Reject additions; log as proposed follow-up CONFERENCE; Chair enforces |
| Lane conflict mid-CONFERENCE | Two agents reach for the same file | Apply TRIPLEX collision rules; Chair arbitrates; log in RECORD under FLAGs |
| Recording agent fails | RECORD not committed | Any participant may draft the RECORD; Chair signs it before commit |
| CONFERENCE never formally closed | Agents uncertain of dismissal | Chair issues explicit DISMISSED signal; if Chair is AFK, CODE AUTHORITY pings via AFK PAGE |
| Phantom CONFERENCE | Work attributed to a "meeting" with no RECORD | No CONFERENCE existed without a committed RECORD; attribute work to the agents' independent lanes instead |

---

## XI. RELATIONSHIP TO EXISTING PROTOCOLS

| Protocol | Relationship |
|---|---|
| **XKCD** | All inter-agent messages during a CONFERENCE use XKCD classes (SIGNAL, REQUEST, SYNC, etc.) |
| **TRIPLEX** | Lane boundaries remain active inside a CONFERENCE; CONFERENCE CALL does not override TRIPLEX |
| **TRIUNE HANDSHAKE** | The TRIUNE HANDSHAKE is a specific three-agent pre-AFK CONFERENCE; it follows this protocol's structure informally |
| **PASSBACK SYNC** | A CONFERENCE may be triggered to BOOTSTRAP context from a dying agent; the TOSS/BOOTSTRAP operations run as agenda items |
| **LEVELSET** | CONVENE phase requires each agent to confirm their LEVELSET before participating |
| **DECISIONS.md** | All decisions made during a CONFERENCE are logged in the CONFERENCE RECORD; Logan promotes durable ones to DECISIONS.md |

---

## XII. OPEN QUESTIONS FOR LOGAN

1. **Record location:** Should CONFERENCE RECORDs live in `!/` (stable layer) or `!/!/` (workbench)? Stable feels right for decisions, workbench for operational sessions.

2. **Async CONFERENCE:** Can a CONFERENCE be asynchronous — e.g., Logan posts an agenda and agents respond over hours rather than synchronously? If yes, does the RECORD structure change?

3. **Automated trigger:** Should a scheduled workflow (e.g., the Monday vault audit) ever auto-emit a CONFERENCE CALL signal, or is that always a Logan-only action?

4. **Naming cadence:** Should CONFERENCE RECORDS be numbered (CONF-001, CONF-002) for reference in DECISIONS.md, or are dated slugs sufficient?

5. **Minimum quorum:** Is a CONFERENCE valid with only one agent and Logan (i.e., a bilateral session), or does "CONFERENCE CALL" imply two or more agents by definition?

---

*Proposed 2026-04-06 by GitHub Copilot (The Clerk). Awaiting Logan's review and adoption.*
*This document is a draft. It has no authority until Logan confirms adoption.*

---

###### [["The world is quiet here."]]
