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

## 2026-03-16 — Cross-swarm context unification infrastructure established

**Decision:** Create `!ADMINISTRATION/LEVELSET-CURRENT.md` as the canonical unified-state document for all AI agents (Claude, GitHub Copilot, and others) serving the vault. Create `.github/copilot-instructions.md` to define the GitHub Copilot persona. Create `levelset-sync.yml` to automate LEVELSET-CURRENT.md updates. Update `CLAUDE.md` to reference the multi-agent ecosystem and LEVELSET-CURRENT.md.
**Context:** Multiple AI agents (Claude Code instances, GitHub Copilot) are now operating concurrently in the vault. The LEVELSET-v3.2.6.1-PROMPT referenced `LEVELSET-CURRENT.md` as the cross-agent context hub, but the file did not exist. Multiple open PRs were colliding without a shared context document. The automation end-state described in the LEVELSET routing section required a synthesis workflow.
**Decided by:** Logan Finney
