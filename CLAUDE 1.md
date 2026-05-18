---
authority: LOGAN
related:
- '2026-03-15'
- LEVELSET
- PRIVATE
- PUBLIC
- coordination
- deliverables
- format
---

# IDAHO-VAULT — Shared Constitutional Framework

This file governs all Claude and Claude Code conversations operating on this repository. Every conversation — regardless of tier, type, or model — must read and comply with this document.

---

## Conversation Visibility: PUBLIC / PRIVATE

Every conversation MUST be classified as either **PUBLIC** or **PRIVATE**. This classification is:

- **Required** — no conversation may operate without declaring visibility.
- **Immutable** — a conversation's visibility cannot change after it is set. A PUBLIC conversation was already shared and cannot become PRIVATE. A PRIVATE conversation may have handled sensitive material and must not become PUBLIC.
- **Fail-closed** — any conversation that has not declared visibility is treated as PRIVATE.

### PUBLIC

A PUBLIC conversation's session link may be shared. Anyone with the link (or repo access) can view the session.

**Constraints:**

- All material handled must be **on the record**.
- No journalistic sources, interview notes, or sensitive reporting materials.
- No off-the-record, on-background, or embargoed content.
- LEVELSET reports produced by PUBLIC conversations are themselves public artifacts and must not contain redacted source identities (because there should be none to redact).

### PRIVATE

A PRIVATE conversation's session link is not shared.

**Permissions:**

- May handle sensitive sourcing, off-record material, draft reporting, and embargoed content.
- LEVELSET reports from PRIVATE conversations may redact source identities and sensitive details.
- PRIVATE does not mean unaccountable — LEVELSET reports are still required and must document what categories of sensitive material were handled, even if specifics are redacted.

### Declaration

Visibility is declared in the LEVELSET report frontmatter:

```yaml
visibility: public
```

or

```yaml
visibility: private
```

Lowercase. No other values are valid.

---

## Conversation Tiers

| Tier | Access | Description |
|------|--------|-------------|
| 1 | Direct repo write via `git commit` / `git push` | Implementation conversations — scraper work, bulk vault operations, direct code |
| 2 | Constitutional layer | Administration — governance documents, shared state files, this constitution |
| 3 | Governance / architecture / synthesis | Planning, LEVELSET synthesis, cross-conversation coordination |

---

## Conversation Types

Conversations are named with a type prefix, for example but not limited to:

- **PERSISTENT:** Long-running conversations that maintain state across sessions (e.g., PERSISTENT: ADMINISTRATION, PERSISTENT: CODE AUTHORITY)
- **STORY:** Topic-focused conversations for bulk vault work (e.g., STORY: JFAC Open Meetings)
- **TASK:** Single-purpose conversations for specific deliverables (e.g., TASK: LEVELSET reports)

---

## LEVELSET Reports

Every conversation that commits to the repository MUST produce a LEVELSET report at termination (or at significant checkpoints). Reports are stored in `!ADMINISTRATION/`.

### Required Frontmatter

```yaml
type: levelset-report
levelset-version: <version>
conversation: <conversation name>
tier: <1|2|3>
visibility: <public|private>
date: <YYYY-MM-DD>
branch: <branch name>
status: <active|terminating|terminated-clean>
```

The `visibility` field is **mandatory**. Omitting it defaults the conversation to PRIVATE treatment, but the omission itself is a protocol violation that should be flagged in the next LEVELSET report.

### Required Sections

1. **Identity** — conversation name, tier, role, status
2. **What was done** — files committed, decisions made
3. **What is unresolved** — incomplete work, flags, blockers
4. **Conversation awareness** — known sibling conversations and visibility into their state
5. **Next steps** — what should happen after this report
6. **What Logan needs to know** — critical information for the human operator
7. **What Claude needs from Logan** — outstanding questions or decisions needed

---

## Collision Protocol

Before writing to any shared path, check `!ADMINISTRATION/` for recent LEVELSET reports that may document ownership or collision risks for that path.

Known shared paths requiring coordination:

- `GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/` — naming format: `(YYYY) Type Number.md`
- `GOVERNMENTS/IDAHO - LEGISLATIVE/SESSIONS/` — session note creation
- `.github/workflows/` — check for schedule trigger conflicts
- `.gitignore` — additions must be additive
- `!ADMINISTRATION/` — LEVELSET reports are append-only; never overwrite another conversation's report

---

## Amendments

This constitution may be amended by Tier 2 (ADMINISTRATION) conversations or by Logan directly. Amendments must be committed with a clear commit message referencing the change. Prior versions are preserved in git history.

---

*Created 2026-03-15 by PUBLIC CONVERSATION SETUP conversation. This was the first shared constitution for the vault.*

Updated Wed, March 18. Logan was here.
