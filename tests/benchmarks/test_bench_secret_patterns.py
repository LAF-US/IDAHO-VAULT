"""Benchmarks for the accidental-secret-commit guard.

`check_secret_patterns.py` is the most regex-heavy guard in the repository: it
runs nineteen path patterns against every normalized variant of every changed
path, then seven content patterns against every line of every changed file.

The credential-shaped strings below are assembled from fragments at runtime so
that no literal token pattern is ever written into this file — the guard scans
its own repository, and a benchmark fixture must not become a finding.
"""

from __future__ import annotations

import check_secret_patterns as csp


def _fake_forge_credential() -> str:
    return "gh" + "p_" + "0123456789abcdefghijklmnopqrstuvwx"


def _fake_cloud_credential() -> str:
    return "AI" + "za" + ("Vault0Bench" * 4)[:35]


def _fake_key_header() -> str:
    return "-----BEGIN " + "PRIVATE " + "KEY-----"


def _credential_shaped_document(clean_lines: list[str]) -> bytes:
    """A mostly clean document with a few lines that do produce findings."""
    lines = list(clean_lines)
    lines.insert(20, f"forge credential: {_fake_forge_credential()}")
    lines.insert(120, f"cloud credential: {_fake_cloud_credential()}")
    lines.insert(220, _fake_key_header())
    return "\n".join(lines).encode("utf-8")


def test_path_findings_over_changeset(benchmark, small_vault_paths):
    """Nineteen path patterns against every normalized variant of each path."""
    findings = benchmark(
        lambda: [
            finding for path in small_vault_paths for finding in csp.path_findings(path)
        ]
    )

    assert isinstance(findings, list)


def test_normalized_path_variants(benchmark, small_vault_paths):
    """The Windows-copy / preserved-suffix variant expansion done per path."""
    variants = benchmark(
        lambda: [csp.normalized_path_variants(path) for path in small_vault_paths]
    )

    assert len(variants) == len(small_vault_paths)


def test_content_findings_clean_document(benchmark, vault_note_bytes):
    """The common case: a long Markdown note with nothing to report."""
    findings = benchmark(lambda: csp.content_findings("handoff.md", vault_note_bytes))

    assert findings == []


def test_content_findings_with_matches(benchmark, vault_note):
    """The reporting path, with matches spread through the document."""
    data = _credential_shaped_document(vault_note.splitlines())

    findings = benchmark(lambda: csp.content_findings("handoff.md", data))

    assert len(findings) >= 3
