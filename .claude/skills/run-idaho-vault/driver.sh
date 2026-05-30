#!/usr/bin/env bash
# Smoke driver for the `idaho_vault` CrewAI deployment-validation shard.
# Agent-facing way to BUILD + RUN + DRIVE the app headless, offline, no API keys
# (the package ships a StaticValidationLLM mock).
#
# Shell: POSIX (Linux / macOS / WSL / Git-Bash). On native Windows PowerShell,
# use the `uv run …` one-liners in SKILL.md — those are the OS-agnostic path.
#
# Run from anywhere inside the checkout:
#   .claude/skills/run-idaho-vault/driver.sh          # full smoke
#   .claude/skills/run-idaho-vault/driver.sh run      # just the validation crew
#   .claude/skills/run-idaho-vault/driver.sh test     # just the test suite
#
# Exit: `all` = 0 when the crew reports PASS and the offline entrypoints run
# (the suite's 2 known pre-existing failures do NOT fail `all`). `test` exits
# with the suite's real status (so a broken checkout is never masked).
set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || { echo "not in a git checkout"; exit 1; }

# CrewAI POSTs telemetry to telemetry.crewai.com and eats a 30s connect-timeout
# when the network blocks it. Silence it.
export CREWAI_DISABLE_TELEMETRY=true OTEL_SDK_DISABLED=true CREWAI_TELEMETRY_OPT_OUT=true

# Resolve the venv script dir (POSIX: bin; Windows: Scripts).
resolve_bin() { BIN=.venv/bin; [ -d .venv/Scripts ] && BIN=.venv/Scripts; PY="$BIN/python"; }
resolve_bin
mode="${1:-all}"

ensure_env() {
  # Ready only if the package's console scripts are actually installed — a bare
  # `python -m venv .venv` (or an interrupted install) is NOT ready.
  [ -x "$BIN/run_crew" ] && return
  echo "== uv sync (canonical, pinned interpreter from uv.lock) ==" >&2
  uv sync >&2 && resolve_bin
  [ -x "$BIN/run_crew" ] && return
  # uv sync was a no-op or the 3.13.3 pin is missing; do a clean editable
  # install on system 3.11, which recreates the venv AND the console scripts.
  echo "== falling back to system 3.11 editable install (run: uv python install 3.13.3 for the canonical env) ==" >&2
  uv venv --python "$(command -v python3.11 || command -v python3)" >&2
  uv pip install -e . >&2
  resolve_bin
}

run_crew() {
  echo "== run_crew: bootstrap validation crew (offline mock LLM) =="
  out="$("$BIN/run_crew" 2>&1)"; rc=$?
  echo "$out" | grep -E "Overall status:" || true
  if [ $rc -eq 0 ] && echo "$out" | grep -q "Overall status: PASS"; then
    echo "  -> run_crew OK (PASS)"; return 0
  fi
  echo "  -> run_crew FAILED (rc=$rc)"; echo "$out" | tail -20; return 1
}

drive_entrypoints() {
  echo "== five_wizards_threshold --dry-run (no materialization) =="
  "$BIN/five_wizards_threshold" --dry-run | tail -3 || return 1
  echo "== civic_scaffold --format json (checkout-only; validate JSON) =="
  # Use civic_scaffold, NOT metadata_survey — the metadata_survey console-script
  # is broken on this checkout (see SKILL.md Gotchas).
  "$BIN/civic_scaffold" --format json 2>/dev/null | "$PY" -c 'import sys,json; json.load(sys.stdin); print("  -> valid JSON")' || return 1
}

run_tests() {
  echo "== test suite (unittest discovery) =="
  "$PY" -m unittest discover -s tests -p 'test_*.py' 2>&1 | tail -4
  rc=${PIPESTATUS[0]}
  # The suite deletes tracked fixtures under tests/_tmp_topology_census_case/;
  # restore them — but preserve the suite's real exit status (don't let the
  # cleanup become the function's result).
  git checkout -- tests/_tmp_topology_census_case/ 2>/dev/null || true
  return "$rc"
}

ensure_env
case "$mode" in
  run)  run_crew; exit $? ;;
  test) run_tests; exit $? ;;   # propagate the suite's real status
  all)
    ok=0
    run_crew || ok=1
    drive_entrypoints || ok=1
    run_tests || true   # reported, not gating: 2 known pre-existing failures
    echo
    if [ $ok -eq 0 ]; then echo "SMOKE PASS — validation crew + offline entrypoints OK"; else echo "SMOKE FAIL"; fi
    exit $ok
    ;;
  *) echo "usage: driver.sh [all|run|test]"; exit 2 ;;
esac
