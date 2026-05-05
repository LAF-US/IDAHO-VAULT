from __future__ import annotations

import argparse
import importlib
import json
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from idaho_vault.bootstrap_contract import build_contract_report_for_root


DEFAULT_REPORT_PATH = REPO_ROOT / "!" / "CREWAI" / "BOOTSTRAP-COMPATIBILITY.md"


@dataclass(frozen=True)
class BootstrapValidation:
    name: str
    ok: bool
    severity: str
    detail: str


def _path_exists(name: str, relpath: str, *, severity: str = "error") -> BootstrapValidation:
    path = REPO_ROOT / relpath
    return BootstrapValidation(
        name=name,
        ok=path.exists(),
        severity=severity,
        detail=f"`{relpath}` {'present' if path.exists() else 'missing'}",
    )


def _check_uv() -> BootstrapValidation:
    uv_path = shutil.which("uv")
    return BootstrapValidation(
        name="uv CLI",
        ok=uv_path is not None,
        severity="warn",
        detail=(f"`uv` available at `{uv_path}`" if uv_path else "`uv` not on PATH; repo runners remain checkout-only."),
    )


def _check_crewai_import() -> BootstrapValidation:
    try:
        importlib.import_module("crewai")
    except Exception as exc:  # pragma: no cover - exact import failure varies by machine
        return BootstrapValidation(
            name="CrewAI import",
            ok=False,
            severity="warn",
            detail=f"`import crewai` failed: {exc}",
        )
    return BootstrapValidation(
        name="CrewAI import",
        ok=True,
        severity="info",
        detail="`import crewai` succeeded in the current environment.",
    )


def _check_repo_entrypoint_import() -> BootstrapValidation:
    try:
        importlib.import_module("idaho_vault.main")
    except Exception as exc:
        return BootstrapValidation(
            name="Repo entrypoint import",
            ok=False,
            severity="error",
            detail=f"`import idaho_vault.main` failed: {exc}",
        )
    return BootstrapValidation(
        name="Repo entrypoint import",
        ok=True,
        severity="info",
        detail="`idaho_vault.main` imports from the checkout-bound `src/` package.",
    )


def _check_install_script_truth() -> BootstrapValidation:
    path = REPO_ROOT / "install_dependencies.sh"
    if not path.exists():
        return BootstrapValidation(
            name="Legacy installer helper",
            ok=False,
            severity="warn",
            detail="`install_dependencies.sh` missing.",
        )

    text = path.read_text(encoding="utf-8")
    markers = (
        "Historical helper",
        "validate_bootstrap.py",
        "requirements.txt",
        "uv.lock",
    )
    missing = [marker for marker in markers if marker not in text]
    return BootstrapValidation(
        name="Legacy installer helper",
        ok=not missing,
        severity="warn",
        detail=(
            "`install_dependencies.sh` clearly advertises its helper-only posture."
            if not missing
            else f"`install_dependencies.sh` is missing expected truthfulness markers: {', '.join(missing)}"
        ),
    )


def validate_bootstrap() -> tuple[dict[str, object], list[BootstrapValidation]]:
    contract = build_contract_report_for_root(REPO_ROOT)
    validations = [
        _path_exists("Requirements lock surface", "requirements.txt"),
        _path_exists("uv lock surface", "uv.lock"),
        _path_exists("Vault launcher", "scripts/Start-CrewAIVault.ps1"),
        _path_exists("Runtime containment helper", "scripts/Use-VaultAgentEnv.ps1"),
        _path_exists("CrewAI doctrine", ".crewai/MANIFEST.md"),
        _path_exists("Bootstrap report lane", "!/CREWAI", severity="warn"),
        _check_uv(),
        _check_crewai_import(),
        _check_repo_entrypoint_import(),
        _check_install_script_truth(),
    ]
    return contract.to_dict(), validations


def render_markdown(contract: dict[str, object], validations: list[BootstrapValidation]) -> str:
    lines = [
        "# Bootstrap Compatibility Report",
        "",
        "This is the canonical Round 2 bootstrap/dependency compatibility snapshot.",
        "",
        "## Bootstrap Contract",
        "",
        f"- Overall status: `{'PASS' if contract['ok'] else 'FAIL'}`",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for check in contract["checks"]:
        status = "PASS" if check["ok"] else "FAIL"
        lines.append(f"| `{check['name']}` | `{status}` | {check['detail']} |")

    lines.extend(
        [
            "",
            "## Runtime And Dependency Notes",
            "",
            "| Check | Status | Severity | Detail |",
            "| --- | --- | --- | --- |",
        ]
    )
    for validation in validations:
        status = "OK" if validation.ok else "FAIL"
        lines.append(
            f"| {validation.name} | `{status}` | `{validation.severity}` | {validation.detail} |"
        )

    lines.extend(
        [
            "",
            "## Scope Notes",
            "",
            "- The canonical CrewAI bootstrap path remains checkout-bound and vault-local.",
            "- `install_dependencies.sh` is a helper/reference surface, not the canonical truth surface.",
            "- The live bootstrap contract is defined by `src/idaho_vault/bootstrap_contract.py`, `.crewai/MANIFEST.md`, `uv.lock`, and the vault launchers.",
        ]
    )
    return "\n".join(lines)


def write_report(markdown: str, path: Path = DEFAULT_REPORT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the local CrewAI bootstrap and dependency contract.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument(
        "--write-report",
        action="store_true",
        help="Write the markdown report to !/CREWAI/BOOTSTRAP-COMPATIBILITY.md.",
    )
    args = parser.parse_args()

    contract, validations = validate_bootstrap()
    if args.format == "json":
        print(
            json.dumps(
                {
                    "contract": contract,
                    "validations": [asdict(validation) for validation in validations],
                },
                indent=2,
            )
        )
    else:
        markdown = render_markdown(contract, validations)
        print(markdown)
        if args.write_report:
            write_report(markdown)

    hard_failures = [check for check in contract["checks"] if not check["ok"]]
    hard_failures.extend(validation for validation in validations if validation.severity == "error" and not validation.ok)
    return 0 if not hard_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
