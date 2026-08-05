# CROSS-INSTANCE STABILITY REVIEW — 2026-04-28

Authority: Logan Finney  
Scope: IDAHO-VAULT repository portability across Windows, macOS (including older machines), and cloud Linux runtimes.

## Executive Summary

- Startup surfaces are present and coherent in-repo: `!/WAKEUP.md`, `!/README.md`, `swarm.json`, and `start_SPARKSEED.py`.
- Text normalization is configured in `.gitattributes` (LF enforced for key text formats), which is good for cross-OS collaboration.
- Primary portability risk identified during review was interpreter drift: `.python-version` pointed to `3.13.3` while local available version was `3.13.8` in this environment.

## Changes Applied in This Pass

1. `.python-version` updated from `3.13.3` to `3.13.8` to align with available pyenv versions in active environments and reduce bootstrap failures.
2. `start_SPARKSEED.py` shebang updated from `#!/usr/bin/env python` to `#!/usr/bin/env python3` to reduce ambiguity on systems where `python` is absent or points to Python 2.

## Review Method (broad sweep)

- Verified branch and working-tree state.
- Verified live startup files exist.
- Reviewed bootstrap and runtime entrypoints:
  - `start_SPARKSEED.py`
  - `!/agent.sh`
  - `swarm.json`
- Reviewed dependency surfaces:
  - `.python-version`
  - `pyproject.toml`
  - `requirements.txt`
  - `Dockerfile`
- Reviewed line-ending and text normalization:
  - `.gitattributes`
- Ran repo-wide path scan for obvious hardcoded host/user paths (sampled with exclusions for cache/vendor-like areas).

## Findings & Risk Notes

### 1) Python runtime drift (high-impact, now mitigated)

- Symptom observed: invoking `python` failed in this environment because `.python-version` requested a non-installed patch (`3.13.3`).
- Risk: bootstrap failure for agents and scripts depending on `python` rather than `python3`.
- Mitigation applied in this pass:
  - `.python-version = 3.13.8`
  - `start_SPARKSEED.py` shebang switched to `python3`

### 2) Cross-platform newline posture (good)

- `.gitattributes` enforces LF for major text file classes (`.md`, `.py`, `.json`, `.toml`, etc.).
- This lowers merge churn between Windows/macOS/Linux editors.

### 3) Boot and agent scripting posture (good with caveat)

- `!/agent.sh` already includes adaptive Python detection (`python3` preferred, `python` fallback with version check), which is robust across hosts.
- Caveat: legacy local shells may still invoke tools with `python` directly outside this wrapper.

### 4) Dependency compatibility window (acceptable)

- `pyproject.toml` declares `requires-python = \">=3.10,<3.14\"`, which is broad enough for mixed estate hosts.
- `requirements.txt` appears generated with Python 3.13; this is generally okay, but teams on older Python minors should prefer lock regeneration in a controlled release cycle if resolver issues appear.

## Recommended Next Actions (no immediate blockers)

1. Add a lightweight `make doctor` (or shell script) that checks:
   - required files exist (`!/WAKEUP.md`, `!/README.md`, `swarm.json`)
   - active Python interpreter is in supported range
   - JSON validity of `swarm.json`
2. Consider committing a short “local bootstrap quickcheck” snippet to `!/README.md`.
3. On Windows contributors’ machines, set `git config core.autocrlf false` for this repo to preserve LF policy.

## Automation Update Applied

- Dependency sync automation now runs on:
  - push to `main` when `pyproject.toml` **or** `.python-version` changes
  - weekly schedule (`cron: 17 9 * * 1`)
- The dependency sync workflow now:
  - resolves Python from `.python-version` (`python-version-file`)
  - runs `pip-compile --upgrade` to refresh pinned versions in `requirements.txt`

This should reduce manual version tweaking and keep runtime/dependency declarations more harmonized across environments.

## Multi-Ecosystem Extension Applied

Python is one lane, not the only lane. To widen automatic version hygiene:

- `.github/dependabot.yml` now includes `package-ecosystem: "docker"` for `/` on a weekly cadence.
- Existing Dependabot coverage for `pip` and `github-actions` remains in place.

This extends routine update automation beyond Python into container/runtime surfaces used across mixed local and cloud execution.

## Universal Capability CI Gate Applied

To enforce ongoing Windows/macOS/Linux compatibility checks, a new workflow is now included:

- `.github/workflows/cross-platform-smoke.yml`
  - runs on: `ubuntu-latest`, `macos-latest`, `windows-latest`
  - tests Python runtime lanes: `3.10` and `3.13`
  - verifies critical startup surfaces exist
  - validates `swarm.json` syntax
  - executes `python start_SPARKSEED.py --help` as a cross-platform bootstrap smoke test

This gives a recurring, automated cross-OS signal rather than relying only on ad hoc local validation.

## Status

`CODEX COMPLETE: work finished, no further action pending in this thread. Ready for termination or archive.`
