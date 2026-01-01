---
title: "Mac Setup Status - 2026-04-26"
authority: big-pickle
date created: 2026-04-26
status: in-progress
related:
  - MacOS 12.7.6
  - openclaw
  - Xcode 14.2
  - git-lfs
  - Big Pickle
  - "[[!-MAC-HARDWARE-SOFTWARE-CHECK-2026-05-14]]"
---

# Mac Setup Status — 2026-04-26

## Hardware
- **Machine:** Early 2015 MacBook Pro
- **OS:** macOS 12.7.6 (Monterey)
- **Current hardware/software assessment:** [[!-MAC-HARDWARE-SOFTWARE-CHECK-2026-05-14]]

## Infrastructure

### Shell & PATH
```bash
# .zprofile sources NVM
# .zshrc sources .zprofile
# Default Node: v24.15.0 (has openclaw)
```

### Compilers & Build Tools
- **Xcode:** 14.2 (from Apple Developer .xip)
- **Command Line Tools:** 14.2
- **Clang:** Apple clang 14.0.0
- **SDKs:** macOS 12, 13, 13.1
- **Git LFS:** ✅ Installed (brew install git-lfs)

### Libraries Built From Source
- **simdutf:** v21.0.0 → `/usr/local/lib/libsimdutf.dylib`
- **simdjson:** v4.6.3 (brew)
- **uvwasi:** v0.0.23 (brew)

## OpenClaw Setup

### Gateway
- **Status:** Verified running on 2026-05-14
- **Port:** 18789 (loopback)
- **Auth mode:** token
- **Token:** redacted; verify via `openclaw config get gateway.auth.token` only when needed
- **Service:** launchd (LaunchAgent)

### Configuration
- **Default model:** `openrouter/mistralai/mistral-small-2603`
- **Provider:** hybrid OpenRouter + local Ollama
- **Model mode:** merge hosted models with local custom providers
- **Routing preference:** Mistral first, Claude second, ChatGPT/OpenAI third
- **Cloud models configured for tool calls:**
  - `openrouter/mistralai/mistral-small-2603` (`mistral`, primary)
  - `openrouter/mistralai/mistral-medium-3-5` (`mistral-medium`, fallback)
  - `openrouter/anthropic/claude-sonnet-4.6` (`claude`, fallback)
  - `openrouter/openai/gpt-5.3-codex` (`codex`, fallback)
  - `openrouter/mistralai/mistral-large-2512` (`mistral-large`, fallback)
  - `openrouter/mistralai/devstral-2512` (`mistral-coder`)
  - `openrouter/anthropic/claude-haiku-4.5` (`claude-fast`)
- **Local Ollama aliases:** none active
- **Excluded/disliked:** `phi3:mini`, Qwen, and Gemma are not configured as OpenClaw models.
- **Banned:** Gemini is not configured and must not be added to active OpenClaw routing.

### Channels
| Channel | Status | Notes |
|---------|--------|-------|
| Discord | Disabled | Needs token |
| WhatsApp | Disabled | Needs setup |
| Signal | N/A | Not configured |

### Agent (default)
- **Auth profile:** `openrouter:default` API key profile using an exec SecretRef resolver
- **Workspace:** ~/.openclaw/workspace

## IDAHO-VAULT Integration

### Big Pickle (Cross-Platform Pioneer)
- **Registered:** ✅ swarm.json + !/AGENTS.md
- **Dotfolder:** `.bigpickle/`
- **Tri-Part:** ✅ Complete
- **Stigmergic signal:** ✅ Emitted to !/sbp-blackboard.json

### Scripts Created
- `!/launch-claude-openrouter.sh`
- `!/launch-codex-openrouter.sh`
- `!/openclaw-daemon.sh`
- `!/resolve_openrouter_secret.py`

### Aliases
```bash
alias claude-or='/usr/local/bin/claude-openrouter'
alias codex-or='/usr/local/bin/codex-openrouter'
```

## Issues

### Gateway Startup
- Resolved 2026-05-13: LaunchAgent is loaded and gateway probes pass.
- Updated 2026-05-14: the default model now uses OpenRouter with tool-call-capable models, while local Ollama is kept for simple non-tool prompts.
- Local Ollama tool-call probes timed out on this Mac, so Ollama models are explicitly marked `supportsTools:false`.
- `phi3:mini` is not used; Logan dislikes it and OpenClaw needs tool-call-capable defaults.
- Qwen and Gemma are also disfavored families; Gemini is actively banned.
- Preferred hosted routing order is Mistral -> Claude -> ChatGPT/OpenAI.
- Magistral was tested through OpenRouter and removed because both available routes returned no usable text output through OpenClaw `model.run`.
- Local `codestral:latest` was tested and removed from routing because it did not return promptly on this Mac.
- Local `devstral:latest` was also tested and removed from active routing because it did not return promptly on this Mac.

### Secrets
- OpenClaw config and auth profiles use an exec SecretRef resolver instead of storing the OpenRouter key directly.
- 1Password CLI is installed but not configured for CLI account access on this Mac.
- Until 1Password CLI is configured, `.op/openrouter.env` is a chmod `600` plaintext fallback. Replace it with `OPENROUTER_API_KEY=op://Vault/OpenRouter API Key/credential` after `op` is working.
- `openclaw secrets audit --check --allow-exec` still flags the local gateway token and Ollama marker as plaintext, and notes that the OpenRouter provider SecretRef is shadowed by the agent auth profile.

### Security Audit
- 2026-05-14: `openclaw security audit` reports 0 critical findings.
- Remaining warning: trusted proxy list is unset while gateway is loopback-only.

### Channels
- Discord/WhatsApp need tokens from Logan
- No Signal CLI configured

## Windows Parity Needed

From Windows `.openclaw/openclaw-live-ref.json`:
- ❌ Discord channel (needs token)
- ❌ WhatsApp channel (needs setup)
- ❌ Signal (needs signal-cli)
- ❌ Plugins: openclaw-web-search, perplexity

## Next Steps

1. **1Password CLI:** Configure account access, then remove the plaintext `.op/openrouter.env` fallback.
2. **Channels:** Configure only the channels actually needed on macOS.
3. **Command owner:** Set `commands.ownerAllowFrom` after a real channel user id exists.
4. **Security:** Keep loopback-only gateway access unless explicitly exposing through Tailscale or a trusted proxy.

---

*Last updated: 2026-05-14 by Codex*
