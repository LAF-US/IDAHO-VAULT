---
type: agent-registry
version: 1.0
date: 2026-03-15
---

# Agent Registry — IDAHO-VAULT

Central registry of all Claude Code agents operating in the IDAHO-VAULT repository. This document tracks agent status, persistence, and sunset readiness.

**Last Updated:** 2026-03-15

---

## Registry Table

| Agent Name | Tier | Type | Status | Persistence | Sunset Status | Flagged Date | Notes |
|---|---|---|---|---|---|---|---|
| **PERSISTENT: CODE AUTHORITY** | 1 | Persistent | Active | Permanent | KEEP_ACTIVE | — | Direct repo write access; core infrastructure |
| **PERSISTENT: ADMINISTRATION** | 2 | Persistent | Active | Permanent | KEEP_ACTIVE | — | Constitutional layer; governance authority |
| **PERSISTENT: IMPLEMENTATION** | 3 | Persistent | Active | Permanent | KEEP_ACTIVE | — | Governance/architecture layer |
| **TASK: Sunset non-persistent agents** | 1 | Task | Active | Ephemeral | FLAGGED_FOR_SUNSET | 2026-03-15 | Agent management/lifecycle; closes upon completion |
| **STORY: JFAC Open Meetings** | 1 | Story | Active | Ephemeral | FLAGGED_FOR_SUNSET | 2026-03-15 | Bulk vault work on specific topic; synthesis pending |
| **TASK: LEVELSET reports** | 3 | Task | On Hold | Ephemeral | FLAGGED_FOR_SUNSET | 2026-03-15 | Synthesis/reporting across conversations; on hold status |
| **Claude Code – Idaho Legislature Scraper** | 1 | Story | Terminating | Ephemeral | TERMINATED | 2026-03-14 | Completed scraper implementation; LEVELSET-v3.2.6 created |

---

## Sunset Status Definitions

- **KEEP_ACTIVE:** Persistent infrastructure agent; do not sunset or close
- **FLAGGED_FOR_SUNSET:** Ephemeral agent awaiting synthesis and Logan's deletion order
- **TERMINATED:** Agent has finished work; LEVELSET report completed; archived in git history
- **DELETION_PENDING:** Awaiting Logan's explicit deletion order; artifacts preserved
- **DELETED:** Artifacts removed per Logan's order; final LEVELSET-DELETE report committed

---

## Non-Persistent Agents Ready for Sunset

### 1. TASK: Sunset non-persistent agents
- **Branch:** `claude/sunset-non-persistent-agents-4iLqH`
- **Role:** Agent management, identification, and sunset process design
- **Artifacts:** Will create AGENT-REGISTRY, SUNSET-PROCESS, and synthesis documents
- **Completion:** Upon completion, will create LEVELSET-SUNSET-sunset-agents.md
- **Status:** FLAGGED_FOR_SUNSET → Awaiting Logan's deletion order after synthesis complete

### 2. STORY: JFAC Open Meetings
- **Role:** Story-scoped bulk vault work on JFAC topic
- **Status:** Active
- **Awaiting:** Synthesis document LEVELSET-SUNSET-jfac-open-meetings.md
- **Status:** FLAGGED_FOR_SUNSET → Awaiting Logan's deletion order after synthesis complete

### 3. TASK: LEVELSET reports
- **Role:** Synthesis and reporting across conversations
- **Status:** On hold
- **Awaiting:** Final synthesis document LEVELSET-SUNSET-levelset-reports.md
- **Status:** FLAGGED_FOR_SUNSET → Awaiting Logan's deletion order after synthesis complete

---

## Sunset Workflow Status

| Step | Status | Owner | Notes |
|---|---|---|---|
| 1. Agent Identification | ✅ Complete | Sunset Agent | All non-persistent agents identified |
| 2. Registry Creation | ✅ Complete | Sunset Agent | This file created |
| 3. Sunset Process Documentation | ⏳ In Progress | Sunset Agent | SUNSET-PROCESS.md being created |
| 4. Agent Synthesis | ⏳ Pending | Various Agents | LEVELSET-SUNSET-*.md reports to be created |
| 5. Logan Review & Approval | ⏳ Pending | Logan | Decision to approve sunset for each agent |
| 6. Artifact Cleanup | ⏳ Pending | Upon Order | Branches, scripts, workflows preserved until explicit deletion order |
| 7. Final LEVELSET-DELETE | ⏳ Pending | Upon Order | Final report for each deleted agent |

---

## Key Assumptions

1. **Persistent agents are NOT sunset** - PERSISTENT, PERMANENT, PUBLIC, ADMIN prefixed agents remain active indefinitely
2. **Artifacts preserved until order** - All branches, scripts, and workflows remain in git history until Logan explicitly orders deletion
3. **LEVELSET reports are permanent audit trail** - Sunset and deletion reports become immutable records
4. **No inter-agent visibility** - Agents coordinate only through LEVELSET reports and collision-risk documentation

---

## Next Actions

1. ✅ Create AGENT-REGISTRY.md (this file)
2. ⏳ Create SUNSET-PROCESS.md (formal sunset workflow)
3. ⏳ Create LEVELSET-SUNSET-sunset-agents.md (this agent's final report)
4. ⏳ Create LEVELSET-SUNSET-jfac-open-meetings.md (JFAC agent synthesis)
5. ⏳ Create LEVELSET-SUNSET-levelset-reports.md (LEVELSET reports task synthesis)
6. ⏳ Push all documentation to branch
7. ⏳ Await Logan's review and approval
8. ⏳ Execute deletion orders per Logan's authorization

---

Last Updated: 2026-03-15 by Sunset non-persistent agents agent
Branch: `claude/sunset-non-persistent-agents-4iLqH`
