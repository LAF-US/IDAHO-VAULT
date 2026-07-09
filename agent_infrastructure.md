---
name: Agent Infrastructure — Hermes + OpenClaw
description: Durable facts about the two AI agent daemons running on Logan's MacBook; their architecture, configuration patterns, and coordination model
type: infrastructure
originSessionId: 56452f88-4aa9-43d4-9109-482212602d2c
---

# Agent Infrastructure

Two autonomous agent daemons run simultaneously on the MacBook as LaunchAgents. Neither supersedes the other.

---

## Hermes Agent (Nous Research)

- **Binary:** `~/.hermes/hermes-agent/venv/bin/hermes` (Python 3.11 venv — this is the active one)
- **LaunchAgent:** `~/Library/LaunchAgents/ai.hermes.gateway.plist`
- **Architecture:** Linear compounding loop — SOUL → sessions → MEMORY → skills → Curator. Depth instrument: the longer it runs in a context, the more it knows about that context.
- **Platforms connected:** Telegram, Discord (LAF-US guild, `ledger` channel), WhatsApp (self-chat bridge). Signal disabled (linking failed).
- **Credential pattern (as of 2026-06-28):** op:// refs in `~/.hermes/.env.op` (NOT `.env`), resolved by `~/.hermes/bin/hermes-gateway-launch.sh` via `op read` calls and exported to process env before exec'ing the daemon. `~/.hermes/.env` retains only `OP_SERVICE_ACCOUNT_TOKEN` (bootstrap), `SUDO_PASSWORD`, and plaintext config vars. The split is the local workaround for upstream `NousResearch/hermes-agent#19201` (`load_hermes_dotenv()` calls `override=True`, which clobbered op-resolved values back to literal `op://...` strings when they lived in `.env`). Upstream fix in flight at `NousResearch/hermes-agent#18734`. See `~/.hermes/README-workaround.md` and `IDAHO-VAULT/HERMES-WORKAROUND-WITNESS-2026-06-28.md` for full context + revert procedure. (Pre-workaround pattern was `op run --env-file=~/.hermes/.env` with op:// refs in `.env` directly; before that, plaintext secrets in `.env`.)
- **Identity layer:** `~/.hermes/SOUL.md` — verbatim slot #1 in every system prompt across all platforms.
- **Memory layer:** `MEMORY.md` + `USER.md` in `~/.hermes/`; Curator runs weekly to refine skills.
- **Project context:** Auto-loads `AGENTS.md` when `terminal.cwd` = `~/IDAHO-VAULT` (slot 8 of 10-layer prompt assembly).
- **MCP (as server):** `hermes mcp serve` — exposes 10 messaging tools over stdio.
- **MCP (as client):** `hermes mcp add <name>` — configured servers load as first-class tools.
- **Skills:** `~/.hermes/skills/` — 21 categories with SKILL.md files; agentskills.io format (Anthropic-originated standard).

---

## OpenClaw

- **Binary:** `~/.nvm/versions/node/v24.15.0/bin/openclaw` (Node.js via nvm)
- **LaunchAgent:** `~/Library/LaunchAgents/ai.openclaw.gateway.plist`
- **Architecture:** Node-graph, event-driven. Maximum reach instrument: organizes execution as a directed acyclic graph; persistent event bus rather than session boundaries.
- **Gateway mode:** `local` — loopback only. No external platform channels. Operates as a local hub.
- **Paired node:** Windows laptop (hostname: ZBFURY) — capabilities: system, browser, file. Currently offline but paired. First paired 2026-05-17.
- **Credential pattern:** Secret provider chain — 1Password CLI (`op read`) primary, vault script (`~/IDAHO-VAULT/!/resolve_openrouter_secret.py`) secondary. More sophisticated than Hermes's .env.
- **Identity layer:** `~/.openclaw/workspace/SOUL.md` — flat layout (single-agent default install).
- **MCP (as server):** `openclaw mcp serve` — exposes 9 messaging tools over WebSocket. `--claude-channel-mode` flag for Claude-specific formatting.
- **MCP (as client):** `openclaw mcp set <name> '<json>'` — client registry in `openclaw.json`.
- **Skills:** 27 built-in active + 1 ClawHub (browser-automation) + 1 workspace (sam-tts).

---

## MCP Coordination (wired 2026-05-26)

After wiring on 2026-05-26, the bidirectional MCP topology is:

```
Claude Code ──▶ hermes mcp serve  (messaging: Telegram, Discord, WhatsApp)
Claude Code ──▶ openclaw mcp serve (local hub, ZBFURY compute)
Hermes      ──▶ openclaw mcp serve (Hermes can reach OpenClaw's local surfaces)
OpenClaw    ──▶ hermes mcp serve  (OpenClaw can reach Hermes's platform channels)
```

`.mcp.json` lives at `~/IDAHO-VAULT/.mcp.json`.

---

## Shared Substrate

Both use the agentskills.io `SKILL.md` format (Anthropic-originated, December 2025). SKILL.md files are compatible across frameworks; OpenClaw adds a `clawmanifest.json` signing requirement that Hermes does not enforce.

Both expose `SOUL.md`-based identity injection. The identities are independent — writing one does not affect the other.

---

## Reference Documents (2026-05-25 witness series)

The full research and local survey is captured in seven vault documents:
- `HERMES-WITNESS-REPORT-2026-05-25` — what Hermes is
- `HERMES-WITNESS-COMPANION-2026-05-25` — local machine survey
- `HERMES-WITNESS-DELTA-2026-05-25` — gap between ideal and actual
- `OPENCLAW-WITNESS-REPORT-2026-05-25` — what OpenClaw is
- `OPENCLAW-WITNESS-COMPANION-2026-05-25` — local machine survey
- `OPENCLAW-WITNESS-DELTA-2026-05-25` — gap between ideal and actual
- `SYZYGY-HERMES-OPENCLAW-2026-05-25` — comparative and conjunction record (canonical home for cross-framework material)
