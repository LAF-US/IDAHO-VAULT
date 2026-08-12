#!/usr/bin/env python3
"""
Normalize Markdown note tags across IDAHO-VAULT.

Rules:
- Parse tags only from YAML frontmatter.
- Treat frontmatter `tags:` as canonical.
- Normalize tags to lowercase slash-path strings.
- Preserve date/session/election tags as tags.
- Remove redundant standalone inline tag-only lines from note bodies.
- Surface ambiguous legacy tags in a review note instead of guessing.
"""

from __future__ import annotations

import argparse
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


VAULT_ROOT = Path(".")
REVIEW_NOTE = Path("!") / "!" / "tag-normalization-review-2026-03-24.md"

FRONTMATTER_RE = re.compile(
    r"\A---(?P<nl>\r?\n)(?P<frontmatter>.*?)(?P=nl)---(?P<after>\r?\n|$)",
    re.DOTALL,
)
INLINE_TAG_LINE_RE = re.compile(r"^\s*#([A-Za-z][A-Za-z0-9_-]*(?:/[A-Za-z0-9_-]+)+)\s*$")
TOP_LEVEL_TAGS_RE = re.compile(r"^tags:\s*(.*)$")
TAG_LIST_ITEM_RE = re.compile(r"^\s*-\s*(.+?)\s*$")

REVIEW_PREFIXES = ("category/",)
REVIEW_EXACT = {
    "admin/protocol",
    "archive",
    "budgets",
    "category",
    "characters",
    "dailynote",
    "goddess",
    "governments",
    "hero",
    "human",
    "idea",
    "letters",
    "magical",
    "mother",
    "numbers",
    "persona",
    "project",
    "quote",
    "sets",
    "today",
    "voice",
    "words",
}
REVIEW_REASON_BY_TAG = {
    "admin/protocol": "Administrative namespace appears one-off and needs taxonomy confirmation.",
    "archive": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "budgets": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "category": "Legacy category family retained pending taxonomy mapping.",
    "characters": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "dailynote": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "goddess": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "governments": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "hero": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "human": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "idea": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "letters": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "magical": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "mother": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "numbers": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "persona": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "project": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "quote": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "sets": "Single-segment legacy tag retained pending taxonomy confirmation.",
    "today": "Temporal tag retained as-is pending a separate decision on whether it belongs in taxonomy.",
    "voice": "Legacy creative taxonomy tag retained pending taxonomy confirmation.",
    "words": "Single-segment legacy tag retained pending taxonomy confirmation.",
}


@dataclass
class FileResult:
    path: Path
    changed: bool
    tags_before: int
    tags_after: int
    duplicates_removed: int
    had_frontmatter_duplicates: bool
    inline_lines_removed: int
    tags_promoted_from_body: int
    review_tags: set[str]
    raw_variants_by_normalized: dict[str, set[str]]


