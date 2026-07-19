from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


def load_manifest(path: Path) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            entries.append(json.loads(line))
    return entries


def write_csv(path: Path, entries: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "action",
                "destination",
                "top_level",
                "source",
                "relative_within_top",
                "collision",
            ],
        )
        writer.writeheader()
        for entry in entries:
            writer.writerow(
                {
                    "action": entry.get("action"),
                    "destination": entry.get("destination") or "",
                    "top_level": entry.get("top_level"),
                    "source": entry.get("source"),
                    "relative_within_top": entry.get("relative_within_top"),
                    "collision": entry.get("collision") or "",
                }
            )


def write_markdown(path: Path, manifest_name: str, csv_name: str, entries: list[dict[str, object]]) -> None:
    counts_by_folder: dict[str, Counter[str]] = defaultdict(Counter)
    for entry in entries:
        folder = str(entry.get("top_level", ""))
        counts_by_folder[folder][str(entry.get("action", ""))] += 1

    lines = [
        "---",
        "authority: Codex",
        f"date created: {date.today().isoformat()}",
        "status: active",
        "source: ground-truth",
        "---",
        "",
        f"# Flatten Attribution - {date.today().isoformat()}",
        "",
        "This note preserves human-readable folder attribution for the doctrinal flatten.",
        "",
        "Companion records:",
        "",
        f"- manifest: `{manifest_name}`",
        f"- attribution csv: `{csv_name}`",
        "",
        "The CSV preserves per-file folder attribution.",
        "This markdown note preserves the folder-level human-readable summary.",
        "",
        "| Source folder | moved | renamed | rehomed | skipped |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]

    for folder in sorted(counts_by_folder.keys(), key=str.lower):
        bucket = counts_by_folder[folder]
        lines.append(
            f"| `{folder}` | {bucket.get('moved_root', 0)} | {bucket.get('moved_root_renamed', 0)} | "
            f"{bucket.get('rehomed_inbox', 0) + bucket.get('rehomed_inbox_renamed', 0)} | "
            f"{bucket.get('skipped_machine_state', 0)} |"
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Render human-readable flatten attribution records from a JSONL manifest.")
    parser.add_argument("--manifest", default=f"!/RESTRUCTURE-MANIFEST-{date.today().isoformat()}.jsonl")
    parser.add_argument("--csv", default=f"!/RESTRUCTURE-ATTRIBUTION-{date.today().isoformat()}.csv")
    parser.add_argument("--markdown", default=f"!/RESTRUCTURE-ATTRIBUTION-{date.today().isoformat()}.md")
    args = parser.parse_args()

    repo_root = Path(".").resolve()
    manifest_path = repo_root / args.manifest
    csv_path = repo_root / args.csv
    markdown_path = repo_root / args.markdown

    entries = load_manifest(manifest_path)
    write_csv(csv_path, entries)
    write_markdown(markdown_path, args.manifest, args.csv, entries)
    print(
        json.dumps(
            {
                "manifest": args.manifest,
                "csv": args.csv,
                "markdown": args.markdown,
                "entries": len(entries),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
