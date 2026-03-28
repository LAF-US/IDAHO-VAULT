#!/usr/bin/env python3
"""
daily_rollover.py — IDAHO-VAULT

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
TASK_RE = re.compile(r'^(\t*)- \[( |x|X)\] (.+)$')


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def extract_todo_section(content: str) -> list[str]:
    """
    Return lines between the [[TO DO LIST]] marker and the next --- separator
    (or end of file). The marker line itself is excluded.
    """
    lines = content.splitlines()
    in_todo = False
    todo_lines = []
    for line in lines:
        if "[[TO DO LIST]]" in line:
            in_todo = True
            continue
        if in_todo:
            if line.strip() == "---":
                break
            todo_lines.append(line)
    return todo_lines


def carry_forward(todo_lines: list[str]) -> list[str]:
    """
    Given raw task lines from a daily note's TODO section, return only the
    incomplete items — with only their incomplete sub-items.

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

        indent_level = len(m.group(1))  # number of leading tabs
        done = m.group(2).lower() == "x"

        # Only handle top-level items in this loop; sub-items collected below.
        if indent_level > 0:
            i += 1
            continue

        # Collect this top-level item's block (itself + all indented children).
        block = [line]
        j = i + 1
        while j < len(todo_lines):
            next_line = todo_lines[j]
            next_m = TASK_RE.match(next_line)
            # Stop at the next top-level task
            if next_m and len(next_m.group(1)) == 0:
                break
            block.append(next_line)
            j += 1

        if not done:
            # Keep parent
            result.append(block[0].rstrip())
            # Keep only incomplete sub-items
            for sub_line in block[1:]:
                sub_m = TASK_RE.match(sub_line)
                if sub_m and sub_m.group(2).lower() != "x":
                    result.append(sub_line.rstrip())
                # Done sub-items and blank lines within block: silently dropped

        i = j

    return result


# ---------------------------------------------------------------------------
# Daily note helpers
# ---------------------------------------------------------------------------

def _ordinal(n: int) -> str:
    if 11 <= (n % 100) <= 13:
        return f"{n}th"
    return f"{n}{['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]}"


def date_aliases(target_date: date) -> list[str]:
    """Return the canonical set of date aliases for a daily note."""
    weekday = target_date.strftime("%A")
    month = target_date.strftime("%B")
    day = target_date.day
    day_ord = _ordinal(day)
    year = target_date.year
    return [
        str(target_date),                           # 2026-03-28
        f"{month} {day}, {year}",                   # March 28, 2026
        f"{month} {day_ord}, {year}",               # March 28th, 2026
        f"{day} {month} {year}",                    # 28 March 2026
        f"{weekday}, {month} {day}, {year}",        # Saturday, March 28, 2026
    ]


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
        f"tags:\n"
        f"  - today\n"
        f"  - {tag_date}\n"
        f"  - dailynote\n"
        f"date created: {created}\n"
        f"date modified: {created}\n"
        f"---"
    )


def todo_block_text(carried: list[str]) -> str:
    if carried:
        return "\n".join(carried)
    return "*(no incomplete items carried forward)*"


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
        content = patch_nav_links(today_file.read_text(), target_date)
        if "[[TO DO LIST]]" in content:
            # Replace the existing TODO section's tasks
            lines = content.splitlines()
            new_lines = []
            in_todo = False
            inserted = False
            for line in lines:
                if "[[TO DO LIST]]" in line and not inserted:
                    in_todo = True
                    inserted = True
                    new_lines.append(line)
                    new_lines.append("")
                    new_lines.extend(carried)
                    continue
                if in_todo:
                    m = TASK_RE.match(line)
                    # Stop skipping at --- separator or non-task, non-blank line
                    if line.strip() == "---":
                        in_todo = False
                        new_lines.append(line)
                    elif m or line.strip() == "":
                        pass  # skip old task lines and blanks in the section
                    else:
                        in_todo = False
                        new_lines.append(line)
                    continue
                new_lines.append(line)
            new_content = "\n".join(new_lines) + "\n"
        else:
            # Append TODO section
            new_content = content.rstrip() + f"\n\n[[TO DO LIST]]\n\n{block}\n"
    else:
        # Create fresh daily note
        fm = build_frontmatter(target_date)
        new_content = f"{fm}\n\n[[TO DO LIST]]\n\n{block}\n"

    if dry_run:
        print(f"\n--- {today_file.name} (dry run) ---")
        print(new_content)
    else:
        today_file.write_text(new_content)
        print(f"Updated {today_file.name}")


def update_todo_list_md(carried: list[str], dry_run: bool = False) -> None:
    block = todo_block_text(carried)

    if TODO_LIST_FILE.exists():
        content = TODO_LIST_FILE.read_text()
    else:
        content = (
            "---\n"
            "title: TO DO LIST\n"
            "aliases:\n"
            "  - TO DO LIST\n"
            "linter-yaml-title-alias: TO DO LIST\n"
            "---\n\n"
            "*Persistent list — incomplete items carry forward daily.*\n"
        )

    if "## Active" in content:
        lines = content.splitlines()
        new_lines = []
        in_active = False
        for line in lines:
            if line.strip() == "## Active" and not in_active:
                in_active = True
                new_lines.append(line)
                new_lines.append("")
                new_lines.extend(carried)
                new_lines.append("")
                continue
            if in_active:
                if line.startswith("## "):
                    in_active = False
                    new_lines.append(line)
                # else: skip old active items
                continue
            new_lines.append(line)
        new_content = "\n".join(new_lines).rstrip() + "\n"
    else:
        new_content = content.rstrip() + f"\n\n## Active\n\n{block}\n"

    if dry_run:
        print(f"\n--- TO DO LIST.md (dry run) ---")
        print(new_content)
    else:
        TODO_LIST_FILE.write_text(new_content)
        print("Updated TO DO LIST.md")


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

    print(f"Rolling over: {source_date} → {target_date}")

    if not source_file.exists():
        print(f"No daily note found for {source_date} — nothing to carry forward.")
        sys.exit(0)

    source_content = source_file.read_text()
    todo_lines = extract_todo_section(source_content)
    carried = carry_forward(todo_lines)

    if carried:
        print(f"Carrying forward {len([l for l in carried if TASK_RE.match(l)])} incomplete item(s):")
        for line in carried:
            print(f"  {line}")
    else:
        print("No incomplete items found — nothing to carry forward.")

    update_today_note(target_date, carried, dry_run=args.dry_run)
    update_todo_list_md(carried, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