def read_text_preserve_newlines(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def write_text_preserve_newlines(path: Path, content: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(content)


def detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def parse_frontmatter(text: str) -> tuple[str, str, str, str] | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    frontmatter = match.group("frontmatter")
    newline = match.group("nl")
    after = match.group("after")
    body = text[match.end():]
    return frontmatter, body, newline, after


def parse_inline_list(raw: str) -> list[str]:
    raw = raw.strip()
    if not raw:
        return []
    parts = [part.strip() for part in raw.split(",")]
    return [strip_tag_wrapping(part) for part in parts if strip_tag_wrapping(part)]


def strip_tag_wrapping(raw: str) -> str:
    value = raw.strip().strip('"').strip("'").strip()
    if value.startswith("#"):
        value = value[1:].strip()
    return value


def normalize_tag(raw: str) -> str:
    value = strip_tag_wrapping(raw)
    return value.lower()


def parse_tags_block(frontmatter: str) -> tuple[list[str], int | None, int | None]:
    lines = frontmatter.splitlines()
    for index, line in enumerate(lines):
        match = TOP_LEVEL_TAGS_RE.match(line)
        if not match:
            continue

        remainder = match.group(1).strip()
        if remainder == "":
            tags: list[str] = []
            cursor = index + 1
            while cursor < len(lines):
                item_match = TAG_LIST_ITEM_RE.match(lines[cursor])
                if not item_match:
                    break
                tags.append(strip_tag_wrapping(item_match.group(1)))
                cursor += 1
            return tags, index, cursor

        if remainder == "[]":
            return [], index, index + 1

        if remainder.startswith("[") and remainder.endswith("]"):
            return parse_inline_list(remainder[1:-1]), index, index + 1

        return [strip_tag_wrapping(remainder)], index, index + 1

    return [], None, None


def format_tags_block(tags: list[str]) -> list[str]:
    if not tags:
        return ["tags: []"]
    return ["tags:"] + [f"  - {tag}" for tag in tags]


def rebuild_frontmatter(frontmatter: str, tags: list[str]) -> str:
    lines = frontmatter.splitlines()
    _, start, end = parse_tags_block(frontmatter)
    tag_lines = format_tags_block(tags)

    if start is None or end is None:
        if lines:
            return "\n".join(lines + tag_lines)
        return "\n".join(tag_lines)

    return "\n".join(lines[:start] + tag_lines + lines[end:])


def dedupe_preserve_order(tags: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for tag in tags:
        if not tag or tag in seen:
            continue
        seen.add(tag)
        ordered.append(tag)
    return ordered


def normalize_tags(tags: list[str]) -> list[str]:
    return [normalize_tag(tag) for tag in tags if normalize_tag(tag)]


def needs_review(tag: str) -> bool:
    if tag in REVIEW_EXACT:
        return True
    return any(tag.startswith(prefix) for prefix in REVIEW_PREFIXES)


def review_reason(tag: str) -> str:
    if tag in REVIEW_REASON_BY_TAG:
        return REVIEW_REASON_BY_TAG[tag]
    if any(tag.startswith(prefix) for prefix in REVIEW_PREFIXES):
        return "Legacy category-family tag retained pending taxonomy mapping."
    return "Legacy tag retained pending taxonomy confirmation."


def remove_standalone_tag_lines(body: str) -> tuple[str, list[str], int]:
    lines = body.splitlines(keepends=True)
    kept: list[str] = []
    promoted: list[str] = []
    removed = 0

    for line in lines:
        stripped = line.strip()
        match = INLINE_TAG_LINE_RE.fullmatch(stripped)
        if match:
            promoted.append(match.group(1))
            removed += 1
            continue
        kept.append(line)

    return "".join(kept), promoted, removed


def reconstruct_file(
    frontmatter: str | None,
    body: str,
    newline: str,
    closing_after: str,
    tags: list[str],
) -> str:
    if frontmatter is None:
        tags_block = newline.join(format_tags_block(tags))
        return f"---{newline}{tags_block}{newline}---{newline}{body}"

    rebuilt_frontmatter = rebuild_frontmatter(frontmatter, tags).replace("\n", newline)
    return f"---{newline}{rebuilt_frontmatter}{newline}---{closing_after}{body}"


def process_file(path: Path) -> FileResult:
    original = read_text_preserve_newlines(path)
    parsed = parse_frontmatter(original)

    if parsed is None:
        frontmatter = None
        body = original
        newline = detect_newline(original)
        closing_after = newline
        frontmatter_tags: list[str] = []
    else:
        frontmatter, body, newline, closing_after = parsed
        frontmatter_tags, _, _ = parse_tags_block(frontmatter)

    cleaned_body, inline_tags, inline_lines_removed = remove_standalone_tag_lines(body)
    raw_tags = frontmatter_tags + inline_tags
    normalized_frontmatter_tags = normalize_tags(frontmatter_tags)
    normalized_raw_tags = normalize_tags(raw_tags)
    deduped_tags = dedupe_preserve_order(normalized_raw_tags)

    had_frontmatter_duplicates = len(normalized_frontmatter_tags) != len(
        dedupe_preserve_order(normalized_frontmatter_tags)
    )
    duplicates_removed = len(normalized_raw_tags) - len(deduped_tags)
    tags_promoted_from_body = len(dedupe_preserve_order(normalize_tags(inline_tags)))

    rebuilt = original
    if deduped_tags or inline_lines_removed:
        rebuilt = reconstruct_file(frontmatter, cleaned_body, newline, closing_after, deduped_tags)

    changed = rebuilt != original
    raw_variants_by_normalized: dict[str, set[str]] = defaultdict(set)
    for raw_tag in raw_tags:
        normalized = normalize_tag(raw_tag)
        if normalized:
            raw_variants_by_normalized[normalized].add(strip_tag_wrapping(raw_tag))

    review_tags = {tag for tag in deduped_tags if needs_review(tag)}
    return FileResult(
        path=path,
        changed=changed,
        tags_before=len(frontmatter_tags),
        tags_after=len(deduped_tags),
        duplicates_removed=duplicates_removed,
        had_frontmatter_duplicates=had_frontmatter_duplicates,
        inline_lines_removed=inline_lines_removed,
        tags_promoted_from_body=tags_promoted_from_body,
        review_tags=review_tags,
        raw_variants_by_normalized=dict(raw_variants_by_normalized),
    ), rebuilt


def iter_markdown_files(root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        if path == root / REVIEW_NOTE:
            continue
        paths.append(path)
    return sorted(paths)


def build_review_note(
    review_data: dict[str, dict[str, object]],
    total_files_changed: int,
    duplicate_note_count: int,
    inline_line_count: int,
) -> str:
    lines = [
        "---",
        "tags:",
        "  - administration/handoff",
        "  - administration/levelset",
        "---",
        "# Tag Normalization Review - 2026-03-24",
        "",
        "Generated by `.github/scripts/normalize_tags.py` during the vault-wide tag normalization pass.",
        "",
        f"- Files changed: {total_files_changed}",
        f"- Notes with duplicate frontmatter tags before normalization: {duplicate_note_count}",
        f"- Standalone inline tag-only lines removed: {inline_line_count}",
        "",
        "## Legacy Tags Requiring Taxonomy Decisions",
        "",
        "| Original tag variants | Normalized tag kept in notes | Note count | Why unresolved |",
        "| --- | --- | ---: | --- |",
    ]

    for normalized_tag in sorted(review_data):
        info = review_data[normalized_tag]
        variants = " <br> ".join(sorted(info["variants"]))
        lines.append(
            f"| {variants} | `{normalized_tag}` | {info['note_count']} | {info['reason']} |"
        )

    if not review_data:
        lines.append("| None | None | 0 | No unresolved legacy tags were detected. |")

    lines.extend(
        [
            "",
            "## Follow-up Guidance",
            "",
            "- Confirm whether the retained legacy tags should map into an existing lowercase taxonomy or remain as dedicated families.",
            "- Re-run the normalization script after any manual taxonomy decisions so the review note stays aligned with the vault state.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize Markdown note tags in IDAHO-VAULT.")
    parser.add_argument("--write", action="store_true", help="Write changes to disk.")
    parser.add_argument(
        "--root",
        type=Path,
        default=VAULT_ROOT,
        help="Vault root to process.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    paths = iter_markdown_files(root)

    total_files_changed = 0
    total_inline_lines_removed = 0
    total_duplicates_removed = 0
    total_tags_promoted = 0
    duplicate_note_count = 0
    review_data: dict[str, dict[str, object]] = {}
    rewritten_files: list[tuple[Path, str]] = []

    for path in paths:
        result, rebuilt = process_file(path)
        if result.had_frontmatter_duplicates:
            duplicate_note_count += 1
        total_inline_lines_removed += result.inline_lines_removed
        total_duplicates_removed += result.duplicates_removed
        total_tags_promoted += result.tags_promoted_from_body

        if result.changed:
            total_files_changed += 1
            rewritten_files.append((path, rebuilt))

        for tag in result.review_tags:
            info = review_data.setdefault(
                tag,
                {
                    "variants": set(),
                    "notes": set(),
                    "reason": review_reason(tag),
                },
            )
            info["variants"].update(result.raw_variants_by_normalized.get(tag, {tag}))
            info["notes"].add(str(path.relative_to(root)).replace("\\", "/"))

    review_payload: dict[str, dict[str, object]] = {}
    for tag, info in review_data.items():
        review_payload[tag] = {
            "variants": info["variants"],
            "note_count": len(info["notes"]),
            "reason": info["reason"],
        }

    review_note_content = build_review_note(
        review_payload,
        total_files_changed,
        duplicate_note_count,
        total_inline_lines_removed,
    )
    review_note_path = root / REVIEW_NOTE
    review_note_path.parent.mkdir(parents=True, exist_ok=True)

    if args.write:
        for path, rebuilt in rewritten_files:
            write_text_preserve_newlines(path, rebuilt)
        write_text_preserve_newlines(review_note_path, review_note_content)

    print(f"files_scanned={len(paths)}")
    print(f"files_changed={total_files_changed}")
    print(f"duplicate_note_count={duplicate_note_count}")
    print(f"duplicates_removed={total_duplicates_removed}")
    print(f"inline_tag_lines_removed={total_inline_lines_removed}")
    print(f"inline_tags_promoted={total_tags_promoted}")
    print(f"review_tags={len(review_payload)}")
    print(f"review_note={REVIEW_NOTE.as_posix()}")
    if not args.write:
        print("mode=dry-run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
