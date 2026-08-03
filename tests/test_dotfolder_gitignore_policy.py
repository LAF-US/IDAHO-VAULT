from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def is_ignored(path: str) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "--quiet", "--", path],
        cwd=ROOT,
        capture_output=True,
        check=False,
        timeout=30,
    )
    if result.returncode not in {0, 1}:
        raise AssertionError(result.stderr.decode("utf-8", errors="replace"))
    return result.returncode == 0


def test_salvaged_secret_and_runtime_variants_are_ignored() -> None:
    paths = [
        ".claude/.credentials (2).json",
        ".claude/settings.local (2).json",
        ".claude/settings.local (12).json",
        ".claude/settings (3).json",
        ".claude/history.jsonl.home",
        ".codex/history.jsonl.home",
        ".codex/history (12).jsonl",
        ".codex/auth.json.home.abcdef123456",
        ".codex/config.toml.home.c9ed9573416d",
        ".codex/.app-server-state-reconciled-v1",
        ".codex/rules/default.rules.home",
        ".codex/rules/default.rules.bak-20260618-083224",
        ".codex/sqlite/codex-dev.db.home",
        ".codex/.sandbox-bin/tool.exe",
        ".config/scoop/config (2).json",
        ".ollama/id_ed25519 (2)",
        ".sbx-denybin/scp (2).cmd",
        ".sbx-denybin/scp (12).cmd",
        ".ssh/1Password/config",
        ".ssh/allowed_signers (2)",
        ".ssh/claude_code_signing (2)",
        ".ssh/known_hosts (2).old",
        ".local/state/tool/state.db",
    ]

    not_ignored = [path for path in paths if not is_ignored(path)]
    assert not not_ignored, f"Expected ignored, but visible: {not_ignored}"


def test_publishable_anchor_names_remain_visible() -> None:
    paths = [
        ".claude/CLAUDE.md",
        ".codex/AGENTS.md",
        ".config/CONFIG.md",
    ]

    ignored = [path for path in paths if is_ignored(path)]
    assert not ignored, f"Expected visible anchors, but ignored: {ignored}"
