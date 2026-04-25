from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = REPO_ROOT / ".op" / "openrouter.env"
RESOLVER = REPO_ROOT / "!" / "resolve_openrouter_secret.py"


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path.resolve()


def apply_runtime_env(agent: str) -> dict[str, str]:
    env = os.environ.copy()

    shared_paths = {
        "TMP": REPO_ROOT / ".tmp",
        "TEMP": REPO_ROOT / ".tmp",
        "TMPDIR": REPO_ROOT / ".tmp",
        "UV_CACHE_DIR": REPO_ROOT / ".uv-cache",
        "PIP_CACHE_DIR": REPO_ROOT / ".pip-cache",
        "NPM_CONFIG_CACHE": REPO_ROOT / ".npm-cache",
        "XDG_CACHE_HOME": REPO_ROOT / ".cache",
        "XDG_STATE_HOME": REPO_ROOT / ".state",
        "PYTHONPYCACHEPREFIX": REPO_ROOT / ".pycache",
    }

    for name, path in shared_paths.items():
        env[name] = str(ensure_dir(path))

    agent_home_root = ensure_dir(REPO_ROOT / ".agent-home")

    if agent == "codex":
        env["CODEX_HOME"] = str(ensure_dir(agent_home_root / "codex"))
    elif agent == "claude":
        env["APPDATA"] = str(ensure_dir(agent_home_root / "claude" / "AppData" / "Roaming"))
        env["LOCALAPPDATA"] = str(ensure_dir(agent_home_root / "claude" / "AppData" / "Local"))

    return env


def ensure_op_available() -> None:
    if shutil.which("op") is None:
        raise SystemExit(
            "1Password CLI 'op' is not installed or not on PATH.\n"
            "If .op/openrouter.env exists, you can use the env file directly."
        )


def ensure_op_signed_in() -> None:
    result = subprocess.run(
        ["op", "whoami"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(
            "1Password CLI is not signed in. Run 'op signin' or unlock desktop integration.\n"
            "If .op/openrouter.env exists, you can use the env file directly."
        )


def ensure_env_file(agent: str) -> Path:
    required_keys = {
        "codex": ["OPENAI_API_KEY", "OPENAI_BASE_URL"],
        "claude": ["ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY"],
    }[agent]

    needs_refresh = not ENV_FILE.exists()
    if not needs_refresh:
        content = ENV_FILE.read_text(encoding="utf-8")
        needs_refresh = any(f"{key}=" not in content for key in required_keys)

    if needs_refresh:
        if shutil.which("op") is None:
            raise SystemExit(
                f"Env file missing or incomplete and 1Password CLI not available.\n"
                f"Please create {ENV_FILE} with your OpenRouter API key."
            )
        subprocess.run([sys.executable, str(RESOLVER)], check=True)

    return ENV_FILE


def exec_agent(agent: str, cli_name: str, args: list[str]) -> int:
    env = apply_runtime_env(agent)
    resolved_cli = shutil.which(cli_name, path=env.get("PATH"))
    if resolved_cli is None:
        raise SystemExit(f"Could not find '{cli_name}' on PATH.")

    result = subprocess.run([resolved_cli, *args], env=env, check=False)
    return result.returncode


def is_help_request(args: list[str]) -> bool:
    return any(arg in {"-h", "--help"} for arg in args)


def launch_agent(agent: str, cli_name: str, args: list[str]) -> int:
    if agent not in {"codex", "claude"}:
        raise SystemExit(f"Unsupported OpenRouter agent: {agent}")

    if is_help_request(args):
        return exec_agent(agent, cli_name, args)

    env_file = ensure_env_file(agent)

    if shutil.which("op") is not None:
        result = subprocess.run(["op", "whoami"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        if result.returncode == 0:
            command = [
                "op",
                "run",
                f"--env-file={env_file}",
                "--",
                sys.executable,
                str(Path(__file__).resolve()),
                "--exec",
                agent,
                cli_name,
                *args,
            ]
            result = subprocess.run(command, check=False)
            return result.returncode

    return exec_agent(agent, cli_name, args)


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--exec", dest="exec_mode", action="store_true")
    parser.add_argument("agent")
    parser.add_argument("cli_name")
    parser.add_argument("args", nargs="*")
    parsed = parser.parse_args()

    if parsed.exec_mode:
        return exec_agent(parsed.agent, parsed.cli_name, parsed.args)

    return launch_agent(parsed.agent, parsed.cli_name, parsed.args)


if __name__ == "__main__":
    raise SystemExit(main())
