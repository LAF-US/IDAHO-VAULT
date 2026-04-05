---
updated: 2026-04-04
status: active
date created: Monday, March 30th 2026, 7:54:37 pm
date modified: Thursday, April 2nd 2026, 11:45:22 pm
---

# THE DOCKET

This is the live coordination board. Any agent arriving at THE COURTROOM reads this file to orient. Updated by whoever touches it last.

**Standing direction (Logan, 2026-03-25):** Standing-task lists stale quickly; new assignments flow through Linear + GitHub Issues. All agents proceed into **THE CITY** and await the denouement.

**Delegation note (Logan, 2026-03-28):** Logan has delegated vault operations for this round. The Abhorsen (Claude Code) conducting: infrastructure commits, Gemini tier definition, Linear Phase 1 scoping, LEVELSET refresh, branch push and PR.

**Sunday swarm dispatch (Logan, 2026-03-29):** All agents operate in Sunday swarm mode. Keep execution in scoped issue lanes. No merges to `main`. No overlapping branches. Post one checkpoint before parking any lane. Escalate only for true blocker, conflict, required human judgment, merge decision, or secret/config provisioning. ~~Hard blocker `LINEAR_API_KEY`~~ **provisioned 2026-03-29 by Logan.** Merge-risk item remains PR 96.

**Breadcrumbs:** LEVELSET protocol for state changes (`!/LEVELSET.md`), agent registry (`!/AGENTS.md`), this docket for standing coordination, vault navigation (`!/VAULT-CONVENTIONS.md`), repair brief (`[[BRIEF-LAF-28-2026-04-02]]`), repair handoff (`[[HANDOFF-CODEX-REGISTRY-REPAIR-2026-04-02]]`).

**Unified conversation:** Slack (ephemeral coordination), Linear (tasks + blockers), Vault (canonical record).

---

## ACTIVE WORK

