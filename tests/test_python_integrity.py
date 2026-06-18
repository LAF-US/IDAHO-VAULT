from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_checker():
    script_path = ROOT / ".github" / "scripts" / "check_python_integrity.py"
    spec = importlib.util.spec_from_file_location("check_python_integrity_test_module", script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = load_checker()


def test_rejects_purge_markers_and_syntax_errors(tmp_path: Path) -> None:
    marker = "***" + "REMOVED" + "***"
    path = tmp_path / "broken.py"
    path.write_text(f"{marker}\ndef nope(:\n", encoding="utf-8")

    findings = checker.python_file_findings(path)

    assert any("contains purge marker" in finding for finding in findings)
    assert any("syntax error" in finding for finding in findings)


def test_active_subprocess_requires_timeout(tmp_path: Path) -> None:
    path = tmp_path / "runner.py"
    path.write_text(
        "import subprocess\nsubprocess.run(['git', 'status'])\n",
        encoding="utf-8",
    )

    findings = checker.python_file_findings(path)

    assert any("subprocess call missing timeout" in finding for finding in findings)


def test_interactive_subprocess_can_be_explicitly_exempted(tmp_path: Path) -> None:
    path = tmp_path / "interactive.py"
    path.write_text(
        "import subprocess\n"
        "# timeout: interactive\n"
        "subprocess.run(['agent', 'serve'])\n",
        encoding="utf-8",
    )

    findings = checker.python_file_findings(path)

    assert findings == []


def test_obvious_flattened_duplicate_is_reported(tmp_path: Path) -> None:
    canonical = tmp_path / "src" / "pkg" / "module.py"
    canonical.parent.mkdir(parents=True)
    canonical.write_text("VALUE = 1\n", encoding="utf-8")
    flattened = tmp_path / "src-pkg-module.py"
    flattened.write_text("VALUE = 1\n", encoding="utf-8")

    findings = checker.flattened_duplicate_findings(tmp_path, [canonical, flattened])

    assert any("byte-identical flattened duplicate" in finding for finding in findings)
