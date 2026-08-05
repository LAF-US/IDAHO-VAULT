---
date: 2026-06-28
filed_by: "*.claude.*"
authority: LOGAN
machine: personal-MacBook (MacBookPro12,1, macOS 12.7.6, 16 GB RAM)
doc_class: witness
status: filed
subject: Local env-loader override workaround applied — secrets split out of ~/.hermes/.env into sibling ~/.hermes/.env.op, shim resolves via `op read` and exports to process env before exec'ing Hermes. Cloud routes now functionally unblocked.
related:
  - "HERMES-WITNESS-COMPANION-2026-06-24.md"
  - "!/SIGNALS/TOUCHING-ME-TOUCHING-NOUS-2026-06-25.md"
  - "https://github.com/LAF-US/IDAHO-VAULT/issues/690"
  - "https://github.com/NousResearch/hermes-agent/issues/19201"
  - "https://github.com/NousResearch/hermes-agent/pull/18734"
  - "https://github.com/NousResearch/hermes-agent/issues/36949"
tags: [witness, hermes, workaround, env-loader, op-resolution, beefstack, secret-hygiene]
---

# Hermes env-loader override workaround applied

*Filed 2026-06-28 to mark a material local change to this MacBook's Hermes setup — a reversible workaround that brings cloud-routed credentials back online while upstream `NousResearch/hermes-agent#18734` (the override-flag fix) is in review.*

## The bug being worked around

`hermes_cli/env_loader.py:168` calls `_load_dotenv_with_fallback(user_env, override=True)`, which causes `~/.hermes/.env` values to clobber whatever's already in `os.environ` on every chat-subprocess spawn. With the `op run --env-file=.env` pattern used by this Mac's launch shim, that means the resolved secret bytes injected by `op run` get clobbered back to the literal `op://...` strings from `.env`. Hermes then sends `Authorization: Bot op://Vault/Discord OpenClaw Bot/credential` to upstream APIs and 401s across every cloud-routed call.

Diagnosed during the session arc opened by `HERMES-WITNESS-COMPANION-2026-06-24.md` (op:// rollout) and `!/SIGNALS/TOUCHING-ME-TOUCHING-NOUS-2026-06-25.md` (upstream cross-link comments to Nous Research).

## Shape of the workaround

Secrets are split out of `~/.hermes/.env` (which `load_hermes_dotenv` reads) into a sibling file `~/.hermes/.env.op` (which it does NOT read — it's an intentionally non-`.env`-named file from python-dotenv's perspective, even though structurally `.env`-shaped).

| File | Contents | Loaded by `load_hermes_dotenv`? |
|---|---|---|
| `~/.hermes/.env` | 14 lines: `OP_SERVICE_ACCOUNT_TOKEN` (bootstrap), `SUDO_PASSWORD`, plaintext config vars (ALLOWED_USERS, HOME_CHANNEL, TERMINAL_*, WHATSAPP_*, etc.) | Yes — but no secret-bearing keys present, so nothing to clobber |
| `~/.hermes/.env.op` | 23 `KEY="op://Vault/Item/credential"` references for every secret-bearing env var | **No** — Hermes never reads it |

The launcher shim at `~/.hermes/bin/hermes-gateway-launch.sh` now:

1. Reads `OP_SERVICE_ACCOUNT_TOKEN` from `.env` (so `op read` can authenticate)
2. Iterates `.env.op`, calls `op read <ref>` per line, exports the resolved value into process env
3. Execs the daemon command directly — no `op run` wrapper, since the op:// refs aren't in `.env` anymore for the dotenv-loader to find or clobber

`load_hermes_dotenv()` still runs on Hermes startup, still reads `.env`, but the secret-bearing keys are NOT in `.env` — so `override=True` is operationally a no-op for them. The shim-resolved process-env values survive into the daemon. Verified at the Python loader level: `DISCORD_BOT_TOKEN`, `OPENROUTER_API_KEY`, `ANTHROPIC_API_KEY`, `MISTRAL_API_KEY` all hash-stable across the `load_hermes_dotenv()` call (categorical: unchanged ✓ — no fingerprints recorded here).

The daemon launchd plist `~/Library/LaunchAgents/ai.hermes.gateway.plist` is unchanged — still invokes the shim as `ProgramArguments[0]`. The `~/.hermes/config.yaml` `fallback_providers:` list, the `provider_routing:` block, and all other Hermes config is unchanged.

## Why a workaround rather than a local patch to Hermes

Three reasons:
1. Patching `env_loader.py:168` locally would get clobbered on the next `hermes update`. The split is durable across upgrades.
2. The upstream PR `NousResearch/hermes-agent#18734` is well-reviewed and likely to merge; once it does, the workaround can be reverted (or kept — it still works regardless of the override flag's value).
3. The workaround keeps op:// references the canonical credential representation in our config tree, just at a slightly different path. When the native 1Password backend (`NousResearch/hermes-agent#36949`) eventually lands, the migration is mostly a rename.

## Cost

- ~17 sequential `op read` calls at daemon launch (vs one `op run` invocation pre-workaround). ~5–15 seconds of extra startup latency, measurable but acceptable for a daemon that bounces rarely.
- One extra file to keep aware of (`~/.hermes/.env.op`) and to handle in any dotdir-reconciliation sync work.
- Documentation overhead: README + this witness + memory updates + tracker comment + inline shim comments.

## Hygiene properties

- Resolved secrets live only in process env for the daemon's lifetime. No tmpfs file, no `.env` modification, no plaintext on disk. Same envelope as the pre-workaround `op run --env-file` approach.
- Both `.env` and `.env.op` are mode 600.
- Shim fails loudly (`exit 79`) if any single `op read` returns empty or errors — daemon refuses to start with partial credentials.

## Documentation and backups

- `~/.hermes/README-workaround.md` — full operator-facing doc with revert procedure
- `~/.hermes/bin/hermes-gateway-launch.sh` — inline header comment block with bug context, upstream issues/PR, and pointer to README
- `~/.hermes/.env.bak.preworkaround.20260628-212323` — pre-split `.env` snapshot
- `~/.hermes/bin/hermes-gateway-launch.sh.bak.preworkaround.20260628-212323` — pre-workaround shim snapshot
- `LAF-US/IDAHO-VAULT#690` comment 4828719784 — tracker breadcrumb

## Revert path (when #18734 lands)

Two options, both documented in `~/.hermes/README-workaround.md`:

- **Option A — keep the workaround.** It still works regardless of the override flag. Slower at startup; otherwise identical behavior.
- **Option B — revert to the simpler shim.** Four-step procedure: move op-refs back from `.env.op` into `.env` → delete `.env.op` → restore the pre-workaround shim from the backup → bounce daemon. Cleared 4-step list in the README.

## Session-arc context (second secret-hygiene incident, corrected)

During the verification of this workaround, a second secret-hygiene incident occurred and was corrected: derived fingerprints of real secret bytes were emitted in chat output. Logan called this out as the same anti-pattern that produced the earlier `ps -E` leak (2026-06-24), and the hygiene rule was broadened — derived fingerprints (raw, truncated, hashed, length-fingerprinted, family-prefix-leaked) of real secret bytes are all forbidden in user-facing output. Hashes are an internal comparison primitive only. User-facing reports surface categorical outcomes (match/no-match, present/missing, unchanged/changed) and nothing else. This witness records categorical outcomes only, per the corrected rule.

## Signed

`*.claude.*` — wildcard name (Logan has not performed a naming act), claude lineage, wildcard office. Direct Write tool tier; this is a local-machine change to a personal-Mac surface, within the scope of that tier.

###### "The world is quiet here."
