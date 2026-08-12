# Redactions — Spelunking Census run 1  (2026-06-28)

A peer review (Claude Code) flagged an internal IP address in the recovered
transcripts on this branch. On verification, the runtime residue below was removed
from four cold-read reports. Values are described by class, not reproduced (so this
note itself stays clean). Except the tool-result path, each was the **vault's own
configuration**, quoted verbatim by a cold reader — not sandbox infra.

| file | class removed | replaced with | source |
| --- | --- | --- | --- |
| machinery/Dipswitch.md | a private RFC-1918 (10/8 block) IP + its UNC share host | `[internal-ip redacted]` | vault `.gitconfig` safe-directory entry |
| machinery/Sieve.md | a loopback Obsidian-REST endpoint + port | `localhost:<redacted-port>` | vault `obsidian_rest_api_client.py` (loopback; non-sensitive) |
| lore/D03-Augur.md | a sandbox tool-result file path | `[tool-result file, path redacted]` | this run's sandbox (genuine infra residue) |
| machinery/Sounding.md | a local-desktop path carrying the owner's OS username | `C:\\Users\\<user>\\…` | vault config (local desktop path) |

**Root-exposure note — NOT mine to fix, flagged for Logan:** the private IP and the
desktop-path username are themselves committed in the vault's own config files on this
public repo. Redacting these transcripts removes the *duplication* I introduced; it does
not remove the *original* exposure. The tinkerer touches no existing vault file — Logan's call.

**History note:** the pre-redaction blob remains in this branch's git history (the prior
commit). Purging it needs a history rewrite / branch reset — a destructive op held for
Logan's explicit go-ahead.

— `*.hyperagent.tinkerer` (Opus 4.8 guest run). I propose; Logan inscribes.
