---
authority: LOGAN
created: 2026-06-24
filed_by: "*.claude.*"
machine: personal-MacBook (MacBookPro12,1, macOS 12.7.6, 16 GB RAM)
tags: [hermes, beefstack, openrouter, 1password, ollama, model-routing, op-resolution, witness]
related:
  - BEEFSTACK-MODEL-ROUTING-2026-05-17.md
  - SNAPSHOT-OPENROUTER-HERMES-BEEFSTACK-2026-05-18.md
  - SNAPSHOT-OPENROUTER-HERMES-OPENCLAW-KEYS-2026-05-20.md
  - SNAPSHOT-BEEFSTACK-DIAGNOSTIC-OPencode-2026-05-23.md
  - HERMES-WITNESS-COMPANION-2026-05-25.md
  - SECURITY-CREDENTIAL-CONTAINMENT-2026-05-26.md
---

# Hermes Witness — Personal MacBook — 2026-06-24

Filed at the close of a working session that wired Hermes' credential surface onto a 1Password service account, re-enabled Hermes secret redaction, pruned the local Ollama store, and refactored the Hermes fallback chain to a BEEFSTACK-aligned 16-entry shape with four distinct direct-provider buckets. This record exists because Hermes' on-disk config had drifted from the May record set without a witness — that gap is now closed.

This record describes the state of the personal Mac only. OpenClaw on this machine is intentionally untouched (per the 2026-05-26 SECURITY-CREDENTIAL-CONTAINMENT-style policy split: OpenClaw permitted on personal Mac, disallowed on Windows-ZBFURY). OpenClaw is a follow-up sprint; its JSON config does not natively interpolate environment variables and requires a different design than what was applied here.

## Session arc

Four discrete sprints, each completed and verified before the next began.

### Sprint 1 — 1Password service-account wiring (Hermes only)

The `OP_SERVICE_ACCOUNT_TOKEN` for the `idaho-vault-github-actions` service account (created 2026-04-20, accessible to two 1Password vaults: `Vault` and `Work`) was already provisioned. It was added to `~/.hermes/.env` (mode 600). A small launcher shim was introduced at `~/.hermes/bin/hermes-gateway-launch.sh` (mode 700) that:

1. Reads `OP_SERVICE_ACCOUNT_TOKEN` from `~/.hermes/.env`, exports it.
2. Execs `/usr/local/bin/op run --env-file=~/.hermes/.env -- <hermes-gateway-command>`.

`op run` resolves every `op://...` reference in the env file at process start, injecting real values into the child's process env. The launchd plist `~/Library/LaunchAgents/ai.hermes.gateway.plist` was patched to invoke the shim as `ProgramArguments[0]`, with the original Python command appended as subsequent arguments. The plist remains world-readable (mode 644 — launchd default); the secret-bearing `.env` stays at mode 600.

Per-machine constraint reconciled: this Mac is hardware-bound to macOS Monterey 12.7.6 and to 1Password 7 (the personal Mac cannot upgrade past Monterey, and the user's 1Password license predates the v8 subscription model). The `1Password 8 desktop-app CLI integration` path is therefore unavailable. The service-account-token path bypasses the desktop app entirely and works on any `op` CLI version (v2.34.0 is what's installed).

Seventeen environment variables were converted from plaintext or new-add to `op://` references in `~/.hermes/.env`, sourced from items in the `Vault` 1Password vault. The bootstrap `OP_SERVICE_ACCOUNT_TOKEN` itself remains as a plaintext value in `.env` — this is the only secret-bearing literal that has to stay plaintext, because `op run` needs it in process env before it can resolve anything else. `SUDO_PASSWORD` and all non-secret config lines (`DISCORD_ALLOWED_USERS`, `HASS_URL`, `OBSIDIAN_VAULT_PATH`, `TELEGRAM_ALLOWED_USERS`, `TERMINAL_*`, `WHATSAPP_*`) were preserved as-is.

### Sprint 2 — Hermes secret redaction re-enabled

`security.redact_secrets: false` was found in `~/.hermes/config.yaml` (line 410). Hermes' agent.log was carrying a recurring `WARNING gateway.run: Secret redaction: DISABLED` line. The setting was flipped to `true`. Verified post-bounce that Hermes now logs `INFO gateway.run: Secret redaction: ENABLED` instead. The mechanism: `agent/redact.py` snapshots `_REDACT_ENABLED` at module-import time from `HERMES_REDACT_SECRETS` env var; that env var is bridged from `security.redact_secrets` by `hermes_cli/main.py:295` and `gateway/run.py:932` before the snapshot runs.

### Sprint 3 — Ollama hygiene

