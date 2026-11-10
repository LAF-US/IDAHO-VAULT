"""Integrity checks for the claude.ai project memory backup (#1103)."""

import re
from pathlib import Path

_ROOT = Path(__file__).parents[1]
_MEMORY = _ROOT / ".claude" / "MEMORY"
_BACKUP = _MEMORY / "CLAUDE-AI-PROJECT-BACKUP-2026-11-10"
_README = _BACKUP / "README.md"
_INDEX = _MEMORY / "MEMORY.md"
_PROVENANCE = "<!-- Copied from the original claude.ai project during the upgrade."

_TABLE_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|", re.MULTILINE)


def _listed_paths():
    """Return the relative paths named in the README contents table."""
    return _TABLE_ROW.findall(_README.read_text(encoding="utf-8"))


def test_contents_table_lists_files_that_exist():
    """Every file named in the README table is present and not empty."""
    listed = _listed_paths()
    assert listed, "README contents table lists no files"
    for relative in listed:
        path = _BACKUP / relative
        assert path.is_file(), relative
        assert path.stat().st_size > 0, relative


def test_every_backup_file_appears_in_the_contents_table():
    """No backup file is left unlisted, so the table stays a full inventory."""
    listed = set(_listed_paths())
    on_disk = {
        path.relative_to(_BACKUP).as_posix()
        for path in _BACKUP.rglob("*.md")
        if path != _README
    }
    assert on_disk - listed == set()


def test_imported_files_keep_their_provenance_header():
    """Imported copies keep the header the claude.ai upgrade wrote."""
    for path in sorted((_BACKUP / "imported").rglob("*.md")):
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        assert first_line.startswith(_PROVENANCE), path.name


def test_shared_memory_index_points_at_the_backup():
    """The shared memory index names the backup directory."""
    assert "CLAUDE-AI-PROJECT-BACKUP-2026-11-10/" in _INDEX.read_text(encoding="utf-8")
