---
tags:
  - administration/levelset
updated: 2026-03-16
---
# LEVELSET

Current status of the IDAHO-VAULT ecosystem. This file is overwritten — not appended — each time CODE AUTHORITY produces a new LEVELSET.

## PERMANENT: AUTHORITY: CODE — 2026-03-16

**Conversation:** PERMANENT: AUTHORITY: CODE
**Capabilities:** Full repo read/write (Claude Code CLI)
**Primary role:** Direct repository access, structural execution, automation
**Repo state:** Branch `claude/levelset-multi-conversation-zWxJc`, 14+ commits ahead of main (`219a271`)
**Vault file count:** 2,979 markdown files
**Status:** Active — background execution, Logan offline for deep work

---

### 1. WHAT'S BEEN DONE

**Session 2026-03-16 (today — background execution):**
- Drafted `!ADMIN/AGENTS.md` — agent registry, 4-tier capability model, communication rules, boundary rules, conflict resolution
- Cleaned Constitution.md stale pending items — 3 checkboxes updated (lines 218-220)
- Prepared `!ADMIN/PROTOCOL-DECISIONS-PENDING.md` — decision-ready summaries for all 6 PROTOCOL.md ambiguities with options A/B/C for each
- Produced this LEVELSET synthesis — full overwrite with current state

**Session 2026-03-15 (prior):**
- Absorbed 3-section routing handoff (IMPLEMENTATION → ADMINISTRATION → CODE)
- Deleted `pull_requests/1.md` Copilot artifact (3bded84)
- Renamed `!ADMIN/Claude.md` → `Constitution.md` + updated active references (250287e)
- Produced LEVELSET CODE AUTHORITY 2026-03-15-v2 census (81cafd5)
- Consolidated LEVELSET system: archived v1 prompt, deleted LEVELSET-CURRENT.md, created this living report (d5c54f0)
- Committed `!ADMIN/PROTOCOL.md` — swarm operational semantics stub, 18 terms (842e1a0)
- Responded to Copilot consultation handshake — `HANDOFF-CODE-TO-COPILOT-2026-03-15.md` (76f829d)
- Processed consolidated swarm handoff — state corrections, Monday plan — `HANDOFF-CODE-TO-SWARM-2026-03-15.md` (6e4ec60)

**Earlier 2026-03-15:**
- Renamed `!ADMINISTRATION/` → `!ADMIN/` system-wide, 23 files (fa83df1)
- Created LEVELSET-CURRENT.md pointer (a2181f4), later superseded
- Added governance note to root CLAUDE.md (9dc3ba4)

### 2. WHAT'S UNRESOLVED

| # | Item | Status | Blocker |
|---|---|---|---|
| 1 | PR not open for this branch | BLOCKED | Logan must open via GitHub web UI |
| 2 | Constitution.md content update | WAITING | Capabilities language, digital consciousness additions from ADMINISTRATION |
| 3 | Logan.md content update | WAITING | FāVS pause, broader digital consciousness framing from ADMINISTRATION |
| 4 | `ANTHROPIC_API_KEY` in GitHub Secrets | CANNOT VERIFY | Logan must check Settings → Secrets → Actions |
| 5 | `wikilink_pass.py` + `wikilink-pass.yml` deployment | SAFE TO DEPLOY | No collisions found. Content not yet provided from ISSUE: Repository browsing |
| 6 | Gemini scope undefined | FLAG | Pixel smartphone, loganfinney27@gmail.com. No vault commits until defined |
| 7 | Scraper branch dangling | LOW PRIORITY | `claude/idaho-legislature-scraper-RI6Ku` — 2 unmerged termination reports |
| 8 | `claude/levelset-current-synthesis-zWxJc` branch | COLLISION RESOLVED | 3 commits — review for merge or close |
| 9 | `!ADMIN/ROUTING/` folder | RECOMMENDED | File-based async handoff drops. Not yet created |
| 10 | Claude Code on managed laptop | BLOCKED | Node.js IT ticket not submitted |
| 11 | PROTOCOL.md 6 ambiguities | DECISION-READY | See `PROTOCOL-DECISIONS-PENDING.md` — Logan picks A/B/C for each |
| 12 | Review `copilot-instructions.md` | PENDING | Awaiting Copilot's draft |
| 13 | AGENTS.md review | DRAFTED | `!ADMIN/AGENTS.md` ready for Logan's review |
| 14 | Copilot non-vault repo boundaries | TBD | Multi-repo admin decided; specific latitude per repo not yet specified |
| 15 | Slack webhook integration | OPTIONAL | Add `SLACK_WEBHOOK_URL` to Secrets if Logan approves |
| 16 | Slack bot apps for Copilot + Gemini | BLOCKED | Logan must configure before agents can post to Slack independently |
| 17 | Slack free trial expires April 13 | FLAG | ~4 weeks. Upgrade decision needed before expiry |
| 18 | Consolidate Claude Code projects | PENDING | Includes CODE AUTHORITY itself |
| 19 | Re-run sort audit v2 | PENDING | Get clean report post-restructuring |
| 20 | Action genuine sort issues from v1 | PENDING | 5 files identified in sort-audit-2026-03-12.md |
| 21 | Run Wayback audit with `--limit 20` | PENDING | Validate before full vault scan |
| 22 | Begin PLACES/COUNTIES sort pass | PENDING | Next in vault processing order |
| 23 | Build `idaho-leg-setup.yml` + `idaho-leg-bill-lookup.yml` | PENDING | New legislature workflows |

