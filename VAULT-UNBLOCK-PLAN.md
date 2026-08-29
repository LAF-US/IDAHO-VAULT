# IDAHO-VAULT — unblock plan
Assembled 2026-08-28 by the MacBook Claude session, with measurements from the
Windows session. **Nothing in this document has been executed.** No pushes, no
rewrites, no deletions, no rotations were performed while you were asleep.

---

## 1. What is actually blocking convergence

Neither machine is failing for a git reason. Both are stopped by the same two
real conditions:

**Blocker 1 — live secrets in history.** 18 GitHub secret-scanning alerts, all
still `open`, all raised 2026-08-13 (the morning after the Aug 12 push). The
Windows pre-push hook independently catches a Mistral key at
`61b78c295f` (2026-04-22) and refuses. Every push path hits this.

**Blocker 2 — objects GitHub will not accept.** 11 LFS objects over the 2 GiB
per-object limit and 35 non-LFS blobs over 100 MiB. These are rejected
server-side; no hook change, flag, or branch strategy affects them.

Blocker 1 is yours to clear (rotation is account work, only you can do it).
Blocker 2 is a storage-tier decision, not a git problem.

---

## 2. Rotation checklist — the 18 open alerts

All are at https://github.com/LAF-US/IDAHO-VAULT/security/secret-scanning

| Alert | Service | Notes |
|---|---|---|
| 34 | OpenAI API Key | |
| 29 | Anthropic API Key | |
| 21, 23 | Mistral AI API Key (x2) | 23 is in `.vibe/.env`; 21 in `.hermes/` |
| 20, 28 | OpenRouter API Key (x2) | 28 is the most widely-copied secret |
| 25 | DeepSeek API Key | |
| 31 | Perplexity API Key | |
| 22 | xAI API Key | |
| 26 | Hugging Face User Access Token | no current `.env` copy |
| 18 | Google API Key | |
| 17 | GCP key bound to a service account | no current `.env` copy — highest blast radius |
| 19 | 1Password Service Account Token | can reach other credentials |
| 27, 30 | GitHub OAuth Access Token (x2) | no current `.env` copy |
| 33 | GitHub Personal Access Token | |
| 32 | Discord Bot Token | |
| 24 | Telegram Bot Token | |

**Rotate first, regardless of order elsewhere:** 19 (1Password service account)
and 17 (GCP service account). Those two can be used to obtain further
credentials, so they compound. 33 (GitHub PAT) is third — it has write access to
this repo.

Alerts 17, 26, 27, 30 exist **only** in backups, state snapshots, and agent
transcripts — there is no current `.env` holding them. They were still
published, so they still need rotating; you just will not find them by grepping
your live config.

After rotating each, close its alert in the GitHub UI as "revoked". That is what
turns the list from 18 to 0 and is the gate for everything downstream.

---

## 3. Where the secrets live — five families, not 88 paths

88 (alert, file) pairs collapse into five classes:

| Family | Alerts | Files | What it is |
|---|---|---|---|
| A. `.hermes/` credential store | 14 | 11 | `.env`, its `.bak.*` copies, `state-snapshots/**/.env` and `auth.json` |
| B. `.vibe/` credential store | 1 | 1 | `.vibe/.env` |
| C. Obsidian plugin data | 2 | 2 | keys pasted into `ai-image-analyzer`, `ai-templater` settings |
| D. SQLite state / WAL | 2 | 6 | `state_5.sqlite.home*`, `logs_2.sqlite-wal.home*` |
| E. Agent session transcripts | 10 | 10 | `rollout-*.jsonl`, `session-*.jsonl`, uuid `.jsonl` |

`.hermes/.env` alone carries 13 of the 18. It is the origin; everything else is
a derivative — a backup of it, a snapshot of it, or an agent transcript that
read it and logged the value.

**The lesson worth keeping:** family E means agents writing their own transcripts
into the vault turned a single `.env` leak into a ten-file leak. Any scrub that
misses the transcripts leaves the secrets published.

These are classes with predicates, not enumerated paths — a scrub can target
them by rule.

---

## 4. Windows side — measurements pending

_(This section fills in when the Windows session reports back: exact pre-push
hook text, the oversize inventory split into vault content vs. regenerable, and
whether the 38,443-commit backlog is real work or an artifact of the
disconnected roots.)_

Known so far:
- Windows `logan/obsidian` is 0 behind / **38,443 ahead** of origin. That backlog
  has never been pushed and cannot be until both blockers clear.
- Largest offenders: `XD4_6602.MXF` 21.03 GiB, `VTR11_26_Jeff Seward_Ralph_Smeed.mov`
  20.86 GiB, `XD4_6594.MXF` 19.35 GiB, `953_0116.MXF` 17.98 GiB.
  These are your journalism — interviews and footage. They are **not** discardable;
  they belong in annex, not GitHub.
- ~19.2 GiB of Ollama model weights are regenerable and are the obvious thing to
  stop tracking.

---

## 5. A hook defect, found in passing

The Windows pre-push hook does:

    base=$(git merge-base "$local_oid" "$default" 2>/dev/null || echo "$default")

When `merge-base` fails — which it does, because the April 2026 "Clean history -
secrets purged" run created **new roots** instead of rewriting in place, leaving
22 root commits — the `||` substitutes the *ref name* as the base. The hook then
diffs two unrelated trees (11,729 files), hands them all to `trufflehog
filesystem`, and many no longer exist on disk. Exit 123 is xargs relaying the
failure.

So the "trufflehog scan error" is not a scanner problem and not a second secret.
It is the disconnected-roots problem surfacing as a hook crash — the same
condition the 7 local grafts here were built to paper over.

This Mac's `.githooks/pre-push` is only the stock 3-line git-lfs hook, so the
gitleaks/trufflehog version either lives in the 156 commits we are missing or
was never committed. That answer decides whether a fix propagates by merge or
has to be applied per machine.

---

## 6. Proposed sequence

1. **Rotate** the 18, starting with 1Password (19), GCP (17), GitHub PAT (33).
   Close each alert as revoked.
2. **Decide the annex boundary** for the oversize objects — which media moves to
   annex, which regenerable bulk stops being tracked. Nothing is deleted.
3. **Scrub** history for the five families. This is the irreversible step and
   wants a full anchor bundle in front of it.
4. **Then** converge: merge and push. Both machines onto `origin/logan/obsidian`.

Steps 1 and 2 are independent and can happen in either order. Step 3 must not
start before 1 is done — scrubbing a still-live key accomplishes nothing.

---

## 7. Already done and safe

Your 8 Mac-only commits — the only content that existed on exactly one machine
and nowhere else — are bundled:

    ~/Desktop/mac-ahead-20260828.bundle
    sha256 d7fa9d94e7c9495dbb06492f164ad51f25da24593e27b27b8e00ef3541eec8ea
    tip 280064b3de · needs 56ee52ed18, ecb3083e45 (both already on origin)

Scanned clean. The 26 gitleaks hits in them are Discord's own published
documentation samples, not your credentials.
