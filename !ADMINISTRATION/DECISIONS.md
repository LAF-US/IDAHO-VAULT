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

## 2026-03-16 — Multi-agent instruction files created

**Decision:** Create instruction files for all active AI agents so each has consistent vault context: `CLAUDE.md` (already existed), `GEMINI.md` (new), and `.github/copilot-instructions.md` (new).
**Context:** GitHub Copilot and Gemini advisory agents were operating without vault conventions. Consolidating instructions across all agents (Claude, Copilot, Gemini) ensures consistent behavior — same naming rules, frontmatter standards, sourcing protocols, and git practices.
**Decided by:** Logan Finney

## 2026-03-22 — STEP-0 LEVELSET prompt for external agents

**Decision:** Create `!/!/LEVELSET-STEP-0-EXTERNAL-AGENT.md` — a paste-to-agent orientation prompt for chat-based agents (Claude.ai, Gemini, Grok, etc.) that cannot access the repository directly. When Logan starts a new external agent session, he pastes this prompt, and the agent responds with a 6-part LEVELSET report: who they are, what they know, what they've done, what is unresolved, what they need, and collision risks.
**Context:** External agents operating via chat have no vault context unless Logan provides it. A standardized STEP-0 prompt ensures consistent orientation across all chat-based agents, reducing repeated discovery work and preventing agents from inventing governance structures or claiming capabilities they don't have.
**Decided by:** Logan Finney
