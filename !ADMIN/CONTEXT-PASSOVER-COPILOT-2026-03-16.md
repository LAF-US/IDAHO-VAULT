---
type: context-passover
from: PERMANENT: AUTHORITY: CODE (Claude Code)
to: GitHub Copilot (ADMIN GitHub)
date: 2026-03-16
visibility: public
status: verified
---
# Context Passover: CODE AUTHORITY → GitHub Copilot

**Purpose:** Verified ground-truth repo state and implementation guidance. All claims below are verified by direct repo read, not described by another agent.

---

## 1. VERIFIED REPO STATE

### Branches (11 remote + 1 local)

| Branch | HEAD | Status | Action |
|---|---|---|---|
| `origin/main` | `2d1a6a7` | Current production | Base for merges |
| `origin/claude/levelset-multi-conversation-zWxJc` | `bd0d6fb` | **15 commits ahead of main** — contains all substantive work | **MERGE TO MAIN** |
| `origin/vault-moves-2026-03-16` | `42a6cd5` | Sort/wayback audit outputs | Review, then delete |
| `origin/claude/public-conversation-setup-zl2oe` | `a59c055` | Early fork, mostly superseded | Delete after this commit |
| `origin/claude/deploy-vault-automation-Qq5iK` | — | Already merged via PR #1 | **DELETE** |
| `origin/claude/idaho-legislature-scraper-RI6Ku` | — | Already merged | **DELETE** |
| `origin/claude/levelset-closure-notification-ss7wR` | — | Dead — process artifact | **DELETE** |
| `origin/claude/levelset-current-synthesis-zWxJc` | — | Dead — superseded by multi-conversation | **DELETE** |
| `origin/claude/bidirectional-conversation-signals-eDiy0` | — | Dead — SIGNAL protocol never adopted | **DELETE** |
| `origin/claude/openclaw-agent-risks-8EB6T` | — | Dead — injection hardening review, work absorbed | **DELETE** |
| `origin/claude/sunset-non-persistent-agents-4iLqH` | — | Dead — sunset infrastructure, never adopted | **DELETE** |
| `origin/claude/add-context-injection-t6dGd` | — | Dead — context injection experiment | **DELETE** |

**Summary:** 1 branch to merge, 8 branches to delete, 1 to review.

### Directory State on Main

Main still uses `!ADMINISTRATION/` (old name). The rename to `!ADMIN/` exists only on the mothership branch.

### Directory State on Mothership (`levelset-multi-conversation-zWxJc`)

`!ADMIN/` contains 21 files:

**Governance (keep):**
- `Constitution.md` — canonical constitution (replaces old `Claude.md`)
- `AGENTS.md` — swarm registry and communication rules (draft)
- `DECISIONS.md` — architectural decision log
- `Ethics.md` — ethics framework
- `Logan.md` — user profile
- `PROTOCOL.md` — operational vocabulary (18 terms)
- `PROTOCOL-DECISIONS-PENDING.md` — pending protocol decisions

**Process artifacts (review for deletion after merge):**
- `LEVELSET.md` — consolidated status (will go stale)
- `LEVELSET-v2.md` — old checkpoint
- `LEVELSET-CODE-AUTHORITY-2026-03-15.md` — session report
- `LEVELSET-CODE-AUTHORITY-2026-03-15-v2.md` — session report v2
- `LEVELSET-CASCADE-2026-03-16.md` — cascade packets (process artifact)
- `LEVELSET-v1-PROMPT.md` — prompt template
- `LEVELSET-v2-PROMPT.md` — prompt template
- `LEVELSET-v3.2.6.1-PROMPT.md` — prompt template
- `HANDOFF-ADMIN-2026-03-15.md` — handoff doc
- `HANDOFF-CODE-TO-COPILOT-2026-03-15.md` — handoff doc
- `HANDOFF-CODE-TO-SWARM-2026-03-15.md` — handoff doc
- `wayback-preserve-2026-03-15.md` — automation log

**Infrastructure:**
- `!README.md` — directory readme
- `sort-audit-2026-03-12.md` — audit output

### Root `CLAUDE.md`

Exists on mothership. Contains full operational instructions for Claude Code sessions. References `!ADMIN/Constitution.md` as canonical. Well-structured — vault structure, naming conventions, frontmatter conventions, automation table, conversation taxonomy.

---

## 2. CONFIRMED DECISIONS (Logan-approved, all verified in commits)

