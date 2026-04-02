#!/usr/bin/env bash
# ============================================================================
# AGENT PROTOCOL - IDAHO-VAULT
# ============================================================================
#
# Local bootstrap entrypoint for agent invocation in IDAHO-VAULT.
# Facts come from !/agents.json, which is generated from swarm.json.
#
# Usage:
#   source !/agent.sh <agent>
#   source !/agent.sh --describe <agent>
#   source !/agent.sh --validate <agent>
#
# ============================================================================

set -euo pipefail

VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BOOTSTRAP_INDEX="$VAULT_ROOT/!/agents.json"


resolve_python() {
  if command -v python3 >/dev/null 2>&1; then
    echo "python3"
    return 0
  fi

  if command -v python >/dev/null 2>&1; then
    echo "python"
    return 0
  fi

  echo "[error] Python is required to read $BOOTSTRAP_INDEX." >&2
  return 1
}


PYTHON_BIN="$(resolve_python)"


bootstrap_query() {
  local mode="$1"
  local agent="${2:-}"

  "$PYTHON_BIN" - "$BOOTSTRAP_INDEX" "$mode" "$agent" <<'PY'
import json
import shlex
import sys
from pathlib import Path

index_path = Path(sys.argv[1])
mode = sys.argv[2]
agent_name = sys.argv[3] if len(sys.argv) > 3 else ""

data = json.loads(index_path.read_text(encoding="utf-8"))
agents = data.get("agents", {})

if mode == "list":
    print("\n".join(sorted(agents)))
    raise SystemExit(0)

if mode == "roles":
    roles = data.get("control_plane", {}).get("system_roles", {})
    for key in sorted(roles):
        print(f"{key}={roles[key]}")
    raise SystemExit(0)

record = agents.get(agent_name)
if record is None:
    raise SystemExit(2)

if mode == "env":
    assignments = {
        "AGENT_NAME": agent_name,
        "AGENT_ID": record["id"],
        "AGENT_DISPLAY_NAME": record["name"],
        "AGENT_VENDOR": record["vendor"],
        "AGENT_DOTFOLDER": record.get("dotfolder") or "",
        "AGENT_TIER": record["capability_tier"],
        "AGENT_INSTRUCTIONS": record["instructions_file"],
        "BOOTSTRAP_SUPPORTED": str(record["supports_local_bootstrap"]).lower(),
        "GIT_AUTHOR_NAME": record["git_identity"]["name"],
        "GIT_AUTHOR_EMAIL": record["git_identity"]["email"],
        "GIT_AUTHOR_SUFFIX": record["git_identity"]["suffix"],
    }

    for key, value in assignments.items():
        print(f"{key}={shlex.quote(str(value))}")

    for key, value in {
        "REQUIRED_CONTEXT": record["context"]["required"],
        "OPTIONAL_CONTEXT": record["context"].get("optional", []),
    }.items():
        rendered = " ".join(shlex.quote(str(item)) for item in value)
        print(f"{key}=({rendered})")
    raise SystemExit(0)

if mode == "json":
    print(json.dumps(record, indent=2))
    raise SystemExit(0)

raise SystemExit(1)
PY
}


print_known_agents() {
  bootstrap_query list | sed 's/^/  - /'
}


resolve_repo_path() {
  local rel_path="$1"
  echo "$VAULT_ROOT/$rel_path"
}


load_agent_record() {
  local agent="$1"

  if ! eval "$(bootstrap_query env "$agent")"; then
    echo "[error] Unknown agent: $agent" >&2
    echo ""
    echo "Known agents:"
    print_known_agents
    return 1
  fi

  export AGENT_NAME
  export AGENT_ID
  export AGENT_DISPLAY_NAME
  export AGENT_VENDOR
  export AGENT_DOTFOLDER
  export AGENT_TIER
  export AGENT_INSTRUCTIONS
  export BOOTSTRAP_SUPPORTED
  export GIT_AUTHOR_NAME
  export GIT_AUTHOR_EMAIL
  export GIT_AUTHOR_SUFFIX
}


