#!/usr/bin/env python3
"""Require a durable transition record for governed version changes.

Authenticated Dependabot PRs that change only requirements.txt are exempt
because the pull request and mandatory dependency-resolution check are their
durable record. Other version transitions must add a record row to
VERSION-TRANSITIONS.md in the same pull request.
"""

from __future__ import annotations

import argparse
import base64
import difflib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[2]
LEDGER_PATH = "VERSION-TRANSITIONS.md"
SHA_PATTERN = re.compile(r"^[0-9a-fA-F]{7,40}$")
REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
RECORD_PATTERN = re.compile(r"^\+\|\s*20\d{2}-\d{2}-\d{2}\s*\|")
PYPROJECT_PATTERN = re.compile(
    r"""(?x)
    ^\s*(?:version|requires-python)\s*=
    |
    ^\s*"[^"]*(?:==|~=|>=|<=|!=|>|<)[^"]*"\s*,?\s*$
    """
)
JSON_VERSION_PATTERN = re.compile(r'"(?:version|registry_version|crewai_version)"\s*:')
AUTOMATION_VERSION_PATTERN = re.compile(
    r"""(?ix)
    \buses:\s*[^\s]+@
    |
    \bpython-version\s*:
    |
    \bversions?\s*:
    |
    \bpip(?:3)?\s+install\b[^\n]*(?:==|~=|>=|<=)
    """
)


def changed_lines(patch: str) -> list[str]:
    return [
        line[1:]
        for line in patch.splitlines()
        if line[:1] in {"+", "-"} and not line.startswith(("+++", "---"))
    ]


def is_version_transition(path: str, patch: str) -> bool:
    normalized = path.replace("\\", "/")
    lines = changed_lines(patch)
    if not lines or normalized == LEDGER_PATH:
        return False
    if normalized == ".python-version":
        return True
    if normalized == "requirements.txt":
        return any(line.strip() and not line.lstrip().startswith("#") for line in lines)
    if normalized == "pyproject.toml":
        return any(PYPROJECT_PATTERN.search(line) for line in lines)
    if normalized in {"swarm.json", ".crewai/manifest.json", "manifest.json"}:
        return any(JSON_VERSION_PATTERN.search(line) for line in lines)
    if normalized.startswith(".obsidian/plugins/") and normalized.endswith("/manifest.json"):
        return any(JSON_VERSION_PATTERN.search(line) for line in lines)
    if normalized == ".github/dependabot.yml":
        return any(AUTOMATION_VERSION_PATTERN.search(line) for line in lines)
    if normalized.startswith((".github/workflows/", ".github/actions/")) and normalized.endswith(
        (".yml", ".yaml")
    ):
        return any(AUTOMATION_VERSION_PATTERN.search(line) for line in lines)
    return False


def has_transition_record(patches: dict[str, str]) -> bool:
    return any(RECORD_PATTERN.match(line) for line in patches.get(LEDGER_PATH, "").splitlines())


def is_dependabot_lock_only(patches: dict[str, str], *, actor: str) -> bool:
    return actor == "dependabot[bot]" and set(patches) == {"requirements.txt"}


def findings_for_patches(patches: dict[str, str], *, actor: str) -> list[str]:
    governed = sorted(path for path, patch in patches.items() if is_version_transition(path, patch))
    if not governed or has_transition_record(patches):
        return []
    if governed == ["requirements.txt"] and is_dependabot_lock_only(patches, actor=actor):
        return []
    return governed


def may_require_content(path: str) -> bool:
    normalized = path.replace("\\", "/")
    if normalized in {
        LEDGER_PATH,
        ".python-version",
        "requirements.txt",
        "pyproject.toml",
        "swarm.json",
        ".crewai/manifest.json",
        "manifest.json",
        ".github/dependabot.yml",
    }:
        return True
    return (
        normalized.startswith(".obsidian/plugins/") and normalized.endswith("/manifest.json")
    ) or (
        normalized.startswith((".github/workflows/", ".github/actions/"))
        and normalized.endswith((".yml", ".yaml"))
    )


