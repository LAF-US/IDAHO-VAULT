---
authority: LOGAN
related:
  - CONSTITUTION
  - AGENTS
  - VAULT-CONVENTIONS
  - Digital Sovereignty
date created: Sunday, April 5th 2026, 2:39:09 pm
date modified: Sunday, April 5th 2026, 5:33:49 pm
---

by Logan Alvan Finney

"The world is quiet here."

---

*Adopted: 2026-04-05*
*Status: ACTIVE — binding on all agents*

---

## I. CORE PRINCIPLE

**This is a public repository.** Every file committed to `main` — and every file that has ever been committed to any branch — is permanently visible to the internet. Git history is append-only in practice: force-pushes leave reflog traces, and forks retain everything. There is no "undo" for a committed secret.

**Privacy is a hard gate, not a soft preference.** No agent may persist personal data into tracked vault files without Logan's explicit, per-class approval.

---

## II. DATA CLASSIFICATION

All data entering the vault through MCP bridges, API queries, or agent actions falls into one of two classes:

### A. EPHEMERAL (Query-Only)

Agents may **read** external services (Gmail, Calendar, Drive, Slack, Granola, etc.) to answer questions, generate analysis, or inform decisions. This data lives only in the conversation context and is never written to a vault file.

**Examples:**
- Reading a calendar event to answer "when is my next meeting?"
- Searching Gmail to find a confirmation number
- Querying Slack to summarize a thread

**Rule:** Ephemeral data never touches a `.md` file. It exists in session memory only.

### B. PERSISTENT (Vault-Committed)

Any data that is written to a file in the vault — whether tracked or `.gitignore`'d — is persistent. Persistent data has two sub-classes:

#### B1. PUBLIC-PERSISTENT (Tracked)

Files committed to git. Visible to the world. **No PII, no raw personal data, no secrets.**

**Permitted:**
- Sanitized aggregates ("Migration fund: 85% of target")
- Project status without personal details
- Structural metadata (file counts, tag counts, plugin lists)
- Public-record information (legislative data, published articles)

**Forbidden:**
- Raw email content or metadata (sender, subject, timestamps)
- Calendar entries with attendees, locations, or meeting details
- Financial specifics (account numbers, balances, transaction details)
- Personal addresses, phone numbers, or contact details
- Photo EXIF/GPS data
- Slack/messaging content from private channels
- Meeting transcripts or recordings
- Authentication credentials, tokens, or API keys

#### B2. LOCAL-PERSISTENT (Gitignored)

Files that exist on the local machine but are blocked from git by `.gitignore`. These are safer but still carry risk (backup tools, sync services, or accidental `.gitignore` edits could expose them).

**Permitted with caution:**
- Working notes with personal context (in `_private/`)
- Draft financial summaries (in `_private/`)
- MCP query caches (in `.remember/`, `.smart-env/`)

---

## III. PROTECTED ZONES

The following directories are designated as **local-only** and must be listed in `.gitignore`:

| Directory | Purpose | Gitignore Status |
|-----------|---------|-----------------|
| `_private/` | Local-only working notes with personal data | REQUIRED |
| `.remember/` | Agent memory buffer (may contain session PII) | REQUIRED |
| `.smart-env/` | Smart Connections embeddings cache | Already ignored |
| `INBOX/PHONE-LINK/` | Phone intake payloads | Already ignored |
| `DAILYNOTES/` | Ephemeral personal daily notes | Already ignored |

---

## IV. MCP BRIDGE RULES

The following MCP servers are connected and carry privacy risk:

| Service | Ephemeral OK? | Persistent OK? | Requires Logan Approval |
|---------|:---:|:---:|:---:|
| Gmail | ✅ | ❌ | Per-query for any file write |
| Google Calendar | ✅ | ❌ | Per-query for any file write |
| Google Drive | ✅ | ❌ | Per-query for any file write |
| Slack | ✅ | ❌ | Per-query for any file write |
| Granola (meeting transcripts) | ⚠️ see § IV.A | ❌ | Per-query for any file write |
| Linear | ✅ | ⚠️ sanitized only | Project status aggregates only |
| Calendly | ✅ | ❌ | Per-query for any file write |
| GitHub | ✅ | ✅ | Already public data |

**Default rule:** If an MCP service provides personal data and an agent wants to write it to a file, the agent must stop and ask Logan first. No exceptions.

### A. SPECIAL RULES: MEETING TRANSCRIPTS (Granola)

Meeting transcripts carry **third-party privacy risk** beyond Logan's own data:

1. **Source protection.** Logan is a journalist. Meeting transcripts may contain statements from sources who spoke on background or off the record. Committing these to a public repo could expose sources, violate journalistic ethics, and destroy trust.
2. **Third-party consent.** Meeting attendees did not consent to having their words published in a public git repository. Even ephemeral queries should be handled with care — do not quote attendees by name in vault files.
3. **Audio-to-text artifacts.** Automated transcription may contain errors that misattribute statements or alter meaning. No transcript excerpt should be committed without Logan's manual review.