print_context_status() {
  local label="$1"
  shift

  echo "$label:"
  for rel_path in "$@"; do
    local abs_path
    abs_path="$(resolve_repo_path "$rel_path")"
    if [ -f "$abs_path" ]; then
      echo "  [ok] $rel_path"
    else
      echo "  [missing] $rel_path"
    fi
  done
}


describe_agent() {
  local agent="$1"

  if ! load_agent_record "$agent"; then
    return 1
  fi

  echo "AGENT PROTOCOL - DESCRIBE"
  echo "Agent: $AGENT_NAME"
  echo "Registry id: $AGENT_ID"
  echo "Display name: $AGENT_DISPLAY_NAME"
  echo "Vendor: $AGENT_VENDOR"
  echo "Tier: $AGENT_TIER"
  echo "Instructions: $AGENT_INSTRUCTIONS"
  echo "Dotfolder: ${AGENT_DOTFOLDER:-<none>}"
  echo "Git identity: $GIT_AUTHOR_NAME <$GIT_AUTHOR_EMAIL> ($GIT_AUTHOR_SUFFIX)"
  echo "Bootstrap supported: $BOOTSTRAP_SUPPORTED"
  echo ""
  print_context_status "Required context" "${REQUIRED_CONTEXT[@]}"
  echo ""
  print_context_status "Optional context" "${OPTIONAL_CONTEXT[@]}"
  echo ""
  echo "Control plane roles:"
  bootstrap_query roles | sed 's/^/  - /'
}


validate_agent() {
  local agent="$1"
  local failed=0
  local instructions_abs

  if ! load_agent_record "$agent"; then
    return 1
  fi

  instructions_abs="$(resolve_repo_path "$AGENT_INSTRUCTIONS")"
  if [ -f "$instructions_abs" ]; then
    echo "[ok] instructions: $AGENT_INSTRUCTIONS"
  else
    echo "[missing] instructions: $AGENT_INSTRUCTIONS"
    failed=1
  fi

  for rel_path in "${REQUIRED_CONTEXT[@]}"; do
    if [ -f "$(resolve_repo_path "$rel_path")" ]; then
      echo "[ok] required: $rel_path"
    else
      echo "[missing] required: $rel_path"
      failed=1
    fi
  done

  for rel_path in "${OPTIONAL_CONTEXT[@]}"; do
    if [ -f "$(resolve_repo_path "$rel_path")" ]; then
      echo "[ok] optional: $rel_path"
    else
      echo "[warn] optional not present: $rel_path"
    fi
  done

  if [ "$failed" -ne 0 ]; then
    echo "[error] Validation failed for $agent."
    return 1
  fi

  echo "[ok] Validation passed for $agent."
}


authenticate_1password() {
  if ! command -v op >/dev/null 2>&1; then
    echo "[warn] 1Password CLI not found. See .op/SETUP.md"
    return 1
  fi

  if [ -z "${OP_SERVICE_ACCOUNT_TOKEN:-}" ] && ! op whoami >/dev/null 2>&1; then
    echo "[warn] 1Password is not authenticated. Run: op signin"
    return 1
  fi

  echo "[ok] 1Password authenticated"
}


load_agent_instructions() {
  local instructions_abs

  instructions_abs="$(resolve_repo_path "$AGENT_INSTRUCTIONS")"
  if [ ! -f "$instructions_abs" ]; then
    echo "[error] Instructions not found: $AGENT_INSTRUCTIONS"
    return 1
  fi

  export AGENT_INSTRUCTIONS="$instructions_abs"
  echo "[ok] Instructions loaded: $AGENT_INSTRUCTIONS"
}


