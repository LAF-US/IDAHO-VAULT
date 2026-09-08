# Orchestrated .git* Layer — IDAHO-VAULT

*(Supersedes the completed Operation Spring Cleaning plan previously in this file.)*

## Context

The vault's git-configuration layer decayed ad-hoc: the 110-line `.gitattributes` ruleset (case-folded LFS + eol policy) was deleted in commit `1bb5f0662`, leaving **zero attributes resolving** — no LFS patterns (1,845 historical pointers orphaned; new media commits as raw blobs), no eol authority (system `core.autocrlf=true` runs unchecked — the mechanism that corrupted the `.ollama` model blobs on 2026-08-11). `core.hooksPath` is currently **unset**, so the proven gitleaks pre-commit gate in `.githooks/` does not run. `.editorconfig` mandates LF on `[*]` with no binary carve-outs. Logan's directive: make the `.git*` files **orchestrated together, not ad-hoc** — one authoritative owner per concern, files that agree with each other.

Doctrine anchors (read, honored): `GIT-CONTROL-SURFACES-2026-05-17.md` ("control surfaces, not convenience filters"), `VAULT-MEDIA-STORAGE.md` (≤100 MB direct / >100 MB LFS / >2 GB external), root `.gitignore` (Logan-authored, SECRETS/CHURNS — **untouched by this plan**).

Locked decisions (Logan): trufflehog **verified mode**, gate on **verified + unknown** (fail closed offline); pre-push runs **both** gitleaks + trufflehog; land as commits on `logan/obsidian`; reconcile with main's merged `.gitattributes`/`.gitignore` (PRs #953/#954 are already merged to main); `.sample` seeds stay; nothing pushes without Logan.

## Design frame — one owner per concern

