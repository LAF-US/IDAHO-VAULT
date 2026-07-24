#!/usr/bin/env python
"""Run compilation checks and pytest on specified files."""

import subprocess
import sys
import os

os.chdir(r"C:\Users\loganf\Documents\IDAHO-VAULT")

compile_files = [
    r".github\scripts\wayback_audit.py",
    r".github\scripts\validate_content.py",
    r".github\scripts\update_manifest.py",
    r".github\scripts\update_budget_tracker_from_minidata.py",
    r".github\scripts\topology_census.py",
    r".github\scripts\tidy_daily_notes.py",
    r".github\scripts\tag_stubs.py",
    r".github\scripts\stale_bot_prs.py",
    r".github\scripts\sort_audit.py",
    r".github\scripts\review_feedback_loop.py",
    r".github\scripts\pr_lifecycle.py",
    r".github\scripts\propose_moves.py",
    r".github\scripts\post_levelset_closure.py",
    r".github\scripts\post_digest.py",
    r".github\scripts\plant_epithets.py",
    r".github\scripts\phone_link_intake.py",
    r".github\scripts\obsidian_rest_api_client.py",
    r".github\scripts\normalize_tags.py",
    r".github\scripts\normalize_budget_data.py",
    r".github\scripts\minidata_appropriations_timeline.py",
    r".github\scripts\metadata_survey.py",
    r".github\scripts\mcp_guardrails.py",
    r".github\scripts\linear_pr_sync.py",
    r".github\scripts\linear_gateway.py",
    r".github\scripts\linear_brief_generator.py",
    r".github\scripts\large_file_watchdog.py",
    r".github\scripts\janitor_sweep.py",
    r".github\scripts\idaho_leg_scraper.py",
    r".github\scripts\generate_name_forms.py",
    r".github\scripts\generate_agents_bootstrap.py",
    r".github\scripts\expand_date_aliases.py",
    r".github\scripts\date_tagger.py",
    r".github\scripts\daily_rollover.py",
    r".github\scripts\classify_paths.py",
    r".github\scripts\check_dotfolder_anchors.py",
    r".github\scripts\chainfire.py",
    r".github\scripts\branch_garden_report.py",
    r".github\scripts\bind_ai_book.py",
    r".github\scripts\backfill_daily_notes.py",
    # audit_repo_payloads.py removed 2026-07-24 (unwired one-shot slimming auditor; PR #854)
    r".github\swarm\tools\state_manager.py",
]

test_files = [
    r"tests\test_topology_census.py",
    r"tests\test_stale_bot_prs.py",
    r"tests\test_review_feedback_loop.py",
    r"tests\test_metadata_survey.py",
    r"tests\test_backfill_daily_notes.py",
    r"tests\test_daily_rollover.py",
]

print("=" * 70)
print("PART 1: PYTHON COMPILATION CHECK")
print("=" * 70)
print()

for filepath in compile_files:
    result = subprocess.run(
        [sys.executable, "-m", "py_compile", filepath],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"✓ PASS: {filepath}")
    else:
        print(f"✗ FAIL: {filepath}")
        if result.stderr:
            print(f"  Error: {result.stderr.strip()}")
        if result.stdout:
            print(f"  Output: {result.stdout.strip()}")

print()
print("=" * 70)
print("PART 2: PYTEST EXECUTION")
print("=" * 70)
print()

for test_file in test_files:
    print(f"\n--- {test_file} ---")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_file, "-v"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"✓ PASS")
    else:
        print(f"✗ FAIL")
        print("Output:")
        print(result.stdout)
        if result.stderr:
            print("Stderr:")
            print(result.stderr)
