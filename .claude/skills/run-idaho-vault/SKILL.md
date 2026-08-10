---
name: run-idaho-vault
description: Build, run, smoke-test, and validate the idaho_vault CrewAI deployment-validation shard — run the bootstrap validation crew and drive its CLI entrypoints, all offline with no API keys. Use when asked to run / start / build / test / smoke / validate idaho_vault, the CrewAI bootstrap, or src/idaho_vault.
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
> the env if needed, runs the crew, and drives the offline entrypoints. Start
> there.
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
python .claude/skills/run-idaho-vault/driver.py test   # no-op, exits 0 (see Test)
```

Full smoke prints, and exits 0 on success:

```text
== run_crew: bootstrap validation crew (offline mock LLM) ==
Overall status: PASS
  -> run_crew OK (PASS)
== five_wizards_threshold --dry-run (no materialization) ==
...
== civic_scaffold --format json (checkout-only; validate JSON) ==
  -> valid JSON
== test mode ==
  -> no tests/ directory; nothing to run
SMOKE PASS — validation crew + offline entrypoints OK
```

The driver sets the CrewAI telemetry-off env vars for you. `all` mode exits 0
on a healthy checkout. **`test` mode is now a no-op that exits 0** — `tests/`
was deleted in #928, and "nothing to run" is not a failure. The mode is kept so
the documented interface still works rather than erroring on an unknown
argument.

## Direct invocation (single entrypoints)

The package installs console scripts; once the env exists, run any directly
(set the telemetry env first to avoid a 30s hang):

```bash
export CREWAI_DISABLE_TELEMETRY=true OTEL_SDK_DISABLED=true
uv run run_crew                          # the validation crew -> PASS report
uv run five_wizards_threshold --dry-run  # gate/council preview, no writes
uv run civic_scaffold --format json      # emits civic-scaffold JSON
```

## Test

`driver.py test` is a **no-op that exits 0**. There is no suite: `tests/` was
deleted in #928. The mode is kept so callers and scripts do not break on an
unknown argument.

If a suite ever returns, hold each test to a standard the deleted one was not:
neuter what it guards and confirm it goes red. The old suite failed that two
ways — some tests could not fail at all (one passed against a `.gitignore` that
ignored nothing), and some failed for the wrong reason (one asserted a redundant
API call, so removing the redundancy read as a regression).

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
  fine — importing the module normally works; only the `exec_module` path fails.
  (A test used to demonstrate that; it went with `tests/` in #928, so this is now
  an unverified claim about the cause, not about the symptom, which reproduces.)
  To demo a `_load_repo_script_module` entrypoint, use **`civic_scaffold --format json`**
  (works). Don't put `metadata_survey` in a smoke path.
- **Checkout-only entrypoints** (`metadata_survey`, `civic_scaffold`,
  `five_wizards_threshold`, `test`) `SystemExit` unless run from a repo root
  containing `AGENTS.md` + `CONSTITUTION.md`.
- **CLI flag is `--format json`**, not `--json` (the latter exits 2).

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `No interpreter found for Python 3.13.3` | `uv python install 3.13.3`, or use the 3.11 fallback build |
| Run stalls ~30s, then a `telemetry.crewai.com … timed out` line | set `CREWAI_DISABLE_TELEMETRY=true OTEL_SDK_DISABLED=true` |
| `metadata_survey`: `AttributeError: 'NoneType' object has no attribute '__dict__'` | known-broken entrypoint; use `civic_scaffold --format json` |
| `… is checkout-only and must run from an IDAHO-VAULT repository root` | `cd` to the repo root before invoking |
