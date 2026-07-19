---
date: 2026-06-30
filed_by: "*.claude.*"
authority: LOGAN
machine: personal-MacBook (MacBookPro12,1, macOS 12.7.6, 16 GB RAM)
doc_class: witness
status: filed
subject: Structural containment around secret-bearing files — "don't promise to be careful, close the leak path." Filed after four secret-hygiene incidents across the 2026-06-23 → 2026-06-30 Hermes arc, named "the diaper rule" by Logan after the third+fourth incidents in a single turn.
related:
  - HAT-ON-A-HAT-WITNESS-2026-06-30.md
  - HERMES-WORKAROUND-WITNESS-2026-06-28.md
  - .claude/MEMORY/CLAUDE-SESSION-2026-06-29.md
tags: [witness, anti-pattern, secret-hygiene, structural-containment, doctrine]
---

# The Diaper Rule

*Filed 2026-06-30 after Logan named the structural shape required to stop a four-event leak streak. The companion to [[HAT-ON-A-HAT-WITNESS-2026-06-30]] — that one named the architectural-defense-as-pile-up anti-pattern; this one names the same shape applied to secret-hygiene defenses. "Wear a diaper rather than insist you'll try harder not to shit the bed."*

## The pattern

Reactive redaction is filter-shaped: I anticipate what kinds of bytes will appear, write a `sed` or comparable transform, pipe output through it, and trust the filter to clean what I missed. Every leak event in the streak below is the same shape: my filter caught the cases I anticipated, the value reached chat anyway, because the value's surface form didn't match my regex.

The diaper is the inverse shape: the probe **cannot** put the value on stdout in the first place. Not because of a filter that catches output, but because the data path from file → chat is structurally severed. The probe reads what it needs for its decision, but its stdout shape carries only category facts — `header_present=true`, `scheme="https://"`, `value_length_class="short"` — never values.

The promise version sounds like *"I'll be more careful next time."* The diaper version sounds like *"I am not allowed to issue the Bash commands that would have leaked it."*

## The case (four events, 2026-06-24 → 2026-06-30)

| # | Date | Probe | Leak surface |
|---|---|---|---|
| 1 | 2026-06-24 | `ps -E -p $CHILD \| grep -E "^OPENAI_API\|^XAI"` | Full raw OpenAI + xAI API keys printed to chat — `ps -E` includes the env of every process, and the grep pattern matched the lines but did not filter the values. Logan rotated both. |
| 2 | 2026-06-28 | `printf` of `sha12` hash prefixes for four named keys in a "verification table" alongside rotation-status metadata | Each fingerprint became a correlatable identifier tied to a specific named key with rotation-state context. Logan: "you cannot be putting raw values in the chat like that, especially in a message about having recommended rotating those very values. basic hygiene…" |
| 3 | 2026-06-30 (same turn as 4) | `python -c "...json.dumps(mcp_servers)..."` to inspect Hermes MCP config structure | The full `obsidian-vault` `Authorization: Bearer <token>` value printed unredacted. No filter applied — I "knew it wasn't an `.env`" and didn't reach for the redaction sed I'd been using on log probes. |
| 4 | 2026-06-30 (same turn as 3) | `grep -A 8 "obsidian-vault:" config.yaml \| sed 's/(Bearer ).*/\1[REDACTED]/'` to verify the config edit | The sed matched lines containing `Bearer ` but the actual token value rendered on a **continuation line** in the YAML output. The filter's pattern was wrong about which line carried the value. Same value as #3, no new blast radius, but the *filter failed exactly as the diaper rule predicts a filter will.* |

The first two had different surface shapes (raw / hashed). The second two had the same value with different leak vectors, in a single turn. The pattern across all four: **I trusted a redaction filter to know what to scrub. The filter's correctness was reasoning about surface forms I anticipated. The value's surface form was something else.**

## The rule

For files in **the secret set** — currently:

- `~/.hermes/.env`
- `~/.hermes/auth.json`
- The `mcp_servers.*.headers` blocks of `~/.hermes/config.yaml` (treated as secret-bearing even though the file as a whole is not)
- `.bak.*` snapshots of any of the above
- `~/.openclaw/secrets/*` (if/when present)
- Any path matched by `*/secrets/*`, or whose contents are known to include `Authorization`, `Bearer`, `Token`, `_KEY=`, `_TOKEN=`, `_SECRET=` lines

The rule has three clauses:

1. **No Bash command that puts contents of these files on stdout.** Not `cat`, not `grep`, not `sed -n`, not `head`, not `tail`, not `awk` that prints lines, not `od`, not `xxd`. The list is exclusionary, not "use redaction with these" — output filters are reactive scaffolding that catches anticipated surface shapes only.

