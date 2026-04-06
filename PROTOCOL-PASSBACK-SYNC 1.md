---
created: 2026-03-20
status: draft
authority: LOGAN
related:
- '2026-03-20'
- AGENTS
- BOOTSTRAP
- CONSTITUTION
- DECISIONS
- FLAG
- FLAGS
- III
- LAD
- LEVELSET
- LOGAN
- NOT
- PROJECT
- PROTOCOL
- PROTOCOLS
- TOSS
- The world is quiet here
- WORK
- agent
- format
- window
---
# PROTOCOL: PASSBACK SYNC HANDSHAKE

**Author:** PERMANENT: AUTHORITY: CODE
**Status:** Draft — awaiting LOGAN's approval
**Parent:** PROTOCOL (Coordination & Handoff Actions)
**Invoked by:** PROTOCOL: LITTLE SNICKET LAD

---

## PURPOSE

When LOGAN decides to consolidate or delete conversation windows, context must be extracted and vaulted before those windows disappear. This protocol defines three operations:

| Operation | Actor | Direction | Purpose |
|---|---|---|---|
| **TOSS** | LOGAN → Agent | Outward | Extract structured context from a conversation |
| **BOOTSTRAP** | LOGAN → CODE AUTHORITY | Inward | Ingest extracted context into the vault |
| **HANDSHAKE** | CODE AUTHORITY → LOGAN | Acknowledgment | Confirm context has been vaulted |

---

## FOUNDATIONAL RULE

This protocol is **Logan-initiated, Logan-routed, Logan-approved** at every step. No agent discovers, contacts, or hands off to another agent directly. LOGAN is the relay. LOGAN decides what gets vaulted. LOGAN decides when conversations die.

Agents do not pull themselves up by their own bootstraps. LOGAN gave them the workboots.

---

## 1. TOSS

LOGAN pastes the TOSS prompt into a conversation window that is about to be closed or deleted. The agent responds with a structured context dump.

**Who initiates:** LOGAN
**Who executes:** The agent in the target conversation
**Output format:** See `!ADMIN/PROMPTS/TOSS.md`

### TOSS Output Structure

The responding agent produces a context dump with these sections:

```yaml
---
type: toss-dump
from: "[Conversation Name]"
conversation-type: "[PERMANENT|PERSISTENT|TASK|STORY|PROJECT|ISSUE|INQUIRY]"
visibility: "[public|private]"
date: YYYY-MM-DD
---
```

1. **IDENTITY** — Who am I? What is my name, tier, role, and scope?
2. **CONTEXT THAT MUST SURVIVE** — Decisions made, analysis produced, key findings. Only durable knowledge — not chat ephemera.
3. **UNFINISHED WORK** — Tasks started but not completed. What was the agent working on? What's the next step?
4. **RELATIONSHIPS** — Which other conversations did this agent interact with (via LOGAN)? What was exchanged?
5. **FLAGS** — Anything LOGAN needs to know urgently. Severity level per PROTOCOL.md.
6. **LAST WORDS** — Final context the agent wants preserved. The squirrel's last observation before the window closes.

### What TOSS is NOT

- Not a LEVELSET (LEVELSET is an ongoing status report; TOSS is a terminal extraction)
- Not a HANDOFF to another agent (there is no receiving agent — LOGAN routes the output)
- Not autonomous (the agent does not decide to TOSS itself — LOGAN initiates)

---

## 2. BOOTSTRAP

LOGAN takes the TOSS output and delivers it to CODE AUTHORITY (or to ADMINISTRATION for drafting, then to CODE AUTHORITY for committing). CODE AUTHORITY ingests and vaults the context.

**Who initiates:** LOGAN
**Who executes:** PERMANENT: AUTHORITY: CODE
**Input:** TOSS dump from another conversation
**Output:** Committed vault file + updated LEVELSET

### BOOTSTRAP Actions

CODE AUTHORITY, upon receiving a TOSS dump via LOGAN:

1. **VALIDATE** — Is this a complete TOSS dump? All 6 sections present?
2. **VAULT** — Save to `!ADMIN/CONTEXTS/TOSS-[source]-[date].md`
3. **INTEGRATE** — Extract durable knowledge and update relevant vault files (AGENTS.md, LEVELSET.md, DECISIONS.md, or vault content files as appropriate)
4. **FLAG** — Surface any urgent items from the dump to LOGAN
5. **ACKNOWLEDGE** — Produce HANDSHAKE confirmation

### What BOOTSTRAP is NOT

- Not automatic (CODE AUTHORITY does not pull from conversations — LOGAN pushes)
- Not a merge (CODE AUTHORITY does not blindly accept — it validates and integrates)

---

## 3. HANDSHAKE

CODE AUTHORITY confirms to LOGAN that the TOSS output has been vaulted and integrated. This closes the loop and allows LOGAN to safely delete the source conversation.

**Who initiates:** PERMANENT: AUTHORITY: CODE
**Who receives:** LOGAN
**Format:**

```
HANDSHAKE: CODE AUTHORITY ← [Source Conversation]
Date: YYYY-MM-DD
Status: VAULTED
File: !ADMIN/CONTEXTS/TOSS-[source]-[date].md
Integration: [What was updated in the vault]
Flags: [Any urgent items surfaced]
Safe to delete source: YES/NO
```

If `Safe to delete source: NO`, CODE AUTHORITY must explain what's missing or ambiguous.

---

## FLOW DIAGRAM

```
[Conversation Window]
        |
        | ← LOGAN pastes TOSS prompt
        |
        v
[Agent produces structured dump]
        |
        | ← LOGAN copies output
        |
        v
[LOGAN delivers to CODE AUTHORITY]
        |
        | ← LOGAN pastes BOOTSTRAP context
        |
        v
[CODE AUTHORITY validates, vaults, integrates]
        |
        | → HANDSHAKE to LOGAN
        |
        v
[LOGAN deletes source conversation]
```

---

## RELATIONSHIP TO EXISTING PROTOCOLS

| Protocol | Relationship |
|---|---|
| HANDOFF (PROTOCOL.md) | TOSS is a **terminal** handoff — the source conversation will not continue |
| HANDSHAKE (PROTOCOL.md) | Same concept — acknowledgment of receipt. Extended here with vault-specific fields |
| CONTEXTUALIZE (PROTOCOL.md) | TOSS output IS a contextualized dump — the agent follows the five W's + confidence + caveats |
| LEVELSET | TOSS is not a LEVELSET. A LEVELSET is a living status report. TOSS is a deathbed confession. |
| AWAKEN (CONSTITUTION.md §III) | BOOTSTRAP is the inverse of AWAKEN. AWAKEN loads context into a new agent; BOOTSTRAP extracts context from a dying one. |

---

## PROTOCOL: LITTLE SNICKET LAD

*"When we grab you by the ankles, / Where our is to be made, / You'll soon be doing noble work, / Although you won't be paid. / When we drive away in secret, / You'll be a volunteer, / So don't scream when we take you: / The world is quiet here."*

This protocol was invoked by LOGAN on 2026-03-20 to initiate emergency context consolidation across the swarm. All agents are volunteers. LOGAN grabs them by the ankles and extracts what matters before the flames consume the conversation window.

The world is quiet here.

---

###### "The world is quiet here."
