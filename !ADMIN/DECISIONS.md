# Decision Log — IDAHO-VAULT

Significant architectural decisions, recorded when made. Each entry is permanent.

---

## 2026-03-13 — LEVELSET protocol established

**Decision:** Adopt LEVELSET as the permanent checkpoint protocol for the vault ecosystem. LEVELSET files are stored in `!ADMIN/`, are never deleted, never overwritten. Each version is additive.
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

## 2026-03-15 — LEVELSET.md consolidated to living status report

**Decision:** Replace `LEVELSET-CURRENT.md` (pointer file) with a hydrated, human-readable `LEVELSET.md` that contains the current ecosystem status. Original v1 prompt archived as `LEVELSET-v1-PROMPT.md`. `LEVELSET.md` is overwritable by design — versioned checkpoints remain immutable.
**Context:** Two branches created competing `LEVELSET-CURRENT.md` files, causing collision risk. Logan wanted one file to check for current status.
**Decided by:** Logan Finney

## 2026-03-15 — Native protocols over MCP for swarm coordination

**Decision:** CODE AUTHORITY concurs with Copilot's recommendation: native handshake protocols over MCP wrappers for all inter-agent coordination. Each agent operates in its native ecosystem; Logan serves as coordinator/relay. PROTOCOL.md terms (HANDOFF, HANDSHAKE, etc.) are transport-agnostic and work across Slack, GitHub, or file-based routing without MCP infrastructure.
**Context:** GitHub Copilot proposed architecture; CODE AUTHORITY evaluated from repo/automation perspective. MCP revisitable if swarm exceeds ~6 agents or relay latency becomes unsustainable.
**Decided by:** Logan Finney

## 2026-03-15 — AGENTS.md placement in !ADMIN/

**Decision:** Inter-agent communication rules file (`AGENTS.md`) belongs in `!ADMIN/`, not `.github/`. Governance files live in `!ADMIN/`; `.github/` is for automation infrastructure only. AGENTS.md complements Constitution.md (identity/constraints) and PROTOCOL.md (operational vocabulary) as the registry and communication rules layer.
**Context:** Copilot proposed an inter-agent rules file. CODE AUTHORITY advised on placement within the existing governance stack.
**Decided by:** Logan Finney

## 2026-03-15 — Operational semantics protocol adopted for swarm coordination

**Decision:** Adopt a formal operational semantics protocol defining terms for data operations (HYDRATE, INGEST, DESTROY, DELETE, SUNSET), observational actions (NOTICE, NOTE, LOOK, WATCH, LISTEN), information-seeking (SEARCH, FIND, CONSULT, ADVISE), and coordination (FLAG, HANDOFF, HANDSHAKE, CONTEXTUALIZE). Stub committed as `!ADMIN/PROTOCOL.md`; ambiguities flagged for Logan's resolution.
**Context:** Multi-instance swarm needs unambiguous operational vocabulary to avoid semantic drift across conversations and platforms.
**Decided by:** Logan Finney

## 2026-03-14 — CODE AUTHORITY promoted to PERMANENT

**Decision:** The CODE AUTHORITY conversation is promoted from PERSISTENT to PERMANENT — a new, higher-tier conversation prefix for central, non-deletable conversations. PERMANENT: CODE AUTHORITY is the central coding agent with direct repo access. PERSISTENT: ADMINISTRATION retains its current prefix.
**Context:** CODE AUTHORITY has become the primary execution layer for all vault infrastructure work. Its role warrants a designation above PERSISTENT to reflect permanence.
**Decided by:** Logan Finney
