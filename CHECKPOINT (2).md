---
created: 2026-03-29
updated: 2026-03-29
status: active
usage: Logan fills this in and pastes it to both Linear (as an issue comment) and
  the active GitHub coding agent to record mid-session state and re-orient execution
date created: Sunday, March 29th 2026, 6:08:00 pm
date modified: Wednesday, April 1st 2026, 10:59:40 pm
related:
- '2026-03-29'
- ALL
- Copilot
- GitHub
- LAF
- LOGAN
- LOW
- Logan's
- MID
- agent
- template
- verbal
authority: LOGAN
---
# CHECKPOINT — LOGAN'S MID-SESSION STATUS

**Usage:** Fill in the template below. Paste the same payload to both destinations:

| Destination | Purpose | Expected response |
|---|---|---|
| **Linear** — comment on the active issue | Durable planning record | No action required from Linear |
| **GitHub coding agent** (Copilot, Claude Code, Codex) | Re-orient execution mid-session | See required response contract below |

Fill it in honestly. If a field is not applicable, write "N/A". If you don't know, write "UNKNOWN — needs Logan."

---

## ✂️ — COPY BELOW THIS LINE — ✂️

---

CHECKPOINT — LOGAN'S MID-SESSION STATUS

Date/Time: [YYYY-MM-DD HH:MM]
Linear Issue: [LAF-XX — issue title]
GitHub Branch / PR: [branch name or PR #, or "none yet"]
Reporting agent / session: [e.g., GitHub Copilot / Claude Code / Codex]

---

DONE THIS SESSION
- [item]
- [item]

IN PROGRESS
- [item — describe current state]

BLOCKED ON
- [what is blocking, and what is needed to unblock] OR: None

SCOPE CHANGES
- [describe any drift from the original issue scope] OR: None

NEXT STEPS
- [item]
- [item]

DECISION NEEDED
- [open approvals or choices Logan must make before work can continue] OR: None

NEEDS FROM LOGAN (other)
- [input, context, or clarification needed that is not a binary decision] OR: None

RESUME POINT
If Logan comes back cold, restart here: [one sentence — what to do next and where to look]

---

ALIGNMENT CHECK

GitHub → Linear: Does current repo work map cleanly to the active Linear issue?
  [ YES / NO / PARTIAL — explain if not YES ]

Linear → intent: Does the Linear issue still reflect Logan's actual intent?
  [ YES / NO / DRIFT — explain if not YES ]

If GitHub and Linear disagree, the authoritative source of truth is:
  [ LINEAR issue as written / LOGAN'S last verbal instruction / THIS CHECKPOINT ]

Risk level: [ LOW / MEDIUM / HIGH ]

---

GITHUB AGENT RESPONSE CONTRACT

If you are a GitHub coding agent receiving this checkpoint, respond with ALL of the following before continuing work:

1. ACKNOWLEDGED — confirm you received this checkpoint
2. MAPPED TO — restate the Linear issue, branch, and PR you are working on
3. ALIGNMENT — confirm (ALIGNED) or reject (MISALIGNED) the alignment check above; explain if misaligned
4. CONFLICTS — name any conflicts between this payload and what you know about the repo or branch; do not silently absorb scope changes

If you are Linear receiving this: this comment is a durable mid-session record. No action required.

---

## ✂️ — STOP COPYING HERE — ✂️