2. **For editing**: use commands whose stdout is decoupled from file content. `sed -i` (in-place), Python text manipulation that writes via `Path.write_text()` (no `print` of the touched content), `op read <ref> > file` (`op` masks its stdout when piped to a TTY but value-to-file via redirect is fine), `cp` for backups. These touch the file without ever streaming its bytes through my output channel.

3. **For verifying**: parser-level introspection that returns only key NAMES and category facts. The probe's `print` statements emit constants, booleans, or enums (`"PRESENT"`, `"MISSING"`, `"scheme: https://"`, `"length_class: full"`), never values read from the secret-bearing field. The probe is structurally incapable of leaking the value — the read path branches into a category test, not a string-format-and-print.

### Practical examples

Wrong — reactive redaction:

```bash
grep -A 8 "obsidian-vault:" ~/.hermes/config.yaml | sed 's/Bearer .*/Bearer [REDACTED]/'
# Filter fires on lines matching the pattern. Continuation lines, JSON dumps,
# unusual whitespace all sail past.
```

Right — structural containment:

```python
import yaml
d = yaml.safe_load(open("/Users/logan/.hermes/config.yaml"))
entry = d["mcp_servers"]["obsidian-vault"]
print({
    "url": entry.get("url"),                      # non-secret
    "ssl_verify": entry.get("ssl_verify"),         # non-secret
    "headers_present": bool(entry.get("headers")), # category
    "enabled": entry.get("enabled"),               # non-secret
})
# No bytes from entry["headers"] are formatted into any string sent to stdout.
```

Wrong:

```bash
cat ~/.hermes/.env | grep DISCORD_BOT_TOKEN
# Even if the grep pattern matches just the line, the value is printed.
```

Right:

```bash
test -n "$(awk -F= '$1=="DISCORD_BOT_TOKEN" {print "PRESENT"}' ~/.hermes/.env)" && echo present || echo missing
# awk's print emits the literal string "PRESENT", not the value.
```

When in doubt, the probe's stdout should be composed entirely of strings I literally typed, plus enumerated values like `True`/`False`. If any string in the output is derived from a read of a secret-bearing field, the diaper is off.

### Editing the secret set

For situations where the goal IS to handle the value (e.g., the 2026-06-30 revert that re-resolved `.env.op` to plaintext `.env`): the value lives in a shell variable that gets `printf`'d straight to a file via redirect. The shell variable's contents never reach stdout, only the file. Verification of the edit is categorical — line count before/after, key-by-name presence check.

This is how the 2026-06-30 revert was actually executed cleanly. The pattern works. The leaks happened on *other* operations the same day where I forgot to apply the same discipline.

## Why each step felt locally safe

- Probe #3 (the `json.dumps`): I was inspecting Hermes' MCP config to find what server to debug. The file as a whole — `config.yaml` — is mostly not secret, just configuration. I treated it as a "non-secret file" rather than as "a non-secret file with a small secret-bearing subtree." The subtree (`mcp_servers.<name>.headers`) is the secret set element; the rest of the file isn't.
- Probe #4 (the `grep | sed`): I'd just been caught leaking once; my response was to add a redaction filter. The filter was for the surface shape I'd just seen leak — the bearer value rendered as a single line. The YAML rendered it on two lines this time. Same anti-pattern as the workaround stack: defending the broken approach instead of switching approaches.

Both steps were the same root failure: **trusting filters to catch what I didn't anticipate**, when the diaper version — structurally cutting the read-to-stdout path for the secret-bearing subtree — would have prevented the leak regardless of surface form.

## Anchor in vault doctrine

This sits in the same shape as the [[smoke-detector-rule]] (`AGENTS.md:52`): both call out *patching the alarm instead of removing the cause*. The Smoke Detector Rule applies to error signals — don't silence the alarm; fix the fire. The Diaper Rule applies to secret hygiene — don't filter the leak; close the path the leak comes through. Both are structural-over-promise rules. Both name the same architectural error: defending the broken approach instead of replacing it.

Companion to [[HAT-ON-A-HAT-WITNESS-2026-06-30]] (workarounds accreting defensive scaffolding) and supports the existing salvaged rule "Secret hygiene — no derived fingerprint in user-facing output" in [[CLAUDE-SESSION-2026-06-29]]. The Operational Rule is the *what*; this witness is the *how-to-actually-enforce-it-mechanically*.

## Signed

`*.claude.*` — wildcard name (Logan has not performed a naming act), claude lineage, wildcard office. Direct Write tool tier; this is a local-machine retrospective filed at vault root, within the scope of that tier.

###### "The world is quiet here."
