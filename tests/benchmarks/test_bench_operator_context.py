"""Benchmarks for the operator front-door context loader.

`idaho_vault.operator_context` resolves the live boot chain, the daily-note
surface, and the active backlog every time an agent orients itself in the
vault. The pure parts of that work — date rendering, backlog extraction, and
evidence-ref resolution — are what these benchmarks measure.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest

from idaho_vault import operator_context as oc


BACKLOG_SECTIONS = ("## Active", "## Waiting", "## Done")


@pytest.fixture(scope="session")
def todo_list_content() -> str:
    lines: list[str] = ["# TO DO LIST", ""]
    for section in BACKLOG_SECTIONS:
        lines.append(section)
        lines.append("")
        for index in range(150):
            marker = " " if section == "## Active" else "x"
            lines.append(f"- [{marker}] {section[3:].lower()} item {index}")
        lines.append("")
    return "\n".join(lines)


@pytest.fixture(scope="session")
def evidence_refs() -> list[str]:
    refs: list[str] = []
    for index in range(400):
        refs.append(f"!/handoffs/handoff-{index:04d}.md#section-{index % 7}")
        refs.append(f"GOVERNMENTS/IDAHO - LEGISLATIVE/BILLS/bill-{index:04d}.md")
    return refs


def test_render_obsidian_date(benchmark):
    """Expand an Obsidian periodic-note format string for a given day."""
    target = date(2026, 4, 19)

    rendered = benchmark(lambda: oc._render_obsidian_date(target, "GGGG-[W]WW/YYYY-MM-DD"))

    assert rendered == "2026-W16/2026-04-19"


def test_extract_active_section(benchmark, todo_list_content):
    """Slice the `## Active` section out of the carryforward list."""
    active = benchmark(lambda: oc._extract_active_section(todo_list_content))

    assert len(active) > 100


def test_open_backlog_items(benchmark, todo_list_content):
    """Filter the active section down to genuinely open checklist items."""
    active = oc._extract_active_section(todo_list_content)

    def load_open_backlog_items():
        context = oc.OperatorContext(
            root=Path("."),
            target_date=date(2026, 4, 19),
            boot_chain_checks=(),
            front_door_checks=(),
            daily_note_path="2026-04-19.md",
            daily_note_exists=True,
            daily_note_tracked=True,
            daily_note_folder="",
            daily_note_format="YYYY-MM-DD",
            active_backlog_lines=active,
        )
        return context.open_backlog_items

    items = benchmark(load_open_backlog_items)

    assert len(items) == 150


def test_evaluate_evidence_refs(benchmark, tmp_path_factory, evidence_refs):
    """Resolve a large evidence-ref list against a tracked-file index."""
    root = tmp_path_factory.mktemp("vault-root")
    tracked = {ref.split("#", 1)[0] for ref in evidence_refs}

    statuses = benchmark(
        lambda: oc.evaluate_evidence_refs(evidence_refs, root=root, tracked_files=tracked)
    )

    assert len(statuses) == len(evidence_refs)
