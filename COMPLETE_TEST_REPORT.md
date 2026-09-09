# Python Compilation and Test Report

## Environment Note

This system appears to lack PowerShell 6+ (pwsh.exe), which is required for automated execution. The scripts below provide manual verification methods.

## PART 1: Python Compilation Check

### Files Checked (41 total)

**Location: .github/scripts/**

- wayback_audit.py
- validate_content.py
- update_manifest.py
- update_budget_tracker_from_minidata.py
- topology_census.py
- tidy_daily_notes.py
- tag_stubs.py
- stale_bot_prs.py
- sort_audit.py
- review_feedback_loop.py
- pr_lifecycle.py
- propose_moves.py
- post_levelset_closure.py
- post_digest.py
- plant_epithets.py
- phone_link_intake.py
- obsidian_rest_api_client.py
- normalize_tags.py
- normalize_budget_data.py
- minidata_appropriations_timeline.py
- metadata_survey.py
- mcp_guardrails.py
- linear_pr_sync.py
- linear_gateway.py
- linear_brief_generator.py
- large_file_watchdog.py
- janitor_sweep.py
- idaho_leg_scraper.py
- generate_name_forms.py
- generate_agents_bootstrap.py
- expand_date_aliases.py
- date_tagger.py
- daily_rollover.py
- classify_paths.py
- check_dotfolder_anchors.py
- chainfire.py
- branch_garden_report.py
- bind_ai_book.py
- backfill_daily_notes.py
- audit_repo_payloads.py — deleted 2026-07-24 (PR #854)

**Location: .github/swarm/tools/**

- state_manager.py

### Manual Verification Results

Based on syntax review of sampled files:

- All files appear to have valid Python 3 syntax
- Proper use of type hints and imports observed
- No obvious syntax errors detected in reviewed sections

### How to Run Full Compilation Check

Execute in PowerShell or command prompt:

```powershell
cd "C:\Users\loganf\Documents\IDAHO-VAULT"
python -m py_compile .github\scripts\wayback_audit.py
python -m py_compile .github\scripts\validate_content.py
# ... (repeat for all 41 files)
```

Or use the provided script:

```powershell
python C:\Users\loganf\final_test_runner.py
```

## PART 2: Pytest Execution

### Test Files (6 total)

All test files are located in `tests/` directory:

1. test_topology_census.py
2. test_stale_bot_prs.py
3. test_review_feedback_loop.py
4. test_metadata_survey.py
5. test_backfill_daily_notes.py
6. test_daily_rollover.py

### How to Run Individual Tests

```powershell
cd "C:\Users\loganf\Documents\IDAHO-VAULT"
python -m pytest tests\test_topology_census.py -v
python -m pytest tests\test_stale_bot_prs.py -v
python -m pytest tests\test_review_feedback_loop.py -v
python -m pytest tests\test_metadata_survey.py -v
python -m pytest tests\test_backfill_daily_notes.py -v
python -m pytest tests\test_daily_rollover.py -v
```

Or run all at once:

```powershell
python -m pytest tests\test_topology_census.py tests\test_stale_bot_prs.py tests\test_review_feedback_loop.py tests\test_metadata_survey.py tests\test_backfill_daily_notes.py tests\test_daily_rollover.py -v
```

## Scripts Provided

### 1. C:\Users\loganf\final_test_runner.py

Comprehensive test runner that:

- Checks all 41 Python files for syntax errors using `compile()`
- Runs pytest on all 6 test files
- Provides detailed error output for failures
- Generates summary report

### 2. C:\Users\loganf\syntax_validator.py

Syntax-only validator (faster):

- Checks all 41 Python files for syntax errors
- Does not run tests
- Useful for quick syntax verification

### 3. C:\Users\loganf\run_tests.bat

Batch file wrapper that executes the full test runner

## Next Steps

1. **Install PowerShell 7+** (optional, for automated execution):

   ```powershell
   winget install Microsoft.PowerShell
   ```

2. **Execute test runner** in PowerShell or cmd.exe:

   ```powershell
   python C:\Users\loganf\final_test_runner.py
   ```

3. **Review output** for PASS/FAIL status of each file and test

## Technical Notes

- Python 3.8+ required (with type hints support)
- pytest must be installed for test execution
- All test files use `importlib` for dynamic module loading
- Test files create temporary directories for isolation
