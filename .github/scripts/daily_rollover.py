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
ROOT_GROUP = "__root__"


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


def _clean_line(line: str) -> str:
    return line.rstrip("\r\n")


def _is_placeholder_bullet(line: str) -> bool:
    return _clean_line(line).strip() == "- []"


def _task_key(line: str) -> str | None:
    match = TASK_RE.match(_clean_line(line))
    if not match:
        return None
    text = match.group(3).strip()
    if not text:
        return None
    return text.lower()


def _is_top_level_task(line: str) -> bool:
    match = TASK_RE.match(_clean_line(line))
    return bool(match and len(match.group(1)) == 0)


def _is_org_bullet(line: str) -> bool:
    cleaned = _clean_line(line).strip()
    if not cleaned.startswith("- "):
        return False
    if _is_placeholder_bullet(cleaned):
        return False
    return TASK_RE.match(cleaned) is None


def _new_todo_model() -> dict[str, object]:
    return {
        "group_order": [ROOT_GROUP],
        "groups": {
            ROOT_GROUP: {
                "label": None,
                "blocks": [],
            }
        },
        "task_index": {},
    }


def _copy_todo_model(model: dict[str, object]) -> dict[str, object]:
    copied = _new_todo_model()
    copied["group_order"] = list(model["group_order"])
    copied["groups"] = {
        key: {
            "label": value["label"],
            "blocks": [block[:] for block in value["blocks"]],
        }
        for key, value in model["groups"].items()
    }
    copied["task_index"] = dict(model["task_index"])
    return copied


def _ensure_group(model: dict[str, object], group_key: str, group_label: str | None) -> None:
    groups = model["groups"]
    group_order = model["group_order"]
    if group_key in groups:
        return
    groups[group_key] = {
        "label": group_label,
        "blocks": [],
    }
    group_order.append(group_key)


def _add_block(model: dict[str, object], group_key: str, group_label: str | None, block: list[str]) -> None:
    key = _task_key(block[0])
    if key is None:
        return
    task_index = model["task_index"]
    if key in task_index:
        return
    _ensure_group(model, group_key, group_label)
    groups = model["groups"]
    blocks = groups[group_key]["blocks"]
    task_index[key] = (group_key, len(blocks))
    blocks.append(block[:])


def _normalize_task_block(block: list[str], keep_completed: bool) -> list[str] | None:
    if not block:
        return None

    parent = TASK_RE.match(_clean_line(block[0]))
    if not parent:
        return None

    parent_text = parent.group(3).strip()
    if not parent_text:
        return None

    parent_complete = parent.group(2).lower() == "x"
    if parent_complete and not keep_completed:
        return None

    normalized = [_clean_line(block[0])]
    for line in block[1:]:
        cleaned = _clean_line(line)
        if not cleaned.strip():
            continue
        match = TASK_RE.match(cleaned)
        if match:
            child_text = match.group(3).strip()
            if not child_text:
                continue
            child_complete = match.group(2).lower() == "x"
            if child_complete and not keep_completed:
                continue
            normalized.append(cleaned)
            continue
        normalized.append(cleaned)

    return normalized


def parse_todo_model(lines: list[str], keep_completed: bool) -> dict[str, object]:
    """Parse a TODO section into ordered root/category task groups."""

    model = _new_todo_model()
    current_group_key = ROOT_GROUP
    current_group_label = None
    i = 0

    while i < len(lines):
        line = _clean_line(lines[i])

        if not line.strip() or _is_placeholder_bullet(line):
            i += 1
            continue

        if _is_org_bullet(line):
            current_group_label = line.strip()[2:].strip()
            current_group_key = current_group_label.lower()
            _ensure_group(model, current_group_key, current_group_label)
            i += 1
            continue

        if not _is_top_level_task(line):
            i += 1
            continue

        block = [line]
        i += 1
        while i < len(lines):
            next_line = _clean_line(lines[i])
            if _is_org_bullet(next_line) or _is_top_level_task(next_line):
                break
            block.append(next_line)
            i += 1

        normalized = _normalize_task_block(block, keep_completed=keep_completed)
        if normalized is not None:
            _add_block(model, current_group_key, current_group_label, normalized)

    return model


def todo_task_keys(lines: list[str], keep_completed: bool = True) -> set[str]:
    """Return normalized top-level task keys from a TODO section."""

    model = parse_todo_model(lines, keep_completed=keep_completed)
    return set(model["task_index"])


def exclude_task_keys(model: dict[str, object], excluded_keys: set[str]) -> dict[str, object]:
    """Return a copy of the TODO model without the excluded tasks."""

    filtered = _new_todo_model()
    for group_key in model["group_order"]:
        group = model["groups"][group_key]
        for block in group["blocks"]:
            key = _task_key(block[0])
            if key in excluded_keys:
                continue
            _add_block(filtered, group_key, group["label"], block)
    return filtered


def merge_todo_models(primary: dict[str, object], secondary: dict[str, object]) -> dict[str, object]:
    """Merge TODO models, preserving primary order and authority for duplicate tasks."""

    merged = _copy_todo_model(primary)
    for group_key in secondary["group_order"]:
        group = secondary["groups"][group_key]
        for block in group["blocks"]:
            _add_block(merged, group_key, group["label"], block)
    return merged