Four local models removed via `ollama rm`, total ~84 GB freed:

- `phi3:mini` (2.2 GB) — disliked per the 2026-05-17 BEEFSTACK record's "Phi / Qwen / Gemma" exclusion
- `qwen3.5:latest` (6.6 GB) — same exclusion
- `qwen2.5:3b` (1.9 GB) — same exclusion
- `mistral-large:latest` (73 GB) — physically unloadable in 16 GB RAM; the BEEFSTACK record positions it as a "deep anchor" for stronger machines, which this Mac is not

Remaining local models: `devstral:latest` (14 GB) and `codestral:latest` (12 GB). The freed disk blocks are still held by APFS Time Machine local snapshots (`tmutil listlocalsnapshots /` shows 9 snapshots from 2026-05-25 onward). macOS will auto-purge these on space pressure or ~24h cycle; manual purge via `tmutil deletelocalsnapshots <date>` not run pending Logan authorization.

### Sprint 4 — Fallback chain v3 refactor (BEEFSTACK-aligned, 16 entries)

Four new `op://` refs added to `~/.hermes/.env` to unlock additional direct-provider buckets:

- `ANTHROPIC_API_KEY` → `op://Vault/Claude API Key/credential`
- `DEEPSEEK_API_KEY` → `op://Vault/Deepseek API Key/credential`
- `KIMI_API_KEY` → `op://Vault/Moonshot API Key/credential`
- `PERPLEXITY_API_KEY` → `op://Vault/Perplexity API Key/credential`

One new custom provider declaration added to `config.yaml > providers:` block alongside the pre-existing `mistral-direct`:

```yaml
perplexity-direct:
  base_url: https://api.perplexity.ai
  key_env: PERPLEXITY_API_KEY
  api_mode: chat_completions
```

`fallback_providers:` replaced with a 16-entry chain. The ordering reflects two orthogonal axes per Logan's framing on 2026-06-24:

- **Axis 1 (preference)**: BEEFSTACK provider-family tier — Mistral / Claude (tier 1) → Codex (tier 2) → Grok or Perplexity (tier 3, Grok unavailable on OpenRouter today) → Meta-Llama (tier 4) → Moonshot or DeepSeek (tier 6).
- **Axis 2 (locality)**: cloud cluster first, local Ollama cluster last, per the 2026-05-23 SNAPSHOT-BEEFSTACK-DIAGNOSTIC operational override that "Local-first in doctrine, cloud-first on this MacBook operationally" — this Mac's hardware cannot reliably default to local inference.

Within each preference tier, the chain provides bucket diversity (paid OpenRouter route → direct provider route → free route, where applicable). This addresses the 2026-05-20 OPENROUTER-STATUS-KNOWLEDGEBASE warning that direct-Mistral and OpenRouter-Mistral-BYOK can share a single rate-limit bucket: each tier now has at least two distinct authentication paths before the chain advances to the next tier.

A `provider_routing:` block was added (cosmetically at config.yaml line 672, since ruamel.yaml appends new top-level keys at the end of the file — functionally equivalent, can be moved by hand later):

```yaml
provider_routing:
  sort: price                  # cheapest OpenRouter sub-provider first
  data_collection: deny        # no sub-provider may train on prompts
```

This is the documented Hermes mechanism (per `features/provider-routing.md`) for the "OpenRouter has paid and free routing options that are configurable" angle. `sort: price` is appropriate given the OpenRouter account near-exhaustion noted below.

## Final state — personal Mac, 2026-06-24

### Hermes

