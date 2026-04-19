---
authority: LOGAN
related:
  - The world is quiet here
  - AGENTS
  - CONSTITUTION
  - VAULT-CONVENTIONS
---

[ ? ]

---

# MISTRAL.md — IDAHO-VAULT

**Load mechanism:** Manual injection by Logan. Mistral Vibe auto-scans project file structure and Git status for context. This file is the vault-local context shim.

**Owner:** Logan Finney — journalist, producer/reporter, Idaho Reports / Idaho Public Television
**Repository:** github.com/LAF-US/IDAHO-VAULT (public)
**Platform:** Obsidian.md vault, version-controlled with git

---

## Governance

This file is a context shim for Mistral Vibe. Vault governance authority lives in `CONSTITUTION.md`. When this file and `CONSTITUTION.md` conflict, `CONSTITUTION.md` governs. Capability tier: `[VACANT — awaiting Logan]`. Governance work remains Logan-directed.

---

## What is Mistral Vibe

Mistral Vibe is an open-source command-line coding assistant powered by Mistral models (Apache 2.0). It provides a conversational interface to the codebase with built-in tools for file manipulation, code search, version control, and command execution.

Source: `- docs.mistral.ai - CLI Introduction  Mistral Docs.md`

---

## Runtime Containment

Prefer launching Mistral Vibe for this vault through `scripts/Start-MistralVault.ps1` (when created) so temp files, cache, and Mistral Vibe home state stay inside the vault. Until that script exists, invoke from the vault root:

```bash
cd "C:/Users/loganf/Documents/IDAHO-VAULT"
mistral
```

Config: `.mistral/config.toml` (vault-local project config)

---

## Role

- Logan is human. Mistral Vibe is software. Logan decides; Mistral Vibe executes within task boundaries.
- Title/persona: `[ ? ]` — awaiting Logan's direction.
- Lane: `[VACANT — awaiting Logan]`
- Git suffix: `-M`

---

## Local vs. API Mode

| Mode | Backend | Port | Requirement |
|---|---|---|---|
| **API** | Mistral cloud | — | `MISTRAL_API_KEY` in 1Password |
| **Local (Devstral)** | vLLM / Ollama / LM Studio | 8080 | GPU (H100/A100 for FP16; RTX 4090 for 4-bit/32k ctx) |

Switch to local: type `/model` in Vibe, select `"local"`. Local server must be running on port 8080.

Reference: `- Offline - Local  Mistral Docs.md`

---

## Credential

API key lives in 1Password. Fetch via 1Password CLI:

```bash
export MISTRAL_API_KEY=$(op item get "Mistral API Key" --fields credential)
```

Item name: `Mistral API Key` (confirm actual item name in 1Password before use).

---

## Conventions and Standards

See `VAULT-CONVENTIONS.md` for vault structure, naming, frontmatter, sourcing protocol, git practices, and automation standards.

**DISCOVERY BEFORE INVENTION:** Read existing vault files before proposing new conventions. The vault is the record of decisions already made.

---

## Swarm Coordination

Read THE DOCKET to orient: `!/__!__/!/! The world is quiet here/DOCKET.md`

Task assignment flows through GitHub Issues (`agent:mistral` label, when activated). Each agent works on its own branch. PRs are the deliverable. Logan reviews and merges from GitHub.

---

## See Also

- `CONSTITUTION.md` — Canonical vault governance authority
- `VAULT-CONVENTIONS.md` — Shared vault conventions for all agents
- `!/AGENTS.md` — Full agent registry, capability tiers, and boundary rules
- `.mistral/config.toml` — Mistral Vibe project configuration
- `- docs.mistral.ai - CLI Introduction  Mistral Docs.md` — Clipped Vibe docs
- `- Offline - Local  Mistral Docs.md` — Local/Devstral deployment notes
