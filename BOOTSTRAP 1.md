---
created: 2026-03-20
status: draft
usage: Logan pastes this into CODE AUTHORITY along with a TOSS dump to trigger context
  ingestion
date created: Wednesday, April 1st 2026, 11:16:46 pm
date modified: Thursday, April 2nd 2026, 10:37:00 pm
related:
- '2026-03-20'
- AGENTS
- BOOTSTRAP
- DECISIONS
- FLAG
- LEVELSET
- PROTOCOL
- TOSS
- agent
authority: LOGAN
---
# BOOTSTRAP PROMPT

**Usage:** After running TOSS on a conversation and copying the output, paste the BOOTSTRAP prompt below into CODE AUTHORITY (Claude Code), followed by the TOSS dump. CODE AUTHORITY will validate, vault, and integrate the context.

---

## ✂️ — COPY BELOW THIS LINE — ✂️

---

**PROTOCOL: BOOTSTRAP — Context ingestion from TOSS dump.**

Logan is speaking. I'm delivering a TOSS dump from a conversation that is being closed. Your job:

1. **VALIDATE** — Confirm all 6 sections are present (Identity, Context That Must Survive, Unfinished Work, Relationships, Flags, Last Words). If any section is missing, FLAG it and proceed with what's available.

2. **VAULT** — Save the dump to `!ADMIN/CONTEXTS/TOSS-[source-name]-[date].md` where `[source-name]` is the conversation name with spaces replaced by hyphens, lowercased. Example: `TOSS-persistent-administration-2026-03-20.md`

3. **INTEGRATE** — Review the dump and update vault files as needed:
   - If the dump contains **decisions**: add to `!ADMIN/!/DECISIONS.md` as pending
   - If the dump contains **agent status changes**: update `!ADMIN/!/AGENTS.md`
   - If the dump contains **unfinished work**: note in `!ADMIN/!/LEVELSET.md` unresolved items
   - If the dump contains **vault content** (facts, research, analysis): route to appropriate vault location
   - Use judgment — not everything needs integration. Chat ephemera stays in the TOSS file and nowhere else.

4. **FLAG** — Surface any CRITICAL or HIGH items from the dump immediately. Don't bury them.

5. **HANDSHAKE** — After vaulting and integration, produce a HANDSHAKE confirmation:

```
HANDSHAKE: CODE AUTHORITY ← [Source Conversation Name]
Date: [today]
Status: VAULTED
File: !ADMIN/CONTEXTS/TOSS-[source]-[date].md
Integration: [What was updated in the vault, or "None — context-only vault"]
Flags: [Any urgent items, or "None"]
Safe to delete source: YES/NO
```

**The TOSS dump follows below this line.**

---

## ✂️ — STOP COPYING HERE — PASTE TOSS DUMP AFTER THIS — ✂️
