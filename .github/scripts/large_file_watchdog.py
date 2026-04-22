#!/usr/bin/env python3
"""Report on tracked large files in the current tree."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def human_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ["B", "KiB", "MiB", "GiB"]:
        if size < 1024.0 or unit == "GiB":
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{num_bytes} B"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report-path", type=Path, required=True)
    parser.add_argument("--total-threshold-mib", type=int, default=150)
    parser.add_argument("--file-threshold-mib", type=int, default=5)
    parser.add_argument("--top-n", type=int, default=20)
    args = parser.parse_args()

    result = subprocess.run(
        ["git", "ls-files", "-z"], check=True, capture_output=True
    )
    tracked = [Path(p.decode("utf-8")) for p in result.stdout.split(b"\0") if p]

    offenders: list[tuple[int, Path]] = []
    total_bytes = 0
    file_threshold = args.file_threshold_mib * 1024 * 1024
    for path in tracked:
        if not path.exists() or not path.is_file():
            continue
        size = path.stat().st_size
        total_bytes += size
        if size >= file_threshold:
            offenders.append((size, path))

    offenders.sort(reverse=True)
    total_threshold = args.total_threshold_mib * 1024 * 1024
    has_findings = total_bytes >= total_threshold or bool(offenders)

    lines = [
        "# Large File Watchdog",
        "",
        f"Tracked payload in current tree: **{human_size(total_bytes)}**",
        f"Total threshold: **{args.total_threshold_mib} MiB**",
        f"Per-file threshold: **{args.file_threshold_mib} MiB**",
        "",
    ]

    if offenders:
        lines.extend(["## Top tracked offenders", ""])
        for size, path in offenders[: args.top_n]:
            lines.append(f"- `{path.as_posix()}` — {human_size(size)}")
        lines.append("")
    else:
        lines.extend(["No tracked files exceed the per-file threshold.", ""])

    args.repo***REMOVED***path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as fh:
            fh.write(f"has_findings={'true' if has_findings else 'false'}\n")
            fh.write(f"total_bytes={total_bytes}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
