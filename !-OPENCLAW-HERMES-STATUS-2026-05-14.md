# OpenClaw And Hermes Status - 2026-05-14

Related:
- [[!-MAC-HARDWARE-SOFTWARE-CHECK-2026-05-14]]
- [[!-MAC-SETUP-STATUS-2026-04-26]]
- [[IMPL-MESH-OPENROUTER-2026-04-24]]
- [[SOURCES-OPENCLAW-OLLAMA-DIAGNOSTICS-2026-05-07]]

## Current OpenClaw State

- Version: `2026.5.14-beta.1`
- Gateway: running as macOS LaunchAgent on port `18789`
- Bind mode: `lan` (`0.0.0.0`), reachable locally at `ws://127.0.0.1:18789`
- Dashboard: `http://192.168.0.95:18789/`
- Tailscale exposure: off
- Node service: not installed
- Paired nodes: none
- Pending node pairings: none
- Channels: none enabled in current OpenClaw status output
- Skills: 28 eligible, 0 missing requirements
- Security audit: 0 critical, 1 warning from a deep gateway probe timeout; normal gateway health/status probes pass

## Current OpenClaw Model Routing

Default:
- `openrouter/mistralai/mistral-small-2603`

Fallbacks:
- `openrouter/mistralai/mistral-medium-3-5`
- `openrouter/anthropic/claude-sonnet-4.6`
- `openrouter/openai/gpt-5.3-codex`
- `openrouter/mistralai/mistral-large-2512`

Aliases:
- `mistral`
- `mistral-large`
- `mistral-medium`
- `mistral-coder`
- `claude-fast`
- `claude`
- `codex`

Policy note:
- This matches Logan's preferred routing order: Mistral, Claude, then ChatGPT/OpenAI.
- Gemini is not configured in active OpenClaw model routing.
- Phi, Qwen, and Gemma remain excluded from active OpenClaw routing.

## Current Hermes State

- Hermes Gateway: running as macOS LaunchAgent
- Hermes model default: `ollama/devstral:latest`
- Hermes model provider: `ollama`
- Hermes OpenRouter key: configured
- Hermes TTS provider: `gemini`
- Hermes `voice.auto_tts`: `false`
- Hermes custom TTS provider added: `sam`
- Hermes SAM wrapper: `/Users/logan/.hermes/bin/hermes-sam-tts.js`
- Hermes doctor: all checks pass after local doctor Gemini health-check correction

## TTS Status

Working:
- Gemini TTS generated `jabberwocky-old-man-gemini.mp3`
- SAM TTS generated `jabberwocky-old-man-sam.wav` and `.mp3`
- Hermes custom provider `sam` generated OGG/Opus voice-compatible output

Deliberately off:
- Global `voice.auto_tts` remains off because MacBook load averages were high during testing.

## Local Code Changes

Hermes local patch:
- `tools/tts_tool.py`: redacts API keys and tokens from TTS provider error text before logging or returning tool errors.
- `hermes_cli/doctor.py`: checks Gemini native API connectivity using Google API-key style auth instead of OpenAI-style bearer auth.

OpenClaw state cleanup:
- `openclaw doctor --fix` moved a heartbeat-owned `agent:main:main` session into a recovered heartbeat session slot.

## Security Notes

- OpenClaw gateway is intentionally LAN-bound for Mac/Windows coordination work. Treat this as trusted-LAN only until Tailscale or SSH tunneling is configured.
- OpenClaw secrets audit is clean, including executable SecretRefs.
- During local diagnostics, one command printed secret values into the terminal transcript. Rotate the affected OpenRouter and Gemini/Google API keys when practical.

## Next Tasks

- Pair the Windows OpenClaw node with this Mac gateway.
- Prefer Tailscale or SSH tunneling before relying on LAN-bound gateway access outside a trusted home network.
- Decide whether Hermes should keep Gemini TTS as default, switch to SAM for retro/local-only voice mode, or expose both as explicit commands.
- Keep `voice.auto_tts` off until machine load is consistently lower.
