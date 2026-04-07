#!/usr/bin/env python3
"""
daily_rollover.py - IDAHO-VAULT

Carries incomplete to-do items forward from yesterday's daily note into today's.
Runs as a scheduled GitHub Action each morning.

Extension points (future stages):
  - Habit tracker section: add inject_habit_section() and call from main()
  - Weekly review digest: aggregate carry-forward counts over 7 days
  - Priority flagging: age-based escalation for items carried N+ days

Usage:
    python3 .github/scripts/daily_rollover.py [--date YYYY-MM-DD] [--dry-run]

Arguments:
    --date      Target date to roll INTO (default: today). Rolls FROM the day before.
    --dry-run   Print output without writing files.
"""

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

VAULT_ROOT = Path(__file__).resolve().parents[2]
TODO_LIST_FILE = VAULT_ROOT / "TO DO LIST.md"

# ---------------------------------------------------------------------------
# Regex
# ---------------------------------------------------------------------------

# Matches markdown task lines: optional leading tabs/spaces, "- [ ]" or "- [x]", text
TASK_RE = re.compile(r'^([ \t]*)- \[( |x|X)\] (.+)$')
TODO_MARKER = "[[TO DO LIST]]"
PLACEHOLDER_LINE = "*(no incomplete items carried forward)*"
FRONTMATTER_RE = re.compile(r'\A---\r?\n(?P<frontmatter>.*?)\r?\n---\r?\n?', re.DOTALL)


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def extract_todo_section(content: str) -> list[str]:
    """
    Return lines from the canonical [[TO DO LIST]] marker.

    Stop at the next frontmatter-style separator, next-level header, 
    or end of file. Preserves organizational bullets (- WORK, - PERSONAL).
    """
    lines = content.splitlines()
    in_todo = False
    todo_lines = []
    for line in lines:
        if is_todo_marker(line):
            in_todo = True
            continue
        if in_todo:
            # Stop if we hit a substantial new section or divider
            if line.strip() == "---" or line.startswith("## ") or line.startswith("Notes:"):
                break
            todo_lines.append(line)
    return todo_lines


def log(message: str = "") -> None:
    """Safe stdout printing for both *nix and Windows."""
    # Ensure no wandering carriage returns mess up the terminal buffer
    if isinstance(message, str):
        message = message.replace("\r", "")
    print(message)


def is_todo_marker(line: str) -> bool:
    return line.strip() == TODO_MARKER


def carry_forward(todo_lines: list[str]) -> list[str]:
    """
    Given raw task lines from a daily note's TODO section, return only the
    incomplete items - with only their incomplete sub-items.

    Rules:
      - Top-level [x]: dropped entirely.
      - Top-level [ ]: kept. Sub-items: only [ ] sub-items kept.
      - If a [ ] parent has ALL sub-items done: parent kept, no sub-items
        (parent not marked complete by the user yet).
    """
    result = []
    i = 0

    while i < len(todo_lines):
        line = todo_lines[i]
        m = TASK_RE.match(line)

        if not m:
            i += 1
            continue

        indent_level = len(m.group(1))
        done = m.group(2).lower() == "x"

        if indent_level > 0:
            i += 1
            continue

        block = [line]
        j = i + 1
        while j < len(todo_lines):
            next_line = todo_lines[j]
            next_m = TASK_RE.match(next_line)
            if next_m and len(next_m.group(1)) == 0:
                break
            block.append(next_line)
            j += 1

        if not done:
            result.append(block[0].rstrip())
            for sub_line in block[1:]:
                sub_m = TASK_RE.match(sub_line)
                if sub_m and sub_m.group(2).lower() != "x":
                    result.append(sub_line.rstrip())

        i = j

    return result


# ---------------------------------------------------------------------------
# Daily note helpers
# ---------------------------------------------------------------------------

def _ordinal(n: int) -> str:
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    return f"{n}{['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]}"


_WEEKDAY_ABBREV = {
    "Monday": "mon", "Tuesday": "tue", "Wednesday": "wed",
    "Thursday": "thu", "Friday": "fri", "Saturday": "sat", "Sunday": "sun",
}


