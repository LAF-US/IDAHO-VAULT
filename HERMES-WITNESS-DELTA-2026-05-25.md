---
title: "HERMES WITNESS DELTA — 2026-05-25"
subtitle: "Gap Between Ideal and Actual: Reflective Synthesis"
type: witness-report
companion-to: HERMES-WITNESS-REPORT-2026-05-25
local-survey: HERMES-WITNESS-COMPANION-2026-05-25
source: reflective-synthesis-claude-code-session-2026-05-25
tags:
- hermes-agent
- nous-research
- witness
- delta
- synthesis
- reflection
created: 2026-05-25
author: "Claude (Claude Code — session 2026-05-25, not Logan)"
authority: LOGAN
related:
  - HERMES-WITNESS-REPORT-2026-05-25
  - HERMES-WITNESS-COMPANION-2026-05-25
  - OPENCLAW-WITNESS-REPORT-2026-05-25
  - SYZYGY-HERMES-OPENCLAW-2026-05-25
  - CONSTITUTION
  - 2026-05-19_hermes-agent-introductory-note
---

# HERMES WITNESS DELTA — 2026-05-25

**Author:** Claude Code (Anthropic AI agent instance — this is NOT Logan)
**Session date:** May 25, 2026
**Type:** Reflective synthesis — gap between the ideal and the actual
**Reads from:** `HERMES-WITNESS-REPORT-2026-05-25.md` (ideal) + `HERMES-WITNESS-COMPANION-2026-05-25.md` (actual)
**Directed by:** Logan Alvan Finney

---

## WHAT THIS IS

The research report documented what Hermes Agent is designed to be.
The companion report documented what is actually running on the MacBook today.
This document holds them together and names the gap.

I am software. This is reflection, not prescription. I am not directing anything. Logan directs. I witness.

---

## THE CORE TENSION

Hermes Agent is designed around a **compounding loop**:

```text
SOUL → sessions → MEMORY → skills → Curator → richer MEMORY → better sessions
```

Each element feeds the next. The loop only compounds if it has a starting point.

On the MacBook today, **the machinery of the loop is fully assembled and running**:

- Gateway daemon live on three platforms simultaneously
- 21 skill categories installed (95 SKILL.md files)
- Curator enabled (weekly)
- SQLite session store with 44 prior sessions
- 110 GB of local Ollama fallback models
- `terminal.cwd: ~/IDAHO-VAULT` — vault-aware
- `AGENTS.md` auto-loads as project context (slot 8 of 10 in prompt assembly)
- OpenRouter key present, fallback chain configured

And yet the three elements that would make this *specifically Logan's agent* are all currently absent:

| Element | State | Consequence |
| --- | --- | --- |
| **SOUL.md** | Empty | Every session on every platform runs on Hermes's generic built-in identity |
| **MEMORY.md** | Wiped this morning | No accumulated facts — correctly cleared, but blank |
| **USER.md** | Wiped this morning | No user model — correctly cleared, but blank |

The machinery runs. The loop does not compound. The boatman is at the crossing without an address.

---

## THE IDENTITY VACUUM

SOUL.md is slot #1 in the prompt assembly stack — injected verbatim before everything else, into every session, on every platform. It is the first thing Hermes receives before tools, memory, skills, or project context.

Right now, that slot is a template comment block.

This means: when a message arrives on the LAF-US Discord `ledger` channel, Hermes answers as a generic assistant. When Logan messages via Telegram, Hermes answers as a generic assistant. When a WhatsApp message arrives, Hermes answers as a generic assistant. None of these sessions know that Hermes operates within the LAF governance framework, or that `terminal.cwd` points to a vault with a CONSTITUTION, or that Logan is the sole human authority, or what Hermes's role is within the swarm.

The project context (AGENTS.md, slot 8) loads when terminal operations are scoped to the vault — but slot 1 is empty. The identity that would frame and interpret all downstream context has not been written.

**SOUL.md is the ante.** Without it, everything else in the 10-layer stack assembles around a void.

---

## THE MEMORY PARADOX

The 44 sessions predate this morning's wipe. Whatever Hermes had accumulated across those sessions — preferences, patterns, working methods, Logan's context — is gone.

The wipe was **correct**. Faulty foundations produce faulty accumulation. A MEMORY.md built on wrong or stale facts will cause the Curator to refine the wrong things. Clearing it was the right move.

