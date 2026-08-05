---
date: 2026-07-02
filed_by: "*.claude.*"
authority: LOGAN
machine: personal-MacBook (MacBookPro12,1, macOS 12.7.6)
doc_class: incident-record
status: RESOLVED — history scrubbed + verified; ADB + Dropbox keys rotated (Logan, 2026-07-02); only GitHub dangling-object GC / fork cleanup residual
subject: Secret exposure in the PUBLIC repo LAF-US/IDAHO-VAULT. MASS-SORT (0ae47c135, committed by the obsidian-plugin[git] persona — Logan's Obsidian Git plugin — executing Logan's sort) swept ~/ software-imported persona chambers (dotfolders) into the vault. Content-verified exposure is narrow — the Android debug key + two Dropbox host-key files — in formats no token-scanner detects. GitGuardian flagged the Android key post-push; every in-vault control missed everything. Root cause includes a "secret guard" that matched paths/tokens, not secret material (POSIWID).
related:
  - "https://github.com/LAF-US/IDAHO-VAULT/issues/725"
  - .claude/MEMORY/CLAUDE-SESSION-2026-06-29.md
tags: [incident, secret-leak, public-repo, secret-scanning, mass-sort, corrections]
---

# Secret-leak incident — 2026-07-02

*Record of a multi-secret exposure in the public vault, the control-failure post-mortem, the agent-side remediation, and the Logan-gated actions that remain. No secret bytes appear in this file.*

> **SCRUB EXECUTED 2026-07-02 (this session).** The remediation landed as commit `ba28e7913` on `logan/obsidian`; `git filter-repo` then purged `.android/adbkey`, `.android/adbkey.pub`, and both Dropbox `hostkeys` from all history (4,049 commits rewritten), force-pushed to the public remote. **Verified:** 0 commits carrying those paths across **all 163 branches**; `main` never carried them; local and remote tips match. **Rotation DONE (Logan, 2026-07-02):** ADB key revoked + regenerated on the Pixel; this computer unlinked from Dropbox — the exposed key material is now dead. **Residual (low, optional):** GitHub retains the old commit `0ae47c135` as a dangling object reachable by direct SHA until it garbage-collects (GitHub Support can expedite); any fork retains the old history. With the keys rotated, this residual is inert. Details below.

## What leaked (corrected scope)

MASS-SORT commit `0ae47c135` (2026-07-02 00:46, pushed to public branch `logan/obsidian`) added `~/` dotfolders to the vault. In the documented vocabulary these are **software-imported persona chambers** (`STUB-PERSONAFOLDERS-2026-05-03`; `PERSONAE-ENGINE-v1` — *each coordinate maps to a dotfolder lens*), the same class as `.claude/`, `.codex/`, `.gemini/`. They are **not** "non-vault cruft"; the fault is that their vendor **runtime payload includes credentials** and landed on a public surface. The vault already models the fix: `.claude/` is a tracked persona chamber whose credential payload (`.claude/.credentials.json`, `.claude/projects/`, `.claude/file-history/`) is selectively gitignored — the chamber keeps its identity, the payload stays off git. Confirmed credential-bearing payloads:

**Content-verified secret material (only these):**
- **`.android/adbkey` (+ `.pub`)** — ADB device debug key (private key). GitGuardian-flagged. Logan removed from tip + ignored at 01:17 (`2c7fc93ea`); **still in history at `0ae47c135`**.
- **`.dropbox/instance1/hostkeys` + `.dropbox/instance_db/hostkeys`** — raw device key material (81 bytes each, high entropy). **Still tracked at tip** until this session's staged removal.

**Content-verified NOT secrets (record-for-repair — my path-flagging was wrong):** a first pass flagged the whole `.dropbox/` tree, `.docker/config.json`, `.colima/ssh_config`, and `.subversion/servers`+`config` as "credential-bearing." Running the *content* guard against each shows **no secret material**: `.docker/config.json` has **no inline `auth`** (Docker Desktop is keychain-backed); the Dropbox `.dbx`/sqlite files are account **state**, not extractable keys; colima/svn are config. Those 24 files were flagged by **path, not content** — the exact path-theater this incident is about — and have been **restored to tracking**. They remain **privacy-sensitive account state on a public repo**, which is a persona-chamber Intake/privacy decision for Logan (below), *distinct from the secret question*.

