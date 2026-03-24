#!/usr/bin/env python3
"""
Linear → Research Brief Generator (Stage 1 Mesh)
=================================================
Reads a Linear issue payload and generates a Markdown research brief
using an LLM API. Output lands in !/ (the vault mailroom) for Logan
to review and route.

Guardrails:
  - Hardcoded output directory: !/
  - Only writes files matching BRIEF-*.md
  - Max output: 50 KB
  - No shell commands, no file deletion, no path traversal
  - Fails gracefully if no API key is set

Usage:
  # From environment (GitHub Actions)
  LINEAR_PAYLOAD='{"title":"...","id":"VAULT-42"}' python3 linear_brief_generator.py

  # From CLI (local testing)
  python3 linear_brief_generator.py --payload '{"title":"...","id":"VAULT-42"}'

  # Dry run (print to stdout, don't write file)
  python3 linear_brief_generator.py --dry-run --payload '...'
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── Guardrails ────────────────────────────────────────────────────────────────

VAULT_ROOT = Path(".")
ALLOWED_OUTPUT_DIR = VAULT_ROOT / "!"
ALLOWED_PREFIX = "BRIEF-"
MAX_OUTPUT_BYTES = 50 * 1024  # 50 KB

# ── LLM Prompt ────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """\
You are a research assistant for a journalism vault. Given a Linear issue
describing a story or investigation, produce a structured research brief
in Markdown. The brief should include:

1. **Summary** — What is this about? (2-3 sentences)
2. **Key Questions** — What needs to be answered? (bulleted list)
3. **Known Sources** — Who or what should be consulted? (bulleted list)
4. **Background** — Relevant context, prior reporting, or public records
5. **Next Steps** — Concrete actions to advance the story

Be specific to Idaho journalism. Cite public records, state agencies,
and legislative processes where relevant. Do not fabricate sources or
quotes. If you don't know something, say so.
"""


def build_user_prompt(payload: dict) -> str:
    """Build the user prompt from Linear issue fields."""
    parts = []
    if payload.get("title"):
        parts.append(f"**Issue:** {payload['title']}")
    if payload.get("description"):
        parts.append(f"**Description:**\n{payload['description']}")
    if payload.get("labels"):
        labels = payload["labels"]
        if isinstance(labels, list):
            label_names = [lb.get("name", str(lb)) if isinstance(lb, dict) else str(lb) for lb in labels]
            parts.append(f"**Labels:** {', '.join(label_names)}")
    if payload.get("priority"):
        parts.append(f"**Priority:** {payload['priority']}")
    if payload.get("assignee"):
        assignee = payload["assignee"]
        name = assignee.get("name", str(assignee)) if isinstance(assignee, dict) else str(assignee)
        parts.append(f"**Assignee:** {name}")
    return "\n\n".join(parts) if parts else "No issue details provided."


# ── LLM Providers ─────────────────────────────────────────────────────────────

def call_anthropic(system: str, user: str) -> str:
    """Call Claude API via the Anthropic SDK."""
    import anthropic
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return message.content[0].text


def call_openai(system: str, user: str) -> str:
    """Call OpenAI API via the openai SDK."""
    import openai
    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=4096,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return response.choices[0].message.content


def call_llm(system: str, user: str) -> str:
    """Try available LLM providers in order."""
    if os.environ.get("ANTHROPIC_API_KEY"):
        return call_anthropic(system, user)
    if os.environ.get("OPENAI_API_KEY"):
        return call_openai(system, user)
    print("ERROR: No LLM API key found.", file=sys.stderr)
    print("  Set ANTHROPIC_API_KEY or OPENAI_API_KEY.", file=sys.stderr)
    sys.exit(1)


# ── Output ────────────────────────────────────────────────────────────────────

def build_frontmatter(payload: dict, date_str: str) -> str:
    """Build YAML frontmatter for the brief."""
    linear_id = payload.get("id", payload.get("identifier", "UNKNOWN"))
    title = payload.get("title", "Untitled")
    lines = [
        "---",
        f"title: \"BRIEF — {title}\"",
        f"linear_id: \"{linear_id}\"",
        f"date: {date_str}",
        "status: draft",
        "type: brief",
        "source: Linear",
        "generated: true",
        "---",
    ]
    return "\n".join(lines)


def safe_output_path(payload: dict, date_str: str) -> Path:
    """Build a safe output path. Rejects path traversal."""
    linear_id = payload.get("id", payload.get("identifier", "UNKNOWN"))
    # Sanitize: only allow alphanumeric, hyphens, underscores
    safe_id = "".join(c for c in str(linear_id) if c.isalnum() or c in "-_")
    if not safe_id:
        safe_id = "UNKNOWN"

    filename = f"{ALLOWED_PREFIX}{safe_id}-{date_str}.md"

    # Belt-and-suspenders: reject traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        print(f"ERROR: Unsafe filename: {filename}", file=sys.stderr)
        sys.exit(1)

    return ALLOWED_OUTPUT_DIR / filename


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate research brief from Linear issue")
    parser.add_argument("--payload", type=str, help="Linear issue JSON (alternative to LINEAR_PAYLOAD env)")
    parser.add_argument("--dry-run", action="store_true", help="Print to stdout instead of writing file")
    args = parser.parse_args()

    # Get payload
    raw = args.payload or os.environ.get("LINEAR_PAYLOAD", "")
    if not raw:
        print("ERROR: No payload provided.", file=sys.stderr)
        print("  Use --payload or set LINEAR_PAYLOAD env var.", file=sys.stderr)
        return 1

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON payload: {e}", file=sys.stderr)
        return 1

    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")

    # Build prompts
    user_prompt = build_user_prompt(payload)
    print(f"Generating brief for: {payload.get('title', 'Untitled')}")

    # Call LLM
    brief_body = call_llm(SYSTEM_PROMPT, user_prompt)

    # Assemble output
    frontmatter = build_frontmatter(payload, date_str)
    output = f"{frontmatter}\n\n{brief_body}\n"

    # Size check
    output_bytes = len(output.encode("utf-8"))
    if output_bytes > MAX_OUTPUT_BYTES:
        print(f"ERROR: Output too large ({output_bytes} bytes > {MAX_OUTPUT_BYTES} limit)", file=sys.stderr)
        return 1

    if args.dry_run:
        print("--- DRY RUN ---")
        print(output)
        print(f"--- {output_bytes} bytes ---")
        return 0

    # Write file
    out_path = safe_output_path(payload, date_str)
    ALLOWED_OUTPUT_DIR.mkdir(exist_ok=True)
    out_path.write_text(output, encoding="utf-8")
    print(f"Brief written to {out_path} ({output_bytes} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