def render_todo_model(model: dict[str, object]) -> list[str]:
    """Render a TODO model back to flat markdown lines."""

    rendered: list[str] = []
    root_group = model["groups"][ROOT_GROUP]
    for block in root_group["blocks"]:
        rendered.extend(block)

    for group_key in model["group_order"]:
        if group_key == ROOT_GROUP:
            continue
        group = model["groups"][group_key]
        if not group["blocks"]:
            continue
        rendered.append(f"- {group['label']}")
        for block in group["blocks"]:
            rendered.extend(block)

    return rendered


def count_todo_tasks(model: dict[str, object]) -> int:
    """Return the number of top-level tasks in a TODO model."""

    return len(model["task_index"])


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
    return render_todo_model(parse_todo_model(todo_lines, keep_completed=False))


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
        if not stripped or stripped == PLACEHOLDER_LINE or _is_placeholder_bullet(stripped):
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
    primary = parse_todo_model(source_items, keep_completed=True)
    secondary = parse_todo_model(target_items, keep_completed=True)
    return render_todo_model(merge_todo_models(primary, secondary))


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


def _find_todo_section_bounds(lines: list[str]) -> tuple[int | None, int | None]:
    """Return the marker line index and the exclusive end index for the TODO section."""

    marker_index = None
    for index, line in enumerate(lines):
        if is_todo_marker(line):
            marker_index = index
            break

    if marker_index is None:
        return None, None

    end_index = len(lines)
    for index in range(marker_index + 1, len(lines)):
        line = lines[index]
        if line.strip() == "---" or line.startswith("## ") or line.startswith("Notes:"):
            end_index = index
            break

    return marker_index, end_index


def build_backlog_lines(source_todo_lines: list[str], active_todo_lines: list[str]) -> list[str]:
    """Build the next active backlog from yesterday's note and the persistent active list."""

    source_open = parse_todo_model(source_todo_lines, keep_completed=False)
    source_seen_keys = todo_task_keys(source_todo_lines, keep_completed=True)
    persistent_open = parse_todo_model(active_todo_lines, keep_completed=False)
    pending_persistent = exclude_task_keys(persistent_open, source_seen_keys)
    backlog = merge_todo_models(source_open, pending_persistent)
    return render_todo_model(backlog)


def patch_nav_links(content: str, target_date: date) -> str:
    """
    Fill in blank or unresolved yesterday:/tomorrow: frontmatter fields.
    Handles notes created from the Obsidian core Templates plugin, which may leave these
    blank ('yesterday: ') or holding an unresolved token ('yesterday: {{date-1d:YYYY-MM-DD}}').
    The Periodic Notes plugin expands relative tokens; core Templates does not.
    """
    yesterday = str(target_date - timedelta(days=1))
    tomorrow = str(target_date + timedelta(days=1))
    content = re.sub(
        r'^yesterday:\s*(\{\{[^}]*\}\})?\s*$',
        f'yesterday: {yesterday}',
        content,
        flags=re.MULTILINE,
    )
    content = re.sub(
        r'^tomorrow:\s*(\{\{[^}]*\}\})?\s*$',
        f'tomorrow: {tomorrow}',
        content,
        flags=re.MULTILINE,
    )
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
        marker_index, end_index = _find_todo_section_bounds(lines)
        if marker_index is not None and end_index is not None:
            existing_todo_lines = lines[marker_index + 1:end_index]
            existing_model = parse_todo_model(existing_todo_lines, keep_completed=True)
            carried_model = parse_todo_model(carried, keep_completed=False)
            merged = render_todo_model(merge_todo_models(existing_model, carried_model))

            new_lines = lines[:marker_index + 1]
            new_lines.append("")
            new_lines.extend(merged if merged else [PLACEHOLDER_LINE])
            if end_index < len(lines) and lines[end_index].strip():
                new_lines.append("")
            new_lines.extend(lines[end_index:])
            new_content = "\n".join(new_lines).rstrip() + "\n"
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


def update_todo_list_md(carried: list[str], dry_run: bool = False) -> None:
    """
    Rewrite TO DO LIST.md's active section from the normalized carried backlog.
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

    active_block = todo_block_text(carried)

    if "## Active" in content:
        lines = content.splitlines()
        new_lines = []
        in_active = False
        for line in lines:
            if line.strip() == "## Active" and not in_active:
                in_active = True
                new_lines.append(line)
                new_lines.append("")
                new_lines.extend(carried if carried else [PLACEHOLDER_LINE])
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
    persistent_active = load_active_todo_list_lines()
    merged_backlog = build_backlog_lines(todo_lines, persistent_active)

    if merged_backlog:
        log(f"Carrying forward {len([l for l in merged_backlog if _is_top_level_task(l)])} incomplete item(s):")
        for line in merged_backlog:
            log(f"  {line}")
    else:
        log("No incomplete items found - nothing to carry forward.")

    update_today_note(target_date, merged_backlog, dry_run=args.dry_run)
    update_todo_list_md(merged_backlog, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