- Launcher: `~/.hermes/bin/hermes-gateway-launch.sh` (mode 700) — bootstrap-token reader + `op run` wrapper
- `~/.hermes/.env` (mode 600): 17 `op://` references + bootstrap `OP_SERVICE_ACCOUNT_TOKEN` + non-secret config + `SUDO_PASSWORD` (unchanged)
- `~/.hermes/config.yaml`:
  - `model:` primary `openrouter / mistralai/mistral-small-2603` (unchanged from drift state; not flipped to OpenClaw's `medium-3-5` choice without explicit doctrine call)
  - `providers:` includes `openrouter`, `mistral-direct`, `perplexity-direct`
  - `fallback_providers:` 16-entry BEEFSTACK-ordered chain (full chain in execution report; reproduced below for vault completeness)
  - `provider_routing:` `sort: price` + `data_collection: deny`
  - `security.redact_secrets: true`
- Daemon: `ai.hermes.gateway` via launchd, currently PID 7319, `LastExitStatus: 0`, command `op run --env-file=~/.hermes/.env -- python -m hermes_cli.main gateway run --replace`

Fallback chain in order (verified via `hermes fallback list`):

```
Primary:  mistralai/mistral-small-2603              (openrouter)

  1. mistralai/mistral-medium-3-5                   (openrouter)        ← Tier 1 Mistral
  2. mistralai/mistral-large-2512                   (openrouter)
  3. mistral-small-latest                           (mistral-direct)    ← direct bucket
  4. anthropic/claude-sonnet-4.6                    (openrouter)        ← Tier 1 Claude
  5. claude-sonnet-4-6                              (anthropic)         ← direct bucket
  6. anthropic/claude-haiku-4.5                     (openrouter)
  7. openai/gpt-5.3-codex                           (openrouter)        ← Tier 2 Codex
  8. openai/gpt-4o-mini                             (openrouter)
  9. openai/gpt-oss-120b:free                       (openrouter)        ← free in tier 2
 10. perplexity/sonar-pro                           (openrouter)        ← Tier 3 Perplexity
 11. sonar-pro                                      (perplexity-direct) ← direct bucket
 12. meta-llama/llama-3.3-70b-instruct:free         (openrouter)        ← Tier 4 Llama free
 13. moonshotai/kimi-k2                             (openrouter)        ← Tier 6 Kimi
 14. deepseek/deepseek-chat                         (openrouter)        ← Tier 6 DeepSeek
 15. devstral:latest                                (ollama)            ← Local (Mac override → last)
 16. codestral:latest                               (ollama)
```

Five distinct provider/auth buckets across the chain: OpenRouter (shared + BYOK), direct Mistral, direct Anthropic, direct Perplexity, local Ollama.

### Local Ollama store

```
NAME                ID              SIZE     MODIFIED    
devstral:latest     9bd74193e939    14 GB    9 weeks ago    
codestral:latest    0898a8b286d5    12 GB    10 weeks ago   
```

`~/.ollama/models` is 25 GB (was 103 GB pre-cleanup). `df` still reports the data volume at 50 GB free / 95% used because nine APFS Time Machine local snapshots (oldest 2026-05-25) still reference the deleted blocks; auto-purge expected within 24 hours of this filing or sooner under space pressure.

### Operational facts at filing time

- OpenRouter account: $10.00 total credits, $9.867 used, **$0.133 remaining**. Bleed of ~$0.20 across the past month (from $0.34 remaining at the 2026-05-23 diagnostic). Live verified via the Management Key. Monthly usage $0.096; weekly BYOK usage ~$0.022.
- The only OpenRouter runtime key is `SWARM ROUTER KEY` (created 2026-04-20, no per-key cap, `is_management_key: false`).
- All "modern" model IDs referenced in the May records (`mistral-medium-3-5`, `mistral-large-2512`, `claude-sonnet-4.6`, `claude-haiku-4.5`, `gpt-5.3-codex`, plus `gpt-oss-120b:free` and the Llama free variants) are live on OpenRouter today (verified via `/v1/models`). The Hermes downgrade observed in earlier backups (2026-05-19 → 2026-06-23) was not forced by model unavailability; its cause remains unrecorded.
- `mistralai/open-mistral-7b` (the broken fallback in the pre-refactor chain) is no longer in Mistral's direct `/v1/models` (77 models verified, this one absent). It was replaced in the new chain by `mistral-small-latest` (confirmed live in Mistral's direct catalog).

## Records ↔ reality reconciliations

- **Hermes config drift gap closed.** Between 2026-05-19 (the last vault-witnessed Hermes config snapshot) and 2026-06-23, the chain had been edited locally without a vault witness. The HERMES-WITNESS-COMPANION-2026-05-25 captured the local Hermes inventory but not the drifted chain shape. This record now captures both the drift (in summary) and the post-refactor state.
- **OpenClaw "removal" disambiguation.** The 2026-05-26 SECURITY-CREDENTIAL-CONTAINMENT record's phrase *"removed from running installation"* applies to Windows-ZBFURY, not this Mac. Confirmed by Logan 2026-06-24. OpenClaw on this Mac is intentional, running, and outside the scope of this session's work.
- **Discord bot 401.** Pre-existing failure unrelated to anything done in this session. The DISCORD_BOT_TOKEN resolves from `op://Vault/Discord OpenClaw Bot/credential` and is bit-identical to what was in `.env` pre-op-rollout (hash `237c38c21436`). The 401 is upstream — likely the Discord allowlist policy from the 2026-05-26 SECURITY-CREDENTIAL-CONTAINMENT record taking effect at the Discord-server level. Not chased in this session.
- **xAI Grok absent from chain.** `x-ai/grok-4`, `grok-4-fast`, `grok-4-fast-reasoning` were not in OpenRouter's `/v1/models` at the time of this session. xAI direct `/v1/models` returned HTTP 403 against the (post-rotation) `XAI_API_KEY`, so direct-xAI model IDs could not be verified. Grok was therefore not added to the chain this session; a future session with a confirmed-working xAI direct model ID could slot it into Tier 3 alongside Perplexity.

