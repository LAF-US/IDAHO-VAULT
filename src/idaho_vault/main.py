#!/usr/bin/env python
"""CLI entrypoints for the IDAHO-VAULT CrewAI bootstrap shard."""

from __future__ import annotations

import json
import sys

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

from idaho_vault.crew import IdahoVaultBootstrapCrew


def _execute() -> str:
    """Execute the bootstrap validation crew and return its raw output."""
    result = IdahoVaultBootstrapCrew().crew().kickoff()
    if result is None:
        return ""
    return str(getattr(result, "raw", result))


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
    """Testing is intentionally deferred for the bootstrap shard."""
    raise SystemExit("Use `crewai run` for bootstrap validation; eval LLM testing is not configured yet.")


def run_with_trigger() -> None:
    """Accept a JSON trigger payload and still run the same validation shard."""
    if len(sys.argv) < 2:
        raise SystemExit("No trigger payload provided.")

    try:
        json.loads(sys.argv[1])
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid trigger payload: {exc}") from exc

    run()
