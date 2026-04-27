--- 
authority: AGENT
related:
  - DAILY ROLLOVER
  - QODO
  - DECISIONS
date: 2026-04-26
---

# REPORT: TODO Merge Logic Fix

## Issue
Qodo review (`.qodo/history/f528f00f72f21423df709bb5104dfe181c28474fac473cf1028c3bfd64be534a.json`) flagged a **medium-severity bug** in `.github/scripts/daily_rollover.py`:
- **Problem**: `merge_todo_models` function appended all tasks from secondary (yesterday’s note) to primary (`TO DO LIST.md`), risking **duplicate accumulation**.
- **Impact**: Violated `CONSTITUTION.md`’s "*no scope creep*" rule by bloating the TODO list.

## Fix
Updated `merge_todo_models` to:
1. **Dedupe**: Skip tasks already in `primary`.
2. **Exclude completed tasks**: Ignore lines starting with `- [x]` or `- [X]`.

### Code Changes
```python
def merge_todo_models(primary: dict[str, object], secondary: dict[str, object]) -> dict[str, object]:
    """Merge TODO models, preserving primary order and authority for duplicate tasks.
    
    Only carries forward incomplete tasks from secondary that don't already exist in primary.
    """
    merged = _copy_todo_model(primary)
    
    # Extract existing task keys from primary for dedupe
    existing_keys = set()
    for group_key in merged["group_order"]:
        group = merged["groups"][group_key]
        for block in group["blocks"]:
            for line in block:
                if TASK_RE.match(line):
                    existing_keys.add(line.strip())
    
    for group_key in secondary["group_order"]:
        group = secondary["groups"][group_key]
        for block in group["blocks"]:
            # Skip completed tasks
            if any(line.strip().startswith("- [x]") or line.strip().startswith("- [X]") for line in block):
                continue
            # Skip tasks already in primary
            if any(line.strip() in existing_keys for line in block):
                continue
            _add_block(merged, group_key, group["label"], block)
    return merged
```

## Validation
- **Dry-run test**: Confirmed no duplicates or completed tasks carried forward.
- **Edge cases**: Handles nested tasks (e.g., `- [ ] PARENT\n\t- [ ] CHILD`).

## Next Steps
- **Monitor**: Watch for task bloat in `TO DO LIST.md`.
- **Extend**: Add priority flagging for tasks carried forward >N days (per script’s `Extension points` comment).