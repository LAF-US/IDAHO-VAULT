---
authority: LOGAN
related:
- '2026-03-15'
- ALL
- BODY
- DECISIONS
- GitHub
- Idaho
- LEVELSET
- LOGAN
- Logan's
- PAC
- PROJECT
- budget
- campaign finance
- infrastructure
- links
---

# SIGNAL Protocol — IDAHO-VAULT

**Version:** 1.0
**Date:** 2026-03-15
**Status:** DRAFT — salvaged from branch `claude/bidirectional-conversation-signals-eDiy0`

---

## Purpose

LEVELSET is pull-based — Logan prompts, conversations report. SIGNAL is push-based — conversations emit structured flags when something needs attention *between* LEVELSET cycles.

LEVELSET answers "where are we?" SIGNAL answers "something just happened."

---

## Signal Types

### ESCALATE

Something needs a higher-tier conversation's attention. A TASK found something that matters at PROJECT level. An INQUIRY surfaced a lead that belongs in a STORY.

**When to emit:** You've discovered information or reached a conclusion that exceeds your conversation's scope or tier.

### BLOCK

This conversation is stuck. It needs Logan or another conversation to unblock it before it can proceed.

**When to emit:** You cannot make progress without input, a decision, or an action from outside this conversation.

### COLLISION

This conversation detects it is about to modify something another conversation is also working on, or has already modified.

**When to emit:** You see evidence of concurrent work on the same files, the same topic area, or the same infrastructure component.

### DISCOVERY

This conversation found something significant that other conversations should know about — a fact, a connection, a pattern, a source lead.

**When to emit:** You've found something that would change how other conversations operate or what they know, but that doesn't require immediate action.

---

## Signal Format

Every signal follows this structure:

```
SIGNAL: [TYPE]
FROM: [conversation name] — [tier]
TO: [target conversation, tier, or "ALL" / "LOGAN"]
DATE: [YYYY-MM-DD HH:MM MT]
PRIORITY: [URGENT / NORMAL]

SUBJECT: [one line]

BODY:
[What happened. What it means. What needs to happen next. Keep it short.]

EVIDENCE:
[File paths, links, quotes, or specific references. Optional but preferred.]
```

### Rules

1. **Any conversation, any tier, can emit a signal.** Read-only conversations can signal just as direct-write can. Signals are information, not actions.
2. **Signals are not actions.** Emitting a signal does not authorize the sender to act on it. The signal is a flag for routing. Logan or the target conversation decides what to do.
3. **URGENT priority** means Logan should see this before the next LEVELSET cycle. Use sparingly. Most signals are NORMAL.
4. **TO field routing:**
   - `LOGAN` — requires Logan's attention directly
   - `ALL` — all active conversations should be aware
   - A specific conversation name — routed to that conversation
   - A tier — routed to all conversations at that tier
5. **Signals are ephemeral by default.** They live in the conversation where they're emitted. They become permanent only if Logan or a direct-write instance commits them.
6. **COLLISION signals are always URGENT.** If you detect a collision, flag it immediately.
7. **Do not signal what LEVELSET already covers.** Routine status belongs in LEVELSET reports. Signals are for things that can't wait.

---

## Routing

**Current state (interim):** Logan is the manual router. When a conversation emits a signal, Logan carries it to the target conversation.

**End state:** Automation. Direct-write instances commit signals to a signals directory. GitHub Actions or a synthesis script routes them. Signals are logged, acted on, and archived.

**Interim workflow:**
1. Conversation emits a signal in its output to Logan
2. Logan reads, decides whether to route
3. Logan carries the signal to the target conversation (or acts on it directly)
4. Target conversation acknowledges receipt

---

## Integration with LEVELSET

LEVELSET Section 2 (WHAT'S UNRESOLVED) and Section 5 (WHAT LOGAN NEEDS TO KNOW) overlap with SIGNAL. The distinction:

- **LEVELSET** = scheduled checkpoint, comprehensive, pull-based
- **SIGNAL** = event-driven, narrow, push-based

A signal emitted between LEVELSET cycles should be referenced in the next LEVELSET report under Section 2 or 5, with its disposition (acted on, pending, dismissed).

---

## Examples

### ESCALATE — TASK finds something bigger

```
SIGNAL: ESCALATE
FROM: TASK: LEVELSET reports
TO: PERSISTENT: ADMINISTRATION
DATE: 2026-03-15 14:30 MT
PRIORITY: NORMAL

SUBJECT: Constitution.md contains outdated tier definitions

BODY:
While synthesizing LEVELSET reports, found that Constitution.md still lists
CODE AUTHORITY as PERSISTENT. It was promoted to PERMANENT on 2026-03-14.
ADMINISTRATION should update the constitution.

EVIDENCE:
Constitution.md: "PERSISTENT: CODE AUTHORITY"
DECISIONS.md: 2026-03-14 entry confirms promotion
```

### COLLISION — concurrent file edits

```
SIGNAL: COLLISION
FROM: STORY: JFAC Open Meetings
TO: PERMANENT: CODE AUTHORITY
DATE: 2026-03-15 09:00 MT
PRIORITY: URGENT

SUBJECT: Both editing GOVERNMENTS/IDAHO - LEGISLATIVE/SESSIONS/

BODY:
I'm about to commit 12 hearing notes to SESSIONS/2026/. CODE AUTHORITY
appears to be restructuring SESSIONS/ in the levelset-multi-conversation
branch. Holding my commit until collision is resolved.

EVIDENCE:
My staged files: SESSIONS/2026/2026-03-10 - JFAC.md through 2026-03-14
CODE AUTHORITY branch: claude/levelset-multi-conversation-zWxJc
```

### BLOCK — waiting on external input

```
SIGNAL: BLOCK
FROM: PROJECT: 2026 Budget Tracker
TO: LOGAN
DATE: 2026-03-15 11:00 MT
PRIORITY: NORMAL

SUBJECT: Need JFAC budget spreadsheet to proceed

BODY:
Cannot build budget comparison tables without the JFAC appropriations
spreadsheet for FY2027. Is this available as a public document?

EVIDENCE:
None — requesting source material.
```

### DISCOVERY — found a connection

```
SIGNAL: DISCOVERY
FROM: INQUIRY: campaign finance
TO: STORY: JFAC Open Meetings
DATE: 2026-03-15 16:00 MT
PRIORITY: NORMAL

SUBJECT: JFAC member campaign contributions from hospital lobby

BODY:
While researching campaign finance filings, found that three JFAC members
received contributions from the Idaho Hospital Association PAC in the
2024 cycle. May be relevant to the open meetings investigation.

EVIDENCE:
Sunshine reports: [specific filing references]
JFAC members: [names]
```