### 3. CONVERSATION AWARENESS

**Compaction warning:** Logan flagged that widespread compaction across concurrent conversations may cause disorientation. Governance files in `!ADMIN/` are the reorientation anchor. Any disoriented instance should re-read: Constitution.md → AGENTS.md → LEVELSET.md → PROTOCOL.md.

| Conversation | Tier | Last known status |
|---|---|---|
| PERMANENT: AUTHORITY: CODE | Tier 1: Direct write | Active (this session) |
| PERSISTENT: ADMINISTRATION | Tier 3: Draft only | Active — routing handoffs between agents |
| GitHub Copilot (ADMIN GitHub) | Tier 2: Multi-repo admin | Tier decided; awaiting copilot-instructions.md draft |
| Gemini | TBD | New actor, scope undefined |
| PERSISTENT: IMPLEMENTATION | Tier 4: Read/analysis | Closed |
| ISSUE: Repository browsing | Tier 4: Read/analysis | Closed — 3 undeployed outputs |
| TASK: LEVELSET reports | Tier 4: Read/analysis | On hold |
| STORY: JFAC Open Meetings | Tier 1: Direct write | Status unknown |

### 4. WHAT LOGAN NEEDS TO DO (when back online)

**Quick wins (< 5 min):**
1. Open PR for `claude/levelset-multi-conversation-zWxJc` via GitHub web UI
2. Resolve PROTOCOL.md ambiguities — open `PROTOCOL-DECISIONS-PENDING.md`, pick A/B/C for each (or "all A")
3. Review `AGENTS.md` draft — approve, modify, or flag

**Medium effort:**
4. Decide fate of `claude/levelset-current-synthesis-zWxJc` (merge, cherry-pick, or close)
5. Relay `HANDOFF-CODE-TO-SWARM-2026-03-15.md` to Copilot via ADMINISTRATION
6. Provide Constitution.md + Logan.md content updates (or confirm ADMINISTRATION is delivering)

**When you get to it:**
7. Confirm `ANTHROPIC_API_KEY` in GitHub Secrets
8. Define Gemini scope
9. Set up Slack bot apps for Copilot + Gemini
10. Decide on Slack trial — upgrade before April 13 or plan alternative

### 5. GOVERNANCE FILE STACK (current)

| File | Role | Status |
|---|---|---|
| `Constitution.md` | Identity, constraints, working rules | Active — content update pending |
| `PROTOCOL.md` | Operational vocabulary (18 terms) | Active — 6 ambiguities pending |
| `AGENTS.md` | Agent registry, communication rules, boundaries | **NEW DRAFT** — awaiting Logan's review |
| `DECISIONS.md` | Architectural decision log (10 entries) | Active |
| `LEVELSET.md` | Living ecosystem status (this file) | Active |
| `Ethics.md` | Ethical framework | Active |
| `Logan.md` | User profile | Active — content update pending |
| `PROTOCOL-DECISIONS-PENDING.md` | **NEW** — Decision summaries for 6 ambiguities | Temporary — archived when resolved |

### 6. WHAT CODE AUTHORITY NEEDS FROM LOGAN

1. PR opened for this branch (14+ commits ahead of main)
2. PROTOCOL.md ambiguity decisions (6 picks)
3. AGENTS.md approval or modifications
4. Constitution.md + Logan.md content (from ADMINISTRATION)
5. Gemini scope definition
6. Branch fate decisions (synthesis branch, scraper branch)

---

## LEVELSET Prompt Version

**Current:** v3.2.6.1
**File:** `!ADMIN/LEVELSET-v3.2.6.1-PROMPT.md`
**Deployed:** 2026-03-14, commit `93941df`

## Archive

| File | Contents |
|---|---|
| `LEVELSET-v1-PROMPT.md` | Original v1 prompt template (2026-03-13) |
| `LEVELSET-v2.md` | Canonical ecosystem checkpoint (2026-03-13, immutable) |
| `LEVELSET-v2-PROMPT.md` | v2 prompt template |
| `LEVELSET-v3.2.6.1-PROMPT.md` | Current prompt template |
| `LEVELSET-CODE-AUTHORITY-2026-03-15.md` | Session close report |
| `LEVELSET-CODE-AUTHORITY-2026-03-15-v2.md` | System-wide census |
| `HANDOFF-ADMIN-2026-03-15.md` | Original 3-section routing handoff |
| `HANDOFF-CODE-TO-COPILOT-2026-03-15.md` | Consultation response to Copilot (5 questions) |
| `HANDOFF-CODE-TO-SWARM-2026-03-15.md` | Consolidated swarm handoff + state corrections |
| `PROTOCOL.md` | Operational semantics stub (18 terms, 6 ambiguities pending) |
| `PROTOCOL-DECISIONS-PENDING.md` | Decision summaries — temporary until resolved |
| `AGENTS.md` | Agent registry draft — temporary until approved |