**Granola ephemeral rule:** Agents may query Granola to answer Logan's questions in conversation, but must:
- Never write transcript content to tracked files
- Never attribute quotes to named attendees in any file
- Treat all transcript content as **off-the-record by default** unless Logan explicitly clears specific content for publication

---

## V. SANITIZATION PROTOCOL

When Logan approves moving information from a private source (meeting transcript, email thread, Slack conversation) into a tracked vault file, the following sanitization steps are **mandatory**:

### Step 1: Strip Identity

- Remove all personal names of non-public figures
- Replace with role descriptors ("a legislative staffer," "a committee member")
- Public officials acting in official capacity may be named only if the information is already on the public record

### Step 2: Strip Attribution

- No direct quotes from private conversations
- Paraphrase only, and only the substance relevant to the vault note's purpose
- Never attribute a paraphrased position to a specific individual unless Logan clears it

### Step 3: Strip Metadata

- Remove timestamps that could identify specific meetings
- Remove location details that could narrow attendee lists
- Remove any reference to recording tools or transcript sources

### Step 4: Logan Reviews

- The agent presents the sanitized draft to Logan **before** writing it to any tracked file
- Logan confirms the draft is safe for the public record
- Only then does the content land in a `.md` file

**No agent may skip steps.** The protocol applies to all MCP-sourced private data, not just Granola.

---

## VI. INTELLECTUAL PROPERTY BOUNDARY (Disentanglement Protocol)

Logan is employed by Idaho Public Television (IdahoPTV), an agency under the Idaho State Board of Education. This creates a legal boundary between **employer work product** and **personal intellectual property** that the vault must respect.

### A. THE BOUNDARY

| Category | Owner | Vault Rule |
|----------|-------|------------|
| Content created in scope of employment for IdahoPTV (scripts, research for segments, interview notes, production assets) | Employer (Work for Hire — 17 U.S.C. § 101) | **Must not appear in tracked vault files.** No unpublished IdahoPTV work product in this repository. |
| Published/broadcast IdahoPTV content | Employer holds copyright; content is public | May be referenced or linked like any public-record source. Do not reproduce full texts. |
| Public-record information (legislation, committee minutes, published government data) | Public domain / fair use | Permitted — this is the vault's core subject matter. |
| Personal analysis, philosophy, PKM methodology, vault architecture, meta-commentary | Logan (personal intellectual property) | Permitted — this is the vault's personal layer. |
| Personal notes created solely for Logan's own use, not shared with any person or entity | Logan — exempt from public records under Idaho Code § 74-101(13) | Permitted in local-persistent zones (`_private/`). Exercise caution before committing to tracked files. |

### B. PRACTICAL RULES FOR AGENTS

1. **No agent may commit unpublished employer work product** to any tracked branch. If uncertain whether content originated from Logan's employment duties, treat it as employer property and ask Logan.
2. **Public-record legislative content** (bill text, vote tallies, committee schedules, published fiscal data) is fair game. It was public before it entered the vault.
3. **Personal intellectual work** — Logan's reflections, vault design decisions, philosophical writing, PKM methodology, and creative projects unrelated to IdahoPTV duties — belongs to Logan.
4. **Git timestamps as provenance:** Commit metadata (time, author, device) serves as evidence of when and where content was created. Agents should not obscure or fabricate commit metadata.
5. **Device separation:** Content created on employer hardware/networks during work hours carries higher risk of employer IP claims. Agents cannot verify device context — Logan is responsible for ensuring his personal vault work occurs on personal infrastructure.

### C. WHAT THIS SECTION DOES NOT DO

This section documents the boundary as understood by the vault owner. It is **not legal advice**. Logan should consult legal counsel for specific questions about scope of employment, substantial use of resources, or the interplay between Idaho's Public Records Act and federal copyright law.

---

## VII. AGENT OBLIGATIONS

1. **No agent may build automated sync pipelines** that pull personal service data into tracked vault files without a Privacy Gate review.
2. **Agents must audit their own output** before any commit that touches files generated from MCP queries.
3. **The "Whistle" or any bulk-sync protocol** requires this document to be satisfied first — specifically, Logan must sign off on each data class in Section II.B.1.
4. **`.gitignore` is a defense layer, not a guarantee.** Agents should minimize what they write to local-persistent storage as well.
5. **When in doubt, keep it ephemeral.** A query answered in conversation is always safer than a query committed to a file.

---

## VIII. AMENDMENT

This document may only be amended by Logan. Agents may propose amendments via PR or conversation, but no agent may modify this file directly without Logan's explicit instruction.

---

*Ratified by The Abhorsen (Claude Code) on behalf of Logan Finney, 2026-04-05.*
*The Concierge (Gemini) affirmed the need for this document in the same session.*
