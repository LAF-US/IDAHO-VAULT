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
---

# Mac Setup Status — 2026-04-26

## Hardware
- **Machine:** Early 2015 MacBook Pro
- **OS:** macOS 12.7.6 (Monterey)

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
- **Status:** Starting (stuck/hanging)
- **Port:** 18789 (loopback)
- **Auth mode:** token
- **Token:** `d58ad86ef01d53b87e30a6e708c69c90b117ae99eab2fe67`
- **Service:** launchd (LaunchAgent)

### Configuration
- **Default model:** `mistral/mistral-small-latest`
- **Provider:** OpenRouter (env:OPENROUTER_API_KEY)
- **Models available:**
  - mistral/mistral-small-latest (free)
  - mistral/mistral-large-latest (paid)
  - openai/gpt-4o-mini (free)
  - anthropic/claude-3.5-haiku (free)

### Channels
| Channel | Status | Notes |
|---------|--------|-------|
| Discord | Disabled | Needs token |
| WhatsApp | Disabled | Needs setup |
| Signal | N/A | Not configured |

### Agent (default)
- **Auth profile:** openrouter (api_key mode)
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

### Aliases
```bash
alias claude-or='/usr/local/bin/claude-openrouter'
alias codex-or='/usr/local/bin/codex-openrouter'
```

## Issues

### Gateway Startup
- Gateway process starts but doesn't bind to port 18789
- Logs show "starting..." but no "listening" confirmation
- CPU spikes to 99% then process hangs
- May be older hardware bottleneck

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

1. **Gateway:** Debug startup hang or restore Windows config
2. **Channels:** Get Discord token from 1Password
3. **Skills:** Install OpenClaw skills from marketplace

---

*Last updated: 2026-04-26 by Big Pickle*