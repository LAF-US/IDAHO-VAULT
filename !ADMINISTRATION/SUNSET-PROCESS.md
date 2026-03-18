---
type: sunset-process
version: 1.0
date: 2026-03-15
---

# Sunset Process — Non-Persistent Agent Lifecycle

Formal workflow for identifying, flagging, synthesizing, and deleting ephemeral Claude Code agents in IDAHO-VAULT.

**Effective Date:** 2026-03-15

---

## Overview

This document defines the structured process for managing the lifecycle of non-persistent agents (Story-type and Task-type conversations) in IDAHO-VAULT. Persistent agents (marked PERSISTENT, PERMANENT, PUBLIC, ADMIN) are excluded from this process.

**Goals:**
- Maintain audit trail of all agent work via LEVELSET reports
- Preserve git history while enabling agent cleanup
- Require explicit authorization from Logan before deletion
- Minimize collision risks and ensure clear handoffs

---

## Sunset Phases

### Phase 1: Flagging
**Goal:** Identify and mark non-persistent agents for sunset

**Steps:**
1. Agent completes its assigned work (deliverables complete, no pending tasks)
2. Agent creates final LEVELSET-SUNSET-<agent-name>.md synthesis report (see template below)
3. Agent updates AGENT-REGISTRY.md to mark status as "FLAGGED_FOR_SUNSET"
4. Agent commits with session URL and clear message
5. Agent pushes to its branch
6. Agent terminates conversation

**Responsible:** Individual agent

**Output:**
- LEVELSET-SUNSET-<agent-name>.md synthesis document
- Updated AGENT-REGISTRY.md entry
- Commit in git history with session tracking

---

### Phase 2: Synthesis
**Goal:** Create comprehensive final documentation for flagged agents

**Steps:**
1. Logan reviews LEVELSET-SUNSET-*.md synthesis reports
2. Logan verifies:
   - All artifacts are documented
   - Git commits are clear and trackable
   - No unresolved work remains
   - Collision risks are documented
3. Logan approves agent for deletion or requests clarification

**Responsible:** Logan (human operator)

**Input:**
- LEVELSET-SUNSET-<agent-name>.md reports
- AGENT-REGISTRY.md
- Git history and branch state

**Output:**
- Approval decision for each agent
- Deletion checklist (below)

---

### Phase 3: Deletion Authorization
**Goal:** Obtain explicit deletion order from Logan

**Steps:**
1. Logan reviews all flagged agents in AGENT-REGISTRY.md
2. Logan issues deletion order in format:
   ```
   DELETE: <Agent Name>
   Reason: [brief rationale]
   Approved: Logan
   Date: YYYY-MM-DD
   ```
3. Logan provides list of agents to delete with authorization
4. Deletion executor updates AGENT-REGISTRY.md to "DELETION_PENDING"

**Responsible:** Logan

**Output:**
- Explicit deletion orders for each agent
- Updated AGENT-REGISTRY.md with DELETION_PENDING status

---

### Phase 4: Artifact Cleanup
**Goal:** Remove agent artifacts per deletion order while preserving git history

**Deletion Checklist (per agent):**

- [ ] Delete remote branch: `git push origin --delete <branch-name>`
- [ ] Delete local branch: `git branch -d <branch-name>`
- [ ] Delete associated GitHub workflows (`.github/workflows/`) if created by agent
- [ ] Delete associated scripts (`.github/scripts/`) if created by agent only
- [ ] Remove agent entries from configuration files (`.gitignore`, etc.) if safe
- [ ] Update AGENT-REGISTRY.md to "DELETION_PENDING_ARTIFACTS_REMOVED"
- [ ] Commit deletion cleanup
- [ ] Create LEVELSET-DELETE-<agent>.md final report (see template below)
- [ ] Update AGENT-REGISTRY.md to "DELETED"
- [ ] Push final commit

**Responsible:** Deletion executor (typically same as current operator)

**Output:**
- Removed branches and artifacts
- LEVELSET-DELETE-<agent>.md final report
- Clean AGENT-REGISTRY.md

---

### Phase 5: Archive
**Goal:** Create permanent audit record of deleted agent

**Steps:**
1. Create LEVELSET-DELETE-<agent>.md report (template provided below)
2. Document:
   - Agent identity and dates of operation
   - All commits/branches created
   - Reason for deletion
   - Date deleted
   - Logan's authorization reference
