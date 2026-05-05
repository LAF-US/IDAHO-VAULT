from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import health_monitor
import validate_openrouter


REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MATRIX_PATH = REPO_ROOT / "!" / "INTEGRATIONS" / "COMPATIBILITY.md"
LOCAL_MESH_CONFIGS = (
    REPO_ROOT / ".openclaw-local-only.yml",
    REPO_ROOT / ".openclaw-local-mesh.yml",
)
DOCUMENTED_SCRIPT_PATHS = (
    REPO_ROOT / "scripts" / "health_monitor.py",
    REPO_ROOT / "scripts" / "validate_openrouter.py",
    REPO_ROOT / "scripts" / "validate_services.py",
)


@dataclass(frozen=True)
class ServiceValidation:
    name: str
    ok: bool
    detail: str


def validate_documented_surfaces() -> list[ServiceValidation]:
    results: list[ServiceValidation] = []
    for path in LOCAL_MESH_CONFIGS:
        results.append(
            ServiceValidation(
                name=f"OpenClaw config `{path.name}`",
                ok=path.exists(),
                detail=f"{path.relative_to(REPO_ROOT)} {'present' if path.exists() else 'missing'}",
            )
        )
    for path in DOCUMENTED_SCRIPT_PATHS:
        results.append(
            ServiceValidation(
                name=f"Documented script `{path.name}`",
                ok=path.exists(),
                detail=f"{path.relative_to(REPO_ROOT)} {'present' if path.exists() else 'missing'}",
            )
        )
    return results


def build_compatibility_markdown(
    local_results: list[ServiceValidation],
    openrouter_results: list[validate_openrouter.ValidationResult],
) -> str:
    lines = [
        "# Runtime Compatibility Matrix",
        "",
        "This is the canonical Round 1 runtime/provider compatibility snapshot.",
        "",
        "## Local Runtime Surfaces",
        "",
        "| Surface | Status | Detail |",
        "| --- | --- | --- |",
    ]
    for result in local_results:
        status = "OK" if result.ok else "FAIL"
        lines.append(f"| {result.name} | `{status}` | {result.detail} |")

    lines.extend(
        [
            "",
            "## OpenRouter Contract",
            "",
            "| Check | Status | Severity | Detail |",
            "| --- | --- | --- | --- |",
        ]
    )
    for result in openrouter_results:
        status = "OK" if result.ok else "FAIL"
        lines.append(f"| {result.name} | `{status}` | `{result.severity}` | {result.detail} |")

    lines.extend(
        [
            "",
            "## Scope Notes",
            "",
            "- `op://...` references are the preferred local secret format for `.op/openrouter.env`.",
            "- 1Password SSH agent guidance is separate and limited to local developer-machine SSH and git workflows.",
            "- Network/provider reachability is checked separately by `scripts/health_monitor.py`.",
        ]
    )
    return "\n".join(lines)


def write_matrix(markdown: str, path: Path = DEFAULT_MATRIX_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(markdown.rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the runtime/provider/OpenClaw documentation surfaces.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument(
        "--write-matrix",
        action="store_true",
        help="Write the compatibility snapshot to !/INTEGRATIONS/COMPATIBILITY.md.",
    )
    parser.add_argument(
        "--include-health",
        action="store_true",
        help="Include external reachability checks from scripts/health_monitor.py.",
    )
    args = parser.parse_args()

    local_results = validate_documented_surfaces()
    openrouter_results = validate_openrouter.validate_openrouter_env()
    health_results = health_monitor.run_health_check() if args.include_health else []

    if args.format == "json":
        payload = {
            "local_results": [asdict(result) for result in local_results],
            "openrouter_results": [asdict(result) for result in openrouter_results],
            "health_results": [asdict(result) for result in health_results],
        }
        print(json.dumps(payload, indent=2))
    else:
        markdown = build_compatibility_markdown(local_results, openrouter_results)
        print(markdown)
        if health_results:
            print("\n---\n")
            print(health_monitor.render_markdown(health_results))
        if args.write_matrix:
            write_matrix(markdown)

    failed_local = [result for result in local_results if not result.ok]
    failed_openrouter = [result for result in openrouter_results if result.severity == "error" and not result.ok]
    failed_health = [result for result in health_results if not result.ok]
    return 0 if not (failed_local or failed_openrouter or failed_health) else 1


if __name__ == "__main__":
    raise SystemExit(main())
