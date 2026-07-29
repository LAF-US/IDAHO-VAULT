#!/usr/bin/env python3
"""Exact lifecycle label management for pull requests.

This script is intentionally narrow: it manages the canonical lifecycle
vocabulary from CONSTITUTION.md as `lifecycle/<state>` labels on PRs.
"""

from __future__ import annotations

import argparse

from gh_cli import run as _run

LIFECYCLE_LABELS: dict[str, tuple[str, str]] = {
    "staged": ("1D76DB", "Lifecycle state: staged"),
    "merged": ("6F42C1", "Lifecycle state: merged"),
    "abandoned": ("D1242F", "Lifecycle state: abandoned"),
}

LIFECYCLE_DOCUMENTED: set[str] = {
    "staged",
    "merged",
    "abandoned",
    "live",
    "superseded",
    "dormant",
    "reactivated",
    "archived",
}


def ensure_labels() -> None:
    for state, (color, description) in LIFECYCLE_LABELS.items():
        _run(
            [
                "gh",
                "label",
                "create",
                f"lifecycle/{state}",
                "--color",
                color,
                "--description",
                description,
                "--force",
            ]
        )


def _pr_arg(pr_number: int) -> str:
    """Render a PR number as an argv token, via an explicit int() barrier.

    `--pr-number` is declared `type=int`, so argparse rejects a non-integer before
    set_state ever runs — but that guarantee lives in the parser, far from the `gh`
    call, so a tracer following argv sees only a value derived from user input and
    flags the command line as uncontrolled (CodeQL py/command-line-injection).
    Converting here makes the invariant local: a decimal integer string, or it raises.
    """
    return str(int(pr_number))


def set_state(pr_number: int, state: str) -> None:
    if pr_number <= 0:
        raise ValueError(f"Invalid PR number: {pr_number}")
    if state not in LIFECYCLE_LABELS:
        raise ValueError(f"Unknown lifecycle state: {state}")

    for known_state in LIFECYCLE_LABELS:
        if known_state == state:
            continue
        _run(
            [
                "gh",
                "pr",
                "edit",
                _pr_arg(pr_number),
                "--remove-label",
                f"lifecycle/{known_state}",
            ],
            check=False,
        )

    _run(
        [
            "gh",
            "pr",
            "edit",
            _pr_arg(pr_number),
            "--add-label",
            f"lifecycle/{state}",
        ],
        check=False,
    )


LIFECYCLE_HUMAN_ONLY: set[str] = {
    "live",
    "superseded",
    "dormant",
    "reactivated",
    "archived",
}


def document_states() -> None:
    for state in LIFECYCLE_HUMAN_ONLY:
        _run(
            [
                "gh",
                "label",
                "create",
                f"lifecycle/{state}",
                "--color",
                "8B949E",
                "--description",
                f"[Human-only] Deprecated lifecycle state: {state}",
                "--force",
            ],
            check=False,
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("ensure-labels")

    set_parser = subparsers.add_parser("set-state")
    set_parser.add_argument("--pr-number", required=True, type=int)
    set_parser.add_argument("--state", required=True, choices=sorted(LIFECYCLE_LABELS))

    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.command == "ensure-labels":
        ensure_labels()
        return 0
    set_state(args.pr_number, args.state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