def run_git(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def diff_patches(base: str, head: str) -> dict[str, str]:
    for value in (base, head):
        if not SHA_PATTERN.fullmatch(value):
            raise ValueError("base and head must be git commit SHAs")
    paths_result = run_git(["diff", "--name-only", "--diff-filter=ACMRD", "-z", base, head])
    if paths_result.returncode != 0:
        raise RuntimeError(paths_result.stderr.strip() or "git diff failed")
    paths = [path for path in paths_result.stdout.split("\0") if path]
    patches: dict[str, str] = {}
    for path in paths:
        diff_result = run_git(["diff", "--unified=0", "--no-color", base, head, "--", path])
        if diff_result.returncode != 0:
            raise RuntimeError(diff_result.stderr.strip() or f"git diff failed for {path}")
        patches[path] = diff_result.stdout
    return patches


def github_api_json(path: str, *, token: str) -> object:
    request = Request(
        f"https://api.github.com{path}",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:  # noqa: S310 - fixed GitHub API host
            return json.load(response)
    except HTTPError as exc:
        if exc.code == 404:
            raise FileNotFoundError(path) from exc
        raise RuntimeError(f"GitHub API request failed with status {exc.code}") from exc
    except URLError as exc:
        raise RuntimeError("GitHub API request failed") from exc


def github_file_text(repo: str, path: str, ref: str, *, token: str) -> str:
    api_path = (
        f"/repos/{quote(repo, safe='/')}/contents/{quote(path, safe='/')}"
        f"?ref={quote(ref, safe='')}"
    )
    try:
        payload = github_api_json(api_path, token=token)
    except FileNotFoundError:
        return ""
    if not isinstance(payload, dict):
        raise RuntimeError(f"Unexpected GitHub content response for {path}")
    content = payload.get("content")
    if payload.get("encoding") != "base64" or not isinstance(content, str):
        raise RuntimeError(f"Unable to inspect governed file contents for {path}")
    try:
        return base64.b64decode(content).decode("utf-8", errors="replace")
    except ValueError as exc:
        raise RuntimeError(f"Invalid GitHub content response for {path}") from exc


def text_patch(path: str, before: str, after: str) -> str:
    return "".join(
        difflib.unified_diff(
            before.splitlines(keepends=True),
            after.splitlines(keepends=True),
            fromfile=f"a/{path}",
            tofile=f"b/{path}",
            n=0,
        )
    )


def github_pr_patches(
    repo: str, pr_number: int, base: str, head: str, *, token: str
) -> dict[str, str]:
    if not REPO_PATTERN.fullmatch(repo) or pr_number <= 0 or not token:
        raise ValueError("GitHub API mode requires a repository, pull request number, and token")
    for value in (base, head):
        if not SHA_PATTERN.fullmatch(value):
            raise ValueError("base and head must be git commit SHAs")

    changed_paths: set[str] = set()
    page = 1
    while True:
        payload = github_api_json(
            f"/repos/{quote(repo, safe='/')}/pulls/{pr_number}/files?per_page=100&page={page}",
            token=token,
        )
        if not isinstance(payload, list):
            raise RuntimeError("Unexpected GitHub pull request files response")
        for file_data in payload:
            if not isinstance(file_data, dict) or not isinstance(file_data.get("filename"), str):
                raise RuntimeError("Unexpected GitHub pull request file entry")
            changed_paths.add(file_data["filename"])
            previous = file_data.get("previous_filename")
            if isinstance(previous, str):
                changed_paths.add(previous)
        if len(payload) < 100:
            break
        page += 1
        if page > 30:
            raise RuntimeError("Pull request exceeds version-transition inspection limit")

    patches = {path: "" for path in sorted(changed_paths)}
    for path in patches:
        if may_require_content(path):
            before = github_file_text(repo, path, base, token=token)
            after = github_file_text(repo, path, head, token=token)
            patches[path] = text_patch(path, before, after)
    return patches


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="base commit SHA")
    parser.add_argument("--head", required=True, help="head commit SHA")
    parser.add_argument("--actor", required=True, help="pull request author login")
    parser.add_argument("--github-repo", help="owner/repository for GitHub API comparison mode")
    parser.add_argument("--pr-number", type=int, help="pull request number for GitHub API mode")
    args = parser.parse_args()

    try:
        if (args.github_repo is None) != (args.pr_number is None):
            raise ValueError("--github-repo and --pr-number must be specified together")
        if args.github_repo:
            patches = github_pr_patches(
                args.github_repo,
                args.pr_number,
                args.base,
                args.head,
                token=os.environ.get("GITHUB_TOKEN", ""),
            )
        else:
            patches = diff_patches(args.base, args.head)
        findings = findings_for_patches(patches, actor=args.actor)
    except (RuntimeError, ValueError) as exc:
        print(f"version-transition guard: {exc}", file=sys.stderr)
        return 2

    if not findings:
        print("version-transition guard: OK")
        return 0

    print("version-transition guard: unrecorded governed version change.", file=sys.stderr)
    for path in findings:
        print(f"  {path}", file=sys.stderr)
    print(
        f"Add a compatibility/rationale row to {LEDGER_PATH}, or keep a "
        "Dependabot PR limited to requirements.txt and let required resolution checks decide it.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
