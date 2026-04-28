# Local Mesh Networking Setup — IDAHO-VAULT
# Guidelines for Running OpenClaw Locally (No Rate Limits)

## Why Local-First?
- Cloud models (OpenRouter, KIMI) hit rate limits on macOS.
- Local Ollama models run directly on your machine — no external API calls.
- Eliminates timeouts, billing, and network dependencies.

## Prerequisites
1. **Ollama installed** (at `/usr/local/bin/ollama`)
2. **Local model downloaded**:
   ```bash
   ollama pull phi3:mini   # 2.2GB, fast, works on macOS 12.7.6
   ```
3. **OpenClaw installed** and running.

## Configuration Files (Now in Vault Root)
1. **`.openclaw-local-only.yml`** — Strict local-only, blocks ALL cloud models:
   - Sets agent model to `ollama/phi3:mini`
   - Denies all models by default, allows only `ollama/*`
   - Binds gateway to `127.0.0.1` (localhost only)
   - Disables external API calls (`allow-external: false`)

2. **`.openclaw-local-mesh.yml`** — Mesh networking with local models:
   - Same local model config
   - Enables local mesh channel for device-to-device communication
   - No cloud fallbacks

## How to Use
1. **Start OpenClaw with local config**:
   ```bash
   openclaw gateway run --config /Users/logan/IDAHO-VAULT/.openclaw-local-only.yml
   ```
   Or set it as default in your shell profile.

2. **Verify no cloud calls**:
   ```bash
   ollama list   # Should show phi3:mini
   ```

3. **Test local response**:
   ```bash
   ollama run phi3:mini "Hello, local mesh!"
   ```

## Benefits
- ⚡ **No rate limits** — runs on your hardware
- ⚡ **No timeouts** — no network calls to external APIs
- ⚡ **Privacy** — all processing stays on your machine
- ⚡ **Speed** — local inference is faster for small models

## File Locations
- Config files: `/Users/logan/IDAHO-VAULT/.openclaw-local-only.yml` and `.openclaw-local-mesh.yml`
- Ollama models: `~/.ollama/models/`
- OpenClaw logs: `/tmp/openclaw/openclaw-local-mesh.log`

## Skills Created (in `skills/`)
- `openrouter-config.md` — OpenRouter API key management
- `1password-resolver.md` — 1Password CLI integration
- `service-health-monitor.md` — External API health checks
- `oauth-configurator.md` — OAuth flow handling
- `service-compat-validator.md` — Service compatibility checks

## Next Steps
1. **Use local config** for all future OpenClaw sessions.
2. **Add more local models** as needed: `ollama pull qwen2.5:3b` (if download completes).
3. **Remove cloud model references** from all agent configs.

---
**Status**: All changes committed and pushed to `origin/main` (commit `db48f97f`).
**Signed-off-by**: Logan Finney <logan@idaho.gov>