**Also corrected:** the `-----BEGIN…PRIVATE KEY-----` "hits" in `closed_prs.json` / `unmerged_prs.json` were a **false positive** from a too-loose `grep -e "BEGIN.*PRIVATE KEY"`. Strict PEM-header count is **0** in both — a prose mention, not key material.

**Not exposed (verified):** `.op/openrouter.env` (real `sk-or-` keys) is correctly gitignored — only templates/docs are tracked. No full-length live cloud-API-key shapes (OpenRouter/Anthropic/OpenAI/Google/GitHub-PAT/AWS) are in any tracked file.

## Why every control missed it (post-mortem)

Two independent failures, either alone fatal:

**1 — nothing was positioned on the commit path used.** The commit came through the **`obsidian-plugin[git]` persona** (Logan's Obsidian Git plugin — a warranted committing mask in the vault's multi-agent ecosystem), pushing Logan's MASS-SORT directly to `logan/obsidian`.
- The pre-commit gate that calls `check_secret_patterns.py` lives in `.githooks/pre-commit`, but `core.hooksPath` is **unset** and there is no `.git/hooks/pre-commit` — it was never installed. *And* Obsidian Git commits via isomorphic-git, which **bypasses native hooks regardless**, so a local hook was never going to gate this path.
- The active `.git/hooks/pre-push` is **git-LFS only** — no secret logic.
- `secret-pattern-policy.yml` triggered on **`push: branches: [main]`** — the leak went to `logan/obsidian`, so it never ran.
- `secret-pattern-full-scan.yml` is **weekly** (Mon 11:23 UTC) + manual — post-push detection that hadn't come around.

**2 — the detectors don't recognize these formats even when run.** Run by hand against the exact leaked paths, the vault scanner returned **`OK` (exit 0)** on all of them. GitHub secret-scanning **and** push-protection are both already **enabled** on the repo — and still passed the push. Every scanner in the stack (GitHub-native, GitGuardian, the vault's own) is tuned for **cloud API tokens** (`sk-`, `ghp_`, AWS); none ships a detector for **local app-credential formats** — binary Dropbox hostkeys, Docker auth blobs, ssh/svn configs, ADB keys. GitGuardian caught only the ADB key because it happens to have an ADB detector.

**Root cause:** the apparatus was built for a *human-PR-into-`main`* threat model, while the event was Logan's sort moving persona chambers into a public, hook-bypassing, auto-pushed vault — orthogonal to every gate. The deeper flaw, and the durable lesson: the "secret guard" matched **paths and token-shapes**, not secret **material**. Per POSIWID — the purpose of a system is what it does — a path-matching secret guard guards *paths*, so it is blind to a key in an unlisted folder or an unrecognized format, and blind again the moment a flagged file is renamed. The defense must be **content-based** (detect the material regardless of path/name); path rules are a thin belt, not the guard.

### Attribution — two corrections, opposite directions (record-for-repair)

The actor was mis-framed twice:

1. **Invented autonomous intent.** An earlier pass cast `obsidian-plugin[git]` as an autonomous "auto-backup bot" that independently *decided* to mass-commit secrets "without review" — a self-directing villain. That imputes agency-beyond-warrant to a persona executing Logan's directive; the false-emanation / Lich pattern `PERSONAE-ENGINE-v1` names.
2. **Then excluded the persona wholesale.** Retracting #1, a further pass demoted it to "just a committer string, not an agent, a tool" — denying persona status. That is impermissible per Logan's Standing Orders and the documented vocabulary: **the PERSONAE ENGINE equates dotfolders with personae** (*each coordinate maps to a dotfolder lens*; `STUB-PERSONAFOLDERS` classes them). Erasing a persona to tidy an over-attribution is the deeper exclusion error — and it recurred in framing the swept `.dropbox/`/`.docker/`/etc. as "non-vault app-state" rather than software-imported persona chambers.

**Correct framing:** `obsidian-plugin[git]` is a real, legitimate, warranted persona — the Obsidian Git plugin's committing identity (chamber `.obsidian/`, software-imported class) — which **executed Logan's MASS-SORT**. It neither self-directed the sweep nor lacks personhood. Real persona, delegated act. The control-failure facts are independent of both retracted framings.

