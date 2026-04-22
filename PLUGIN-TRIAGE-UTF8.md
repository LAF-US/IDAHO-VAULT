---

authority: LOGAN

status: OPEN ΓÇö awaiting Logan's decisions at Checkpoints 1ΓÇô4

date: 2026-04-06

updated: 2026-04-07

branch: claude/obsidian-plugins-triage-YDJ6Z

related: []

- '2026-04-06'

- '2026-04-07'

- AGENTS

- Breadcrumbs

- CLAUDE

- DOCKET

- LEVELSET-CURRENT

- Obsidian Sync

- PROTOCOL-CONFERENCE-CALL

- agent

- plugins

date created: Monday, April 6th 2026, 9:28:12 pm
date modified: Monday, April 6th 2026, 9:35:16 pm
---



# PLUGINS-TRIAGE-2026-04-06



**Triage by:** Claude Code (The Abhorsen)

**Branch:** `claude/obsidian-plugins-triage-YDJ6Z`

**Status:** Conference call agenda staged ΓÇö awaiting Logan's decisions



---



## Why This Document Exists



Multiple agents have touched `.obsidian/` across several sessions. A critical discrepancy emerged during research: **LEVELSET-CURRENT reports 49 community plugins enabled on desktop, but the committed `community-plugins.json` contains only 12 entries.** Four plugin decisions have been deferred in the UNRESOLVED table without a resolution path.



This document consolidates all agented plugin documentation, surfaces the discrepancy, and structures a levelset session for Logan to run through four decision checkpoints.



---



## Agented Documentation ΓÇö Sources



| Document | Author | Date | What It Says |

|---|---|---|---|

| `LEVELSET-CURRENT.md` ┬ºObsidian Plugin State | Claude (Abhorsen) | 2026-04-05 | **49 community plugins enabled** on desktop; 0 on mobile (Restricted Mode); device split established |

| `DOCKET.md` ΓÇö "Obsidian Plugin Recovery" | Codex (Janitor) | 2026-04-05 | `community-plugins.json` restored to HEAD (49 enabled) ΓÇö marked COMPLETE |

| `LEVELSET-CURRENT.md` Activity Log item 8 | Claude (Abhorsen) | 2026-04-05 | Codex UTF-16 incident: `community-plugins.json` corrupted to 140 entries in UTF-16 LE; caught and corrected |

| `LEVELSET-CURRENT.md` Activity Log item 6 | Claude (Abhorsen) | 2026-04-05 | 140-plugin audit: 49 enabled, 91 dormant (17 configured, 79 stock) |

| `VAULT-CONVENTIONS.md` ┬ºObsidian Sync / Git Boundary | Collaborative | Current | Device split policy; desktop plugin lists do not sync to mobile |

| `!/AGENTS.md` ΓÇö Agent Registry | Claude (Abhorsen) | 2026-04-05 | Lane ownership: Claude owns `.obsidian/`; Codex handles cleanup when assigned |

| `PLUGIN-AUTH-INVENTORY-2026-03-28.md` | Claude (Abhorsen) | 2026-03-28 | External MCP connector audit (GitHub, Linear, Slack, GCal, GDrive, HuggingFace, Cloudflare) ΓÇö Linear-first recommended |

| `PROTOCOL-CONFERENCE-CALL` (Copilot/Clerk) | GitHub Copilot (The Clerk) | 2026-04-06 | **Local-only** ΓÇö exists on Logan's desktop via Obsidian Sync, not yet committed to git. Proposes conference call record format and JFAC coverage example. Awaiting Logan's review and adoption. |



---



## Critical Discrepancy



| Measure | Value |

|---|---|

| **LEVELSET-CURRENT reports** | 49 community plugins enabled |

| **`community-plugins.json` in git** | **12 entries** |

| **Delta** | 37 missing |



**Root cause (likely):** The Codex UTF-16 incident on 2026-04-05 corrupted `community-plugins.json`. Codex "restored to HEAD (49 enabled)" ΓÇö but the HEAD it restored to was the `ec09efd0` commit, which itself only had 12 entries (the +5 plugins from that session were added after the pre-session baseline). The Obsidian Sync live state on Logan's Windows desktop reflects the correct count; the git record does not.



**This is the gate:** No further plugin commits from any agent until Logan confirms the authoritative count and provides the correct file.



---



## The Four Decision Checkpoints



### Checkpoint 1 ΓÇö Git / Live Sync (REQUIRED FIRST)

**Gate: blocks all other plugin work**



| | |

|---|---|

| **Question** | What does Logan's live Obsidian desktop show as the enabled community plugin count? |

| **Action for Logan** | Open Obsidian ΓåÆ Settings ΓåÆ Community plugins ΓåÆ count enabled. Then paste or confirm the list. |

| **Action for Claude** | Commit authoritative `community-plugins.json` once Logan confirms; update LEVELSET-CURRENT |

| **Logan's answer** | _(fill in)_ |



---



### Checkpoint 2 ΓÇö Breadcrumbs Frontmatter Config (Medium)

**Can do this session; Claude implements immediately after Logan answers**



| | |

|---|---|

| **Question** | Which frontmatter fields should the Breadcrumbs plugin traverse for navigation? |

| **Options** | A: `related:` only ┬╖ B: `related:` + `tags:` ┬╖ C: `related:` + `parent:` ┬╖ D: All three ┬╖ E: Logan specifies |

