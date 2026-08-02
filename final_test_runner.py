#!/usr/bin/env python3
"""
Direct Python syntax checker and test runner.
Generates a comprehensive report without relying on subprocess.
"""

import sys
import os
import subprocess

# Change to repo directory
os.chdir(r"C:\Users\loganf\Documents\IDAHO-VAULT")

# Map files with forward slashes to backslashes for Windows
COMPILE_FILES = [
    ".github\\scripts\\wayback_audit.py",
    ".github\\scripts\\validate_content.py",
    ".github\\scripts\\update_manifest.py",
    ".github\\scripts\\update_budget_tracker_from_minidata.py",
    ".github\\scripts\\topology_census.py",
    ".github\\scripts\\tidy_daily_notes.py",
    ".github\\scripts\\tag_stubs.py",
    ".github\\scripts\\stale_bot_prs.py",
    ".github\\scripts\\sort_audit.py",
    ".github\\scripts\\review_feedback_loop.py",
    ".github\\scripts\\pr_lifecycle.py",
    ".github\\scripts\\propose_moves.py",
    ".github\\scripts\\post_levelset_closure.py",
    ".github\\scripts\\post_digest.py",
    ".github\\scripts\\plant_epithets.py",
    ".github\\scripts\\phone_link_intake.py",
    ".github\\scripts\\obsidian_rest_api_client.py",
    ".github\\scripts\\normalize_tags.py",
    ".github\\scripts\\normalize_budget_data.py",
    ".github\\scripts\\minidata_appropriations_timeline.py",
    ".github\\scripts\\metadata_survey.py",
    ".github\\scripts\\mcp_guardrails.py",
    ".github\\scripts\\linear_pr_sync.py",
    ".github\\scripts\\linear_gateway.py",
    ".github\\scripts\\linear_brief_generator.py",
    ".github\\scripts\\large_file_watchdog.py",
    ".github\\scripts\\janitor_sweep.py",
    ".github\\scripts\\idaho_leg_scraper.py",
    ".github\\scripts\\generate_name_forms.py",
    ".github\\scripts\\generate_agents_bootstrap.py",
    ".github\\scripts\\expand_date_aliases.py",
    ".github\\scripts\\date_tagger.py",
    ".github\\scripts\\daily_rollover.py",
    ".github\\scripts\\classify_paths.py",
    ".github\\scripts\\check_dotfolder_anchors.py",
    ".github\\scripts\\chainfire.py",
    ".github\\scripts\\branch_garden_report.py",
    ".github\\scripts\\bind_ai_book.py",
    ".github\\scripts\\backfill_daily_notes.py",
    ".github\\scripts\\audit_repo_payloads.py",
    ".github\\swarm\\tools\\state_manager.py",
]

print("=" * 80)
print("PART 1: PYTHON COMPILATION CHECK")
print("=" * 80)
print()

compile_results = []

for filepath in COMPILE_FILES:
    abs_path = os.path.abspath(filepath)
    try:
        if not os.path.exists(abs_path):
            print(f"✗ FAIL: {filepath}")
            print("  Error: File not found")
            compile_results.append((filepath, "FAIL", "File not found"))
        else:
            with open(abs_path, 'r', encoding='utf-8', errors='replace') as f:
                code = f.read()
            
            compile(code, abs_path, 'exec')
            print(f"✓ PASS: {filepath}")
            compile_results.append((filepath, "PASS", None))
            
    except SyntaxError as e:
        print(f"✗ FAIL: {filepath}")
        error_msg = f"SyntaxError at line {e.lineno}: {e.msg}"
        print(f"  Error: {error_msg}")
        if e.text:
            print(f"  Code: {e.text.strip()}")
        compile_results.append((filepath, "FAIL", error_msg))
        
    except Exception as e:
        print(f"✗ FAIL: {filepath}")
        error_msg = f"{type(e).__name__}: {str(e)}"
        print(f"  Error: {error_msg}")
        compile_results.append((filepath, "FAIL", error_msg))

print()
print("=" * 80)
print("PART 2: PYTEST EXECUTION")
print("=" * 80)
print()

TEST_FILES = [
    "tests\\test_topology_census.py",
    "tests\\test_stale_bot_prs.py",
    "tests\\test_review_feedback_loop.py",
    "tests\\test_metadata_survey.py",
    "tests\\test_backfill_daily_notes.py",
    "tests\\test_daily_rollover.py",
]

test_results = []

for test_file in TEST_FILES:
    print(f"\n--- {test_file} ---")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=os.getcwd()
        )
        
        if result.returncode == 0:
            print("✓ PASS")
            test_results.append((test_file, "PASS", None))
        else:
            print("✗ FAIL")
            output = result.stdout
            if result.stderr:
                output = result.stderr + "\n" + output
            print("Output:")
            print(output if output else "(no output)")
            test_results.append((test_file, "FAIL", output))
            
    except subprocess.TimeoutExpired:
        print("✗ FAIL")
        print("Error: Timeout (>60s)")
        test_results.append((test_file, "FAIL", "Timeout (>60s)"))
        
    except FileNotFoundError:
        print("✗ FAIL")
        print("Error: pytest not found or test file not found")
        test_results.append((test_file, "FAIL", "pytest not found"))
        
    except Exception as e:
        print("✗ FAIL")
        print(f"Error: {type(e).__name__}: {str(e)}")
        test_results.append((test_file, "FAIL", str(e)))

print()
print("=" * 80)
print("SUMMARY")
print("=" * 80)
print()

compile_pass = sum(1 for _, status, _ in compile_results if status == "PASS")
compile_fail = sum(1 for _, status, _ in compile_results if status == "FAIL")
print(f"Compilation: {compile_pass} PASS, {compile_fail} FAIL ({len(COMPILE_FILES)} total)")

test_pass = sum(1 for _, status, _ in test_results if status == "PASS")
test_fail = sum(1 for _, status, _ in test_results if status == "FAIL")
print(f"Tests: {test_pass} PASS, {test_fail} FAIL ({len(TEST_FILES)} total)")

print()
if compile_fail == 0 and test_fail == 0:
    print("✓ ALL CHECKS PASSED")
    sys.exit(0)
else:
    print("✗ SOME CHECKS FAILED")
    sys.exit(1)
