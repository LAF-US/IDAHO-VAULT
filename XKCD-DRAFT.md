# XKCD Protocols — DRAFT

*Proposed 2026-03-17 by TASK: Claude Code session*
*Status: DRAFT — requires Logan's review and synthesis*
*Named for Randall Munroe's principle: if it can't fit on a napkin, it's too complex.*

---

## What This Is

Simple coordination primitives for the vault's agent swarm. These are not replacements for LEVELSET (which handles checkpointing) or the Constitution (which handles identity and authority). These are the small, mechanical rules that prevent agents from stepping on each other.

Think of it as traffic signals, not urban planning.

---

## Protocol 1: PING / PONG

**Already in use informally.** This codifies it.

**Purpose:** Check if an agent session is alive and has relevant context.

**Rules:**
- Any agent can PING any other agent — routed through Logan (manual bridge) or Slack (when bot apps exist)
- A PONG confirms: (1) alive, (2) current priority, (3) any blockers
- No response within one Logan-work-session = assume session is cold
- PONG must be ≤3 sentences. If you need more, that's a HANDOFF, not a PONG

**Format:**
```
PING → [agent name]
PONG ← [agent name]: [priority] | [blocker or "clear"] | [one-line status]
```

**Example:**
```
PING → STORY: JFAC
PONG ← STORY: JFAC: CCA deadline 3/18 | 5 quotes pending audio | quiet mode
```

---

## Protocol 2: CLAIM / RELEASE

**Purpose:** Prevent two agents from editing the same file simultaneously.

**Rules:**
- Before editing a governance file (`!ADMIN/`, `CLAUDE.md`, `.github/`), an agent states CLAIM [filepath]
- Other agents must not edit a claimed file until RELEASE [filepath] or until the claiming session closes
- Claims expire when the session ends — they do not persist across sessions
- Claims are announced via the coordination channel (Slack or Logan-as-bridge)
- Vault content files (bills, notes, sources) do NOT require claims — only governance and infrastructure files

**Scope:** Governance and infrastructure files only. The scraper owns bill files. Individual story sessions own their source files. No claims needed for those.

**Format:**
```
CLAIM: !ADMIN/Constitution.md — [agent name] — [reason]
RELEASE: !ADMIN/Constitution.md — [agent name]
```

---

## Protocol 3: COLLISION CHECK

**Purpose:** Before deploying new automation (scripts, workflows), verify no existing automation touches the same files.

**Rules:**
- Before adding a new `.py` script or `.yml` workflow, the deploying agent must:
  1. List all files/directories the new automation will read or write
  2. Check existing workflows for overlap (grep workflow YAML for those paths)
  3. Report conflicts to Logan before proceeding
- This is a pre-deployment gate, not a runtime check

**Format:**
```
COLLISION CHECK: wikilink_pass.py
  WRITES: GOVERNMENTS/**, SOURCES/**, TOPICS/**
  CONFLICTS WITH: idaho_leg_scraper.py (writes GOVERNMENTS/IDAHO - LEGISLATIVE/**)
  RESOLUTION: [proposed approach]
```

---

## Protocol 4: HANDOFF

**Already in use.** This trims it to essentials.

**Purpose:** Transfer context from one agent session to another.

**Rules:**
- A HANDOFF must contain exactly four sections:

```
HANDOFF: [source] → [destination]
DATE: YYYY-MM-DD

## STATE (what exists now)
[3-5 bullet points max]

## PENDING (what needs doing)
[Bulleted list, each item tagged with owner]

## BLOCKERS (what's stuck and why)
[Bulleted list, or "None"]

## FILES TOUCHED
[List of files modified in this session]
```

- If a HANDOFF exceeds one screen, it's too long. Split into a HANDOFF + a committed vault file with details.
- The consolidated handoff Logan shared on 2026-03-15 is the right ceiling for complexity — anything larger should be a LEVELSET instead.

---

## Protocol 5: DEAD MAN'S SWITCH

**Purpose:** Ensure no agent session goes stale without notice.

**Rules:**
- Every PERSISTENT or PERMANENT session must produce a PONG or LEVELSET at least once per Logan-work-session when active
- If a session has no output for >1 work session and has pending items, Logan (or ADMINISTRATION) marks it COLD
- COLD sessions get their pending items redistributed via HANDOFF
- A COLD session can be revived — it just needs to re-LEVELSET before resuming work

**States:**
```
HOT    — active, producing output
WARM   — idle but has context, can resume
COLD   — no output for >1 work session, pending items should be redistributed
CLOSED — session ended, all items handed off or completed
```

---

## What These Protocols Do NOT Cover

- **Authority and identity** → Constitution.md
- **Checkpointing and audit trail** → LEVELSET protocol
- **File structure and naming** → CLAUDE.md
- **Ethics and sourcing** → Ethics.md
- **Decisions** → DECISIONS.md

These protocols are strictly mechanical coordination. They have no opinions about what agents should do — only how they avoid tripping over each other while doing it.

---

## Implementation

If Logan approves:
1. This file moves to `!ADMIN/XKCD.md` (after the Monday rename)
2. Reference added to Constitution.md under a "Coordination Protocols" section
3. Each agent's next LEVELSET should acknowledge XKCD protocols
4. No code changes required — these are social/procedural protocols

---

*All content is a draft until Logan verifies.*
*Generated by TASK: Claude Code session — 2026-03-17 — On the record.*
