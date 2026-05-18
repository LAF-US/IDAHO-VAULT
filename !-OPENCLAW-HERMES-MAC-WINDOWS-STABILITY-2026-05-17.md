---
title: "OpenClaw Hermes Mac Windows Stability"
date: 2026-05-17
status: active
authority: LOGAN
doc_class: operational_status
related:
  - OpenClaw
  - Hermes
  - OpenRouter
  - Ollama
  - OpenCode
  - Windows-ZBFURY
  - "!-OPENCLAW-HERMES-STATUS-2026-05-14"
  - "OPENROUTER-MESH-2026-04-24"
  - "PROTOCOL-XKCD-DRAFT"
---

# OpenClaw Hermes Mac Windows Stability - 2026-05-17

This note supersedes the Mac/Windows pairing task listed in [[!-OPENCLAW-HERMES-STATUS-2026-05-14]] and records the current stable operating surface.

## Stable State

- Mac OpenClaw gateway: `2026.5.16-beta.3`.
- Windows OpenClaw node: `2026.5.16-beta.3`.
- Windows node display name: `Windows-ZBFURY`.
- Mac gateway bind: loopback only, `127.0.0.1:18789`.
- Windows tunnel: `127.0.0.1:18790 -> Mac 127.0.0.1:18789`.
- Gateway token remained out of chat during final Windows setup.
- Mac gateway dashboard: `http://127.0.0.1:18789/`.
- `admin-http-rpc`: disabled.
- Windows node commands present: `system.run`, `system.run.prepare`, `system.which`, `browser.proxy`.

## Verification

- Mac-to-Windows invoke stress test: `15/15` successful.
- Observed latency range: `188-391 ms`.
- Observed average latency: `249 ms`.
- No pending node requests after stress test.
- Post-hardening smoke test resolved Windows `cmd`, `powershell`, and `ollama`.
- Explicit scoped gateway calls work.
- Follow-up consistency check on 2026-05-17: after a Mac gateway restart, Windows-ZBFURY reconnected automatically and `5/5` `openclaw nodes invoke --command system.which` probes succeeded.
- Verified Windows paths: `C:\WINDOWS\system32\cmd.exe`, `C:\WINDOWS\System32\WindowsPowerShell\v1.0\powershell.exe`, and `C:\Users\loganf\AppData\Local\Programs\Ollama\ollama.exe`.

## Security And Hardening

- Mac gateway is now loopback-bound instead of LAN-bound.
- Cross-machine access depends on the SSH tunnel rather than exposing the gateway on the LAN.
- `/Users/logan/.openclaw/secrets` tightened to mode `700`.
- Gateway token file remains mode `600`.
- `secrets.providers.gateway_token_file` points at `/Users/logan/.openclaw/secrets/gateway-token` using `singleValue`.
- `openclaw doctor` no longer blocks on gateway auth.
- Deep security audit: `0 critical`, `1 warn`, `1 info`.
- Remaining warning: `gateway.trusted_proxies_missing`; acceptable while gateway is loopback-only and accessed through SSH tunnel.

## Model Calling Direction

Desired reliable stack:

- Ollama for local/simple calls where a local model is fast enough and policy-acceptable.
- OpenRouter for complex calls, tool-call-capable cloud models, and fallback routing.
- OpenCode as a coding execution surface, not the durable authority layer.

Preferred hosted family order:

1. Mistral
2. Claude
3. ChatGPT/OpenAI

Policy exclusions:

- Do not route active agent work through Phi, Qwen, or Gemma.
- Do not use Gemini for active routing decisions.
- Gemini/Google credentials may remain appropriate for TTS or Google Cloud infrastructure when explicitly scoped.

## Standing Caveats

- Reboot persistence has not been proven yet.
- Stock `openclaw nodes invoke` works when the Codex process is allowed to connect to the local OpenClaw gateway. In a restricted Codex sandbox it can fail with a misleading `1006 abnormal closure`; the gateway log shows the real cause as `connect EPERM 127.0.0.1:18789`.
- If invoke tests fail inside Codex, rerun them with local gateway WebSocket access allowed before treating the Mac/Windows link as broken.
- `system.run` is intentionally blocked on the generic `nodes invoke` surface; route shell execution through OpenClaw's exec path rather than bypassing policy.
- Windows process persistence depends on the current tunnel/node launcher arrangement until a startup mechanism is tested.

## Next Strengthening Tasks

- Prove reboot recovery on Mac and Windows.
- Add a durable runbook for restarting the tunnel and Windows node without leaking the gateway token.
- Keep gateway loopback-only unless Logan explicitly approves another exposure model.
- Prefer SSH tunnel over LAN exposure for cross-machine work.
- Record cross-machine handoffs in plain language. [[!-XKCD-MINIMAL-HANDOFF-2026-05-17]] is guidance, not a required protocol.

###### [["The world is quiet here."]]
