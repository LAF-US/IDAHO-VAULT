#!/usr/bin/env python3
"""
Comprehensive test runner for compilation checks and pytest execution.
"""

import subprocess
import sys
import os

# Change to repo directory
os.chdir(r"C:\Users\loganf\Documents\IDAHO-VAULT")

# List of files to compile check
COMPILE_FILES = [
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
    r".github\scripts\thread_witness.py",
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

TEST_FILES = [
    r"tests\test_topology_census.py",
    r"tests\test_stale_bot_prs.py",
    r"tests\test_review_feedback_loop.py",
    r"tests\test_thread_witness.py",
    r"tests\test_gh_cli.py",
    r"tests\test_metadata_survey.py",
    r"tests\test_backfill_daily_notes.py",
    r"tests\test_daily_rollover.py",
]


def run_compilation_checks():
    """Run py_compile on all specified files."""
    print("=" * 80)
    print("PART 1: PYTHON COMPILATION CHECK")
    print("=" * 80)
    print()
    
    results = []
    for filepath in COMPILE_FILES:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "py_compile", filepath],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            
            if result.returncode == 0:
                print(f"✓ PASS: {filepath}")
                results.append((filepath, "PASS", None))
            else:
                error_msg = result.stderr if result.stderr else result.stdout
                print(f"✗ FAIL: {filepath}")
                if error_msg:
                    print(f"  Error: {error_msg.strip()}")
                results.append((filepath, "FAIL", error_msg.strip()))
        except subprocess.TimeoutExpired:
            print(f"✗ FAIL: {filepath}")
            print("  Error: Timeout (>10s)")
            results.append((filepath, "FAIL", "Timeout (>10s)"))
        except Exception as e:  # pylint: disable=broad-except
            print(f"✗ FAIL: {filepath}")
            print(f"  Error: {str(e)}")
            results.append((filepath, "FAIL", str(e)))
    
    print()
    return results


def run_pytest_tests():
    """Run pytest on all specified test files."""
    print("=" * 80)
    print("PART 2: PYTEST EXECUTION")
    print("=" * 80)
    print()
    
    results = []
    for test_file in TEST_FILES:
        print(f"\n--- {test_file} ---")
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            
            if result.returncode == 0:
                print("✓ PASS")
                results.append((test_file, "PASS", None))
            else:
                output = result.stdout
                if result.stderr:
                    output = output + "\n" + result.stderr
                print("✗ FAIL")
                print("Output:")
                print(output)
                results.append((test_file, "FAIL", output))
        except subprocess.TimeoutExpired:
            print("✗ FAIL")
            print("  Error: Timeout (>60s)")
            results.append((test_file, "FAIL", "Timeout (>60s)"))
        except Exception as e:  # pylint: disable=broad-except
            print("✗ FAIL")
            print(f"  Error: {str(e)}")
            results.append((test_file, "FAIL", str(e)))
    
    print()
    return results


def main():
    """Run all checks and tests."""
    compile_results = run_compilation_checks()
    test_results = run_pytest_tests()
    
    # Summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print()
    
    compile_pass = sum(1 for _, status, _ in compile_results if status == "PASS")
    compile_fail = sum(1 for _, status, _ in compile_results if status == "FAIL")
    print(f"Compilation: {compile_pass} PASS, {compile_fail} FAIL")
    
    test_pass = sum(1 for _, status, _ in test_results if status == "PASS")
    test_fail = sum(1 for _, status, _ in test_results if status == "FAIL")
    print(f"Tests: {test_pass} PASS, {test_fail} FAIL")


if __name__ == "__main__":
    main()
