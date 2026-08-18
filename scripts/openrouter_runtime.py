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
AGENT_COMMANDS = {
    "codex": "codex",
    "claude": "claude",
}


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path.resolve()


def approved_agent(agent: str) -> str:
    """Map parsed input to one of the fixed agent literals used at execution boundaries."""
    if agent == "codex":
        return "codex"
    if agent == "claude":
        return "claude"
    supported = ", ".join(sorted(AGENT_COMMANDS))
    raise SystemExit(f"Unsupported OpenRouter agent '{agent}'. Supported agents: {supported}.")


def agent_command(agent: str) -> str:
    """Return the sole approved executable for a supported OpenRouter agent."""
    return AGENT_COMMANDS[approved_agent(agent)]


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
        raise SystemExit("1Password CLI 'op' is not installed or not on PATH.")


def ensure_op_signed_in() -> None:
    try:
        result = subprocess.run(
            ["op", "whoami"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=15,
        )
    except subprocess.TimeoutExpired as exc:
        raise SystemExit("1Password CLI 'op whoami' timed out after 15s.") from exc
    except OSError as exc:
        raise SystemExit(f"1Password CLI 'op whoami' could not run: {exc}") from exc
    if result.returncode != 0:
        raise SystemExit(
            "1Password CLI is not signed in. Run 'op signin' or unlock desktop integration first."
        )


def parse_env_content(content: str) -> dict[str, str]:
    """Parse non-empty KEY=value lines without evaluating shell syntax."""
    values: dict[str, str] = {}
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        if key.strip():
            values[key.strip()] = value.strip()
    return values


def ensure_env_file(agent: str) -> Path:
    required_keys = {
        "codex": ["OPENAI_API_KEY", "OPENAI_BASE_URL"],
        "claude": ["ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY"],
    }[agent]

    needs_refresh = not ENV_FILE.exists()
    if not needs_refresh:
        populated = parse_env_content(ENV_FILE.read_text(encoding="utf-8"))
        needs_refresh = any(not populated.get(key) for key in required_keys)

    if needs_refresh:
        try:
            subprocess.run([sys.executable, str(RESOLVER)], check=True, timeout=60)
        except subprocess.TimeoutExpired as exc:
            raise SystemExit(f"{RESOLVER.name} timed out after 60s.") from exc
        except subprocess.CalledProcessError as exc:
            raise SystemExit(f"{RESOLVER.name} failed (exit {exc.returncode}).") from exc
        except OSError as exc:
            raise SystemExit(f"{RESOLVER.name} could not run: {exc}") from exc

    return ENV_FILE


def exec_agent(agent: str, args: list[str]) -> int:
    selected_agent = approved_agent(agent)
    approved_agent_args(args)
    env = apply_runtime_env(selected_agent)
    command = ["codex"] if selected_agent == "codex" else ["claude"]
    try:
        os.execvpe(command[0], command, env)
    except FileNotFoundError as exc:
        raise SystemExit(f"Could not find approved '{command[0]}' executable on PATH.") from exc
    return 0


def approved_agent_args(args: list[str]) -> None:
    """Reject all caller-provided command arguments at the execution boundary."""
    if args:
        raise SystemExit("OpenRouter launchers do not accept command arguments.")


def launch_agent(agent: str, args: list[str]) -> int:
    selected_agent = approved_agent(agent)
    approved_agent_args(args)

    ensure_op_available()
    ensure_op_signed_in()
    env_file = ensure_env_file(selected_agent)

    command = [
        "op",
        "run",
        f"--env-file={env_file}",
        "--",
        sys.executable,
        str(Path(__file__).resolve()),
        "--exec",
        selected_agent,
    ]
    try:
        os.execvpe("op", command, os.environ.copy())
    except FileNotFoundError as exc:
        raise SystemExit("1Password CLI 'op' is not installed or not on PATH.") from exc
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--exec", dest="exec_mode", action="store_true")
    parser.add_argument("agent")
    parser.add_argument("args", nargs="*")
    parsed = parser.parse_args()

    if parsed.exec_mode:
        return exec_agent(parsed.agent, parsed.args)

    return launch_agent(parsed.agent, parsed.args)


if __name__ == "__main__":
    raise SystemExit(main())
