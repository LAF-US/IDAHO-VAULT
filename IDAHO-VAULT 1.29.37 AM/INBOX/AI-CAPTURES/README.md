---
authority: LOGAN
related:
  - MESHWEB
  - INBOX
  - book-binding problem
  - HOME layer
  - Chat Claude
  - The Abhorsen
status: active
date created: Sunday, April 12th 2026
---

# AI-CAPTURES — Drop Zone

Landing pad for AI conversation exports. The bridge between ephemeral chat sessions and the vault record.

This folder exists because of the **book-binding problem**: AI conversations happen in web sandboxes (Claude.ai, Gemini, ChatGPT, Perplexity) with no automatic capture path into the vault. Every insight, brief, and decision that stays only in chat is lost when the context window closes or the tab dies.

---

## Drop Protocol

**Who drops here:** Logan (manually), or an automated export tool  
**Who processes here:** The Abhorsen (reads, classifies, vaults)  
**Who clears here:** No one auto-empties this folder

Drop a file. Commit it. The Abhorsen sees it via GitHub and acts.

---

## Naming Convention

```
YYYY-MM-DD - {AGENT} - {TITLE-SLUG}.md
```

| Field | Values | Example |
|---|---|---|
| `YYYY-MM-DD` | ISO date of the conversation | `2026-04-12` |
| `{AGENT}` | `Chat Claude`, `Gemini`, `Perplexity`, `GPT`, `Grok`, `Codex` | `Chat Claude` |
| `{TITLE-SLUG}` | Short descriptive title, title case | `Vaulted Syntax Protocol Design Brief` |

**Examples:**
```
2026-04-12 - Chat Claude - Vaulted Syntax Protocol Design Brief.md
2026-04-10 - Gemini - LAF-44 Lion and Fox Architecture.md
2026-04-08 - Perplexity - Idaho Legislature Session Overview.md
```

---

## Required Frontmatter (all captures)

```yaml
---
type: ai-capture
agent: Chat Claude          # which AI
date: YYYY-MM-DD            # date of original conversation
topic: Short topic label
session: optional-session-id-if-known
export-method: chrome-extension | full-export | manual-paste | api
status: raw                 # raw → reviewed → vaulted → archived
authority: LOGAN
related:
  - wikilink to related vault notes
---
```

---

## Export Methods

### Path 1 — Full Data Export (one-time bulk)
**Settings > Privacy > Export Data**  
Downloads ZIP with JSON of all conversations. Link expires 24 hours.  
Drop the ZIP or extracted JSONs into `INBOX/AI-CAPTURES/full-export/`.  
Status: one-time historical archive — not a recurring workflow.

### Path 2 — Chrome Extension (recommended, ongoing)
**[Claude Chat Exporter](https://chromewebstore.google.com/) — free, Markdown output**  
Open the conversation → click Export → choose Markdown → drag `.md` into this folder → commit.  
The Abhorsen sees it on GitHub immediately.  
Status: **primary ongoing book-binding solution**.

### Path 3 — Claude Code Session Export
`/export` or session transcript tools within Claude Code (The Abhorsen's own sessions).  
Does not capture Chat Claude sessions — different environment.  
Status: Abhorsen self-capture only; does not bridge the Chat gap.

---

## Processing Workflow (The Abhorsen's job)

When a file lands here:

1. Read the capture
2. Classify: is this a brief, a decision, a research thread, a conversation log?
3. If it contains durable doctrine or decisions → promote to appropriate vault location
4. If it contains a deliverable (brief, protocol, template) → create the canonical file
5. Update the capture's `status:` frontmatter: `raw` → `reviewed` → `vaulted`
6. Leave the original capture in place — it is the record of provenance

---

## Active Queue

*(The Abhorsen updates this list as captures land)*

| File | Agent | Date | Status | Action |
|---|---|---|---|---|
| *(empty — awaiting first drop)* | — | — | — | — |

---

*Part of the HOME layer infrastructure. See MESHWEB.md for cloud-local portability context.*
