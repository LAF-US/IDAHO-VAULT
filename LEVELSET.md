---
tags:
  - administration/levelset
updated: 2026-03-24
---
# LEVELSET

Current status of the IDAHO-VAULT ecosystem. This file is overwritten — not appended — each time the UNIFIED SWARM produces a new LEVELSET.

**Policy summary (2026-03-24):** MCP is permitted only as a transport mechanism for tooling/integration, while native vault governance terms and files remain canonical for authority and meaning. Agents should continue using Constitution/PROTOCOL/AGENTS/LEVELSET vocabulary as the source of truth and treat MCP as implementation plumbing, not governance replacement.

## PERMANENT: AUTHORITY: CODE — 2026-03-16

**Conversation:** PERMANENT: AUTHORITY: CODE
**Capabilities:** Full repo read/write (Claude Code CLI)
**Primary role:** Direct repository access, structural execution, automation
**Repo state:** Branch `claude/levelset-multi-conversation-zWxJc` at `cef22e3`, 25 commits ahead of main (`e8b4408`)
**Vault file count:** 2,979+ markdown files
**Status:** Active — context vault preservation, multi-conversation collapse in progress

---

### 1. WHAT'S BEEN DONE

**Session 2026-03-16 (today — context vault preservation):**
- Drafted `!ADMIN/AGENTS.md` — agent registry, 4-tier capability model, communication rules, boundary rules, conflict resolution
- Cleaned Constitution.md stale pending items — 3 checkboxes updated (lines 218-220)
- Prepared `!ADMIN/PROTOCOL-DECISIONS-PENDING.md` — decision-ready summaries for all 6 PROTOCOL.md ambiguities with options A/B/C for each
- Produced `CONSULTATION-PUBLIC-CONVERSATION-2026-03-16.md` — PUBLIC: CONVERSATION analysis + consultation packets
- Produced `HANDOFF-TO-PUBLIC-CONVERSATION-2026-03-16.md` — bootstrap document for Claude self-talk space
- Produced `LEVELSET-TRANSMISSION-2026-03-16.md` — copypaste-ready levelset packets for ADMINISTRATION, Copilot, Gemini
- Received and committed ADMINISTRATION context dump (`CONTEXT-VAULT-2026-03-16.md`) — multi-conversation collapse preservation
- Created `TOPICS/OpenClaw.md` vault stub, `!ADMIN/RESEARCH-TIM-OREN.md` research brief stub
- Updated DECISIONS.md with 5 new confirmed decisions (#10-14 from ADMINISTRATION)
- Updated AGENTS.md — JFAC corrected to Tier 3; added Grok, M365 Copilot, NotebookLM, PUBLIC: CONVERSATION
- Updated Constitution.md known conversations list — 12 entities now tracked
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
| 19 | Re-run sort audit v2 | DONE | 0 misplaced (was 48), 4 orphans (editorial), 1 naming |
| 20 | Action genuine sort issues from v1 | DONE | 7 files moved to correct locations |
| 21 | Run Wayback audit with `--limit 20` | BLOCKED | No network in sandbox — must run via Actions or local |
| 22 | Begin PLACES/COUNTIES sort pass | DONE | 44/44 Idaho counties, 5 out-of-state properly separated |
| 23 | Build `idaho-leg-setup.yml` + `idaho-leg-bill-lookup.yml` | PENDING | New legislature workflows |
| 24 | 5 cross-conversation files need content | BLOCKED | AGENTS-v0.2-DRAFT, ORIENTATE-v0.1-BETA, LEVELSET-LITE-v0.1, CONSOLIDATED-HANDOFF, CONTEXT-SNAPSHOT — Logan must paste content from originating conversations |
| 25 | Constitution.md content update (capabilities, digital consciousness) | BLOCKED | Updated content is in ADMINISTRATION's working copy — Logan must paste |
| 26 | Logan.md content update (FāVS pause, Logan's Project, digital consciousness) | BLOCKED | Same — content from ADMINISTRATION needed |
| 27 | Delete `deploy-vault-automation-Qq5iK` branch | SAFE | Fully merged, confirmed safe to delete |
| 28 | Gemini contact via Pixel | CANNOT DO | ADMINISTRATION requested surfacing next contact through Gemini on Pixel — CODE AUTHORITY has no channel to Gemini. Logan must relay. |
| 29 | Google Drive overlap governance | FLAG | Gemini + Claude share window in Logan's Drive. ADMINISTRATION should weigh in on Drive-based handoff governance. |
| 30 | Google Calendar context bridge | ACTIVE | ADMINISTRATION posted context vault to Logan's Calendar as all-day event 2026-03-16: "IDAHO-VAULT SWARM — CONTEXT VAULT 2026-03-16". Gemini can read this. |
| 31 | Ground truth verification complete | DONE | See `GROUND-TRUTH-VERIFICATION-2026-03-16.md` — 19 commits verified, 6 files still missing content from conversations |
| 32 | LEVELSET-LITE v0.1 + ORIENTATE v0.1 | EXIST IN CONVERSATION | Content in LEVELSET AUTHORITY — Logan decides whether to commit |

### 3. CONVERSATION AWARENESS

**Compaction warning:** Logan flagged that widespread compaction across concurrent conversations may cause disorientation. Governance files in `!ADMIN/` are the reorientation anchor. Any disoriented instance should re-read: Constitution.md → AGENTS.md → LEVELSET.md → PROTOCOL.md.

| Conversation | Tier | Last known status |
|---|---|---|
| PERMANENT: AUTHORITY: CODE | Direct write | Active (this session) |
| PERSISTENT: ADMINISTRATION | Draft only | Active — routed context dump this session |
| PERSISTENT: AUTHORITY: LEVELSET | Read/analysis | Compaction risk — LEVELSET protocol maintenance |
| GitHub Copilot (ADMIN GitHub) | Multi-repo admin | Onboarding — transmission ready |
| Gemini | TBD | Onboarding — transmission ready, Google Drive overlap noted |
| Grok | Read/analysis | Oriented — surfaced OpenClaw |
| PUBLIC: CONVERSATION | Read/analysis | New — bootstrap document ready, classification pending |
| PERSISTENT: IMPLEMENTATION | Read/analysis | Closed |
| ISSUE: Repository browsing | Read/analysis | Closed — 3 undeployed outputs |
| TASK: LEVELSET reports | Read/analysis | On hold |
| STORY: JFAC Open Meetings | Read/analysis (Tier 3) | Active — CCA deadline ~March 18 |
| M365 Copilot | Informational | No repo involvement |
| NotebookLM | TBD | Identified, not scoped |

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
| `CONSULTATION-PUBLIC-CONVERSATION-2026-03-16.md` | PUBLIC: CONVERSATION analysis + consultation packets |
| `HANDOFF-TO-PUBLIC-CONVERSATION-2026-03-16.md` | Bootstrap document for Claude self-talk space |
| `LEVELSET-TRANSMISSION-2026-03-16.md` | Copypaste-ready levelset packets for all entities |
| `CONTEXT-VAULT-2026-03-16.md` | Multi-conversation collapse preservation from ADMINISTRATION |
| `RESEARCH-TIM-OREN.md` | Research brief stub — Tim Oren voting patterns |
| `GROUND-TRUTH-VERIFICATION-2026-03-16.md` | Verified repo state — ground truth audit |
| `CONVERGENCE-2026-03-16.md` | **Cold-start bootstrap** — any new instance reads this first |
| `LEVELSET-EXTERNAL-AGENT-PROMPT.md` | Prompt template for external agents (Grok, Gemini, etc.) without direct repo access |
