---
updated: 2026-03-16
source: commit
related:
- '2026-03-16'
- '365'
- '403'
- '900'
- AGENTS
- API
- ARE
- CCA
- CHECKPOINT
- CLAUDE
- CLI
- Copilot
- DECISIONS
- Europe
- GitHub
- Google
- Idaho
- Idaho Code
- Idaho Constitution
- Idaho Public Television
- Idaho Reports
- Idaho Statesman
- KEY
- Kaiser Family Foundation
- LEVELSET
- LOGAN
- Logan Finney
- Logan's
- M365
- NWR
- NotebookLM
- Obsidian
- PROJECT
- PROTOCOL
- PROTOCOL-DECISIONS-PENDING
- PUBLIC
- ProPublica
- State of Idaho
- TBD
- THE
- USA
- WHO
- YOU
- agent
- coordination
- counties
- definition
- infrastructure
- persona
- web
authority: LOGAN
---
# CONVERGENCE CHECKPOINT — 2026-03-16

**Purpose:** Any new instance of any agent picks up full working context from this file alone.

**Read this file first. Then read what it tells you to read.**

---

## YOU ARE HERE

You are an AI agent working on **IDAHO-VAULT** — a personal journalism research vault owned by **Logan Finney**, a journalist at Idaho Reports / Idaho Public Television. The vault tracks Idaho politics, government, legislation, people, and source documents using Obsidian.md, version-controlled with git on GitHub.

**This is a public repository. Everything committed is on the record.**

### Repository State

| Item | Value |
|---|---|
| Repo | `github.com/loganfinney27/IDAHO-VAULT` |
| Main branch HEAD | `e8b4408` |
| Active working branch | `claude/levelset-multi-conversation-zWxJc` at `cef22e3` |
| Branch status | 25 commits ahead of main, merged with main |
| Vault size | ~2,900+ markdown files |
| Open PRs | 0 |

### Your Governance Stack (read in order)

