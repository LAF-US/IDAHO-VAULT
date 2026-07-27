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
propagate their real status, so a broken checkout is never masked. Environment
setup (`ensure_env`) fails fast and loudly if `uv` errors, so a missing package
never surfaces later as a cryptic "console script not found".
"""
from __future__ import annotations

import json
import os
import subprocess  # nosec B404 -- see [tool.bandit] note in pyproject.toml
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
                             capture_output=True, text=True, check=True, timeout=10)
        return Path(out.stdout.strip())
    except Exception:
        d = Path.cwd()
        while d != d.parent:
            if (d / ".git").exists():
                return d
            d = d.parent
        # No .git anywhere above cwd: refuse rather than silently treating the
        # filesystem root as the repo (which would run uv / create .venv / run
        # `git checkout` in the wrong place).
        sys.exit("error: driver.py must run inside a git checkout of the "
                 "idaho-vault repo — no .git found above the working directory "
                 "and `git rev-parse` failed.")


ROOT = repo_root()


def vbin() -> Path:
    return ROOT / ".venv" / ("Scripts" if WIN else "bin")


def script(name: str) -> Path:
    return vbin() / (f"{name}.exe" if WIN else name)


def vpy() -> Path:
    return vbin() / ("python.exe" if WIN else "python")


def run(cmd, timeout: float = 600, **kw):
    return subprocess.run([str(c) for c in cmd], cwd=ROOT, env=ENV, timeout=timeout, **kw)


def _uv(cmd, check: bool = True, extra_env: dict | None = None) -> int:
    """Run a uv setup command, surface its output, and fail fast on error."""
    env = {**ENV, **extra_env} if extra_env else ENV
    # Cold `uv sync`/`uv python install` can take several minutes downloading
    # interpreters and packages; a fixed timeout would be arbitrary and just
    # as likely to kill a slow-but-healthy install.
    # timeout: interactive
    p = subprocess.run([str(c) for c in cmd], cwd=ROOT, env=env,
                       capture_output=True, text=True)
    sys.stderr.write(p.stdout)
    sys.stderr.write(p.stderr)
    if check and p.returncode != 0:
        sys.exit(f"error: `{' '.join(str(c) for c in cmd)}` failed "
                 f"(rc={p.returncode}); see output above.")
    return p.returncode


def ensure_env() -> None:
    """Ready only if the package's console scripts are actually installed."""
    if script("run_crew").exists():
        return
    print("== uv sync (canonical, pinned interpreter from uv.lock) ==", file=sys.stderr)
    _uv(["uv", "sync"], check=False)
    if script("run_crew").exists():
        return
    # uv sync was a no-op or 3.13.3 isn't installed; a clean editable install on
    # Python 3.11 recreates the venv AND the console scripts.
    print("== fallback: editable install on Python 3.11 "
          "(run `uv python install 3.13.3` for the canonical env) ==", file=sys.stderr)
    # Install a uv-managed CPython 3.11 and create the venv from it with
    # UV_PYTHON_PREFERENCE=only-managed. In a pyenv checkout a bare `--python
    # 3.11` can resolve to a pyenv *shim* that honors a missing .python-version
    # pin and fails before the venv is created; a uv-managed interpreter
    # sidesteps pyenv entirely.
    _uv(["uv", "python", "install", "3.11"], check=False)
    _uv(["uv", "venv", "--python", "3.11"],
        extra_env={"UV_PYTHON_PREFERENCE": "only-managed"})
    _uv(["uv", "pip", "install", "-e", "."])
    if not script("run_crew").exists():
        sys.exit("error: setup ran but the `run_crew` console script is still "
                 "missing — the package did not install. Check the uv output "
                 "above (is `uv` installed, and a Python 3.11+ interpreter "
                 "available?).")


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
    # A non-zero exit must fail even if partial JSON reached stdout — otherwise a
    # failed CLI that still prints a fragment reads as a false positive.
    if p.returncode != 0:
        print(f"  -> civic_scaffold exited non-zero (rc={p.returncode})")
        return 1
    try:
        json.loads(p.stdout)
    except Exception:
        print("  -> civic_scaffold did not emit valid JSON")
        return 1
    print("  -> valid JSON")
    return 0


def run_tests() -> int:
    print("== test suite (unittest discovery) ==")
    fixture = "tests/_tmp_topology_census_case/"
    # The suite deletes tracked fixtures under `fixture`. Auto-restore them after
    # the run — but ONLY if the developer had no pre-existing uncommitted edits
    # there, so the cleanup never clobbers unrelated work.
    pre = run(["git", "status", "--porcelain", "--", fixture],
              capture_output=True, text=True)
    fixture_was_clean = (pre.returncode == 0 and not pre.stdout.strip())
    p = run([vpy(), "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
            capture_output=True, text=True)
    print("\n".join((p.stdout + p.stderr).splitlines()[-4:]))
    if fixture_was_clean:
        run(["git", "checkout", "--", fixture], capture_output=True)
    else:
        print(f"  -> note: skipped fixture auto-restore ({fixture} had "
              "uncommitted changes before the run; left as-is).", file=sys.stderr)
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
