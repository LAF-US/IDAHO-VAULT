---
updated: 2026-05-07
status: active
authority: LOGAN
scope:
  - sources
  - openclaw
  - ollama
  - diagnostics
---
# Sources: OpenClaw And Ollama Diagnostics

These sources were used on 2026-05-07 while interpreting local OpenClaw gateway, channel, model-auth, and Ollama diagnostics.

## OpenClaw

- OpenClaw models CLI and auth profiles: https://docs.openclaw.ai/cli/models
- OpenClaw channels CLI: https://docs.openclaw.ai/cli/channels
- OpenClaw WhatsApp channel guide: https://docs.openclaw.ai/channels/whatsapp
- OpenClaw OpenAI / Codex OAuth setup: https://docs.openclaw.ai/openai
- OpenClaw troubleshooting index reference from local CLI output: https://docs.openclaw.ai/troubleshooting

## Ollama

- Ollama model library: https://ollama.com/library
- Ollama CLI documentation: https://github.com/ollama/ollama/blob/main/docs/cli.md
- Ollama API documentation: https://github.com/ollama/ollama/blob/main/docs/api.md

## Local Diagnostic Notes

- `ollama pull claude` failed because `claude` is not an Ollama registry model name.
- Local Ollama models observed:
  - `devstral:latest`
  - `llama3.2-vision:90b`
  - `gemma4:latest`
  - `mistral`
- OpenClaw gateway was observed running manually on `127.0.0.1:18789`.
- OpenClaw background service persistence and channel auth still need verification.
- OpenClaw doctor reported OpenAI Codex OAuth refresh failure with `refresh_token_reused`; recommended action is `openclaw models auth login --provider openai-codex`.
- OpenClaw WhatsApp channel reported logged out; recommended action is `openclaw channels login --channel whatsapp`.
- A plaintext OpenRouter API key appeared in chat context and must be treated as compromised. Rotate it before further OpenRouter testing.

## Source Handling Rule

After web sources are used for diagnostics or implementation decisions, add them to a durable `SOURCES-*` note in the vault before closing the thread.