load_vault_context() {
  local failed=0

  for rel_path in "${REQUIRED_CONTEXT[@]}"; do
    if [ ! -f "$(resolve_repo_path "$rel_path")" ]; then
      echo "[error] Required context missing: $rel_path"
      failed=1
    fi
  done

  if [ "$failed" -ne 0 ]; then
    return 1
  fi

  export VAULT_README="$(resolve_repo_path '!/README.md')"
  export VAULT_CONSTITUTION="$(resolve_repo_path '!/CONSTITUTION.md')"
  export VAULT_AGENTS="$(resolve_repo_path '!/AGENTS.md')"
  export VAULT_DECISIONS="$(resolve_repo_path '!/DECISIONS.md')"
  export VAULT_CONVENTIONS="$(resolve_repo_path '!/VAULT-CONVENTIONS.md')"

  if [ -f "$(resolve_repo_path '!/LEVELSET.md')" ]; then
    export VAULT_LEVELSET="$(resolve_repo_path '!/LEVELSET.md')"
    echo "[ok] Optional advisory context loaded: !/LEVELSET.md"
  else
    export VAULT_LEVELSET=""
    echo "[warn] Optional advisory context not present: !/LEVELSET.md"
  fi

  echo "[ok] Vault context loaded: README, CONSTITUTION, AGENTS, DECISIONS, VAULT-CONVENTIONS"
}


configure_git_signing() {
  git config user.name "$GIT_AUTHOR_NAME" >/dev/null 2>&1 || true
  git config user.email "$GIT_AUTHOR_EMAIL" >/dev/null 2>&1 || true
  git config gpg.format ssh >/dev/null 2>&1 || true

  echo "[ok] Git identity configured: $GIT_AUTHOR_NAME ($GIT_AUTHOR_SUFFIX)"
}


emit_checkpoint() {
  local agent="$1"
  local phase="$2"
  local checkpoint_path="$VAULT_ROOT/!/agent-protocol.log"
  local timestamp

  timestamp="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"

  cat >> "$checkpoint_path" <<EOF
{
  "timestamp": "$timestamp",
  "agent": "$agent",
  "phase": "$phase",
  "vault_root": "$VAULT_ROOT",
  "git_author": "$(git config user.name)",
  "auth_status": "authenticated"
}
EOF

  echo "[ok] Checkpoint logged: $phase"
}


usage() {
  echo "AGENT PROTOCOL - IDAHO-VAULT"
  echo ""
  echo "Usage:"
  echo "  source !/agent.sh <agent>"
  echo "  source !/agent.sh --describe <agent>"
  echo "  source !/agent.sh --validate <agent>"
  echo ""
  echo "Known agents:"
  print_known_agents
}


main() {
  local first_arg="${1:-}"

  case "$first_arg" in
    ""|-h|--help)
      usage
      return 1
      ;;
    --describe)
      if [ -z "${2:-}" ]; then
        usage
        return 1
      fi
      describe_agent "$2"
      return $?
      ;;
    --validate)
      if [ -z "${2:-}" ]; then
        usage
        return 1
      fi
      validate_agent "$2"
      return $?
      ;;
  esac

  if ! load_agent_record "$first_arg"; then
    return 1
  fi

  echo ""
  echo "AGENT PROTOCOL - IDAHO-VAULT"
  echo "===================================="
  echo ""

  if ! authenticate_1password; then
    echo "[warn] Continuing without secrets."
  fi
  echo ""

  echo "[ok] Agent identified: $AGENT_NAME"
  echo "[ok] Authorization granted: $AGENT_TIER"
  echo ""

  if ! load_agent_instructions; then
    return 1
  fi

  if ! load_vault_context; then
    echo "[error] Vault context incomplete."
    return 1
  fi
  echo ""

  configure_git_signing
  echo ""

  emit_checkpoint "$AGENT_NAME" "init"
  echo ""

  echo "[ok] AGENT PROTOCOL INITIALIZED"
  echo "===================================="
  echo ""
  echo "Ready: $AGENT_NAME (Tier: $AGENT_TIER)"
  echo "Instructions: $AGENT_INSTRUCTIONS"
  echo "Signing suffix: $GIT_AUTHOR_SUFFIX"
  echo "Next: read your instructions, consult the loaded vault context, then proceed."
  echo ""
}


if [[ "${BASH_SOURCE[0]}" == "${0}" ]] || [ -n "${1:-}" ]; then
  main "$@"
fi
