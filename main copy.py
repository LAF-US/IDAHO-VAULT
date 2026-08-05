#!/usr/bin/env python
"""CLI entrypoints for the IDAHO-VAULT CrewAI bootstrap shard."""

from __future__ import annotations

import argparse
import importlib.util
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


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _is_valid_module_spec(spec: object) -> bool:
    return bool(spec is not None and spec.loader is not None and hasattr(spec.loader, "exec_module"))


def _require_checkout(command_name: str, *, required_paths: tuple[str, ...] = ()) -> Path:
    repo_root = _repo_root()
    required = ("AGENTS.md", "CONSTITUTION.md", *required_paths)
    missing = [relpath for relpath in required if not (repo_root / relpath).exists()]
    if missing:
        missing_rendered = ", ".join(missing)
        raise SystemExit(
            f"{command_name} is checkout-only and must run from an IDAHO-VAULT repository root. "
            f"Missing required path(s): {missing_rendered}"
        )
    return repo_root


def _load_repo_script_module(script_name: str, *, command_name: str):
    repo_root = _require_checkout(command_name)
    script_path = repo_root / ".github" / "scripts" / script_name
    if not script_path.exists():
        raise SystemExit(f"Required script was not found: {script_path}")
    normalized_script_name = re.sub(r"[^A-Za-z0-9_]", "_", script_name)
    module_name = f"idaho_vault_{normalized_script_name}"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    if not _is_valid_module_spec(spec):
        raise SystemExit(f"Unable to load script module from: {script_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


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
    # Test discovery depends on the repository's tracked tests directory and root wiring.
    repo_root = _require_checkout("test", required_paths=("tests",))
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
    parser = argparse.ArgumentParser(
        prog="five_wizards_threshold",
        description="Run the 5Wizards threshold slice from a local vault checkout.",
    )
    parser.add_argument(
        "--run-id",
        help="Optional explicit run id for deterministic staging paths.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Evaluate and render without writing staged artifacts.",
    )
    args = parser.parse_args(sys.argv[1:])

    repo_root = _require_checkout("five_wizards_threshold")
    from idaho_vault.operator_context import load_operator_context
    from idaho_vault.five_wizards.threshold_runner import (
        render_threshold_stage_summary,
        run_threshold_stage,
    )

    context = load_operator_context(root=repo_root)
    result = run_threshold_stage(
        run_id=args.run_id,
        materialize=not args.dry_run,
        context=context,
    )
    print(render_threshold_stage_summary(result, context=context))


def run_civic_scaffold() -> None:
    """Render the current civic scaffold through a truthful local CLI front door."""
    parser = argparse.ArgumentParser(
        prog="civic_scaffold",
        description="Render the civic scaffold from the current local checkout.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        help="Optional output file path. Defaults to stdout.",
    )
    args = parser.parse_args(sys.argv[1:])

    repo_root = _require_checkout("civic_scaffold")
    from idaho_vault.civic_scaffold import build_civic_scaffold, render_civic_scaffold_markdown
    from idaho_vault.operator_context import load_operator_context

    context = load_operator_context(root=repo_root)
    scaffold = build_civic_scaffold(context=context)
    if args.format == "json":
        rendered = json.dumps(scaffold.to_dict(), indent=2, ensure_ascii=False)
    else:
        rendered = render_civic_scaffold_markdown(scaffold)

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
        return
    print(rendered)


def run_metadata_survey() -> None:
    """Run the metadata/frontmatter survey from the local checkout."""
    parser = argparse.ArgumentParser(
        prog="metadata_survey",
        description="Survey markdown frontmatter state for this vault checkout.",
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Include the _private directory in the scan.",
    )
    parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        help="Optional output path. Defaults to stdout.",
    )
    args = parser.parse_args(sys.argv[1:])

    repo_root = _require_checkout("metadata_survey")
    metadata_survey = _load_repo_script_module("metadata_survey.py", command_name="metadata_survey")
    summary = metadata_survey.survey_vault(repo_root, include_private=args.include_private)
    if args.format == "markdown":
        rendered = metadata_survey.render_markdown(summary)
    else:
        rendered = json.dumps(summary, indent=2, ensure_ascii=False)

    if args.output:
        Path(args.output).write_text(rendered, encoding="utf-8")
        return
    print(rendered)