| Surface | Single responsibility |
|---|---|
| `.gitignore` | tracked-vs-ignored (Logan-owned; not modified) |
| `.gitattributes` | text/binary, eol, LFS — **the authority**; overrides autocrlf; portable |
| `.editorconfig` | editor formatting only; defers to `.gitattributes` on `-text` paths |
| `.githooks/` | enforcement backstop (pre-commit done; pre-push this plan) |
| per-machine git config | one documented idempotent bootstrap line (can't be committed) |

## Step 0 — pre-flight (no commit)

1. `git fetch origin main` (local origin/main is stale at #945; must include #954's block).
2. Capture base: `git show origin/main:.gitattributes` — adopt **verbatim** as the top of the new file (guarantees suffix-only diff3 at the eventual #926 merge).
3. Sanity: `git ls-files --eol | grep 'i/crlf'` — eyeball for files whose index is CRLF but would match a `text eol=lf` rule (expected near-empty; look-before-commit).

## Commit 1 — `.gitattributes`: restore canonical ruleset + vault guards

File = main's merged content verbatim (case-folded LFS blocks; uppercase-only `*.MTS` carve-out; `text eol=lf` block incl. `*.cmd -text`, `*.csv -text`; #954's anchored extensionless-config block), then append:

```gitattributes

# =====================================================================
# VAULT-LOCAL ADDITIONS (logan/obsidian) — everything above this line is
# the canonical main ruleset, adopted verbatim; add vault rules HERE only
# so the eventual logan/obsidian -> main merge stays suffix-only.
# Later rules win: anchored guards below override generic classes above.
# =====================================================================

# --- .ollama model store: byte-exact or nothing ----------------------
# 2026-08-11 incident: core.autocrlf CRLF conversion + truncation
# corrupted model blobs while .ollama/models was briefly tracked. Blobs
# are gitignored (.ollama/models/blobs/**); the tracked manifests are
# extensionless JSON keyed into a content-addressed store. Everything
# under .ollama is opted out of eol conversion, text diff/merge, and
# every clean/smudge filter (including LFS).
/.ollama/** -text -diff -merge -filter
# The one human document in the store stays normal prose:
/.ollama/OLLAMA.md text eol=lf

# --- Repo plumbing must land LF on disk ------------------------------
# Extensionless (no generic rule matches); core.autocrlf=true would
# smudge a fresh Windows checkout to CRLF, breaking sh hooks. Anchored.
/.githooks/* text eol=lf
/.gitattributes text eol=lf
/.gitignore text eol=lf
/.editorconfig text eol=lf

# --- Binary classes in the vault census with no rule above -----------
# Declared binary (no eol/diff/merge mangling). Deliberately NOT LFS:
# small classes; LFS stays reserved for plausibly-large media.
*.[Ww][Oo][Ff][Ff] binary
*.[Ww][Oo][Ff][Ff]2 binary
*.[Tt][Tt][Ff] binary
*.[Oo][Tt][Ff] binary
*.[Ii][Cc][Oo] binary
*.[Pp][Yy][Cc] binary
*.[Ee][Tt][Ll] binary
*.[Dd][Aa][Tt] binary
*.[Ss][Qq][Ll][Ii][Tt][Ee]-[Ww][Aa][Ll] binary
*.[Ss][Qq][Ll][Ii][Tt][Ee]-[Ss][Hh][Mm] binary

# ---------------------------------------------------------------
# THE WORLD IS QUIET HERE．ESTO PERPETUA!
# ---------------------------------------------------------------
```

(Current 4-line banner preserved as footer, matching `.gitignore` house style.)

**Split-LFS backlog decision:** leave the 440 raw jpg / 130 png / 52 mp4 / 16 MOV historical blobs alone — no history rewrite, **no `git add --renormalize`** (would churn tens of thousands of blobs). Restored patterns mean: historical pointers smudge correctly again; all *future* adds of these classes go to LFS automatically; raw blobs migrate individually whenever next modified.

**Immediately after commit:** `git lfs checkout` (working-tree only) to re-smudge the 1,845 pointer paths.

Commit msg: `gitattributes: restore canonical ruleset from main; add vault guards`.

## Commit 2 — `.editorconfig`: defer to gitattributes on -text classes

Full final content:

```editorconfig
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false

# .gitattributes says *.cmd -text (bytes preserved; cmd.exe label/goto
# scanning misbehaves on bare LF). Editors write CRLF; git won't touch it.
[*.cmd]
end_of_line = crlf

# .gitattributes says *.csv -text (data fidelity; RFC 4180 endings).
[*.csv]
end_of_line = unset
insert_final_newline = unset
trim_trailing_whitespace = unset

# Binary store: never let an editor normalize anything under .ollama
# (model-blob corruption incident, 2026-08-11). Mirrors /.ollama/** -text.
[.ollama/**]
charset = unset
end_of_line = unset
insert_final_newline = unset
trim_trailing_whitespace = unset
```

No ps1/bat carve-out (main mandates `text eol=lf` for them; PowerShell parses LF fine). **Flag only, don't fix:** main is internally inconsistent — `*.bat text eol=lf` vs `*.cmd -text`.

Commit msg: `editorconfig: defer to gitattributes on -text classes (.cmd, .csv, .ollama)`.

## Commit 3 — `.githooks/pre-push`: secret range-gate + LFS chain

Replaces the stock LFS shim (main's pre-push is also just the stock shim, so ours wins cleanly at the #926 merge with LFS functionality preserved via chaining). Full script:

```sh
#!/usr/bin/env sh
# .githooks/pre-push — secret range-gate (gitleaks + trufflehog) then LFS
# transfer. Fails CLOSED: missing engine, scan error, or findings all block.
#
# Protocol: git feeds lines "<local ref> <local oid> <remote ref> <remote oid>"
# on stdin. `git lfs pre-push` consumes the SAME stdin format, so stdin is
# buffered once here and replayed for LFS at the end. A remote oid of all
# zeros means the remote ref is being created.
set -u

ZERO=0000000000000000000000000000000000000000
fail() { printf >&2 'pre-push: %s\n' "$*"; exit 1; }

command -v gitleaks   >/dev/null 2>&1 || fail 'gitleaks not on PATH - secret gate fails closed; push blocked.'
command -v trufflehog >/dev/null 2>&1 || fail 'trufflehog not on PATH - secret gate fails closed; push blocked.'
command -v git-lfs    >/dev/null 2>&1 || fail 'git-lfs not on PATH - LFS transfer gate fails closed; push blocked.'

refs=$(cat)
[ -n "$refs" ] || exit 0    # nothing to push

# trufflehog is a native Windows exe: needs C:/ style paths, not /c/ style.
top=$(git rev-parse --show-toplevel)
if command -v cygpath >/dev/null 2>&1; then top=$(cygpath -m "$top"); fi

blocked=0
while IFS=' ' read -r local_ref local_oid remote_ref remote_oid; do
  [ -n "$local_ref" ] || continue
  [ "$local_oid" = "$ZERO" ] && continue   # deleting a remote ref: nothing to scan

  if [ "$remote_oid" = "$ZERO" ] || ! git cat-file -e "$remote_oid^{commit}" 2>/dev/null; then
    logopts="$local_oid --not --remotes=origin"
    default=$(git symbolic-ref --quiet refs/remotes/origin/HEAD || echo refs/remotes/origin/main)
    since=$(git merge-base "$local_oid" "$default" 2>/dev/null) || since=
  else
    logopts="$remote_oid..$local_oid"
    since=$remote_oid
  fi

  # --- Gate 1: gitleaks range scan (offline backstop) -------------------
  if ! gitleaks git --log-opts "$logopts" --redact --verbose --no-color --no-banner; then
    printf >&2 'pre-push: gitleaks flagged %s (range: %s). Values redacted above.\n' "$local_ref" "$logopts"
    blocked=1
  fi

  # --- Gate 2: trufflehog, verified mode (gate on verified + unknown) ---
  # Exit 183 = findings (--fail). Any other nonzero = scan/verification
  # error = fail closed (offline verification counts as blocked).
  if [ -n "$since" ]; then
    trufflehog git "file://$top" --since-commit "$since" --branch "$local_ref" \
      --results=verified,unknown --fail --no-update
  else
    printf >&2 'pre-push: no merge-base for %s; trufflehog scanning full ref history.\n' "$local_ref"
    trufflehog git "file://$top" --branch "$local_ref" \
      --results=verified,unknown --fail --no-update
  fi
  rc=$?
  if [ "$rc" -eq 183 ]; then
    printf >&2 'pre-push: trufflehog found verified/unknown secrets on %s.\n' "$local_ref"
    blocked=1
  elif [ "$rc" -ne 0 ]; then
    printf >&2 'pre-push: trufflehog scan error (exit %s) on %s - fail closed.\n' "$rc" "$local_ref"
    blocked=1
  fi
done <<EOF
$refs
EOF

[ "$blocked" -eq 0 ] || fail 'secret gate(s) failed - push blocked. Fix findings; do not bypass hooks.'

# --- Gate 3: LFS object transfer (replay the original stdin) ------------
printf '%s\n' "$refs" | git lfs pre-push "$@"
exit $?
```

Commit msg: `githooks: pre-push secret range-gate (gitleaks + trufflehog) chaining LFS`.

## Commit 4 — `.githooks/GITHOOKS.md`: bootstrap + coexistence + controls

Document (replacing the 3-line stub):
- **Bootstrap (per machine/clone, idempotent):** `git config core.hooksPath .githooks` — required; currently unset, so no custom hooks run.
- **LFS coexistence (verified, git-lfs 3.6.1):** plain `git lfs install`/`update` upgrades *known* stock shims harmlessly and **refuses (errors, does not overwrite)** on unrecognized content like our pre-push. That error is expected — answer with `git lfs install --skip-repo` (filters only) or `git lfs update --manual`. **Never `--force`** — the only path that silently replaces the secret gate with the stock shim.
- Positive-control one-liners for each gate (below).

Commit msg: `githooks: document bootstrap, LFS coexistence, positive controls`.

## Verification (end-to-end)

- **A. check-attr spot checks:** `git check-attr filter text eol -- "photo.JPG" "clip.MOV" "foo.MTS" "foo.mts" "script.cmd" ".ollama/models/blobs/sha256-x" ".ollama/OLLAMA.md" ".githooks/pre-push" "font.woff" "notes.md"` → media = `filter: lfs`; `foo.mts` = text/lf, no filter; `.cmd` = `text: unset`; `.ollama/**` = **unset** (not unspecified) across the board; `OLLAMA.md` = text/lf. `git lfs track` lists full set; `git lfs ls-files | wc -l` ≈ 1,845.
- **B. LFS round-trip (new media, no commit):** copy a jpg → `git add` → `git show :file | head -c 60` shows `version https://git-lfs...` pointer → unstage, delete.
- **C. pre-commit positive control:** random canary `AKIAQZKPXVJWMNBTUCRD` (NOT AWS's doc example — default configs may allowlist it) in a staged file → commit must be **blocked**.
- **D. pre-push positive control (Logan runs):** build canary commit via plumbing (`hash-object`/`mktree`/`commit-tree` — constructs a fixture whose push is *expected to fail*; no gate bypassed), branch `tmp/secret-canary`, push → **blocked before any transfer** (gitleaks findings + trufflehog 183). Include trufflesecurity/test_keys canary pair so the *verified* path is exercised. Delete branch after.
- **E. fail-closed control:** invoke hook directly with synthetic stdin while engines are off PATH → immediate "not on PATH" block.
- **F. editorconfig non-interference:** save-touch a `.cmd`, a `.csv`, an `.ollama` file → `git diff` stays clean.
- **G. worktree quiescence:** `git status --porcelain` before/after commit 1 differs only by intended files (no renormalization storm).

## #926 merge-time notes (record now, act later)

- `.gitattributes`: suffix-only → merges clean.
- `.gitignore`: main brings `/node_modules/**` last-rule (#953) → take it; no local action.
- `.githooks/pre-push`: ours wins (main's is stock shim; LFS chained inside ours).
- `.githooks/pre-commit`: **will conflict** — main's is a rich script chain (`sync_obsidian_plugin_registry.py`, `laf_usb_manifest.py`, `check_secret_patterns.py`, `check_large_files.py`, jupytext) whose `.github/scripts/` don't exist on this branch. Guidance: combined hook = main's chain **plus** gitleaks gate prepended — decide at merge, flag loudly.

## Out of scope

`.gitignore` rewrites (Logan-owned); converting historical raw blobs to LFS; `.github/workflows` CI; the ~27k untracked pool files; revisiting pre-commit (done, proven); main's `*.bat` vs `*.cmd` inconsistency (flagged only).

## Judgment calls (made, stated)

1. `/.ollama/** -text -diff -merge -filter` over bare `binary`: `-filter` also forbids clean/smudge (incl. LFS) in the store; carve-back only for `OLLAMA.md`.
2. Census binary classes get `binary`, not LFS — avoids creating new split-LFS classes; protection needed is eol-safety, not transport.
3. `/.githooks/* text eol=lf` — insurance against a fresh Windows clone smudging extensionless sh hooks to CRLF.
4. Real expected-block push over `--dry-run` for control D — blocking is client-side pre-transfer; avoids dry-run hook semantics.
5. Random AKIA canary (gitleaks) + trufflesecurity/test_keys pair (trufflehog verified path).
6. `cygpath -m` for trufflehog's `file://` URL — native exe under Git-Bash sh.