def date_aliases(target_date: date) -> list[str]:
    """Return the canonical set of date aliases for a daily note."""
    weekday = target_date.strftime("%A")
    month = target_date.strftime("%B")
    day = target_date.day
    day_ord = _ordinal(day)
    year = target_date.year
    return [
        str(target_date),
        f"{month} {day}, {year}",
        f"{month} {day_ord}, {year}",
        f"{day} {month} {year}",
        f"{weekday}, {month} {day}, {year}",
    ]


def parse_frontmatter(content: str) -> dict[str, str]:
    """Extract frontmatter as a raw key-value mapping (very basic)."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return {}
    
    block = match.group("frontmatter")
    # Simple line-based split for basic YAML keys
    kv = {}
    for line in block.splitlines():
        if ":" in line and not line.startswith(" "):
            key, val = line.split(":", 1)
            kv[key.strip()] = val.strip()
    return kv


def build_frontmatter(target_date: date) -> str:
    yesterday = target_date - timedelta(days=1)
    tomorrow = target_date + timedelta(days=1)
    weekday = target_date.strftime("%A")
    month = target_date.strftime("%B")
    day_ord = _ordinal(target_date.day)
    year = target_date.year
    created = f"{weekday}, {month} {day_ord} {year}, 12:00:00 am"
    tag_date = target_date.strftime("%Y/%m/%d")
    alias_lines = "".join(f"  - {a}\n" for a in date_aliases(target_date))
    cssclass = f"roygbiv-{_WEEKDAY_ABBREV[weekday]}"

    return (
        f"---\n"
        f"title: {target_date}\n"
        f"aliases:\n"
        f"{alias_lines}"
        f"linter-yaml-title-alias: {target_date}\n"
        f"yesterday: {yesterday}\n"
        f"tomorrow: {tomorrow}\n"
        f"weekday:\n"
        f"  - {weekday}\n"
        f"cssclasses:\n"
        f"  - {cssclass}\n"
        f"tags:\n"
        f"  - today\n"
        f"  - {tag_date}\n"
        f"  - dailynote\n"
        f"date created: {created}\n"
        f"date modified: {created}\n"
        f"---"
    )


def todo_block_text(lines: list[str]) -> str:
    if lines:
        return "\n".join(lines)
    return PLACEHOLDER_LINE


def _clean_todo_lines(lines: list[str]) -> list[str]:
    cleaned = []
    for line in lines:
        stripped = line.strip("\r\n")
        if not stripped or stripped == PLACEHOLDER_LINE:
            continue
        cleaned.append(stripped)
    return cleaned


def _split_todo_blocks(lines: list[str]) -> list[list[str]]:
    blocks = []
    current_block = None

    for line in _clean_todo_lines(lines):
        match = TASK_RE.match(line)
        is_top_level_task = bool(match and len(match.group(1)) == 0)

        if is_top_level_task:
            if current_block:
                blocks.append(current_block)
            current_block = [line]
            continue

        if current_block is None:
            blocks.append([line])
            continue

        current_block.append(line)

    if current_block:
        blocks.append(current_block)

    return blocks


def merge_todo_lines(source_items: list[str], target_items: list[str], sync_completions: bool = False) -> list[str]:
    """
    Keep source items first, then preserve any target items already present.
    Tasks merge their children by parent context.
    
    Organizational bullets (e.g. - WORK) are treated as mergeable parents.
    
    If sync_completions is True: marks tasks [x] in result if they are [x] in source.
    """
    merged_blocks = []
    block_index_by_parent = {}
    
    # Map of clean task/bullet text -> status in source
    source_status = {}
    if sync_completions:
        for block in _split_todo_blocks(source_items):
            for line in block:
                m = TASK_RE.match(line)
                if m:
                    # Map text -> is_complete
                    text = m.group(3).strip().lower()
                    source_status[text] = (m.group(2).lower() == "x")

    for items in (source_items, target_items):
        for block in _split_todo_blocks(items):
            parent = block[0]
            # Normalize parent key: if it's a task, use group(3); if it's a bullet, use the text after '-'
            m = TASK_RE.match(parent)
            if m:
                parent_key = f"task:{m.group(3).strip().lower()}"
                # If sync_completions, ensure parent shows correct status if it's in source
                if sync_completions and m.group(3).strip().lower() in source_status:
                    if source_status[m.group(3).strip().lower()]:
                        parent = parent.replace("[ ]", "[x]")
            elif parent.strip().startswith("-"):
                parent_key = f"bullet:{parent.strip().lstrip('-').strip().lower()}"
            else:
                # Standalone text, just append if it hasn't been added exactly elsewhere
                if parent not in [b[0] for b in merged_blocks]:
                    merged_blocks.append(block.copy())
                continue

            if parent_key not in block_index_by_parent:
                block_index_by_parent[parent_key] = len(merged_blocks)
                merged_blocks.append(block.copy())
            else:
                # Merge children into existing block
                target_block = merged_blocks[block_index_by_parent[parent_key]]
                seen_children = set()
                # Clean up existing children state
                for i in range(len(target_block)):
                    line = target_block[i]
                    tm = TASK_RE.match(line)
                    if tm:
                        text = tm.group(3).strip().lower()
                        seen_children.add(text)
                        # Sync status of existing child if needed
                        if sync_completions and text in source_status:
                            if source_status[text]:
                                target_block[i] = line.replace("[ ]", "[x]")

                for child in block[1:]:
                    cm = TASK_RE.match(child)
                    if cm:
                        text = cm.group(3).strip().lower()
                        if text not in seen_children:
                            # Apply source status to new child if syncing
                            if sync_completions and text in source_status:
                                if source_status[text]:
                                    child = child.replace("[ ]", "[x]")
                            target_block.append(child)
                            seen_children.add(text)
                    else:
                        if child not in target_block:
                            target_block.append(child)

    merged = []
    for block in merged_blocks:
        merged.extend(block)
    return merged


def extract_active_section(content: str) -> list[str]:
    """
    Return the raw lines inside TO DO LIST.md's ## Active section.

    Stop at the next markdown header. Blank lines inside the section are kept so
    merge_todo_lines() can normalize them away safely.
    """
    lines = content.splitlines()
    in_active = False
    active_lines = []

    for line in lines:
        if line.strip() == "## Active":
            in_active = True
            continue

        if in_active:
            if line.startswith("## "):
                break
            active_lines.append(line)

    return active_lines


def patch_nav_links(content: str, target_date: date) -> str:
    """
    Fill in blank yesterday:/tomorrow: frontmatter fields.
    Handles notes created from the Obsidian template, which leaves these empty.
    Only patches lines that are genuinely blank (e.g. 'yesterday:' or 'yesterday: ').
    """
    yesterday = str(target_date - timedelta(days=1))
    tomorrow = str(target_date + timedelta(days=1))
    content = re.sub(r'^yesterday:\s*$', f'yesterday: {yesterday}', content, flags=re.MULTILINE)
    content = re.sub(r'^tomorrow:\s*$', f'tomorrow: {tomorrow}', content, flags=re.MULTILINE)
    return content


def ensure_daily_frontmatter(content: str, target_date: date) -> str:
    """
    Ensure a daily note has canonical frontmatter.
    Non-destructive: preserves existing keys while overwriting authoritative ones.
    """
    weekday = target_date.strftime("%A")
    month = target_date.strftime("%B")
    day_ord = _ordinal(target_date.day)
    year = target_date.year
    created = f"{weekday}, {month} {day_ord} {year}, 12:00:00 am"
    tag_date = target_date.strftime("%Y/%m/%d")
    cssclass = f"roygbiv-{_WEEKDAY_ABBREV[weekday].lower()}"

    canonical_updates = {
        "title": str(target_date),
        "linter-yaml-title-alias": str(target_date),
        "yesterday": str(target_date - timedelta(days=1)),
        "tomorrow": str(target_date + timedelta(days=1)),
        "date created": created,
        "date modified": created,
    }

    match = FRONTMATTER_RE.match(content)
    if not match:
        return f"{build_frontmatter(target_date)}\n\n{content.lstrip()}"

    lines = match.group("frontmatter").splitlines()
    new_lines = []
    handled_keys = set()
    
    # Authoritative keys we ALWAYS overwrite if present, or add if missing
    authoritative = list(canonical_updates.keys()) + ["aliases", "weekday", "cssclasses", "tags"]

    # Iterate through existing lines to preserve order and unknown keys
    i = 0
    while i < len(lines):
        line = lines[i]
        if ":" in line and not line.startswith(" "):
            key = line.split(":", 1)[0].strip()
            if key in canonical_updates:
                new_lines.append(f"{key}: {canonical_updates[key]}")
                handled_keys.add(key)
                i += 1
                continue
            
            # Special multi-line handling for specific known list keys
            if key in ["aliases", "weekday", "cssclasses", "tags"]:
                # Replace with canonical if it's one of ours
                if key == "aliases":
                    new_lines.append("aliases:")
                    for a in date_aliases(target_date):
                        new_lines.append(f"  - {a}")
                elif key == "weekday":
                    new_lines.append("weekday:")
                    new_lines.append(f"  - {weekday}")
                elif key == "cssclasses":
                    new_lines.append("cssclasses:")
                    new_lines.append(f"  - {cssclass}")
                elif key == "tags":
                    new_lines.append("tags:")
                    new_lines.append("  - today")
                    new_lines.append(f"  - {tag_date}")
                    new_lines.append("  - dailynote")
                
                handled_keys.add(key)
                # Skip existing list items
                i += 1
                while i < len(lines) and lines[i].startswith(" "):
                    i += 1
                continue
            
            # Unknown key: keep it
            new_lines.append(line)
            i += 1
            continue
        
        # Non-key line or continuation (shouldn't happen at root, but safety first)
        new_lines.append(line)
        i += 1

    # Add missing authoritative keys that weren't in the original
    for key in authoritative:
        if key not in handled_keys:
            if key in canonical_updates:
                new_lines.append(f"{key}: {canonical_updates[key]}")
            elif key == "aliases":
                new_lines.append("aliases:")
                for a in date_aliases(target_date):
                    new_lines.append(f"  - {a}")
            # ... (add others if needed, but build_frontmatter handles fresh notes)

    body = content[match.end():].lstrip("\r\n")
    return f"---\n" + "\n".join(new_lines) + "\n---\n\n" + body


# ---------------------------------------------------------------------------
# Write operations
# ---------------------------------------------------------------------------

def update_today_note(
    target_date: date,
    carried: list[str],
    dry_run: bool = False,
) -> None:
    today_file = VAULT_ROOT / f"{target_date}.md"
    block = todo_block_text(carried)

    if today_file.exists():
        content = today_file.read_text(encoding="utf-8")
        content = ensure_daily_frontmatter(content, target_date)
        content = patch_nav_links(content, target_date)
        lines = content.splitlines()
        if any(is_todo_marker(line) for line in lines):
            new_lines = []
            in_todo = False
            inserted = False
            existing_todo_lines = []

            for line in lines:
                if is_todo_marker(line) and not inserted:
                    in_todo = True
                    inserted = True
                    new_lines.append(line)
                    continue

                if in_todo:
                    m = TASK_RE.match(line)
                    if m or line.strip() == "" or line.strip() == PLACEHOLDER_LINE:
                        existing_todo_lines.append(line)
                        continue

                    merged = merge_todo_lines(carried, existing_todo_lines)
                    new_lines.append("")
                    new_lines.extend(merged if merged else [PLACEHOLDER_LINE])
                    in_todo = False
                    new_lines.append(line)
                    continue

                new_lines.append(line)

            if in_todo:
                merged = merge_todo_lines(carried, existing_todo_lines)
                new_lines.append("")
                new_lines.extend(merged if merged else [PLACEHOLDER_LINE])

            new_content = "\n".join(new_lines) + "\n"
        else:
            new_content = content.rstrip() + f"\n\n{TODO_MARKER}\n\n{block}\n"
    else:
        fm = build_frontmatter(target_date)
        new_content = f"{fm}\n\n{TODO_MARKER}\n\n{block}\n"

    if dry_run:
        log(f"\n--- {today_file.name} (dry run) ---")
        log(new_content.rstrip("\n"))
    else:
        today_file.write_text(new_content, encoding="utf-8")
        log(f"Updated {today_file.name}")


def update_todo_list_md(source_todo_lines: list[str], carried: list[str], dry_run: bool = False) -> None:
    """
    Sync source items (completed ones) back to TO DO LIST.md and then add the new
    completed items carried forward.
    """
    if TODO_LIST_FILE.exists():
        content = TODO_LIST_FILE.read_text(encoding="utf-8")
    else:
        content = (
            "---\n"
            "title: TO DO LIST\n"
            "aliases:\n"
            "  - TO DO LIST\n"
            "linter-yaml-title-alias: TO DO LIST\n"
            "---\n\n"
            "*Persistent list - incomplete items carry forward daily.*\n"
        )

    existing_active = extract_active_section(content)
    
    # First, sync completions from yesterday's full task list back to the active section
    # Then merge in the incomplete items carried forward
    merged_active = merge_todo_lines(source_todo_lines, existing_active, sync_completions=True)
    merged_active = merge_todo_lines(carried, merged_active)
    
    active_block = todo_block_text(merged_active)

    if "## Active" in content:
        lines = content.splitlines()
        new_lines = []
        in_active = False
        for line in lines:
            if line.strip() == "## Active" and not in_active:
                in_active = True
                new_lines.append(line)
                new_lines.append("")
                new_lines.extend(merged_active if merged_active else [PLACEHOLDER_LINE])
                new_lines.append("")
                continue
            if in_active:
                if line.startswith("## "):
                    in_active = False
                    new_lines.append(line)
                continue
            new_lines.append(line)
        new_content = "\n".join(new_lines).rstrip() + "\n"
    else:
        new_content = content.rstrip() + f"\n\n## Active\n\n{active_block}\n"

    if dry_run:
        log("\n--- TO DO LIST.md (dry run) ---")
        log(new_content.rstrip("\n"))
    else:
        TODO_LIST_FILE.write_text(new_content, encoding="utf-8")
        log("Updated TO DO LIST.md")


def load_active_todo_list_lines() -> list[str]:
    """Return the current persistent active backlog from TO DO LIST.md."""
    if not TODO_LIST_FILE.exists():
        return []
    return extract_active_section(TODO_LIST_FILE.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Future extension point: habit tracker
# ---------------------------------------------------------------------------

# def inject_habit_section(target_date: date, dry_run: bool = False) -> None:
#     """
#     Stage 2: inject a habit-tracking section into today's daily note.
#     Habits defined in a config (e.g. !/HABITS.md or .claude/habits.json).
#     Each habit renders as an unchecked box for the user to fill in Obsidian.
#     """
#     pass


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Daily to-do rollover for IDAHO-VAULT")
    parser.add_argument(
        "--date",
        help="Target date to roll INTO (YYYY-MM-DD). Defaults to today.",
        default=None,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print output without writing files.",
    )
    args = parser.parse_args()

    if args.date:
        target_date = date.fromisoformat(args.date)
    else:
        target_date = date.today()

    source_date = target_date - timedelta(days=1)
    source_file = VAULT_ROOT / f"{source_date}.md"

    log(f"Rolling over: {source_date} -> {target_date}")

    if not source_file.exists():
        log(f"No daily note found for {source_date} - nothing to carry forward.")
        sys.exit(0)

    source_content = source_file.read_text(encoding="utf-8")
    todo_lines = extract_todo_section(source_content)
    carried = carry_forward(todo_lines)
    persistent_active = load_active_todo_list_lines()
    merged_backlog = merge_todo_lines(carried, persistent_active)

    if merged_backlog:
        log(f"Carrying forward {len([l for l in merged_backlog if TASK_RE.match(l)])} incomplete item(s):")
        for line in merged_backlog:
            log(f"  {line}")
    else:
        log("No incomplete items found - nothing to carry forward.")

    update_today_note(target_date, merged_backlog, dry_run=args.dry_run)
    update_todo_list_md(todo_lines, merged_backlog, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
