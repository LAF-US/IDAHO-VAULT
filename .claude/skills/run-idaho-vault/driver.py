#!/usr/bin/env python3
"""Cross-platform smoke driver for the `idaho_vault` CrewAI validation shard.

Agent-facing way to BUILD + RUN + DRIVE the app headless, offline, with no API
keys (the package ships a StaticValidationLLM mock). Pure stdlib, so it runs
natively wherever Python does — Linux, macOS, and **Windows PowerShell/cmd**
(no Git-Bash / WSL required; per VAULT-CONVENTIONS.md NETWEB guidance).

    python .claude/skills/run-idaho-vault/driver.py            # full smoke
    python .claude/skills/run-idaho-vault/driver.py run        # validation crew
    python .claude/skills/run-idaho-vault/driver.py test       # test suite

Exit: `all` -> 0 when the crew reports PASS and the offline entrypoints run
(the suite's 2 known pre-existing failures do NOT fail `all`). `run`/`test`
propagate their real status, so a broken checkout is never masked.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

WIN = os.name == "nt"
# CrewAI POSTs telemetry to telemetry.crewai.com and eats a 30s connect-timeout
# when the network blocks it. Silence it for every child process.
ENV = {**os.environ, "CREWAI_DISABLE_TELEMETRY": "true",
       "OTEL_SDK_DISABLED": "true", "CREWAI_TELEMETRY_OPT_OUT": "true"}


def repo_root() -> Path:
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True)
        return Path(out.stdout.strip())
    except Exception:
        d = Path.cwd()
        while not (d / ".git").exists() and d != d.parent:
            d = d.parent
        return d


ROOT = repo_root()


def vbin() -> Path:
    return ROOT / ".venv" / ("Scripts" if WIN else "bin")


def script(name: str) -> Path:
    return vbin() / (f"{name}.exe" if WIN else name)


def vpy() -> Path:
    return vbin() / ("python.exe" if WIN else "python")


def run(cmd, **kw):
    return subprocess.run([str(c) for c in cmd], cwd=ROOT, env=ENV, **kw)


def ensure_env() -> None:
    """Ready only if the package's console scripts are actually installed."""
    if script("run_crew").exists():
        return
    print("== uv sync (canonical, pinned interpreter from uv.lock) ==", file=sys.stderr)
    run(["uv", "sync"])
    if script("run_crew").exists():
        return
    # uv sync was a no-op or 3.13.3 isn't installed; a clean editable install on
    # system 3.11 recreates the venv AND the console scripts.
    print("== fallback: editable install on Python 3.11 "
          "(run `uv python install 3.13.3` for the canonical env) ==", file=sys.stderr)
    # Pass the version request, not a resolved path: in a pyenv checkout
    # `which python3.11` returns a shim that honors the missing .python-version
    # pin and exits 127. Letting uv resolve "3.11" itself bypasses the shim.
    run(["uv", "venv", "--python", "3.11"])
    run(["uv", "pip", "install", "-e", "."])


def run_crew() -> int:
    print("== run_crew: bootstrap validation crew (offline mock LLM) ==")
    p = run([script("run_crew")], capture_output=True, text=True)
    for line in p.stdout.splitlines():
        if "Overall status:" in line:
            print(line.strip(" │"))
    if p.returncode == 0 and "Overall status: PASS" in p.stdout:
        print("  -> run_crew OK (PASS)")
        return 0
    print(f"  -> run_crew FAILED (rc={p.returncode})")
    print("\n".join((p.stdout + p.stderr).splitlines()[-20:]))
    return 1


def drive_entrypoints() -> int:
    print("== five_wizards_threshold --dry-run (no materialization) ==")
    if run([script("five_wizards_threshold"), "--dry-run"]).returncode != 0:
        return 1
    print("== civic_scaffold --format json (checkout-only; validate JSON) ==")
    # Use civic_scaffold, NOT metadata_survey — the metadata_survey
    # console-script is broken on this checkout (see SKILL.md Gotchas).
    p = run([script("civic_scaffold"), "--format", "json"], capture_output=True, text=True)
    try:
        json.loads(p.stdout)
    except Exception:
        print(f"  -> civic_scaffold did not emit valid JSON (rc={p.returncode})")
        return 1
    print("  -> valid JSON")
    return 0


def run_tests() -> int:
    print("== test suite (unittest discovery) ==")
    p = run([vpy(), "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
            capture_output=True, text=True)
    print("\n".join((p.stdout + p.stderr).splitlines()[-4:]))
    # The suite deletes tracked fixtures under tests/_tmp_topology_census_case/;
    # restore them but preserve the suite's real exit status.
    run(["git", "checkout", "--", "tests/_tmp_topology_census_case/"],
        capture_output=True)
    return p.returncode


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode not in {"all", "run", "test"}:
        print("usage: driver.py [all|run|test]")
        return 2
    ensure_env()
    if mode == "run":
        return run_crew()
    if mode == "test":
        return run_tests()
    ok = 0
    ok |= run_crew()
    ok |= drive_entrypoints()
    run_tests()  # reported, not gating: 2 known pre-existing failures
    print()
    print("SMOKE PASS — validation crew + offline entrypoints OK" if ok == 0 else "SMOKE FAIL")
    return ok


if __name__ == "__main__":
    raise SystemExit(main())