3. Commit LEVELSET-DELETE report
4. Push to master branch
5. Mark AGENT-REGISTRY.md as "DELETED"

**Responsible:** Deletion executor

**Output:**
- LEVELSET-DELETE-<agent>.md report in git history
- AGENT-REGISTRY.md marked DELETED
- Immutable audit trail

---

## Document Templates

### LEVELSET-SUNSET-<agent-name>.md Template

```markdown
---
type: levelset-report
levelset-version: v3.2.6-sunset
conversation: <Agent Name>
tier: <1|2|3>
date: YYYY-MM-DD
branch: claude/<agent-purpose>-<session-id>
status: flagged-for-sunset
---

# LEVELSET Sunset Report — <Agent Name> — YYYY-MM-DD

## 1. IDENTIFY MYSELF

- **Conversation name:** <Agent name>
- **Tier:** <1|2|3>
- **Type:** Story/Task (non-persistent ephemeral)
- **Status:** Flagged for sunset
- **Work completed:** [Summary of deliverables]
- **Last known repo state:** [Clean/Commits pending/Branches unmerged]

## 2. WHAT I'VE DONE

| File | Type | Commit | Action |
|------|------|--------|--------|
| [list of files created/modified] | [type] | [commit hash] | [description] |

## 3. WHAT'S UNRESOLVED

- [List any outstanding issues or collision risks]

## 4. CONVERSATION AWARENESS

[List other known agents and visibility into their work]

## 5. SUNSET RECOMMENDATION

This agent is ready for sunset. All work is complete and committed.

## 6. WHAT LOGAN NEEDS TO KNOW

[Any critical information for deletion decision]

## 7. WHAT CLAUDE NEEDS FROM LOGAN

Authorization to delete this agent's artifacts upon completion of other pending synthesis tasks.
```

### LEVELSET-DELETE-<agent-name>.md Template

```markdown
---
type: levelset-report
levelset-version: v3.2.6-delete
conversation: <Agent Name>
tier: <1|2|3>
date: YYYY-MM-DD
branch: <deleted>
status: deleted
---

# LEVELSET Deletion Report — <Agent Name> — YYYY-MM-DD

## 1. AGENT IDENTITY

- **Name:** <Agent Name>
- **Tier:** <1|2|3>
- **Type:** Story/Task (non-persistent ephemeral)
- **Branches:** <branch names deleted>
- **Deleted:** YYYY-MM-DD

## 2. DELETED ARTIFACTS

| Item | Type | Reason |
|------|------|--------|
| [files/branches deleted] | [type] | [reason] |

## 3. DELETION AUTHORIZATION

- **Authorized by:** Logan
- **Date authorized:** YYYY-MM-DD
- **Reason:** [Brief reason for deletion]

## 4. GIT HISTORY PRESERVATION

All work is permanently preserved in git history:
- Commits remain in commit log
- LEVELSET-SUNSET-<agent>.md remains as immutable record
- This LEVELSET-DELETE report serves as deletion audit trail

## 5. WHAT LOGAN KNOWS

Agent deleted per authorization. All artifacts removed. Git history preserved.
```

---

## Authority & Authorization

**Logan is the sole agent authorized to issue deletion orders.**

All deletion orders must be explicit and documented in AGENT-REGISTRY.md and LEVELSET-DELETE reports.

---

## Preservation & Safety

1. **Git history is immutable** - All agent commits remain in git log forever
2. **Branches are archived** - Deleted branches can be recovered from git reflog if needed
3. **LEVELSET reports are permanent** - SUNSET and DELETE reports become permanent audit trail
4. **No data loss** - Deletion only removes live artifacts; all content preserved in history

---

## Constraints & Assumptions

1. Only non-persistent agents (Story/Task type) are sunset via this process
2. Persistent agents remain active indefinitely
3. Artifacts are preserved in git history even after deletion
4. Inter-agent collision risks are documented in LEVELSET reports
5. All deletions require explicit Logan authorization
6. Deletion executor must not exceed Logan's authorization scope

---

## Process Status

See AGENT-REGISTRY.md for current status of all agents and sunset workflow phases.

---

**Document Version:** 1.0
**Created:** 2026-03-15
**Last Updated:** 2026-03-15
**Branch:** `claude/sunset-non-persistent-agents-4iLqH`