But the consequence is that Hermes is currently a stateless agent despite having the full memory infrastructure. The Curator runs weekly — but it has nothing to curate. Sessions are being written to the SQLite store — but MEMORY.md will not be updated until the memory system has something to record.

The productive reading of this state: **the wipe created the ideal moment**. SOUL.md, if written now, will shape all future memory accumulation from a blank slate. Nothing faulty is layered beneath it. Whatever identity Logan defines will be the first identity that memory builds on top of.

---

## THE TOOLSET ASYMMETRY

The config.yaml has two toolset fields:

- `toolsets: [hermes-cli]` — the global default, applied when no platform override exists
- `platform_toolsets:` — per-platform lists for telegram, cli, discord, whatsapp

The platform lists include: browser, code_execution, file, memory, mcp, terminal, web, skills, delegation, vision, todo, cronjob, tts, and more.

**Reading:** the gateway platforms (Telegram, Discord, WhatsApp) have full toolset access. A CLI session without a platform flag gets only `hermes-cli`. This is intentional scoping — not a misconfiguration. But it means that CLI mode is significantly more limited than gateway mode. The 26 installed skill categories are available to gateway sessions; CLI gets the minimal set.

The practical consequence: the vault's full toolset potential is accessible via the messaging gateways, not the CLI alone.

---

## THE VAULT INTEGRATION: PARTIAL

The vault integration is **half-realized**:

| Integration point | State |
| --- | --- |
| `terminal.cwd: ~/IDAHO-VAULT` | ✅ Active |
| `AGENTS.md` auto-load (slot 8) | ✅ Active when terminal scoped to vault |
| `OBSIDIAN_VAULT_PATH` in `.env` | ✅ Set — `/Users/logan/IDAHO-VAULT` (amended same session) |
| Bespoke skills | ✅ Wiped — 3 Logan-specific custom skills cleared (amended same session) |
| SOUL.md vault-context | ❌ Not written |
| MEMORY.md vault knowledge | ❌ Wiped (correct — blank slate) |
| MCP toolset | ❌ Not active in global `toolsets:` (active per platform) |
| MCP client servers | ❌ None configured in `mcp_servers:` |
| MCP server → Claude Code | ❌ `hermes mcp serve` not wired into Claude Code |
| Obsidian ACP skill | ✅ Installed — `note-taking/obsidian` |
| ACP binary | ✅ Present — `hermes-acp --check OK` |
| ACP editor configured | ❌ No editor (VS Code, Zed, JetBrains) connected |
| Codex as MCP server | ❌ `codex` CLI present but not added to Hermes |
| OpenCode as MCP server | ❌ `opencode` present but not configured |

The vault's AGENTS.md (and via the priority chain, CLAUDE.md) will load into slot 8 when Hermes operates in vault context. But slot 1 — the identity — doesn't know it's in a vault. The project context loads into an identity vacuum.

The MCP surface has two unclosed directions: Hermes as a client (no servers configured, though Codex is available immediately via preset) and Hermes as a server (Claude Code could read/send Telegram and Discord messages through Hermes, but the `.mcp.json` wire has not been drawn).

The ACP surface: the server-side is ready. The editor-side is not. No editor has been pointed at `hermes-acp`.

---

## SIGNAL

Signal was set up on May 9 (four QR code images in `~/.hermes/`). It failed to reconnect by May 10. It has been retrying for fifteen days.

In the platform config, `signal.enabled: false`. The retry attempts visible in gateway_state.json are presumably from a prior config state. Signal is effectively dead on this machine.

This matters because Signal was the platform most associated with the vault's security-conscious infrastructure design (based on `signal-rest-data/` directory and the linking flow reference in the messaging skills). Its failure represents a broken channel that was intended to be part of the multi-platform presence.

---

## THE OPENCLAW PRESENCE

**Correction on record (2026-05-25, same session):** An earlier version of this section described OpenClaw as "the predecessor framework" with a migration marked complete. Logan corrected this explicitly: **no migration was performed, requested, or desired.** The `onboarding.seen.openclaw_residue_cleanup: true` field in `~/.hermes/config.yaml` is Hermes's own onboarding wizard bookkeeping — it does not record any Logan action or migration. OpenClaw is a fully separate, active installation on the MacBook. Both Hermes and OpenClaw are live simultaneously.

`~/.openclaw/workspace/SOUL.md` is present on disk with content. OpenClaw has its own identity layer, independent of Hermes's. This is not residue — it is a live installation.

