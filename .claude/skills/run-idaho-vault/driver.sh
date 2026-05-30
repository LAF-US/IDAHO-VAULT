#!/usr/bin/env bash
# Smoke driver for the `idaho_vault` CrewAI deployment-validation shard.
# This is the agent-facing way to BUILD + RUN + DRIVE the app headless,
# offline, with no API keys (the package ships a StaticValidationLLM mock).
#
# Run from the repo root (the unit):
#   .claude/skills/run-idaho-vault/driver.sh          # full smoke
#   .claude/skills/run-idaho-vault/driver.sh run      # just run the crew
#   .claude/skills/run-idaho-vault/driver.sh test     # just the test suite
#
# Exit 0 = the validation crew reported PASS and the offline entrypoints ran.
# The test suite is reported but its 2 known-pre-existing failures (see SKILL.md
# Gotchas) do NOT fail this smoke.
set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || { echo "not in a git checkout"; exit 1; }

# CrewAI tries to POST telemetry to telemetry.crewai.com and eats a 30s
# connect-timeout when the network blocks it. Silence it.
export CREWAI_DISABLE_TELEMETRY=true OTEL_SDK_DISABLED=true CREWAI_TELEMETRY_OPT_OUT=true

PY=.venv/bin/python
mode="${1:-all}"

ensure_env() {
  [ -x "$PY" ] && return
  # Canonical: pinned 3.13.3 from uv.lock. Needs `uv python install 3.13.3`
  # first (downloads are manual per pyproject). Falls back to system 3.11.
  echo "== uv sync (canonical, pinned interpreter from uv.lock) ==" >&2
  if uv sync >&2; then return; fi
  echo "== uv sync needs 3.13.3 (run: uv python install 3.13.3); falling back to system 3.11 editable install ==" >&2
  uv venv --python "$(command -v python3.11 || command -v python3)" >&2
  uv pip install -e . >&2
}

run_crew() {
  echo "== run_crew: bootstrap validation crew (offline mock LLM) =="
  out="$(.venv/bin/run_crew 2>&1)"; rc=$?
  echo "$out" | grep -E "Overall status:" || true
  if [ $rc -eq 0 ] && echo "$out" | grep -q "Overall status: PASS"; then
    echo "  -> run_crew OK (PASS)"; return 0
  fi
  echo "  -> run_crew FAILED (rc=$rc)"; echo "$out" | tail -20; return 1
}

drive_entrypoints() {
  echo "== five_wizards_threshold --dry-run (no materialization) =="
  .venv/bin/five_wizards_threshold --dry-run | tail -3 || return 1
  echo "== civic_scaffold --format json (checkout-only; validate JSON) =="
  # NOTE: use civic_scaffold, NOT metadata_survey — the metadata_survey
  # console-script is broken on this checkout (see SKILL.md Gotchas).
  .venv/bin/civic_scaffold --format json 2>/dev/null | "$PY" -c 'import sys,json; json.load(sys.stdin); print("  -> valid JSON")' || return 1
}

run_tests() {
  echo "== test suite (unittest discovery) =="
  # The suite deletes tracked fixtures under tests/_tmp_topology_census_case/;
  # restore them afterward so the tree stays clean.
  "$PY" -m unittest discover -s tests -p 'test_*.py' 2>&1 | tail -4
  git checkout -- tests/_tmp_topology_census_case/ 2>/dev/null || true
}

ensure_env
case "$mode" in
  run)  run_crew ;;
  test) run_tests ;;
  all)
    ok=0
    run_crew || ok=1
    drive_entrypoints || ok=1
    run_tests
    echo
    if [ $ok -eq 0 ]; then echo "SMOKE PASS — validation crew + offline entrypoints OK"; else echo "SMOKE FAIL"; fi
    exit $ok
    ;;
  *) echo "usage: driver.sh [all|run|test]"; exit 2 ;;
esac