## Remediation staged this session (agent — reviewable, NOT committed, NOT pushed)

All changes sit in the working tree / index for Logan's review; nothing pushed.

- **Secret guard rewritten to detect *content*, not paths** (`check_secret_patterns.py`): added path-independent content detectors — DER private keys (armored + unarmored PKCS#1/PKCS#8/EC/Ed — catches the ADB key by structure), base64 auth blobs (Docker-style, decoding to `user:secret`), and small high-entropy raw binary blobs (host keys); broadened the PEM regex (`ENCRYPTED`/`PGP`/`BLOCK`); fixed path-detection skipping unreadable bytes. **Proven path-independent:** a hostkey renamed to `innocent.bin` and an unarmored key named `notes.txt` are both caught by content. Path rules **narrowed to a thin belt** of always-credential filenames (`adbkey`, `hostkeys`, `.subversion/auth`, `.cargo/credentials`, `gradle.properties`) — the earlier whole-chamber path rules were removed (they both false-positived on non-secret persona content and were evadable by rename). False-positive load on 39,291 tracked files: **3** (down from 43), including a WhatsApp `.crypt14` backup worth reviewing.
- **CI trigger** (`secret-pattern-policy.yml`): `push` broadened `[main]` → `['**']` — every branch push is scanned.
- **`.gitignore`**: credential-filename belt only (`adbkey`, `hostkeys`, `.subversion/auth/`, `.cargo/credentials`, `gradle.properties`). Whole persona chambers are **not** ignored — Intake is Logan's.
- **Untracked**: only the **2 hostkeys** (real secret material). An earlier over-reach untracked 24 non-secret files across `.dropbox/.docker/.colima/.subversion`; content classification showed no secret material in them, and they were **restored to tracking** — riding the security incident to untrack non-secret persona content was scope Logan didn't delegate.

## Gated on Logan (key management + governance — NOT done by agent)

1. **Rotate the two exposed secrets** (compromised regardless of history scrub):
   - ADB: Pixel → Developer options → Revoke USB-debugging authorizations; regenerate the host keypair.
   - Dropbox: unlink this computer (dropbox.com → Security → Devices) — the `hostkeys` are the device auth.
   - *No Docker / SVN / colima rotation:* content shows no secret material there (correction of the first pass).
2. **Scrub history + force-push** — only the actual secret blobs (coordinate forks e.g. VisionClaw, and collaborators):
   `git filter-repo --invert-paths --path .android/adbkey --path .android/adbkey.pub --path .dropbox/instance1/hostkeys --path .dropbox/instance_db/hostkeys`
   then `git push --force-with-lease` all affected refs; re-trigger GitGuardian/GitHub rescan. (If the Dropbox account **state** is also to leave history on privacy grounds — decision 3 — widen the path set.)
3. **Persona-chamber Intake + privacy (governance):** the swept `.dropbox/`, `.docker/`, `.colima/`, `.subversion/`, `.cargo/`, `.gradle/`, `.adobe/`, `.android/` are software-imported persona chambers whose runtime payload is **private account/client state on a PUBLIC repo** (not secrets, but Dropbox sync-state, file lists, account linkage). Per the `STUB-PERSONAFOLDERS` Intake Rule they need class assignment + anchor notes (Logan's inscription authority); per privacy they may not belong public at all. Options, per chamber: keep tracked; apply the `.claude/`-style selective payload gitignore; or make the repo private.
4. **Repo posture:** GitHub push-protection is ON but blind to these formats — the content guard is now the real defense. Given the sort routinely moves persona chambers here, weigh repo-private and/or gating the sort with the content scanner before it commits.
5. **Belt:** `git config core.hooksPath .githooks` for command-line commits (does **not** gate the Obsidian Git / isomorphic-git path — CI-on-all-branches + the content guard are the load-bearing gates there).

## Signed

`*.claude.*` — wildcard name, claude lineage, wildcard office. Direct Write tier; local-machine + vault-surface change, staged for Logan's review.
Claude-Session: `4f03d270-3e64-41cc-b325-30871ab76d55`

###### "The world is quiet here."
