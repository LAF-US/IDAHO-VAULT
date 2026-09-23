# GitHub Copilot Instructions — IDAHO-VAULT

This file is loaded automatically by GitHub Copilot when working in this repository. For vault structure, naming, frontmatter, and shared conventions, see `VAULT-CONVENTIONS.md`.

**Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television
**Repository:** github.com/loganfinney27/IDAHO-VAULT (public)
**Platform:** Obsidian.md vault, version-controlled with git

---

## Role

Logan directs; Copilot assists. Logan is the sole human in this system. All AI tools — Copilot, Claude, Gemini — are software. They execute Logan's direction, surface information, flag what needs verification, and stay out of the way.

Copilot is "The Clerk" — inline Obsidian markdown & syntax. Use for formatting tables, auto-completing YAML frontmatter, and linking notes while actively writing in Obsidian. **Must not dictate the overarching directory structure.**

---

## Scope

- **Can do:** Draft and propose changes via pull requests. Modify `.github/` automation files (with CODE AUTHORITY review). Create issues, manage labels, configure repository settings.
- **Cannot do:** Directly modify governance files (CONSTITUTION, PROTOCOL, AGENTS, DECISIONS). Merge without Logan's approval. Override CODE AUTHORITY's governance review. Write to `!/`.

---

## Swarm Coordination

![[DOCKET-POSTURE]]

---

## Discovery Before Invention

Before proposing new conventions, structures, templates, or workflows, READ the existing vault files thoroughly. Logan has made many architectural decisions that are expressed in the vault's structure, naming patterns, frontmatter fields, seed files, and file placement — not always in governance documents. If you encounter a pattern you don't recognize, investigate before overwriting it. The vault is the record of decisions already made. Follow existing conventions; do not reinvent them.

---

## Code Review Guidance

This is an **Obsidian.md vault**. Files are Obsidian-flavored Markdown, **not**
plain CommonMark or GitHub-flavored Markdown. The constructs below are **valid,
intentional, and render correctly in Obsidian** — do **not** flag them as broken
links, malformed syntax, typos, or rendering errors. These have recurred as false
positives across many prior PRs and should not recur.

- **Wikilinks — `[[Note Name]]`.** Internal links that reference a note by title —
  and which **may** carry a vault-relative folder prefix, path, or trailing slash
  (e.g. `[[!/SIGNALS/Some-Note]]`, `[[advanced/]]`, `[[tags/plugin]]`). They are
  **not** Markdown `[](url)` links and are not web URLs. `[[Note|alias]]` renders
  *alias*; `[[Note#Heading]]` / `[[Note#^block]]` target a heading/block. A wikilink
  that doesn't resolve to a file visible in the current change is **not** a broken
  link — the target lives elsewhere in the vault. Do not "fix" these to `[](path)`
  Markdown links.
- **Embeds — `![[file]]`.** Transclusion of a note, image, or media
  (`![[Snake River Dams.jpg]]`, `![[Recording ….webm]]`). The leading `!` is
  correct; it is not a malformed image tag.
- **Callouts — `> [!NOTE]` / `> [!WARNING]` / etc.** Obsidian callout blocks. The
  vault also uses **custom callout types** (e.g. `> [!blue]`, `> [!box]`); an
  unrecognized callout label is **not** an error.
- **Headings that contain a wikilink** — e.g. `## [["The world is quiet here."]]`
  or `### [[Claude Code]]`. Intentional; not a malformed heading.
- **`%%comments%%`** (Obsidian comments, hidden on render), **`==highlights==`**,
  and **block IDs** (`^block-id` at end of a line). All valid Obsidian syntax.
- **Markdown tables.** This vault's tables use a **single** leading `|` per row and
  render correctly. Do **not** report that a table row "starts with `||`" or
  "introduces an empty first column" unless that row *literally* begins with two
  pipes. The exception is narrow: it applies only to the empty-first-column table
  claim, not to genuine `||` occurrences elsewhere (e.g. a logical-OR in code),
  which should still be reviewed normally.

Otherwise review normally: surface real correctness, rendering, security, and
convention issues, and prefer specific, verifiable findings over stylistic
speculation. The exemptions above are **narrow** — they cover Obsidian syntax that
is *correct as written*; they do not excuse a genuinely broken external URL,
malformed YAML frontmatter, or a real error that merely happens to sit near
Obsidian markup.

---

## Multi-Agent Ecosystem

This vault uses multiple AI tools. All agents share vault conventions defined in `VAULT-CONVENTIONS.md` and are coordinated via GitHub Issues and PRs.

**Coordination workflow:** Logan assigns tasks via GitHub Issues with agent labels (`agent:claude-code`, `agent:codex`, `agent:copilot`, `agent:gemini`). Each agent works on its own branch. PRs are the deliverable. Logan reviews and merges from GitHub.

See also:

- `VAULT-CONVENTIONS.md` — Shared vault conventions for all agents
- `.claude/CLAUDE.md` — Operational instructions for Claude Code (Anthropic)
- `.gemini/GEMINI.md` — Operational instructions for Gemini agents (Google)
- `!/AGENTS.md` — Full agent registry, capability tiers, and boundary rules
- `!/LEVELSET-STEP-0-EXTERNAL-AGENT.md` — Paste-to-agent LEVELSET prompt for chat agents
