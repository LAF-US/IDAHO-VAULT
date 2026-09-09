from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = REPO_ROOT / ".op" / "openrouter.env"
RESOLVER_PY = REPO_ROOT / "!" / "resolve_openrouter_secret.py"
RESOLVER_PS1 = REPO_ROOT / "!" / "resolve-openrouter-secret.ps1"
RUNTIME_SCRIPT = REPO_ROOT / "scripts" / "openrouter_runtime.py"
LAUNCHER_PATHS = (
    REPO_ROOT / "scripts" / "Start-CodexOpenRouter.ps1",
    REPO_ROOT / "scripts" / "Start-ClaudeOpenRouter.ps1",
    REPO_ROOT / "!" / "launch-codex-openrouter.cmd",
    REPO_ROOT / "!" / "launch-claude-openrouter.cmd",
)


@dataclass(frozen=True)
class ValidationResult:
    name: str
    ok: bool
    severity: str
    detail: str


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def _check_path_exists(name: str, path: Path) -> ValidationResult:
    return ValidationResult(
        name=name,
        ok=path.exists(),
        severity="error",
        detail=f"{path.relative_to(REPO_ROOT)} {'present' if path.exists() else 'missing'}",
    )


def _check_op_status() -> ValidationResult:
    if shutil.which("op") is None:
        return ValidationResult(
            name="1Password CLI",
            ok=False,
            severity="warn",
            detail="`op` is not on PATH; local fallback depends on .op/openrouter.env.",
        )
    result = subprocess.run(
        ["op", "whoami"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode == 0:
        return ValidationResult(
            name="1Password CLI",
            ok=True,
            severity="info",
            detail="`op whoami` succeeded.",
        )
    return ValidationResult(
        name="1Password CLI",
        ok=False,
        severity="warn",
        detail="`op` is installed but not signed in; env-file fallback is required.",
    )


def validate_openrouter_env() -> list[ValidationResult]:
    results = [
        _check_path_exists("Resolver (Python)", RESOLVER_PY),
        _check_path_exists("Resolver (PowerShell)", RESOLVER_PS1),
        _check_path_exists("Runtime launcher", RUNTIME_SCRIPT),
    ]
    results.extend(_check_path_exists(f"Launcher `{path.name}`", path) for path in LAUNCHER_PATHS)
    results.append(_check_path_exists("OpenRouter env file", ENV_FILE))
    results.append(_check_op_status())

    env_values = parse_env_file(ENV_FILE)
    required_keys = {
        "OPENROUTER_API_KEY": "OpenRouter API key ref/value",
        "OPENAI_API_KEY": "OpenAI compatibility key ref/value",
        "OPENAI_BASE_URL": "OpenAI compatibility base URL",
        "ANTHROPIC_AUTH_TOKEN": "Anthropic compatibility auth token ref/value",
        "ANTHROPIC_BASE_URL": "Anthropic compatibility base URL",
        "ANTHROPIC_API_KEY": "Anthropic compatibility API key ref/value",
    }

    for key, description in required_keys.items():
        value = env_values.get(key, "")
        results.append(
            ValidationResult(
                name=f"Env key `{key}`",
                ok=bool(value),
                severity="error",
                detail=f"{description} {'present' if value else 'missing'}",
            )
        )

    if env_values:
        openai_base_url = env_values.get("OPENAI_BASE_URL")
        results.append(
            ValidationResult(
                name="OpenAI base URL",
                ok=openai_base_url == "https://openrouter.ai/api/v1",
                severity="error",
                detail=f"expected `https://openrouter.ai/api/v1`, got `{openai_base_url or '<missing>'}`",
            )
        )
        anthropic_base_url = env_values.get("ANTHROPIC_BASE_URL")
        results.append(
            ValidationResult(
                name="Anthropic base URL",
                ok=anthropic_base_url == "https://openrouter.ai/api",
                severity="error",
                detail=f"expected `https://openrouter.ai/api`, got `{anthropic_base_url or '<missing>'}`",
            )
        )

        for key in ("OPENROUTER_API_KEY", "OPENAI_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_API_KEY"):
            value = env_values.get(key, "")
            if value.startswith("sk-"):
                results.append(
                    ValidationResult(
                        name=f"Secret style `{key}`",
                        ok=False,
                        severity="warn",
                        detail="plaintext key detected; prefer `op://...` references for local env files.",
                    )
                )
            elif value.startswith("op://"):
                results.append(
                    ValidationResult(
                        name=f"Secret style `{key}`",
                        ok=True,
                        severity="info",
                        detail="uses a 1Password item reference.",
                    )
                )

    return results


def render_markdown(results: list[ValidationResult]) -> str:
    lines = [
        "# OpenRouter Runtime Validation",
        "",
        "| Check | Status | Severity | Detail |",
        "| --- | --- | --- | --- |",
    ]
    for result in results:
        status = "OK" if result.ok else "FAIL"
        lines.append(f"| {result.name} | `{status}` | `{result.severity}` | {result.detail} |")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the local OpenRouter runtime contract.")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()

    results = validate_openrouter_env()
    if args.format == "json":
        print(json.dumps([asdict(result) for result in results], indent=2))
    else:
        print(render_markdown(results))

    hard_failures = [result for result in results if result.severity == "error" and not result.ok]
    return 0 if not hard_failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
