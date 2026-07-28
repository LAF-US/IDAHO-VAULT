---
authority: LOGAN
related:
- '2026-03-15'
- API
- CDX
- CLAUDE
- CONSTITUTION
- DECISIONS
- GitHub
- Idaho
- Idaho Legislature
- Internet
- LEVELSET
- LOW
- Logan's
- Obsidian
- OpenClaw
- agent
- chain
- syntax
- website
---

# Threat Model — IDAHO-VAULT

Established 2026-03-15 following review of OpenClaw autonomous agent incident. This document describes the vault's attack surfaces, trust boundaries, and mitigations.

---

## What This Vault Is (and Is Not)

IDAHO-VAULT is a public Obsidian journalism research vault with GitHub Actions automation and a tiered Claude conversation structure. It is **not** a running service, does not expose endpoints, does not accept inbound messages, and does not run persistent autonomous agents. The "swarm" is a set of Claude conversation sessions — not continuously running agents.

The vault is **public by design** (journalism transparency). Confidentiality is handled by **exclusion**: off-the-record material never enters the repository.

---

## Trust Boundaries

### 1. Legislature.idaho.gov → Scraper → Vault

**Risk:** HIGH — the only active external-to-vault data pipeline.

The `idaho_leg_scraper.py` fetches HTML from the Idaho Legislature website daily and writes parsed content directly into YAML frontmatter and markdown body of bill/member files.

**Attack vector:** A compromised or injected legislature page could write arbitrary content into the vault — including YAML injection in frontmatter, wikilink manipulation, or embedded executable patterns.

**Mitigations:**
- `sanitize_text()` function strips HTML tags, control characters, wikilink syntax, and escapes YAML-special characters in all scraped content before it enters markdown
- `validate_content.py` runs as a CI gate before every commit — checks YAML parsing, dangerous patterns, file sizes, sponsor name formats, and directory boundaries
- Content validation halts the workflow on failure (no commit occurs)

### 2. Wayback CDX API → Audit Scripts → Vault

**Risk:** LOW — writes to `!/` audit reports only, not vault content files.

The `wayback_audit.py` and `wayback_preserve.py` scripts query the Internet Archive's CDX API and write results to admin reports or submit URLs for preservation.

**Mitigations:**
- Output restricted to `!/` directory
- `validate_content.py` gate runs before commit
- Wayback preserve is outbound-only (submits URLs, does not ingest content)

### 3. Claude Sessions → Repository

**Risk:** MEDIUM — Claude sessions have write access to the repository through git operations.

**Attack vector:** If malicious content were committed to governance files (CLAUDE.md, `!/CONSTITUTION.md`), it would persist across all future sessions. Scraped bill files read by future Claude sessions could contain injected instructions.

**Mitigations:**
- CODEOWNERS file requires Logan's review for changes to CLAUDE.md, `!/`, and `.github/` (requires branch protection for enforcement)
- LEVELSET protocol provides auditable checkpoints
- Conversation tier system restricts which sessions have commit access (procedural, not technical)
- Branch protection (pending decision) would prevent direct pushes to main

---

## Explicitly Out of Scope

- **Server exposure:** No running services, no endpoints, no inbound message handling
- **Secrets management:** Vault is public by design; `.env` with `VAULT_TOKEN` is in `.gitignore` and local-only
- **Network isolation for Claude sessions:** Sessions run in sandboxed environments
- **Supply chain attacks via dependencies:** The scraper uses `requests` and `beautifulsoup4` only, pinned in `requirements-scraper.txt`

---

## Open Decisions

- **Branch protection on main:** Deferred for CODE AUTHORITY consultation. Options: bypass for automation, PRs for everything, or skip entirely. See `DECISIONS.md` for tracking.
