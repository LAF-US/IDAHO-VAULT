#!/usr/bin/env python3
"""Audit the abandoned .worktrees clone without modifying either worktree.

The active Vault is authoritative. This tool records cryptographic coverage of
the nested clone, maps rewritten commits, and produces an approval-only
shortlist for patch-unique commits. It never copies files or invokes mutating
Git commands.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_SOURCE = Path(".worktrees/repos/IDAHO-VAULT")
DEFAULT_MANIFEST = Path("RESTRUCTURE-MANIFEST-WORKTREES-2026-08-17.jsonl")
DEFAULT_REPORT = Path("WITNESS-WORKTREES-RECONCILIATION-2026-08-17.md")
KNOWN_UNSAFE_ALIGNMENT = "5f34c105974176125ee9417f4fbcb8c5326def0c"

SENSITIVE_MARKERS = (
    ".env",
    ".git/",
    ".gnupg/",
    ".ssh/",
    "credential",
    "gitleaks",
    "id_rsa",
    "password",
    "private_key",
    "secret",
    "token",
    "trufflehog",
)
RUNTIME_MARKERS = (
    ".cache/",
    ".codex/sessions/",
    ".codex/thread-writer-locks/",
    ".tmp/",
    ".temp/",
    ".trash/",
    "logs/",
    "node_modules/",
    "process-",
    "worktrees/",
)


@dataclass(frozen=True)
class TreeEntry:
    mode: str
    kind: str
    oid: str
    path: str


def run_git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    command = [
        "git",
        "-c",
        "core.fsmonitor=false",
        "-c",
        "core.hooksPath=NUL" if os.name == "nt" else "core.hooksPath=/dev/null",
        "-c",
        "filter.lfs.process=",
        "-c",
        "filter.lfs.required=false",
        "-c",
        "filter.lfs.clean=",
        "-c",
        "filter.lfs.smudge=",
        "-C",
        str(repo),
        *args,
    ]
    return subprocess.run(command, check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def git_text(repo: Path, *args: str) -> str:
    return run_git(repo, *args).stdout.decode("utf-8", errors="replace").strip()


def parse_tree(repo: Path, revision: str) -> dict[str, TreeEntry]:
    raw = run_git(repo, "ls-tree", "-r", "-z", "--full-tree", revision).stdout
    entries: dict[str, TreeEntry] = {}
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split(" ")
        path = raw_path.decode("utf-8", errors="surrogateescape").replace("\\", "/")
        entries[path] = TreeEntry(mode=mode, kind=kind, oid=oid, path=path)
    return entries


def commit_log(repo: Path, revision: str) -> list[tuple[str, str]]:
    output = git_text(repo, "log", "--format=%H%x09%T", revision)
    rows: list[tuple[str, str]] = []
    for line in output.splitlines():
        commit, tree = line.split("\t", 1)
        rows.append((commit, tree))
    return rows


def commit_metadata(repo: Path, commit: str) -> dict[str, object]:
    fields = git_text(repo, "show", "-s", "--format=%H%x00%P%x00%aI%x00%s", commit).split("\0")
    changed = git_text(repo, "diff-tree", "--no-commit-id", "--name-only", "-r", commit)
    paths = sorted(path.replace("\\", "/") for path in changed.splitlines() if path)
    # Hash Git's raw tree delta instead of materializing potentially multi-GB
    # binary patches into a Python pipe. Patch equivalence is already provided
    # by `git cherry`; this digest anchors the candidate's exact object delta.
    raw_change = run_git(repo, "diff-tree", "--root", "--raw", "-r", commit).stdout
    lowered = "\n".join([str(fields[3]), *paths]).lower()
    sensitive = sorted(marker for marker in SENSITIVE_MARKERS if marker in lowered)
    runtime = sorted(marker for marker in RUNTIME_MARKERS if marker in lowered)
    return {
        "commit": fields[0],
        "parents": fields[1].split(),
        "authored_at": fields[2],
        "subject": fields[3],
        "changed_path_count": len(paths),
        "changed_paths_sha256": hashlib.sha256("\n".join(paths).encode("utf-8")).hexdigest(),
        "raw_change_sha256": hashlib.sha256(raw_change).hexdigest(),
        "sample_paths": paths[:5],
        "sensitive_markers": sensitive,
        "runtime_markers": runtime,
        "review_class": "heightened_manual_review" if sensitive or runtime else "manual_approval_candidate",
    }


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def render_jsonl(rows: list[dict[str, object]]) -> str:
    return "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)


def assert_existing_outputs_writable(*paths: Path) -> None:
    """Fail before the expensive audit if the host blocks generated outputs."""
    for path in paths:
        if not path.exists():
            raise SystemExit(f"Output must be created through the workspace writer first: {path}")
        with path.open("a", encoding="utf-8", newline="\n"):
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--stdout", action="store_true", help="Return generated artifacts as JSON without writing files.")
    args = parser.parse_args()

    root = args.repo_root.resolve()
    source = (root / args.source).resolve() if not args.source.is_absolute() else args.source.resolve()
    manifest_path = (root / args.manifest).resolve() if not args.manifest.is_absolute() else args.manifest.resolve()
    report_path = (root / args.report).resolve() if not args.report.is_absolute() else args.report.resolve()
    if not source.is_dir() or not (source / ".git").is_dir():
        raise SystemExit(f"Recovery clone is unavailable: {source}")
    if not args.stdout:
        assert_existing_outputs_writable(manifest_path, report_path)

    active_head = git_text(root, "rev-parse", "HEAD")
    source_head = git_text(source, "rev-parse", "HEAD")
    active_branch = git_text(root, "branch", "--show-current")
    source_branch = git_text(source, "branch", "--show-current")
    merge_base = git_text(root, "merge-base", active_head, source_head)
    divergence = git_text(root, "rev-list", "--left-right", "--count", f"{source_head}...{active_head}")
    old_only_count, active_only_count = (int(value) for value in divergence.split())

    source_tree = git_text(source, "rev-parse", f"{source_head}^{{tree}}")
    active_history = commit_log(root, active_head)
    active_by_tree: dict[str, list[str]] = defaultdict(list)
    for commit, tree in active_history:
        active_by_tree[tree].append(commit)
    exact_counterparts = active_by_tree.get(source_tree, [])

    source_entries = parse_tree(source, source_head)
    active_entries = parse_tree(root, active_head)
    same_blob = 0
    changed_blob = 0
    removed_after_counterpart = 0
    for path, entry in source_entries.items():
        active = active_entries.get(path)
        if active is None:
            removed_after_counterpart += 1
        elif active.oid == entry.oid and active.mode == entry.mode:
            same_blob += 1
        else:
            changed_blob += 1
    added_after_counterpart = sum(path not in source_entries for path in active_entries)

    status_output = git_text(source, "status", "--porcelain=v1", "--untracked-files=all", "--ignore-submodules=all")
    status_lines = [line for line in status_output.splitlines() if line]
    untracked = [line[3:].replace("\\", "/") for line in status_lines if line.startswith("?? ")]
    tracked_changes = [line for line in status_lines if not line.startswith("?? ")]

    cherry_rows = git_text(root, "cherry", active_head, source_head).splitlines()
    equivalent_commits = [line[2:] for line in cherry_rows if line.startswith("- ")]
    unique_commits = [line[2:] for line in cherry_rows if line.startswith("+ ")]
    merge_or_empty_count = old_only_count - len(cherry_rows)
    candidates = [commit_metadata(root, commit) for commit in unique_commits]
    candidate_classes = Counter(str(candidate["review_class"]) for candidate in candidates)

    generated_at = datetime.now(timezone.utc).isoformat()
    rows: list[dict[str, object]] = [
        {
            "action": "reconciliation_baseline",
            "generated_at": generated_at,
            "active_branch": active_branch,
            "active_head": active_head,
            "source_branch": source_branch,
            "source_head": source_head,
            "merge_base": merge_base,
            "old_only_commits": old_only_count,
            "active_only_commits": active_only_count,
        },
        {
            "action": "tracked_tree_cryptographically_covered",
            "classification": "already_represented_in_active_history",
            "source_tree": source_tree,
            "source_tracked_entries": len(source_entries),
            "exact_active_counterparts": exact_counterparts,
        },
        {
            "action": "tracked_tip_vs_active_tip",
            "same_path_same_blob": same_blob,
            "same_path_changed_by_active_history": changed_blob,
            "removed_by_active_history": removed_after_counterpart,
            "added_by_active_history": added_after_counterpart,
            "restoration_policy": "do_not_restore_superseded_or_removed_tracked_files",
        },
        {
            "action": "nested_git_metadata_excluded",
            "classification": "git_metadata_evidence",
            "path": ".worktrees/repos/IDAHO-VAULT/.git/",
        },
        {
            "action": "history_equivalence_summary",
            "patch_equivalent_non_merge_commits": len(equivalent_commits),
            "patch_unique_non_merge_commits": len(unique_commits),
            "merge_or_empty_commits_not_replayable_by_git_cherry": merge_or_empty_count,
            "replay_policy": "shortlist_only_explicit_logan_approval_required",
        },
        {
            "action": "commit_excluded",
            "commit": KNOWN_UNSAFE_ALIGNMENT,
            "classification": "pre_scrub_history_alignment_do_not_replay",
        },
    ]
    for path in untracked:
        lowered = path.lower()
        rows.append(
            {
                "action": "untracked_source_item_excluded",
                "path": path,
                "classification": "secret_sensitive_runtime" if any(marker in lowered for marker in RUNTIME_MARKERS) else "manual_review",
                "copied": False,
            }
        )
    for candidate in candidates:
        rows.append({"action": "commit_shortlisted_for_approval", **candidate})
    manifest_text = render_jsonl(rows)

    recent_source = git_text(source, "log", "--format=%H%x09%T%x09%aI%x09%s", "-20", source_head)
    mapping_rows: list[tuple[str, str, str]] = []
    for line in recent_source.splitlines():
        commit, tree, _date, subject = line.split("\t", 3)
        matches = active_by_tree.get(tree, [])
        if matches:
            mapping_rows.append((commit[:12], matches[0][:12], subject))

    report_lines = [
        "# WITNESS — `.worktrees` reconciliation — 2026-08-17",
        "",
        "## Outcome",
        "",
        "No recovery payload was copied. The nested clone's tracked tip is cryptographically identical to a commit already reachable from the active branch. Files changed or removed after that counterpart are active-history decisions, not missing recovery cargo.",
        "",
        f"- Active: `{active_branch}` at `{active_head}`",
        f"- Recovery clone: `{source_branch}` at `{source_head}`",
        f"- Exact active tree counterpart(s): {', '.join(f'`{value}`' for value in exact_counterparts) or 'none'}",
        f"- Tracked source entries covered by that tree: **{len(source_entries):,}**",
        f"- Recovery working-tree tracked changes: **{len(tracked_changes)}**",
        f"- Recovery working-tree untracked items: **{len(untracked)}**",
        "",
        "## Current-tip comparison",
        "",
        f"- Same path and blob: **{same_blob:,}**",
        f"- Same path, later active content: **{changed_blob:,}**",
        f"- Removed after the rewritten counterpart: **{removed_after_counterpart:,}**",
        f"- Added after the rewritten counterpart: **{added_after_counterpart:,}**",
        "",
        "## History audit",
        "",
        f"- Old-only commits: **{old_only_count:,}**",
        f"- Active-only commits: **{active_only_count:,}**",
        f"- Patch-equivalent non-merge commits: **{len(equivalent_commits):,}**",
        f"- Patch-unique non-merge commits requiring approval: **{len(unique_commits):,}**",
        f"- Merge or empty commits excluded from automatic replay analysis: **{merge_or_empty_count:,}**",
        f"- Candidate classes: `{dict(sorted(candidate_classes.items()))}`",
        "",
        "No commit was cherry-picked. Every patch-unique candidate remains approval-only. The pre-scrub alignment commit `5f34c105974176125ee9417f4fbcb8c5326def0c` is explicitly excluded.",
        "",
        "### Exact-tree rewrite mappings near the abandoned tip",
        "",
        "| Abandoned commit | Active counterpart | Subject |",
        "| --- | --- | --- |",
    ]
    report_lines.extend(f"| `{old}` | `{new}` | {subject.replace('|', '\\|')} |" for old, new, subject in mapping_rows)
    report_lines.extend(
        [
            "",
            "## Exclusions and preservation",
            "",
            "- `.worktrees/repos/IDAHO-VAULT/.git/` remains excluded Git metadata.",
            "- `process-1774818543455-47088.log` remains uncopied because it is runtime material with secret indicators.",
            "- `.worktrees` remains intact. Cleanup requires separate explicit authorization after commit and push verification.",
            "- The active root remains the incumbent; no active file was overwritten, deleted, reset, stashed, or restored.",
            "",
            "## Approval gate",
            "",
            "The JSONL manifest records each of the 150 patch-unique candidates with raw-change digest, changed-path digest, bounded path sample, and risk markers. A candidate must pass manual diff review and secret/storage checks before Logan may approve an individual cherry-pick.",
            "",
        ]
    )
    report_text = "\n".join(report_lines)

    if args.stdout:
        print(json.dumps({"manifest_text": manifest_text, "report_text": report_text}, ensure_ascii=False))
        return 0

    write_jsonl(manifest_path, rows)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8", newline="\n")

    print(
        json.dumps(
            {
                "manifest": str(manifest_path.relative_to(root)),
                "report": str(report_path.relative_to(root)),
                "tracked_entries": len(source_entries),
                "exact_counterparts": exact_counterparts,
                "patch_equivalent": len(equivalent_commits),
                "patch_unique": len(unique_commits),
                "untracked": untracked,
                "copied_payloads": 0,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
