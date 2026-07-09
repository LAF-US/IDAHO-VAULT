---
name: feedback-secret-hygiene
description: "Never publish ANY derived fingerprint of a real secret value in chat output — not raw, not truncated, not hashed. Hashing is an internal comparison primitive only. User-facing reports surface boolean/categorical outcomes (matches/doesn't match, present/missing, rotated/not), never derived fingerprints. Applies even when the local repo has secret scanners (IDAHO-VAULT does); the agent layer must practice hygiene independently."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4f03d270-3e64-41cc-b325-30871ab76d55
---

Never emit anything derived from a real secret value in chat output. That includes:

- **Raw values** — the obvious case
- **Truncated prefixes / suffixes** — even 4–8 chars of a 32-char key is a unique partial fingerprint
- **Hashes** — sha12/sha8/even a single fingerprint byte is a unique correlatable identifier tied to the real bytes
- **Combinations of length + family-prefix** when the family-prefix narrows the possibility space (e.g., `len=72 starts-with-sk-ant`)

Hashing is a comparison primitive for INTERNAL use (compare two values without printing either; pipe each to `shasum`, diff the hashes, print only a boolean). It is NOT authorization to publish the hash to the user.

**Why this rule:**

On 2026-06-24 I leaked plaintext xAI and OpenAI API keys into a transcript by probing `ps -E -p $CHILD | grep -E "^OPENAI_API|^XAI"` — full key bytes printed before I could redact. Filed the original version of this memory in response. Logan rotated both keys.

On 2026-06-28 I leaked sha12 prefixes for DISCORD_BOT_TOKEN, OPENROUTER_API_KEY, ANTHROPIC_API_KEY, MISTRAL_API_KEY into chat as a "verification table" — and worse, paired them with rotation-status metadata ("flagged for rotation but apparently not rotated yet"), which both proves the un-rotated state of each named key and lets anyone with the value elsewhere correlate. Logan called it out: *"bro you cannot be putting raw values in the chat like that, especially in a message about having recommended rotating those very values. basic hygiene…"* Four more rotations recommended as a result.

The pattern across both incidents: I prioritized *evidence-of-work-shown-to-user* over *secret-doesn't-touch-output*. The user does not need the fingerprint to trust the verification result — they need the categorical outcome.

**How to apply:**

- **For "does this var exist?" checks** — `printf "VAR: present=%s len_class=%s\n" "$([ -n "$VAR" ] && echo yes)" "$(test -z "$VAR" && echo n/a || ([ ${#VAR} -lt 30 ] && echo short || echo full))"`. Never the actual length, since length can be a fingerprint (Spotify client ID = 32, sk-ant = 108, etc. are recognizable). Coarse length-class is OK; precise length is borderline.
- **For "do two values match?" checks** — internally `[ "$(printf %s "$A" | shasum)" = "$(printf %s "$B" | shasum)" ] && echo MATCH || echo DIFFERS`. Print only `MATCH` or `DIFFERS`. Don't show the hash to the user.
- **For "did the value survive transformation X?"** — internally compare hashes before/after, print boolean: `unchanged ✓` or `changed ✗`. Never the hashes themselves.
- **For env probes** — explicitly exclude secret-shaped var names (`*_KEY`, `*_TOKEN`, `*_SECRET`, `*_PASSWORD`, `*_API*`) and only show counts / non-sensitive vars.
- **For `op` CLI** — masked output is a feature. Don't add `--no-masking` to "see what's there." If you must verify a value resolved correctly, do it inside a child shell that only emits boolean/categorical output (`op run -- sh -c 'test -n "$VAR" && echo OK || echo MISSING'`).
- **For verification reports to the user** — surface the categorical conclusion (`all 4 sampled secrets hash-stable across load_hermes_dotenv`) without the comparison values. The user trusts the outcome; they don't need the supporting digits.
- **For "what changed?" diffs across two secret-containing states** — describe by category (`new key present, old key absent`) or by count (`23 of 23 resolved`); never by content fingerprint.
- **Treat any accidental publication as a compromise.** Immediately notify Logan, recommend rotation for every key whose fingerprint (in any form) appeared, and note the blast radius (chat-only / vault / GitHub / etc.).
- **Session logs at `~/.hermes/sessions/` and `~/Library/Application Support/Claude/...` retain everything.** Even a chat-only leak persists on disk. Recommend rotation regardless of whether the leak reached external surfaces.

Related: [[agent-infrastructure]] (Hermes/OpenClaw credential surfaces), [[claude-vault-address]] (Direct Write tier — leaks here are on me, not the harness), [[records-vs-doctrine]] (self-validating "I hashed it, so it's safe" is the same anti-pattern in a different costume).