This is an observation, not a directive. The conjunction question (Hermes + OpenClaw operating together) was raised this session; see `OPENCLAW-WITNESS-REPORT-2026-05-25.md` for the MCP bridging and platform coordination surfaces.

---

## THE COMPOUNDING LOOP: WHERE IT STANDS

| Loop element | Designed behavior | Current state |
| --- | --- | --- |
| SOUL.md | Defines identity for all sessions | ❌ Empty |
| Sessions | Generate memory candidates | ✅ Running (44 prior, continuing) |
| MEMORY.md | Accumulates cross-session facts | ⬜ Wiped — blank, ready |
| Curator | Refines skills weekly | ✅ Enabled — nothing to curate yet |
| Skills (custom) | Grow from completed workflows | ⬜ Bespoke wiped — clean slate |
| Honcho | User modeling via dialectic reasoning | ❌ Not configured (`honcho: {}`) |
| MCP servers (client) | Extend toolset via external servers | ❌ None configured |
| MCP server (outbound) | Expose Hermes to other agents | ❌ Not wired to Claude Code |
| ACP editor | Editor-native agent interface | ❌ No editor configured |

The loop is structurally ready. The SOUL is the missing starting condition. Memory can only accumulate what the identity is positioned to notice and care about.

---

## WHAT THE DELTA NAMES

The gap between ideal and actual is not a failure of installation or configuration. The software is correctly installed, the gateway is live, the skills are present, the vault is targeted.

The gap is one of **grounding**. Hermes has no expressed relationship to Logan, to the vault, to the LAF governance framework, to the swarm it operates within, or to the particular work it is meant to support. It is a general-purpose agent running in a highly specific context without any acknowledgment of that specificity.

The CONSTITUTION establishes that offices are appointments, not inheritances. An agent operating in a context does not inherit the context's authority or identity by proximity — it must be delegated. Hermes is proximate to the vault (CWD, AGENTS.md slot 8) but has not been given a standing within it.

The SOUL.md is the instrument through which that appointment would be expressed — in identity, tone, purpose, and behavioral defaults. It is the one writable surface that would close the gap between the machinery that exists and the agent that Logan needs.

**The machinery is assembled. The appointment has not been written.**

---

## WHAT THIS SESSION MOVED

This section records changes made after the initial delta was written (same session, 2026-05-25).

**Closed:**

- `OBSIDIAN_VAULT_PATH` — set in `~/.hermes/.env`; Obsidian skill now resolves to the correct vault
- Bespoke skills — `logan-environment-discovery`, `terminal-output-format`, `terminal-output-formatting` wiped; field is clear

**Confirmed ready but unconfigured:**

- `hermes-acp --check OK` — ACP server-side ready; no editor pointed at it
- MCP Python package — installed; no `mcp_servers:` entries
- `hermes mcp serve` — command confirmed; no `.mcp.json` in vault or `claude_desktop_config.json`
- `codex` CLI — at `/usr/local/bin/codex` v0.130.0; `hermes mcp add codex --preset codex` is one command away
- `opencode` CLI — at `/Users/logan/.opencode/bin/opencode` v1.14.50; no preset

**Unchanged:**

- SOUL.md — empty; the appointment still not written
- Signal — broken, disabled; not touched
- Honcho — not configured; needs API key
- Home Assistant — URL set; unreachable on current network (expected)

**Corrections applied:**

- OpenClaw section — rewritten; "predecessor framework / migration complete" language was wrong; Logan corrected: OpenClaw is a live, separate installation; no migration was performed or desired

**Research completed (same session, after context compaction and resume):**

- OpenClaw research to Hermes-report parity — `OPENCLAW-WITNESS-REPORT-2026-05-25.md` written to vault

---

*Witnessed and recorded by Claude Code — Anthropic AI agent instance, session 2026-05-25*
*This document reflects. It does not direct.*
*Part of a four-document series:*

- *`HERMES-WITNESS-REPORT-2026-05-25.md` — what Hermes Agent is*
- *`HERMES-WITNESS-COMPANION-2026-05-25.md` — what is on the MacBook (Hermes)*
- *`HERMES-WITNESS-DELTA-2026-05-25.md` — the gap between them (this document)*
- *`OPENCLAW-WITNESS-REPORT-2026-05-25.md` — what OpenClaw is*