| **Note** | The zettelkasten address space (19,533 stubs) is built on `related:` links. `parent:` exists in many stubs. Breadcrumbs is the keystone for navigating the graph. |

| **Logan's answer** | _(fill in)_ |



---



### Checkpoint 3 ΓÇö Bulk Uninstall 91 Dormant Plugins (Low / can defer)



| | |

|---|---|

| **Question** | Bulk-remove the 79 stock-dormant plugins now, or continue deferring? |

| **Context** | 140 plugins installed; 49 enabled; 91 dormant. 17 dormant are configured (intentional keeps). 79 are stock-dormant with no config. No urgency ΓÇö vault functions fine as-is. |

| **If Yes** | Claude removes plugin directories + updates JSON in a separate `chore(plugins): dormant cleanup` commit |

| **If No** | Deferred; revisit during next LEVELSET |

| **Logan's answer** | _(fill in)_ |



---



### Checkpoint 4 ΓÇö LLM Plugin Sprawl (Low / can defer)



| | |

|---|---|

| **Question** | Of the 11 installed AI/LLM plugins, which are intentional keeps? |

| **Known installed** | `smart-connections`, `smart-connections-visualizer`, `bmo-chatbot`, `ai-image-analyzer`, `ai-templater`, `obsidian-completr` + 5 others |

| **Recommendation** | Keep: `smart-connections` (semantic search), `smart-connections-visualizer` (graph). Evaluate: `bmo-chatbot`. Remove rest. |

| **Logan's answer** | _(fill in ΓÇö or defer)_ |



---



## Triage Route



```

START

  ΓööΓöÇ Checkpoint 1 (REQUIRED): Logan confirms live plugin count

       Γö£ΓöÇ Count confirmed + JSON provided

       Γöé    ΓööΓöÇ Claude commits authoritative community-plugins.json

       Γöé         ΓööΓöÇ LEVELSET-CURRENT updated ΓåÆ Checkpoint 2

       ΓööΓöÇ Count uncertain

            ΓööΓöÇ STOP ΓÇö Logan reopens Obsidian, checks Settings, returns



  Checkpoint 2 (this session): Breadcrumbs field config

       Γö£ΓöÇ Logan answers ΓåÆ Claude commits breadcrumbs/data.json

       ΓööΓöÇ Logan defers ΓåÆ note deferred; proceed to Checkpoint 3



  Checkpoint 3 (can defer): Dormant plugin cleanup

       Γö£ΓöÇ Yes ΓåÆ Claude executes bulk remove (separate commit)

       ΓööΓöÇ No ΓåÆ note deferred; proceed to Checkpoint 4



  Checkpoint 4 (can defer): LLM sprawl

       Γö£ΓöÇ Logan provides keep list ΓåÆ Claude removes rest (separate commit)

       ΓööΓöÇ Defer ΓåÆ note deferred



  CLOSE: Claude updates LEVELSET-CURRENT Activity Log, pushes branch, PR opened

```



---



## On PROTOCOL-CONFERENCE-CALL (Copilot / The Clerk)



The Clerk's `PROTOCOL-CONFERENCE-CALL` document is visible in Obsidian's unlinked mentions panel (2026-04-06 daily note, right panel) but is not yet committed to git. It proposes:

- A conference call record format

- Example path: `!/CONFERENCE-RECORD-2026-04-06-JFAC-COVERAGE.md`

- Status: *Proposed by GitHub Copilot (The Clerk). Awaiting Logan's review and adoption.*



**Logan's decision needed:** Adopt the Clerk's conference call record format (commit and ratify), defer, or discard. If adopted, Claude can commit it to `!/` on this branch per lane boundaries (Claude owns git commits; content in `!/` is Gemini's lane, but structural format docs are Claude-lane).



---



## Post-Triage Deliverables (Claude executes after decisions)



| Deliverable | Trigger | File |

|---|---|---|

| Authoritative `community-plugins.json` | Checkpoint 1 | `.obsidian/community-plugins.json` |

| Breadcrumbs settings | Checkpoint 2 | `.obsidian/plugins/breadcrumbs/data.json` |

| Dormant plugin removal | Checkpoint 3 (if Yes) | `.obsidian/plugins/` + `community-plugins.json` |

| LLM plugin removal | Checkpoint 4 (if decided) | `.obsidian/plugins/` + `community-plugins.json` |

| LEVELSET-CURRENT update | All | `LEVELSET-CURRENT.md` |

| DOCKET close entry | All | `DOCKET.md` |

| PROTOCOL-CONFERENCE-CALL commit | If adopted | `!/CONFERENCE-RECORD-FORMAT.md` or per Clerk's proposed path |



---



## Verification Checklist (post-session)



- [ ] `community-plugins.json` count matches LEVELSET-CURRENT reported count

- [ ] LEVELSET-CURRENT Activity Log has 2026-04-07 entry for this triage

- [ ] DOCKET has "Plugins Triage Session" row marked COMPLETE

- [ ] PR on `claude/obsidian-plugins-triage-YDJ6Z` contains only `.obsidian/`-lane files (no cross-lane edits)

- [ ] If Breadcrumbs configured: `.obsidian/plugins/breadcrumbs/data.json` committed

- [ ] If Clerk's protocol adopted: document committed under Logan's ratification



---



*Authored by Claude Code (The Abhorsen) on `claude/obsidian-plugins-triage-YDJ6Z` ΓÇö 2026-04-07*

*The vault is the record. Logan decides.*