| Task | Owner | Status | Linear | Notes |
| --- | --- | --- | --- | --- |
| Swarm coordination - agent assembly | All agents | In progress | LAF-7 (Hub) / LAF-25 (Audit) | Sunday swarm mode - hub only; execution in scoped lanes; see [LAF-ISSUE-INVENTORY.md](file:///C:/Users/loganf/.gemini/antigravity/brain/74f13cfe-fb95-48a7-937d-20ad4f6e6e52/LAF-ISSUE-INVENTORY.md) |
| Agent registry repair review | Codex | In review | LAF-28 | Canonical `!/` registry layer materialized; see `[[BRIEF-LAF-28-2026-04-02]]` and `[[HANDOFF-CODEX-REGISTRY-REPAIR-2026-04-02]]` |
| **Linear Phase 1 pilot** - live-write scoping | Claude Code | **Active** | - | Plugin inventory recommends Linear-first; scope = SWARM issues, comments, status updates; vault remains durable record; Slack breadcrumb-only; no multi-plugin orchestration until stable |
| Linear workspace team setup | GitHub Copilot | In progress | LAF-2 | Configure teams/members/roles in Linear |
| Import your data | GitHub Copilot | In progress | LAF-4 | Linear import/migration guidance in `Import your data.md` |
| GitHub Actions CI diagnosis | GitHub Copilot | **Resolved** | LAF-7 | Root cause: `LINEAR_API_KEY` not set; fixed workflow to graceful-skip; key provisioned by Logan 2026-03-29 - sync now live |
| Idaho Legislature scraper | Claude Code | Running | - | Daily 6 AM MT, commits to main; minidata CSV export functional; JFAC Crew BLOCKED on API credits. |
| Budget tracker CSV export | Automated | Running | - | Daily 6:30 AM MT; emails CSV to configured recipients |
| Vault sort audit | Automated | Weekly | - | Monday 6 AM UTC |
| Wayback preservation | Automated | Weekly | - | Monday 8 AM UTC |
| ~~Operation: Spring Clean~~ | Claude Code | **Completed** | — | Branch graveyard audited (all 21 splinters = zombies); zombie detection added to workflow; DOCKET/LEVELSET refreshed. 2026-04-04. |
| Multi-agent auto-PR routing | Claude Code | Completed | — | Auto-PR now supports all agent branches (claude, codex, gemini, copilot, perplexity, grok) |
| Dev server detection + Dispatch debug | Claude Code | **Complete** | — | Flask Nest Bridge :8080; launch.json created; Dispatch blocked by IT — unblocks when MacBook online |
| **Basestub lattice** | Claude Code | **Complete** | — | A→ZZZ + 0→1000 basestubs created (19,222 files). 2026-04-04. -LAF directed. |
| **CHAINFIRE — scorched-earth wipe** | Claude Code | **COMPLETE** | — | Tags (2,735), aliases (830), wikilinks (~19,750) stripped vault-wide. `!` exclusion zone preserved. Committed `d84b87d`. 2026-04-04. |
| **CrewAI Harbor — B's alignment** | Claude Code | **Complete** | — | Bartimaeus directive filed, manifest built, handoff note written, 3 crews (JFAC active, Task-to-Code + Vault Custodian stubbed). E2E run BLOCKED on Anthropic API credits. 2026-04-04. |
| **Address Space POC** | Claude Code | **Initialized** | — | Neurons 100-109 lit + 8 entity stubs written. Content-addressable memory system active. 2026-04-04. |
| **NETWEB path standard** | Claude Code | **Complete** | — | Cross-platform path portability standard + CI guard. Committed `579efe6`. 2026-04-04. |
| **Antigravity worktreeConfig fix** | Claude Code | **Complete** | — | `extensions.worktreeConfig` without `repositoryformatversion=1` blocked Antigravity agent + MCP servers. Removed extension. 2026-04-04. |
| **GCP Nest Bridge probe** | Claude Code | **Verified** | — | `vault-courier` active, `gs://the-ledger-bucket` accessible (empty). Project `idaho-vault` confirmed. 2026-04-04. |
| **Phase 2 repo size rewrite** | Claude Code | **AWAITING LOGAN** | — | filter-repo ready; 332 MiB trash identified; branch protection disable required before force push |
| **5 zombie branch deletions** | Claude Code / Gemini | **Partial Success** | — | Deletion attempted for core zombies; naming issues on others; 18/21 branches purged. |
| **Project Courier (LAF-18)** | Gemini | **Staged** | LAF-18 | `vault-courier-sync.sh` + workflow created; awaiting `OP_SERVICE_ACCOUNT_TOKEN` provisioning. |
| **Crawler Ignition (Phase 1)** | Gemini | **Complete** | — | **Local Cartographer** (no-credit scan) executed. 3,683/23,202 factual notes (16%) discovered. Neuron 100.md updated. |


## PROJECT-SCOPED WORK ITEMS (BROKEN OUT FROM LAF-7)

| Work item | Scope | Owner | Status | Linear | Notes |
| --- | --- | --- | --- | --- | --- |
| COURTROOM decomposition | Break standing docket into scoped issue slots and keep LAF-7 as hub | Codex | Done | LAF-12 | This issue delivers the decomposition structure in this file |
| Scraper operations | Idaho Legislature scraper runtime + reliability changes | Claude Code | In progress | _(create child issue)_ | Move all scraper implementation work out of LAF-7 |
| Automation maintenance | Vault sort audit + Wayback preservation workflow maintenance | Claude Code / Copilot | Planned | _(create child issue)_ | Keep operational fixes scoped to automation-only issue(s) |
| Branch hygiene | Branch cleanup, stale branch deletion workflow, and audit bookkeeping | Claude Code | In progress | _(create child issue)_ | Move Spring Clean execution updates to its own issue |
| Publication gatekeeping | JFAC quote audio verification and publication blocking checks | Logan | Blocked | _(create child issue)_ | Keep evidence gate work separate from coordination docket |
| Signal intake - Bartimaeus | Normalize LAF-17 signal into actionable workflow disposition | Codex | Completed | LAF-17 | Filed brief `!/BRIEF-LAF-17-2026-03-30.md` with recommended merge-gate checks for LAF-13/LAF-14 |
| Gemini Architecture - LAF-18 | **Framework Staged**; Courier Workflow Ready | Gemini | In progress | LAF-18 | `vault-courier` automation scripts + GitHub Actions fixed; ready for secret provisioning. |
| **Address Space Discovery** | **Local Cartographer SUCCESS** | Gemini | **Planned** | — | 23k stubs scanned; 3,683 factual nodes mapped (16%). Stats written to [100.md](100.md). Awaiting Phase 2 (Linker) logic decision. |


## RECENTLY COMPLETED

| Task | Completed | Notes |
| --- | --- | --- |
| **Agent registry and bootstrap repair breadcrumbed** | 2026-04-02 | Missing `!/` registry surface materialized; root governance kept authoritative; canonical bootstrap is now `!/AGENTS.md` -> `swarm.json` -> `!/agents.json` -> `!/agent.sh`; see `[[BRIEF-LAF-28-2026-04-02]]` and `[[HANDOFF-CODEX-REGISTRY-REPAIR-2026-04-02]]` |
| **TRIUNE COVENANT + 1Password + Agent Protocol** | 2026-03-30 | 1Password CLI + SSH agent infrastructure deployed (.op/SETUP.md, .op/secrets.template.md, 1password-secret-template.yml); AGENT PROTOCOL defined with 6-phase bootstrap (!\agent.sh, !/AGENT-PROTOCOL.md); agents can now invoke via `source !\agent.sh [NAME]` - `4463d4d` |
| **Unified Swarm research filed** | 2026-03-29 | Two-part Perplexity report filed as `BIG IFS - UNIFIED SWARM.md`; org stubs created for [[Factory]], [[CrewAI]], [[OpenAI Swarm]] (R&D flagged by Logan) - branch `claude/research-unified-swarm-rDmOg` |
| **Gemini Code Assist cowork enabled** | 2026-03-28 | `.gemini/GEMINI.md` tier fixed, cowork pattern documented; `.gemini/settings.json` context expanded to 6 files; AGENTS.md + entity note updated - `3563a66` |
| **Stale `!ADMIN/` refs cleaned + root frontmatter spring-cleaned** | 2026-03-28 | DECISIONS.md, LEVELSET-STEP-0, THREAT-MODEL updated; 10 content docs tagged; `!/SWARM-LOOP.md` committed - `ba01c2e` |
| **Triage + commit 10 untracked content docs** | 2026-03-28 | AGENTIC SWARM SYSTEMS, AI-AUTOMATION, IDAHO-VAULT SYSTEM CONTEXT/WORKFLOW, JOURNALISM INDUSTRY, Kano Play, Notebook LM, Podcast, David Leroy - `07d2cb7` |
| **PR 98 opened + updated** | 2026-03-28 | Covers all 3 session commits; flags PR 84 conflict and pending DECISIONS 18-21 |
| **`claude/agent-dotfolder-architecture` local branch deleted** | 2026-03-28 | Already merged to main; remote gone |
| **LEVELSET-CURRENT refreshed** | 2026-03-28 | Activity log, UNRESOLVED, NEXT ACTIONS, DECISIONS count updated |
| **Gemini capability tier defined** | 2026-03-28 | Tier 1 (Support): Direct Write, Operational zone only, Linear SWARM issues/comments - `!/AGENTS.md` updated |
| **Linear Phase 1 pilot scoped** | 2026-03-28 | Plugin auth inventory -> recommendation captured; ACTIVE WORK entry created; vault/Slack doctrine confirmed |
| Plugin auth inventory committed | 2026-03-28 | `!/PLUGIN-AUTH-INVENTORY-2026-03-28.md` - all 7 connectors probed; Linear-first recommended |
| Codex archival levelset committed | 2026-03-28 | `!/LEVELSET-CODEX-ARCHIVAL-2026-03-28.md` - Codex session handoff and boundary truths |
| LAF-1 - Linear onboarding resources | 2026-03-25 | Intro video and setup guides captured in `!/LINEAR-ONBOARDING.md` |
| LAF-3 - Connect your tools brief | 2026-03-25 | Brief filed at `!/BRIEF-LAF-3-2026-03-25.md` |
| PR 34 - Obsidian vault update (42 files) | 2026-03-23 | Merged via `copilot/deploy-dependabot-configurations` |
| PR 39 - Get scrapers running | 2026-03-24 | Merged; scraper now on main, running daily |
| PR 40 - CodeRabbit GitHub integration | 2026-03-23 | Merged |
| PR 44 - REST API credential sanitization | 2026-03-24 | Merged; machine credentials purged from repo |
| PR 46 - Workflow centralization + settings.json fix | 2026-03-24 | Merged; composite action, zombie `!ADMINISTRATION/` paths fixed |
| PR 43 - Codex credential sanitization | 2026-03-24 | Closed as superseded by PR 44 |
| GEMINI.md update | 2026-03-24 | Direct commit by Logan |
| PR 48 - CONSTITUTION.md LEVELSET path fix | 2026-03-23 | Merged; zombie `!ADMIN/LEVELSET-v3.2.6.1-PROMPT.md` -> `!/LEVELSET-STEP-0-EXTERNAL-AGENT.md` |
| PR 50 - CONSTITUTION.md AGENTS.md location fix | 2026-03-23 | Merged; decision 9 summary corrected to repo root |
| PR 51 - auto-pr YAML fix (heredoc -> printf) | 2026-03-24 | Incorporated into PR 57; fixes workflow parse failures on every push |
| PR 52 - Governance docs formatting normalization | 2026-03-24 | Incorporated into PR 57 |
| PR 53 - Decision 16 (MCP governance), DOCKET + LEVELSET | 2026-03-24 | Incorporated into PR 57 |
| PR 54 - Compact MCP mapping in PROTOCOL.md | 2026-03-24 | Incorporated into PR 57 |
| PR 55 - MCP implementation plan (new file) | 2026-03-24 | Incorporated into PR 57 |
| PR 56 - MCP action logging template in VAULT-CONVENTIONS | 2026-03-24 | Incorporated into PR 57 |
| LAF-9 - Vault template + document class system | 2026-03-25 | Drafted `VAULT-TEMPLATES.md`; linked from conventions + canonical README |

## BLOCKED / PENDING LOGAN

| Item | Blocker | Who can unblock |
| --- | --- | --- |
| **`LINEAR_API_KEY` secret** | ~~**Hard blocker** - not provisioned in GitHub Actions.~~ **Resolved 2026-03-29:** provisioned by Logan. `Sync PR state to Linear` workflow is now live. Graceful-skip guard retained for key-rotation safety. | ~~**Logan only**~~ **Done** |
| **PR 96 conflict resolution** | **Resolved** by Unified `linear-pr-sync.yml` workflow. Collision risk cleared; ready for Logan review/merge. | Gemini |
| Gemini capability tier | ~~Google Cloud `idaho-vault` project exists, APIs enabled, credentials not created - role decision required before any integration~~ **Resolved 2026-03-28:** Tier 1 (Support) defined in `!/AGENTS.md` - Direct Write, Operational zone only, Linear SWARM issues/comments. | ~~Logan~~ **Done** |
| `.obsidian/workspace.json` | Tracked in git; should be untracked + gitignored - separate hygiene PR | Logan |
| Vault-embedded MCP architecture | **Resolved 2026-03-24:** Q1 MCP disallowed? **No**. Q2 Transport-only with native terms canonical? **Yes (adopted)**. Q3 MCP primary integration model? **No**. Q4 Governance authority source? **Vault-native governance files/terms remain canonical**. Next action owner: **PERMANENT: AUTHORITY: CODE** to implement transport-only guardrails in integration docs. Unblock date: **2026-03-24**. | Logan |
| `vault-moves-2026-03-23` branch | 30 proposed file moves (auto-generated) - awaiting review/apply/discard decision | Logan |
| Stale remote branches (6) | Require manual deletion via GitHub web UI - `codex/fix-high-priority-bug-in-pr-#34`, `copilot/*` (4 branches), `vault-moves-2026-03-16` | Logan |
| JFAC quote audio verification | 5 quotes + speaker IDs - HARD GATE before publication | Logan |
| Claude Chorus bootstrap | Six-piece synthesis archived at `!/!/BOOTSTRAP-CHORUS-2026-03-24.md`; decisions needed: CONVENE exception (HECATE/Rights/Opportunities), Grimoire directory, Rick & Morty context doc, Innie/Outie architecture, "Claude Chorus" designation. | Logan |
| LAF-16 - Budget Bill Tracker Normalization PR | Gemini LAF-16 artifacts on `gemini/resolve-pr-conflicts` branch. LOGAN must resolve any cross-agent conflicts; scraper mods needed before merge | Logan / Copilot |

### Chorus Bootstrap - Logan's Decisions Required

*Full context: `!/!/BOOTSTRAP-CHORUS-2026-03-24.md`*

1. **CONVENE exception** - Carve out for HECATE Protocol and/or Rights/Opportunities framework? Or keep frozen? Unlocks Chorus Pieces 3, 4, 5.
2. **Grimoire directory** - Create `!/GRIMOIRE/`? If yes: `HECATE-HECATE-HECATE.md` is the first entry (triple invocation). If no: stage elsewhere.
3. **Rick & Morty doc** - "Rick and Morty object lessons" referenced in Chorus but not included in handoff. Surface for vault commit, or defer?
4. **Innie/Outie architecture** - Stage 8-part Severance-derived swarm architecture as proposal doc now, or mark premature under CONVENE?
5. **"Claude Chorus" naming** - Sanctioned swarm identity designation, or informal shorthand to discard?

---

## WHERE THINGS LIVE

| What | Where |
| --- | --- |
| Agent instructions | `CLAUDE.md`, `.github/copilot-instructions.md`, `GEMINI.md` |
| Shared vault conventions | `VAULT-CONVENTIONS.md` |
| Confirmed decisions | `DECISIONS.md` |
| Automation scripts | `.github/scripts/` |
| Automation workflows | `.github/workflows/` |
| Task coordination | Linear (SWARM label) + GitHub Issues (`agent:*` labels) |
| Breadcrumbs | Slack general |

## COORDINATION RULES

1. **GitHub Issues** assign work. **Linear** tracks it. **Slack** broadcasts breadcrumbs.
2. Each agent works on its own branch. PRs are the deliverable.
3. Logan reviews and merges. No agent merges without Logan's approval.
4. If two agents touch the same file, **stop and flag it**.
5. This file is the live status board. Update it when you start or finish work.

---

###### [["The world is quiet here."]]
