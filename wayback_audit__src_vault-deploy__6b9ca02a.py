#!/usr/bin/env python3
"""
IDAHO-VAULT Wayback Machine Audit
Scans all vault notes for URL fields, checks live status, and for dead links
queries the Wayback Machine for the best available snapshot.

Outputs:
  !ADMINISTRATION/wayback-audit-YYYY-MM-DD.md  — human-readable report
  !ADMINISTRATION/wayback-patches-YYYY-MM-DD.md — proposed frontmatter patches

Rate limits:
  - Live URL checks: 2 req/sec max (be a good citizen)
  - Wayback CDX API: 1 req/sec max
  - Wayback Save API: skipped by default; enable with --save flag

Usage:
  python3 wayback_audit.py           # dry run, report only
  python3 wayback_audit.py --save    # also submit dead URLs to Save Page Now
  python3 wayback_audit.py --limit N # only check first N URLs (for testing)
"""

import os
import re
import sys
import time
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ── Config ────────────────────────────────────────────────────────────────────

VAULT_ROOT = Path(".")
ADMIN_DIR = VAULT_ROOT / "!ADMINISTRATION"

# Folders to skip entirely (scratch, templates)
SKIP_FOLDERS = {"x hey you make sure to link these", "X LABELER", "ATTACHMENTS"}

# Seconds between requests (per API)
RATE_LIVE = 0.5       # live URL head requests
RATE_CDX = 1.0        # Wayback CDX lookups
RATE_SAVE = 5.0       # Save Page Now submissions (slow by design)

# HTTP timeout in seconds
TIMEOUT = 10

# User-Agent (be identifiable)
UA = "IDAHO-VAULT/1.0 (Idaho Reports journalism archive; github.com/loganfinney27/IDAHO-VAULT)"

# Status codes we treat as "dead"
DEAD_STATUSES = {400, 403, 404, 410, 451, 500, 502, 503, 504}

# ── Helpers ───────────────────────────────────────────────────────────────────

def head_request(url: str) -> int | None:
    """Returns HTTP status code, or None on connection error."""
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return resp.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None


def cdx_lookup(url: str) -> dict | None:
    """
    Query Wayback CDX API for the most recent snapshot of a URL.
    Returns dict with 'snapshot_url', 'timestamp', 'status_code' or None.
    """
    cdx_url = (
        "http://web.archive.org/cdx/search/cdx"
        f"?url={urllib.parse.quote(url, safe='')}"
        "&output=json&limit=1&fl=timestamp,statuscode,original&filter=statuscode:200"
        "&fastLatest=true"
    )
    try:
        req = urllib.request.Request(cdx_url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read())
            # data[0] is header row, data[1] is first result
            if len(data) < 2:
                return None
            ts, sc, orig = data[1]
            return {
                "snapshot_url": f"https://web.archive.org/web/{ts}/{orig}",
                "timestamp": ts,
                "status_code": sc,
            }
    except Exception:
        return None


