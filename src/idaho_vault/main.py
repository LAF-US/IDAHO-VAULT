#!/usr/bin/env python
"""CLI entrypoints for the IDAHO-VAULT CrewAI bootstrap shard."""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

from idaho_vault.bootstrap_contract import build_contract_report
from idaho_vault.runtime import configure_vault_runtime


def _force_utf8_stdio() -> None:
    """Keep CrewAI's Windows console output from dying on emoji/status glyphs."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


_force_utf8_stdio()
configure_vault_runtime()

def _execute() -> str:
    """Execute the bootstrap validation crew and return its raw output."""
    from idaho_vault.crew import IdahoVaultBootstrapCrew

    report = build_contract_report()
    result = IdahoVaultBootstrapCrew(report=report).crew().kickoff()
    if result is None:
        return ""
    raw = str(getattr(result, "raw", result))
    return f"{report.to_markdown()}\n\n---\n\n{raw}".strip()


def _coerce_relaxed_trigger_payload(payload: str) -> dict[str, object]:
    """Parse a trigger payload, tolerating PowerShell-mangled object syntax.

    On Windows PowerShell, a JSON object argument such as
    `{"source":"toolkit-test"}` may arrive as `{source:toolkit-test}` when
    passed to a native CLI. We accept strict JSON first, then repair that
    relaxed object form for bootstrap use.
    """
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        normalized = payload.strip()
        if not (normalized.startswith("{") and normalized.endswith("}")):
            raise

        normalized = re.sub(
            r'([{,]\s*)([A-Za-z_][A-Za-z0-9_-]*)(\s*:)',
            r'\1"\2"\3',
            normalized,
        )

        def _quote_value(match: re.Match[str]) -> str:
            value = match.group(1)
            suffix = match.group(2)
            lowered = value.lower()
            if lowered in {"true", "false", "null"}:
                return f": {lowered}{suffix}"
            if re.fullmatch(r"-?\d+(?:\.\d+)?", value):
                return f": {value}{suffix}"
            return f': "{value}"{suffix}'

        normalized = re.sub(
            r':\s*([A-Za-z_./-][A-Za-z0-9_./-]*)(\s*[,}])',
            _quote_value,
            normalized,
        )
        parsed = json.loads(normalized)

    if not isinstance(parsed, dict):
        raise json.JSONDecodeError("Trigger payload must decode to an object.", payload, 0)

    return parsed


def run() -> None:
    """Run the bootstrap validation crew."""
    output = _execute()
    if output:
        print(output)


def train() -> None:
    """Training is intentionally deferred for the bootstrap shard."""
    raise SystemExit("Training is not implemented for the bootstrap validation shard.")


def replay() -> None:
    """Replay is intentionally deferred for the bootstrap shard."""
    raise SystemExit("Replay is not implemented for the bootstrap validation shard.")


def test() -> None:
    """Run the repository test suite from a plain checkout or installed environment."""
    repo_root = Path(__file__).resolve().parents[2]
    src_root = repo_root / "src"
    tests_root = repo_root / "tests"

    if str(src_root) not in sys.path:
        sys.path.insert(0, str(src_root))

    suite = unittest.defaultTestLoader.discover(
        start_dir=str(tests_root),
        pattern="test_*.py",
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)


def run_with_trigger() -> None:
    """Accept a JSON trigger payload and still run the same validation shard."""
    if len(sys.argv) < 2:
        raise SystemExit("No trigger payload provided.")

    try:
        _coerce_relaxed_trigger_payload(sys.argv[1])
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid trigger payload: {exc}") from exc

    run()


def run_five_wizards_threshold() -> None:
    """Run the fixed 5Wizards threshold slice and stage it to !/CREWAI/."""
    from idaho_vault.five_wizards.threshold_runner import (
        render_threshold_stage_summary,
        run_threshold_stage,
    )

    result = run_threshold_stage()
    print(render_threshold_stage_summary(result))
