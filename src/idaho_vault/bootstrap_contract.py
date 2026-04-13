"""Deterministic validation of the CrewAI bootstrap contract."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
from typing import Any


@dataclass(frozen=True)
class ContractCheck:
    """One bootstrap validation check."""

    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class ContractReport:
    """Structured report for the bootstrap validation shard."""

    ok: bool
    checks: tuple[ContractCheck, ...]

    def to_markdown(self) -> str:
        """Render a concise markdown report for humans and agents."""
        lines = [
            "# Bootstrap Contract Report",
            "",
            f"Overall status: {'PASS' if self.ok else 'FAIL'}",
            "",
            "| Check | Status | Detail |",
            "| --- | --- | --- |",
        ]

        for check in self.checks:
            status = "PASS" if check.ok else "FAIL"
            lines.append(f"| `{check.name}` | {status} | {check.detail} |")

        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        """Return a machine-readable representation."""
        return {
            "ok": self.ok,
            "checks": [
                {"name": check.name, "ok": check.ok, "detail": check.detail}
                for check in self.checks
            ],
        }


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _check_exists(root: Path, relpath: str, name: str) -> ContractCheck:
    path = root / relpath
    return ContractCheck(
        name=name,
        ok=path.exists(),
        detail=f"`{relpath}` {'present' if path.exists() else 'missing'}",
    )


def _check_pyproject(root: Path) -> ContractCheck:
    path = root / "pyproject.toml"
    if not path.exists():
        return ContractCheck("pyproject", False, "`pyproject.toml` missing")

    text = path.read_text(encoding="utf-8")
    required_tokens = (
        'name = "idaho-vault"',
        'type = "crew"',
        'idaho_vault = "idaho_vault.main:run"',
    )
    missing = [token for token in required_tokens if token not in text]
    if missing:
        return ContractCheck(
            "pyproject",
            False,
            f"`pyproject.toml` missing expected tokens: {', '.join(missing)}",
        )
    return ContractCheck(
        "pyproject",
        True,
        "`pyproject.toml` exposes the CrewAI project and script contract",
    )


def _check_lockfile(root: Path) -> ContractCheck:
    path = root / "uv.lock"
    if not path.exists():
        return ContractCheck("lockfile", False, "`uv.lock` missing")

    text = path.read_text(encoding="utf-8")
    if "crewai" not in text:
        return ContractCheck(
            "lockfile",
            False,
            "`uv.lock` present but does not mention `crewai`",
        )

    return ContractCheck(
        "lockfile",
        True,
        "`uv.lock` present and references CrewAI dependencies",
    )


def _check_manifest(root: Path) -> ContractCheck:
    path = root / ".crewai" / "manifest.json"
    if not path.exists():
        return ContractCheck("manifest-json", False, "`.crewai/manifest.json` missing")

    data = json.loads(path.read_text(encoding="utf-8"))
    crews = data.get("crews", [])
    active_bootstrap = any(
        crew.get("id") == "idaho-vault-bootstrap" and crew.get("status") == "active"
        for crew in crews
    )
    if not active_bootstrap:
        return ContractCheck(
            "manifest-json",
            False,
            "`.crewai/manifest.json` does not register an active bootstrap crew",
        )
    return ContractCheck(
        "manifest-json",
        True,
        "`.crewai/manifest.json` registers the active bootstrap crew",
    )


def _check_training_doctrine(root: Path) -> ContractCheck:
    path = root / ".crewai" / "TRAINING.md"
    if not path.exists():
        return ContractCheck("training-doctrine", False, "`.crewai/TRAINING.md` missing")

    text = path.read_text(encoding="utf-8")
    markers = (
        "One bootstrap crew is live",
        "No crew is training-ready yet.",
        "`idaho_vault.bootstrap`",
    )
    missing = [marker for marker in markers if marker not in text]
    if missing:
        return ContractCheck(
            "training-doctrine",
            False,
            f"training doctrine missing markers: {', '.join(missing)}",
        )
    return ContractCheck(
        "training-doctrine",
        True,
        "training doctrine matches the live bootstrap posture",
    )


def _check_launcher(root: Path) -> ContractCheck:
    path = root / "scripts" / "Start-CrewAIVault.ps1"
    if not path.exists():
        return ContractCheck("launcher", False, "`scripts/Start-CrewAIVault.ps1` missing")

    text = path.read_text(encoding="utf-8")
    if "Use-VaultAgentEnv.ps1" not in text or "uv" not in text:
        return ContractCheck(
            "launcher",
            False,
            "launcher present but missing expected runtime isolation or uv invocation",
        )
    return ContractCheck(
        "launcher",
        True,
        "launcher routes CrewAI through the vault-contained runtime helper",
    )


def _check_config_surfaces(root: Path) -> ContractCheck:
    agents_path = root / "src" / "idaho_vault" / "config" / "agents.yaml"
    tasks_path = root / "src" / "idaho_vault" / "config" / "tasks.yaml"
    if not agents_path.exists() or not tasks_path.exists():
        return ContractCheck(
            "config-surfaces",
            False,
            "`agents.yaml` or `tasks.yaml` missing from `src/idaho_vault/config/`",
        )

    agents_text = agents_path.read_text(encoding="utf-8")
    tasks_text = tasks_path.read_text(encoding="utf-8")
    ok = "bootstrap_validator:" in agents_text and "deployment_probe:" in tasks_text
    return ContractCheck(
        "config-surfaces",
        ok,
        (
            "bootstrap config surfaces present"
            if ok
            else "bootstrap config files present but expected keys were not found"
        ),
    )


def _check_runtime_surface(root: Path) -> ContractCheck:
    path = root / "src" / "idaho_vault" / "runtime.py"
    if not path.exists():
        return ContractCheck("runtime-surface", False, "`src/idaho_vault/runtime.py` missing")

    text = path.read_text(encoding="utf-8")
    expected = ("APPDATA", "LOCALAPPDATA", "HOME", "USERPROFILE", ".agent-home")
    missing = [token for token in expected if token not in text]
    if missing:
        return ContractCheck(
            "runtime-surface",
            False,
            f"runtime containment missing markers: {', '.join(missing)}",
        )
    return ContractCheck(
        "runtime-surface",
        True,
        "runtime containment maps CrewAI state into vault-local paths",
    )


def _check_python_version(root: Path) -> ContractCheck:
    path = root / ".python-version"
    if not path.exists():
        return ContractCheck("python-version", False, "`.python-version` missing")

    version = path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"3\.(1[0-3])(?:\.\d+)?", version):
        return ContractCheck(
            "python-version",
            False,
            f"unexpected Python version marker `{version}`",
        )
    return ContractCheck(
        "python-version",
        True,
        f"repo Python marker present: `{version}`",
    )


def build_contract_report() -> ContractReport:
    """Inspect the repository and return a bootstrap contract report."""
    root = _project_root()
    checks = (
        _check_pyproject(root),
        _check_lockfile(root),
        _check_manifest(root),
        _check_training_doctrine(root),
        _check_launcher(root),
        _check_config_surfaces(root),
        _check_runtime_surface(root),
        _check_python_version(root),
        _check_exists(root, "src/idaho_vault/crew.py", "bootstrap-crew"),
        _check_exists(root, ".crewai/MANIFEST.md", "manifest-doc"),
    )
    return ContractReport(
        ok=all(check.ok for check in checks),
        checks=checks,
    )
