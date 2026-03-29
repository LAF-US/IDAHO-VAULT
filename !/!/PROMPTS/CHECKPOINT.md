---
tags:
  - administration/prompts
  - protocol/checkpoint
created: 2026-03-29
updated: 2026-03-29
status: active
usage: Logan fills this in and pastes it to both Linear (as an issue comment) and the active GitHub coding agent to record mid-session state and re-orient execution
---
# CHECKPOINT — LOGAN'S MID-SESSION STATUS

**Usage:** Fill in the template below and paste it to:
1. **Linear** — as a comment on the active issue, to record progress on the planning surface
2. **GitHub** — to the active coding agent (Copilot, Claude Code, Codex), to re-orient execution

Both surfaces receive the same payload. Fill it in honestly. If a field is not applicable, write "N/A". If you don't know, write "UNKNOWN — needs Logan."

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

NEEDS FROM LOGAN
- [decision, input, approval, or clarification needed] OR: None

---

ALIGNMENT CHECK

GitHub → Linear: Does current repo work map cleanly to the active Linear issue?
  [ YES / NO / PARTIAL — explain if not YES ]

Linear → intent: Does the Linear issue still reflect Logan's actual intent?
  [ YES / NO / DRIFT — explain if not YES ]

Risk level: [ LOW / MEDIUM / HIGH ]

---

If you are a GitHub coding agent receiving this: acknowledge the checkpoint, confirm your current understanding of scope, and flag anything in this payload that conflicts with what you know about the repo or the branch. Do not silently absorb scope changes — surface them.

If you are Linear receiving this: this comment is a durable mid-session record. No action required from Linear.

---

## ✂️ — STOP COPYING HERE — ✂️