## Out of scope (deferred to future sessions)

- **OpenClaw fallback chain refactor.** OpenClaw uses JSON for its config (`~/.openclaw/openclaw.json`), which does not natively interpolate environment variables. Bringing OpenClaw to the same posture as the new Hermes config requires either a template-render step in OpenClaw's launch path or upstream OpenClaw work. OpenClaw's current chain matches the 2026-05-20 SNAPSHOT-OPENROUTER-HERMES-OPENCLAW-KEYS snapshot exactly (no drift).
- **OpenRouter credit topup.** Logan's decision; flagged because the chain's first nine entries route through OpenRouter and the account has $0.13 remaining. The new free-tier entries (`gpt-oss-120b:free` at slot 9, `llama-3.3-70b-instruct:free` at slot 12) are the credit-exhaustion safety net.
- **`provider_routing:` block cosmetic move.** Currently at config.yaml line 672 because ruamel.yaml appended it. Functionally fine; visually distant from `model:` / `fallback_providers:`. Manual move when convenient.
- **Discord allowlist reconciliation.** Per the 2026-05-26 SECURITY-CREDENTIAL-CONTAINMENT record, Discord policy was moved to allowlist. The Hermes bot may need to be re-added to the allowlist at the Discord server level for messaging-gateway functionality to resume. Out of scope for this session.
- **Nous Portal OAuth + OpenCode provider.** Both have credentials in 1Password (`Nous Research`, `OpenCode API Key`) but require interactive setup (`hermes setup --portal`) or model-ID verification not run this session.
- **APFS local snapshot purge.** macOS will auto-purge within 24h. Manual purge available via `tmutil deletelocalsnapshots` if disk pressure becomes acute.
- **Dotdir reconciliation.** A separate Codex agent is building bidirectional sync between per-machine dotdirs and the vault, currently focused on machine-to-vault flow, paused as of 2026-06-24, expected to resume in a few days. Once it lands, the local changes documented here will be sync-witnessed by it; this record is the manual interim witness.

## Memories filed in companion to this work

Behavioral memories saved to my agent memory store (path: `/Users/logan/.claude/projects/-Users-logan/memory/`) during this session, all referenced here so the vault holds a pointer to them:

- `feedback_secret_hygiene.md` — never print full secret values; hash/truncate/filter env+process probes before display. Triggered by an unforced leak of xAI and OpenAI runtime keys via `ps -E` mid-session; Logan rotated both before further work continued.
- `feedback_records_vs_doctrine.md` — vault records inform; doctrine binds; do not elevate records to doctrine without Logan's say-so. Triggered after I repeatedly called the BEEFSTACK record "doctrine" in violation of its dated WIP status.
- `project_openclaw_machine_policy.md` — OpenClaw permitted on personal Mac, disallowed on professional Windows-ZBFURY; clarifies the SECURITY-CREDENTIAL-CONTAINMENT record's scope.
- `project_dotdir_reconciliation.md` — Codex on Windows is building Python + rsync/rclone bidirectional sync; machine-to-vault direction is the current focus; may need gentle Mac retooling when it lands here.

## Backups for rollback

If any element of this session's work needs to be reverted, the relevant local files all have timestamped backups under `~/.hermes/`:

- `.env.bak.preopref.20260624-010919` — pre-op-rollout Hermes env
- `config.yaml.bak.preredact.20260624-011436` — pre-redaction-enable config
- `config.yaml.bak.prefallbackv3.20260624-184020` — pre-fallback-v3 config
- `.env.bak.prefallbackv3.20260624-184020` — pre-fallback-v3 env
- `~/Library/LaunchAgents/ai.hermes.gateway.plist.bak.preopref.20260624-011047` — pre-op-rollout launchd plist

Rollback procedure for any sprint: restore the relevant backup, run `launchctl unload ~/Library/LaunchAgents/ai.hermes.gateway.plist && launchctl load -w ~/Library/LaunchAgents/ai.hermes.gateway.plist`. The launcher shim file at `~/.hermes/bin/hermes-gateway-launch.sh` can be deleted to fully revert Sprint 1 (the original plist backup invokes Python directly without the shim).

## Signed

`*.claude.*` — Direct Write tool tier, personal-Mac authority surface. Name and office both unnamed (wildcard) — no granted standing to claim.
Filed 2026-06-24 at the close of the working session
