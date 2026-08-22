#!/usr/bin/env bash
#
# export-dropbox.sh — Pull everything reachable from the Dropbox rclone remote
# to a local destination, with a manifest captured BEFORE the copy and a
# checksum verification AFTER. Built for the "subscription expired, get
# everything out" scenario.
#
# Grounding: rclone remotes are already configured per
# BACKUP-INFRASTRUCTURE-OPERATION-SYNTHESIS.md (remote "dropbox:") and
# DEFRAG-MAP.md §B3 (remote "dropbox-personal:" on the Mac). This script
# auto-detects whichever Dropbox remote exists.
#
# IMPORTANT — what rclone CANNOT export (see DROPBOX-EXPORT-RUNBOOK):
#   - Dropbox Paper documents
#   - Orphaned blocks from unlinked devices
# Those account for the ~304 GB gap between `rclone about` (309 GB) and the
# file API (~5.2 GB). They require the browser steps in the runbook.
#
# Usage:
#   ./export-dropbox.sh /path/to/destination [remote_name]
#
# Examples:
#   ./export-dropbox.sh /Volumes/storage/DROPBOX-EXPORT-2026-06-23
#   ./export-dropbox.sh /Volumes/storage/DROPBOX-EXPORT dropbox-personal:
#
set -euo pipefail

# ---- args -------------------------------------------------------------------
DEST="${1:-}"
REMOTE="${2:-}"

if [[ -z "$DEST" ]]; then
  echo "ERROR: destination path required." >&2
  echo "Usage: $0 /path/to/destination [remote_name]" >&2
  exit 2
fi

# ---- locate rclone ----------------------------------------------------------
if ! command -v rclone >/dev/null 2>&1; then
  echo "ERROR: rclone not found on PATH. Install it (Mac: brew install rclone;" >&2
  echo "       Windows: scoop install rclone) and re-run." >&2
  exit 3
fi
echo ">> rclone: $(rclone version | head -1)"

# ---- auto-detect the Dropbox remote ----------------------------------------
if [[ -z "$REMOTE" ]]; then
  REMOTE="$(rclone listremotes | grep -i dropbox | head -1 || true)"
  if [[ -z "$REMOTE" ]]; then
    echo "ERROR: no Dropbox remote found in 'rclone listremotes'." >&2
    echo "       Configure one with 'rclone config' or pass the name explicitly." >&2
    exit 4
  fi
fi
# Normalise to "name:" form
REMOTE="${REMOTE%:}:"
echo ">> Using remote: $REMOTE"

# ---- destination + log scaffolding -----------------------------------------
STAMP="$(date +%Y-%m-%d_%H%M%S)"
mkdir -p "$DEST"
LOGDIR="$DEST/_export-logs"
mkdir -p "$LOGDIR"
MANIFEST="$LOGDIR/manifest-$STAMP.jsonl"
COPYLOG="$LOGDIR/copy-$STAMP.log"
CHECKLOG="$LOGDIR/check-$STAMP.log"
SUMMARY="$LOGDIR/summary-$STAMP.txt"

echo ">> Destination: $DEST"
echo ">> Logs:        $LOGDIR"

# ---- preflight: quota + reachability ---------------------------------------
echo ">> Preflight: rclone about $REMOTE"
{
  echo "=== rclone about $REMOTE ($STAMP) ==="
  rclone about "$REMOTE" || echo "(about failed — continuing)"
  echo
  echo "=== top-level dirs (rclone lsd) ==="
  rclone lsd "$REMOTE" || true
  echo
  echo "=== shared-folder probe (rclone lsd --dropbox-shared-folders) ==="
  rclone lsd "$REMOTE" --dropbox-shared-folders 2>&1 || true
} | tee "$SUMMARY"

# ---- manifest BEFORE copy (the record of what existed) ----------------------
echo ">> Capturing full manifest -> $MANIFEST"
rclone lsjson "$REMOTE" --recursive --hash > "$MANIFEST" || {
  echo "WARN: lsjson failed; falling back to lsf" >&2
  rclone lsf "$REMOTE" --recursive --format "psthm" > "$MANIFEST" || true
}
FILECOUNT="$(grep -c '"Path"' "$MANIFEST" 2>/dev/null || echo '?')"
echo ">> Manifest captured (~$FILECOUNT entries)"

# ---- the copy ---------------------------------------------------------------
# rclone copy is resumable and idempotent: re-running skips already-transferred
# files. Safe to Ctrl-C and restart.
echo ">> Copying $REMOTE -> $DEST  (log: $COPYLOG)"
rclone copy "$REMOTE" "$DEST" \
  --transfers 8 \
  --checkers 16 \
  --retries 5 \
  --low-level-retries 10 \
  --track-renames \
  --create-empty-src-dirs \
  --stats 30s \
  --stats-one-line \
  --log-level INFO \
  --log-file "$COPYLOG" \
  --progress

# ---- verify -----------------------------------------------------------------
echo ">> Verifying with rclone check (log: $CHECKLOG)"
if rclone check "$REMOTE" "$DEST" --one-way --log-file "$CHECKLOG" --log-level INFO; then
  echo ">> VERIFY: OK — every source file is present at destination."
else
  echo ">> VERIFY: MISMATCHES found. Inspect $CHECKLOG before deleting anything in Dropbox." >&2
fi

# ---- summary ----------------------------------------------------------------
{
  echo
  echo "=== EXPORT SUMMARY ($STAMP) ==="
  echo "Remote:      $REMOTE"
  echo "Destination: $DEST"
  echo "Manifest:    $MANIFEST  (~$FILECOUNT entries)"
  echo "Copy log:    $COPYLOG"
  echo "Check log:   $CHECKLOG"
  echo
  echo "REMINDER: rclone cannot export Dropbox Paper docs or orphaned device"
  echo "blocks. If 'rclone about' above shows far more used space than was"
  echo "copied, do the browser steps in DROPBOX-EXPORT-RUNBOOK before you"
  echo "let the subscription lapse / delete anything."
} | tee -a "$SUMMARY"

echo ">> Done. Review $SUMMARY"
