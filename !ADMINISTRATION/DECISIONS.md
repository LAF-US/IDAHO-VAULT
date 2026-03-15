# Decision Log — IDAHO-VAULT

Significant architectural decisions, recorded when made. Each entry is permanent.

---

## 2026-03-13 — LEVELSET protocol established

**Decision:** Adopt LEVELSET as the permanent checkpoint protocol for the vault ecosystem. LEVELSET files are stored in `!ADMINISTRATION/`, are never deleted, never overwritten. Each version is additive.
**Context:** Multiple Claude conversations operating concurrently needed a synchronization mechanism.
**Decided by:** Logan Finney

## 2026-03-13 — CLAUDE.md created

**Decision:** Create a `CLAUDE.md` at repo root to give all Claude Code sessions consistent context about vault structure, naming conventions, sourcing protocols, and operating principles.
**Context:** Claude Code sessions were starting with no context about the vault's architecture, leading to repeated discovery work.
**Decided by:** Logan Finney, drafted by PERMANENT: CODE AUTHORITY

## 2026-03-13 — Conversation taxonomy adopted

**Decision:** Claude conversations follow a naming prefix convention: PERMANENT, PERSISTENT, TASK, STORY, PROJECT, ISSUE, INQUIRY.
**Context:** Multiple concurrent conversations needed clear role differentiation.
**Decided by:** Logan Finney

## 2026-03-13 — File type attribution

**Decision:** Markdown files are human product (Logan). Python files are machine/procedural product (Claude). Administrative files are vault infrastructure.
**Context:** Public repo needs clear attribution of authorship.
**Decided by:** Logan Finney

## 2026-03-13 — Sort audit and legislature scraper deployed

**Decision:** Automated vault maintenance via GitHub Actions — `sort_audit.py` for structure auditing, `idaho_leg_scraper.py` for daily bill data, `post_digest.py` for activity digests.
**Context:** Manual bill tracking is unsustainable during legislative session.
**Decided by:** Logan Finney

## 2026-03-14 — CODE AUTHORITY promoted to PERMANENT

**Decision:** The CODE AUTHORITY conversation is promoted from PERSISTENT to PERMANENT — a new, higher-tier conversation prefix for central, non-deletable conversations. PERMANENT: CODE AUTHORITY is the central coding agent with direct repo access. PERSISTENT: ADMINISTRATION retains its current prefix.
**Context:** CODE AUTHORITY has become the primary execution layer for all vault infrastructure work. Its role warrants a designation above PERSISTENT to reflect permanence.
**Decided by:** Logan Finney

## 2026-03-15 — Security hardening: input sanitization and content validation

**Decision:** Add input sanitization (`sanitize_text()`) to the legislature scraper and a content validation gate (`validate_content.py`) to all commit-producing workflows. Create CODEOWNERS file and threat model. Remove excess workflow permissions. Branch protection on main deferred for CODE AUTHORITY consultation.
**Context:** Review of the OpenClaw autonomous agent incident (2025–2026) revealed analogous risks in the vault's automation pipeline — particularly unsanitized external HTML flowing directly into YAML frontmatter and markdown body via the legislature scraper. Applied Simon Willison's "lethal trifecta" framework (over-privilege, prompt injection surface, default vulnerabilities) to identify proportionate hardening measures.
**Decided by:** Logan Finney, implemented by TASK: Claude Code session