def save_page_now(url: str) -> str | None:
    """
    Submit a URL to Wayback Save Page Now.
    Returns the archived URL if successful, else None.
    No auth required for public pages.
    """
    save_url = f"https://web.archive.org/save/{url}"
    try:
        req = urllib.request.Request(
            save_url,
            method="GET",
            headers={"User-Agent": UA, "Accept": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            # SPN returns the archived URL in Content-Location header
            loc = resp.headers.get("Content-Location", "")
            if loc:
                return f"https://web.archive.org{loc}"
            return save_url  # fallback
    except Exception:
        return None


def find_vault_notes() -> list[Path]:
    """Walk vault, skip excluded folders, return all .md files."""
    notes = []
    for path in sorted(VAULT_ROOT.rglob("*.md")):
        # Check if any parent folder is in skip list
        parts = path.parts
        if any(p in SKIP_FOLDERS for p in parts):
            continue
        if ".github" in parts:
            continue
        notes.append(path)
    return notes


def extract_url(content: str) -> str | None:
    """Extract URL from YAML frontmatter URL field."""
    m = re.search(r"^URL:\s*(.+)$", content, re.MULTILINE)
    if not m:
        return None
    url = m.group(1).strip()
    if not url or url.lower() == "null" or url.lower() == "n/a":
        return None
    # Already a Wayback URL — skip
    if "web.archive.org" in url:
        return None
    return url


def extract_wayback_field(content: str) -> str | None:
    """Check if note already has a wayback: frontmatter field."""
    m = re.search(r"^wayback:\s*(.+)$", content, re.MULTILINE)
    return m.group(1).strip() if m else None

# ── Main ──────────────────────────────────────────────────────────────────────

import urllib.parse  # needed for cdx_lookup

def main():
    parser = argparse.ArgumentParser(description="Wayback Machine audit for IDAHO-VAULT")
    parser.add_argument("--save", action="store_true", help="Submit dead URLs to Save Page Now")
    parser.add_argument("--limit", type=int, default=0, help="Limit to N URLs (for testing)")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")

    print(f"IDAHO-VAULT Wayback Audit — {date_str}")
    print("Scanning vault notes...")

    notes = find_vault_notes()
    print(f"Found {len(notes)} notes")

    # Collect notes that have URLs
    url_notes = []
    for note in notes:
        content = note.read_text(encoding="utf-8", errors="replace")
        url = extract_url(content)
        if url:
            already_has_wayback = extract_wayback_field(content)
            url_notes.append({
                "path": note,
                "url": url,
                "content": content,
                "already_patched": already_has_wayback,
            })

    total_urls = len(url_notes)
    print(f"Found {total_urls} notes with URLs")

    if args.limit:
        url_notes = url_notes[:args.limit]
        print(f"Limiting to first {args.limit} URLs")

    # Results buckets
    live = []
    dead = []
    unreachable = []  # timeout/connection error — skip, don't flag
    already_patched = []

    print("\nChecking live status...")

    for i, item in enumerate(url_notes, 1):
        note_name = item["path"].name
        url = item["url"]

        if item["already_patched"]:
            already_patched.append(item)
            print(f"  [{i}/{len(url_notes)}] SKIP (already patched) {note_name}")
            continue

        print(f"  [{i}/{len(url_notes)}] {note_name[:60]}", end=" ", flush=True)
        status = head_request(url)
        time.sleep(RATE_LIVE)

        if status is None:
            print(f"→ UNREACHABLE")
            unreachable.append({**item, "live_status": None})
        elif status in DEAD_STATUSES:
            print(f"→ DEAD ({status})")
            dead.append({**item, "live_status": status})
        else:
            print(f"→ OK ({status})")
            live.append({**item, "live_status": status})

    # For dead URLs, query Wayback CDX
    print(f"\nQuerying Wayback for {len(dead)} dead URLs...")

    patches = []
    no_archive = []

    for i, item in enumerate(dead, 1):
        note_name = item["path"].name
        url = item["url"]
        print(f"  [{i}/{len(dead)}] {note_name[:60]}", end=" ", flush=True)

        snapshot = cdx_lookup(url)
        time.sleep(RATE_CDX)

        if snapshot:
            print(f"→ snapshot {snapshot['timestamp']}")
            item["snapshot"] = snapshot
            patches.append(item)

            if args.save:
                print(f"    Submitting to Save Page Now...", end=" ", flush=True)
                saved = save_page_now(url)
                if saved:
                    print(f"saved")
                    item["saved_url"] = saved
                else:
                    print(f"failed")
                time.sleep(RATE_SAVE)
        else:
            print(f"→ NO ARCHIVE FOUND")
            item["snapshot"] = None
            no_archive.append(item)

    # ── Write report ──────────────────────────────────────────────────────────

    ADMIN_DIR.mkdir(exist_ok=True)
    report_path = ADMIN_DIR / f"wayback-audit-{date_str}.md"
    patches_path = ADMIN_DIR / f"wayback-patches-{date_str}.md"

    report_lines = [
        f"# Wayback Audit — {date_str}",
        "",
        f"Scanned {total_urls} notes with URL fields.",
        "",
        f"| Status | Count |",
        f"|---|---|",
        f"| ✅ Live | {len(live)} |",
        f"| ❌ Dead — snapshot found | {len(patches)} |",
        f"| ❌ Dead — no archive | {len(no_archive)} |",
        f"| ⚠️ Unreachable (network error) | {len(unreachable)} |",
        f"| ⏭️ Already patched | {len(already_patched)} |",
        "",
        "---",
        "",
    ]

    if patches:
        report_lines += [
            "## Dead — Wayback Snapshot Found",
            "",
            "These notes have dead URLs with Wayback snapshots available. "
            "See `wayback-patches-{date_str}.md` for proposed frontmatter additions.",
            "",
            "| Note | Original URL | Snapshot | Archived |",
            "|---|---|---|---|",
        ]
        for item in patches:
            snap = item["snapshot"]
            ts = snap["timestamp"]
            archived_date = f"{ts[0:4]}-{ts[4:6]}-{ts[6:8]}"
            report_lines.append(
                f"| `{item['path'].name}` "
                f"| [{item['url'][:60]}]({item['url']}) "
                f"| [snapshot]({snap['snapshot_url']}) "
                f"| {archived_date} |"
            )
        report_lines.append("")

    if no_archive:
        report_lines += [
            "## Dead — No Archive Found",
            "",
            "These URLs are dead and have no Wayback snapshot. "
            "Manual recovery required (Google Cache, original author, etc.).",
            "",
            "| Note | Dead URL | HTTP Status |",
            "|---|---|---|",
        ]
        for item in no_archive:
            report_lines.append(
                f"| `{item['path'].name}` "
                f"| {item['url'][:80]} "
                f"| {item['live_status']} |"
            )
        report_lines.append("")

    if unreachable:
        report_lines += [
            "## Unreachable (Network Error)",
            "",
            "Connection failed — may be transient. Re-run to confirm.",
            "",
            "| Note | URL |",
            "|---|---|",
        ]
        for item in unreachable:
            report_lines.append(
                f"| `{item['path'].name}` | {item['url'][:80]} |"
            )
        report_lines.append("")

    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"\nReport written to {report_path}")

    # ── Write patches file ────────────────────────────────────────────────────

    if patches:
        patch_lines = [
            f"# Wayback Patches — {date_str}",
            "",
            "Proposed `wayback:` frontmatter additions for notes with dead URLs.",
            "Each entry shows the note path and the line to insert after the `URL:` field.",
            "",
            "**To apply:** Insert the `wayback:` line into each note's frontmatter, "
            "directly after the `URL:` field.",
            "",
            "---",
            "",
        ]
        for item in patches:
            snap = item["snapshot"]
            rel_path = item["path"].relative_to(VAULT_ROOT)
            patch_lines += [
                f"### `{rel_path}`",
                "",
                f"```",
                f"URL: {item['url']}",
                f"wayback: {snap['snapshot_url']}",
                f"```",
                "",
            ]

        patches_path.write_text("\n".join(patch_lines), encoding="utf-8")
        print(f"Patches written to {patches_path}")

    # ── Summary ───────────────────────────────────────────────────────────────

    print(f"\n{'─'*50}")
    print(f"Total URLs scanned:      {total_urls}")
    print(f"Live:                    {len(live)}")
    print(f"Dead (snapshot found):   {len(patches)}")
    print(f"Dead (no archive):       {len(no_archive)}")
    print(f"Unreachable:             {len(unreachable)}")
    print(f"Already patched:         {len(already_patched)}")


if __name__ == "__main__":
    main()