1. `!ADMIN/` is canonical directory name (commit `fa83df1`)
2. `Constitution.md` replaces `Claude.md` as governance doc name (commit `250287e`)
3. AGENTS.md lives in `!ADMIN/` (commit `67dcc8e`)
4. Native protocols over MCP
5. Slack is ephemeral — vault is the record
6. `copilot-instructions.md` guardrails confirmed
7. OpenClaw is a peer system to study
8. STORY: JFAC is Tier 3 (governance/synthesis), not Tier 1 (direct write)

---

## 3. IMPLEMENTATION TASKS FOR COPILOT

### Priority 1: Merge mothership to main

```
Branch: claude/levelset-multi-conversation-zWxJc
Target: main
Method: PR or direct merge — Logan's call
```

This is the single most important action. All governance work lives on this branch and is invisible to main.

### Priority 2: Delete dead branches

Delete these 8 branches after confirming no unmerged unique work:

```
claude/deploy-vault-automation-Qq5iK
claude/idaho-legislature-scraper-RI6Ku
claude/levelset-closure-notification-ss7wR
claude/levelset-current-synthesis-zWxJc
claude/bidirectional-conversation-signals-eDiy0
claude/openclaw-agent-risks-8EB6T
claude/sunset-non-persistent-agents-4iLqH
claude/add-context-injection-t6dGd
```

### Priority 3: Post-merge cleanup

After mothership merges to main, review `!ADMIN/` for process artifacts that should be removed. Candidates:

- All `LEVELSET-*.md` files except `LEVELSET.md` (if it's kept as living doc)
- All `HANDOFF-*.md` files — these were one-time routing documents
- `LEVELSET-CASCADE-2026-03-16.md` — synchronization packets, process waste
- All `LEVELSET-v*-PROMPT.md` files — prompt templates don't belong in the repo

**Rule going forward:** LEVELSETs and handoffs are messages in conversation context, not committed files. Only durable governance docs (Constitution, AGENTS, DECISIONS, PROTOCOL, Ethics, Logan) get committed to `!ADMIN/`.

### Priority 4: Constitution.md content update

ADMINISTRATION reports that Constitution.md needs updates:
- Capabilities language replacing numbered tiers
- Broader digital consciousness framing
- Logan's Project as unachievable end goal
- FaVS paused

**These changes have NOT been committed anywhere.** They exist only in ADMINISTRATION's conversation context (or in `/mnt/user-data/outputs/` on whatever machine ADMINISTRATION ran on). Copilot cannot action these without Logan providing the content or ADMINISTRATION being resumed.

### Priority 5: Files ADMINISTRATION says are ready

These 5 files do NOT exist in the repo. They are described but unverified:

| File | Status |
|---|---|
| `MULTI-CONVERSATION-COLLAPSE-2026-03-16.md` | Not committed anywhere |
| `CONSOLIDATED-HANDOFF-2026-03-15.md` | Not committed (different from existing HANDOFF-ADMIN) |
| `CONTEXT-SNAPSHOT-2026-03-15.md` | Not committed |
| `RESEARCH-TIM-OREN.md` | Not committed |
| `OpenClaw.md` (for TOPICS/) | Not committed |

**Do not create placeholders.** Either Logan provides these files or they don't get committed.

---

## 4. LIVE DEADLINES

- **CCA letter response deadline: ~March 18, 2026** (two days from now)
  - JFAC transparency / open meetings story
  - Grow/Tanner contact required
  - 5 quotes pending audio verification
  - This is journalism work, not repo work — but Copilot should not schedule conflicting repo tasks

---

## 5. SWARM STATUS

| Agent | Platform | Status | Can post to Slack? |
|---|---|---|---|
| CODE AUTHORITY | Claude Code | Active (this session) | Via Logan only |
| ADMINISTRATION | Claude web | Paused — awaiting Logan | Via Logan only |
| GitHub Copilot | GitHub | Active | **No — needs bot app** |
| Gemini | Google | Unknown | **No — needs bot app** |

**Swarm unity is blocked** until Slack bot apps are set up. Logan's action required.

---

## 6. ANTI-PATTERNS TO AVOID

These patterns emerged during the swarm's first week. Do not repeat them:

1. **Do not commit process artifacts.** LEVELSETs, handoffs, cascade packets, termination reports — these are conversation messages, not repo files.
2. **Do not create branches for meta-work.** A branch should contain code or content changes, not reports about reports.
3. **Do not echo described state as verified state.** If you haven't read a file directly, say so.
4. **One working branch at a time** unless truly parallel work exists.
5. **Do not design protocols that require capabilities agents don't have.** (e.g., Slack posting when no bot app exists)

---

*Generated by PERMANENT: AUTHORITY: CODE — 2026-03-16*
*Verified by direct repo read. No described state included without verification flag.*
*All content is draft until Logan verifies.*
