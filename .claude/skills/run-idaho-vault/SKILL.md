---
name: run-idaho-vault
description: Build, run, smoke-test, and validate the idaho_vault CrewAI deployment-validation shard — run the bootstrap validation crew, drive its CLI entrypoints, and run the test suite, all offline with no API keys. Use when asked to run / start / build / test / smoke / validate idaho_vault, the CrewAI bootstrap, or src/idaho_vault.
---

# Run: idaho_vault (CrewAI deployment-validation shard)

`src/idaho_vault` is a Python/CrewAI package whose job is to **validate that the
repo's CrewAI deployment contract is wired up** — it is not a GUI or a server.
It ships a `StaticValidationLLM` mock, so the whole thing **runs offline with no
model keys**. `run_crew` kicks off the validation crew and prints a
`Bootstrap Contract Report` (`Overall status: PASS`).

Drive it with the committed smoke script. **All paths below are relative to the
repo root** (the unit).

> Agent path first: **`python .claude/skills/run-idaho-vault/driver.py`** builds
> the env if needed, runs the crew, drives the offline entrypoints, and runs the
> tests. Start there.
>
> **Portability:** `driver.py` is pure-stdlib Python — it runs natively on
> Linux, macOS, and **Windows PowerShell/cmd** (no Git-Bash / WSL), resolving
> `.venv/Scripts` vs `.venv/bin` and the `.exe` suffix itself, per
> `VAULT-CONVENTIONS.md` NETWEB guidance. The `uv …` one-liners in *Build* /
> *Direct invocation* are the same commands it runs, for driving it by hand.

## Prerequisites

- **`uv`** (installed and on `PATH`; confirm with `uv --version`). No `apt-get`
  packages are needed — CrewAI and all deps install as pure-Python wheels.
- A Python interpreter: the repo pins **3.13.3** (`.python-version`, `uv.lock`);
  system **3.11** also satisfies `requires-python` and works for the core surface.

## Build

Canonical (pinned interpreter, from the lockfile) — **verified**:

```bash
uv python install 3.13.3   # downloads are 'manual' in pyproject; do this first
uv sync                    # installs crewai + deps into .venv on 3.13.3
```

Fallback when you can't fetch 3.13.3 (uses system 3.11) — **verified**:

```bash
uv venv --python "$(command -v python3.11)"
uv pip install -e .
```

(`.venv` and `.uv-cache` are git-ignored.)

## Run — agent path (the driver)

```bash
python .claude/skills/run-idaho-vault/driver.py        # full smoke (build if needed)
python .claude/skills/run-idaho-vault/driver.py run    # just the validation crew
python .claude/skills/run-idaho-vault/driver.py test   # just the test suite
```

Full smoke prints, and exits 0 on success:

```
== run_crew: bootstrap validation crew (offline mock LLM) ==
Overall status: PASS
  -> run_crew OK (PASS)
== five_wizards_threshold --dry-run (no materialization) ==
...
== civic_scaffold --format json (checkout-only; validate JSON) ==
  -> valid JSON
== test suite (unittest discovery) ==
Ran 149 tests in ~1.4s   (2 known pre-existing failures — see Gotchas)
SMOKE PASS — validation crew + offline entrypoints OK
```

The driver sets the CrewAI telemetry-off env vars and restores test-deleted
fixtures for you (see Gotchas). `all` mode exits 0 on a healthy checkout (the
2 known test failures don't gate it); **`test` mode propagates the suite's real
exit status** — so it currently exits non-zero because of those 2 pre-existing
failures, and will surface any genuine regression rather than mask it.

## Direct invocation (single entrypoints)

The package installs console scripts; once the env exists, run any directly
(set the telemetry env first to avoid a 30s hang):

```bash
export CREWAI_DISABLE_TELEMETRY=true OTEL_SDK_DISABLED=true
uv run run_crew                          # the validation crew -> PASS report
uv run five_wizards_threshold --dry-run  # gate/council preview, no writes
uv run civic_scaffold --format json      # emits civic-scaffold JSON
```

Run one test module (tests put `src/` on `sys.path` themselves). The venv
interpreter is `.venv/bin/python` on POSIX and `.venv\Scripts\python.exe` on
Windows — or just let the driver resolve it (`driver.py test`):

```bash
.venv/bin/python -m unittest tests.test_main_cli           # POSIX
.venv\Scripts\python.exe -m unittest tests.test_main_cli   # Windows
```

## Test

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'        # POSIX
.venv\Scripts\python.exe -m unittest discover -s tests -p test_*.py  # Windows
```

149 tests. **2 fail on a clean checkout, unrelated to setup** (data/pin drift):
- `test_check_secret_patterns … test_allow_marker_does_not_suppress_dedicated_token` — expects a `github_token` rule; resolves to an empty set.
- `test_workflow_security_invariants … _dependabot_auto_merge_…` — asserts a stale pinned SHA for `dependabot/fetch-metadata` (the action was bumped; the test wasn't).

## Gotchas (battle scars)

- **`uv sync` fails with "No interpreter found for Python 3.13.3."** The repo
  pins 3.13.3 and `python-downloads = "manual"`. Either `uv python install 3.13.3`
  first, or use the 3.11 fallback (`uv venv --python python3.11 && uv pip install -e .`).
- **Every run hangs ~30s at the end** trying to POST to `telemetry.crewai.com`.
  It's non-fatal but slow. `export CREWAI_DISABLE_TELEMETRY=true OTEL_SDK_DISABLED=true`
  silences it. The driver already does this.
- **The `metadata_survey` console-script is BROKEN on this checkout** (both 3.11
  and 3.13): `main._load_repo_script_module` execs `.github/scripts/metadata_survey.py`
  via `exec_module` **without inserting it into `sys.modules`**, so a `@dataclass`
  field-type check does `sys.modules.get(cls.__module__).__dict__` on `None` →
  `AttributeError: 'NoneType' object has no attribute '__dict__'`. The *logic* is
  fine — `tests.test_metadata_survey` passes by importing the module normally. To
  demo a `_load_repo_script_module` entrypoint, use **`civic_scaffold --format json`**
  (works). Don't put `metadata_survey` in a smoke path.
- **The full test suite deletes tracked fixtures** under
  `tests/_tmp_topology_census_case/`, dirtying the tree. Restore with
  `git checkout -- tests/_tmp_topology_census_case/` (the driver does this).
- **Checkout-only entrypoints** (`metadata_survey`, `civic_scaffold`,
  `five_wizards_threshold`, `test`) `SystemExit` unless run from a repo root
  containing `AGENTS.md` + `CONSTITUTION.md`.
- **CLI flag is `--format json`**, not `--json` (the latter exits 2).

## Troubleshooting

| Symptom | Fix |
|---|---|
| `No interpreter found for Python 3.13.3` | `uv python install 3.13.3`, or use the 3.11 fallback build |
| Run stalls ~30s, then a `telemetry.crewai.com … timed out` line | set `CREWAI_DISABLE_TELEMETRY=true OTEL_SDK_DISABLED=true` |
| `metadata_survey`: `AttributeError: 'NoneType' object has no attribute '__dict__'` | known-broken entrypoint; use `civic_scaffold --format json` |
| `… is checkout-only and must run from an IDAHO-VAULT repository root` | `cd` to the repo root before invoking |
| `git status` shows deleted `tests/_tmp_topology_census_case/*` after tests | `git checkout -- tests/_tmp_topology_census_case/` |
