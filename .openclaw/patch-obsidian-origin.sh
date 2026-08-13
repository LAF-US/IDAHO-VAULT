#!/usr/bin/env bash
# patch-obsidian-origin.sh — re-apply the app://obsidian.md origin fallback to OpenClaw.
#
# WHY: Obsidian's renderer loads from app://obsidian.md, which is a custom scheme
# and therefore an opaque ("null") origin per the URL spec. Vanilla OpenClaw's
# allowlist compares the *parsed* origin, which never matches, so it refuses the
# Obsidian plugin's websocket. This injects a one-line raw-origin fallback into
# the gateway auth code so a raw Origin string in allowedOrigins is honored.
#
# WHEN: `openclaw update` wipes ~/node_modules/openclaw/dist, so re-run this after
# every update. The CONFIG side (gateway.controlUi.allowedOrigins must contain
# "app://obsidian.md") lives in ~/.openclaw/openclaw.json and SURVIVES updates —
# this script only checks it and warns; it does not modify config.
#
# SAFE: idempotent, backs up the auth file to *.obsidianclaw.bak, aborts cleanly
# if the code layout shifted (no silent corruption). Files are user-owned — NO sudo.
# Adapted from github.com/oscarhenrycollins/obsidianclaw (corrected path, sudo removed).

set -euo pipefail

DIST="${OPENCLAW_DIST:-$HOME/node_modules/openclaw/dist}"

if [ ! -d "$DIST" ]; then
  echo "X OpenClaw dist not found at $DIST — set OPENCLAW_DIST to override." >&2
  exit 1
fi

AUTH="$(grep -l 'checkBrowserOrigin' "$DIST"/auth-*.js 2>/dev/null | head -1 || true)"
if [ -z "$AUTH" ]; then
  echo "X Could not find the auth file (checkBrowserOrigin) under $DIST." >&2
  echo "  OpenClaw's layout may have changed; not patching." >&2
  exit 1
fi

if grep -q 'rawOriginNormalized' "$AUTH"; then
  echo "= Already patched: $AUTH"
else
  cp -p "$AUTH" "$AUTH.obsidianclaw.bak"
  python3 - "$AUTH" <<'PY'
import io, sys
path = sys.argv[1]
src = io.open(path, encoding="utf-8").read()
target = (
    '\tif (allowlist.has("*") || allowlist.has(parsedOrigin.origin)) return {\n'
    '\t\tok: true,\n'
    '\t\tmatchedBy: "allowlist"\n'
    '\t};\n'
)
if target not in src:
    sys.stderr.write("ERROR: allowlist block not found verbatim; aborting without changes.\n")
    sys.exit(2)
inj = (
    '\tconst rawOriginNormalized = normalizeOptionalLowercaseString(params.origin);\n'
    '\tif (rawOriginNormalized && allowlist.has(rawOriginNormalized)) return {\n'
    '\t\tok: true,\n'
    '\t\tmatchedBy: "allowlist"\n'
    '\t};\n'
)
io.open(path, "w", encoding="utf-8").write(src.replace(target, target + inj, 1))
print("+ Patched: " + path)
PY
fi

# Config side (survives updates) — check only, do not modify.
if openclaw config get gateway.controlUi.allowedOrigins 2>/dev/null | grep -q 'app://obsidian.md'; then
  echo "= Config allowedOrigins already contains app://obsidian.md"
else
  echo "! Config gateway.controlUi.allowedOrigins is MISSING app://obsidian.md."
  echo "  Re-add it (keeping any existing origins), e.g.:"
  echo "  openclaw config set gateway.controlUi.allowedOrigins '[\"app://obsidian.md\"]' --strict-json"
fi

echo "Restarting gateway..."
openclaw gateway restart >/dev/null 2>&1 || echo "  (restart the gateway manually if needed)"
echo "Done — Obsidian plugin origin fallback is in place."