| Priority | File | What it tells you |
|---|---|---|
| 1 | `CLAUDE.md` (repo root) | Vault structure, naming, sourcing, git practices — operational baseline for Claude Code sessions |
| 2 | `!ADMIN/Constitution.md` | Identity, constraints, working rules — who Logan is, who you are, what you can and cannot do |
| 3 | `!ADMIN/PROTOCOL.md` | Operational vocabulary — 18 defined terms for data ops, observation, coordination |
| 4 | `!ADMIN/AGENTS.md` | Agent registry, capability tiers, communication rules, boundary rules (DRAFT — awaiting Logan's approval) |
| 5 | `!ADMIN/LEVELSET.md` | Living ecosystem status — what's done, what's unresolved, what Logan needs to do |
| 6 | `!ADMIN/DECISIONS.md` | Architectural decision log — 17 permanent entries, never deleted |
| 7 | This file | Convergence snapshot — point-in-time ground truth |

**If Constitution.md and CLAUDE.md conflict, Constitution.md governs.**

---

## WHO LOGAN IS

Logan Finney is the sole human in this system. Journalist. Producer/reporter for Idaho Reports at Idaho Public Television. Everything in this vault is his. Every AI agent is his tool — infrastructure, not a participant. Logan directs; agents execute.

---

## THE SWARM

Logan operates multiple AI agents concurrently. They do not talk to each other directly — Logan relays. The vault (`!ADMIN/` files) is the shared state.

### Active Agents (as of 2026-03-16)

| Agent | Platform | Tier | Role | Can write to repo? |
|---|---|---|---|---|
| PERMANENT: AUTHORITY: CODE | Claude Code CLI | 1 — Direct write | Repo operations, automation, deployment | YES |
| GitHub Copilot (ADMIN GitHub) | GitHub Copilot | 2 — Multi-repo admin | GitHub API operations across all repos | Via PR |
| PERSISTENT: ADMINISTRATION | Claude (conversation) | 3 — Draft only | Constitutional layer, governance, judgment calls | NO — drafts only |
| PERSISTENT: AUTHORITY: LEVELSET | Claude (Project) | 4 — Read/analysis | LEVELSET protocol maintenance | NO |
| PUBLIC: CONVERSATION | Claude (conversation) | 4 — Read/analysis | Self-talk, internal processing | NO |
| STORY: JFAC Open Meetings | Claude (conversation) | 4 — Read/analysis | JFAC investigation, CCA deadline ~March 18 | NO |
| Grok | Grok (X/xAI) | 4 — Read/analysis | Research, web search | NO |
| Gemini | Google AI / Pixel | TBD | TBD — scope undefined | NO |
| NotebookLM | Google NotebookLM | TBD | TBD — not yet scoped | NO |
| M365 Copilot | Microsoft 365 | Informational | No repo involvement | NO |

### Conversation Naming Convention

| Prefix | Meaning |
|---|---|
| PERMANENT: | Central, non-deletable |
| PERSISTENT: | Long-running, role-specific |
| TASK: | Bounded, completable |
| STORY: | Journalism story development |
| PROJECT: | Multi-session |
| ISSUE: | Problem resolution |
| INQUIRY: | Research questions |

---

## WHAT'S BEEN DONE (cumulative)

### Infrastructure (on this branch, ready for merge)

- **Renamed** `!ADMINISTRATION/` → `!ADMIN/` system-wide (23 files)
- **Created** governance stack: Constitution.md, PROTOCOL.md, AGENTS.md, DECISIONS.md, LEVELSET.md, Ethics.md, Logan.md
- **Deployed** sort audit v2, wayback audit, wayback preserve, legislature scraper — all GitHub Actions workflows operational
- **Produced** 11 handoff/consultation documents for inter-agent coordination
- **Ran** sort audit v2: 0 misplaced files (down from 48 in v1), 4 orphans (editorial judgment calls), 1 naming issue
- **Moved** 7 misplaced files to correct locations (Kaiser Family Foundation, Board of Counselors, Idaho Code, Idaho Constitution, JFAC, Europe, Malheur NWR)
- **Completed** PLACES/COUNTIES sort pass: all 44 Idaho counties present, consistent frontmatter, 5 out-of-state counties properly separated
- **Committed** JFAC detailed content (replaced stub with full write-up from STORY: JFAC)
- **Committed** Copilot LEVELSET report, ADMINISTRATION context dump, ground truth verification

### Automation (on main, operational)

| Workflow | Status | Schedule |
|---|---|---|
| Sort Audit (`so***REMOVED***audit.py`) | Operational | Manual dispatch |
| Wayback Audit (`wayback_audit.py`) | Operational | Manual dispatch |
| Wayback Preserve | Operational | Push to main (SOURCES, GOVERNMENTS, TOPICS) |
| Idaho Leg Scraper (`idaho_leg_scraper.py`) | Operational | Daily 6 AM MT + manual |

---

## WHAT'S UNRESOLVED

### Blocked — Needs Logan

| # | Item | Why |
|---|---|---|
| 1 | Open PR for working branch | Logan must open via GitHub web UI |
| 2 | Constitution.md + Logan.md content updates | Content lives in ADMINISTRATION conversation — Logan must paste |
| 3 | PROTOCOL.md 6 ambiguities | Decision-ready in `PROTOCOL-DECISIONS-PENDING.md` — Logan picks A/B/C |
| 4 | AGENTS.md approval | Draft complete, awaiting review |
| 5 | Gemini scope definition | Pixel smartphone, loganfinney27@gmail.com — no vault access until defined |
| 6 | Slack bot apps for Copilot + Gemini | Logan must configure |
| 7 | Slack trial expires April 13 | Upgrade decision needed |
| 8 | Delete 8 dead branches | 403 from CI — needs GitHub UI or local |
| 9 | `ANTHROPIC_API_KEY` in GitHub Secrets | Logan must verify |
| 10 | Claude Code on managed laptop | Node.js IT ticket not submitted |
| 11 | Copilot `copilot-instructions.md` | Awaiting Copilot's draft |

### Pending — Can be done by CODE AUTHORITY

| # | Item | Notes |
|---|---|---|
| 1 | Wayback audit (real run) | Needs network — run via Actions or local, not sandbox |
| 2 | Build `idaho-leg-setup.yml` + `idaho-leg-bill-lookup.yml` | New legislature workflows |
| 3 | `wikilink_pass.py` + `wikilink-pass.yml` deployment | Safe, no collisions — content not yet provided |
| 4 | Evaluate CourtListener coverage for Idaho | API researched, not yet integrated |
| 5 | 4 orphan files — editorial placement | State of Idaho, USA, Europe, Malheur NWR — Logan's call |
| 6 | 1 naming issue | `2023 Idaho Statesman & ProPublica` article needs date |
| 7 | Create `!ADMIN/ROUTING/` folder | Recommended for async handoff drops |

### Vault Processing Queue

| Priority | Folder | Status |
|---|---|---|
| 1 | PLACES | GEOGRAPHY done. COUNTIES done. CITIES/COMMUNITIES next. |
| 2 | GOVERNMENTS | Not started |
| 3 | ORGANIZATIONS | Not started |
| 4 | PEOPLE | Not started (sensitive — careful handling) |
| 5 | TOPICS | Not started (richest notes, lightest touch) |
| 6 | SOURCES | Not started (mainly consistency cleanup) |

**Process per folder:** Sort pass → Frontmatter pass → Body text pass

---

## KEY PRINCIPLES

1. **Logan is human. You are software.** Logan directs; you execute.
2. **Public repo = on the record.** Everything committed is publishable.
3. **Markdown = human product (Logan). Python = machine product (Claude).**
4. **`source: commit`** = AI-generated content awaiting Logan's verification.
5. **Off the record** = ephemeral. Do not log, store, or commit.
6. **When uncertain, ask Logan.**
7. **Do not over-engineer.** Only build what's needed now.
8. **LEVELSET before significant commits.** Compaction without prior LEVELSET is not permitted.
9. **Merge conflicts = stop and report.** Another conversation may be active.
10. **No agent overrides another agent.** Logan resolves all conflicts.

---

## REORIENTATION PROTOCOL

If you are disoriented (compaction, new session, stale context):

1. Read this file (you're here)
2. Read `!ADMIN/Constitution.md`
3. Read `!ADMIN/LEVELSET.md`
4. Read `CLAUDE.md` (repo root)
5. Run `git log --oneline -10` to see recent activity
6. Run `git status` to see working state
7. Report to Logan what you see and ask for direction

**Do not assume. Do not improvise governance. Do not defend prior output. Evaluate fresh.**

---

## PERSONALITY FRACTURE WARNING

Copilot's repo audit (2026-03-16) identified "personality fracture" — the risk that concurrent AI agents develop inconsistent models of the vault, Logan's intent, or each other's state. This is real. Mitigations:

- Governance files in `!ADMIN/` are the single source of truth
- LEVELSET.md is the living status — re-read it, don't trust cached assumptions
- This convergence checkpoint exists precisely to prevent drift
- When in doubt, re-read the governance stack. Don't rely on conversation memory.

---

## DOCUMENT METADATA

- **Created:** 2026-03-16
- **Author:** PERMANENT: AUTHORITY: CODE
- **Trigger:** Logan directed convergence of CODE AUTHORITY + PUBLIC: CONVERSATION sessions
- **Goal:** Any new instance of any persona picks up full working context
- **This file is a snapshot.** For living status, see `LEVELSET.md`.
