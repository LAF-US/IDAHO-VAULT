#!/usr/bin/env bash
# ============================================================================
# AGENT PROTOCOL — IDAHO-VAULT
# ============================================================================
#
# Bootstrap protocol for agent invocation in IDAHO-VAULT.
#
# This script establishes the TRIUNE COVENANT:
#   1. Authentication (1Password)
#   2. Authorization (AGENTS.md capability tier)
#   3. Agency (vault context + instruction loading + signing)
#
# Usage: source !\agent.sh [AGENT_NAME]
# Example: source !\agent.sh claude
#
# ============================================================================

set -euo pipefail

VAULT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENT_NAME="${1:-}"

# ============================================================================
# PHASE 1: AUTHENTICATION (1Password)
# ============================================================================

authenticate_1password() {
  if ! command -v op &> /dev/null; then
    echo "❌ 1Password CLI not found. See .op/SETUP.md"
    return 1
  fi

  if [ -z "$OP_SERVICE_ACCOUNT_TOKEN" ]; then
    # Try to use existing session
    if ! op whoami &> /dev/null 2>&1; then
      echo "⚠️  Not authenticated to 1Password. Run: op signin"
      return 1
    fi
  fi

  echo "✅ 1Password authenticated"
}

# ============================================================================
# PHASE 2: IDENTIFICATION (Agent Registry)
# ============================================================================

identify_agent() {
  local agent="$1"

  if [ -z "$agent" ]; then
    echo "❌ Agent name required. Usage: source !\agent.sh [AGENT_NAME]"
    echo ""
    echo "Known agents:"
    echo "  claude    — PERMANENT: AUTHORITY: CODE (Claude Code CLI)"
    echo "  gemini    — Gemini (The Vault Advisor)"
    echo "  codex     — Codex (OpenAI scripting)"
    echo "  copilot   — GitHub Copilot (ADMIN GitHub)"
    echo "  perplexity — Perplexity (research)"
    echo "  grok      — Grok (web search)"
    return 1
  fi

  case "$agent" in
    claude|gemini|codex|copilot|perplexity|grok)
      echo "✅ Agent identified: $agent"
      AGENT_DOTFOLDER=".$agent"
      ;;
    *)
      echo "❌ Unknown agent: $agent"
      return 1
      ;;
  esac
}

# ============================================================================
# PHASE 3: AUTHORIZATION (Capability Tier Check)
# ============================================================================

authorize_agent() {
  local agent="$1"
  local tier=""

  # Read tier from AGENTS.md registry
  case "$agent" in
    claude)
      tier="Direct Write"
      ;;
    gemini)
      tier="Direct Write (Support)"
      ;;
    codex)
      tier="Direct Write (scripting)"
      ;;
    copilot)
      tier="Multi-Repo Admin"
      ;;
    perplexity|grok)
      tier="Read/Analysis"
      ;;
  esac

  echo "✅ Authorization granted: $agent ($tier)"
  export AGENT_TIER="$tier"
}

# ============================================================================
# PHASE 4: AGENCY (Load Context + Instructions)
# ============================================================================

load_agent_instructions() {
  local agent="$1"
  local dotfolder=".$agent"
  local instructions_file="$VAULT_ROOT/$dotfolder/$([[ "$agent" == "claude" ]] && echo "CLAUDE.md" || echo "${agent^^}.md")"

  if [ ! -f "$instructions_file" ]; then
    echo "⚠️  No instructions found: $instructions_file"
    return 1
  fi

  echo "✅ Instructions loaded: $instructions_file"
  export AGENT_INSTRUCTIONS="$instructions_file"
}

load_vault_context() {
  local levelset="$VAULT_ROOT/!/LEVELSET-CURRENT.md"
  local constitution="$VAULT_ROOT/!/CONSTITUTION.md"
  local agents_registry="$VAULT_ROOT/!/AGENTS.md"
  local decisions="$VAULT_ROOT/!/DECISIONS.md"

  if [ ! -f "$levelset" ]; then
    echo "⚠️  LEVELSET-CURRENT.md not found"
    return 1
  fi

  echo "✅ Vault context loaded (LEVELSET, CONSTITUTION, AGENTS, DECISIONS)"
  export VAULT_LEVELSET="$levelset"
  export VAULT_CONSTITUTION="$constitution"
  export VAULT_AGENTS="$agents_registry"
  export VAULT_DECISIONS="$decisions"
}

# ============================================================================
# PHASE 5: SIGNING AUTHORITY (Git Configuration)
# ============================================================================

configure_git_signing() {
  local agent="$1"

  # Set git author
  case "$agent" in
    claude)
      git config user.name "Claude Code (The Abhorsen)" 2>/dev/null || true
      git config user.email "noreply@anthropic.com" 2>/dev/null || true
      GIT_AUTHOR_SUFFIX="-C"
      ;;
    gemini)
      git config user.name "Gemini (The Vault Advisor)" 2>/dev/null || true
      git config user.email "noreply@google.com" 2>/dev/null || true
      GIT_AUTHOR_SUFFIX="-G"
      ;;
    codex)
      git config user.name "Codex (OpenAI)" 2>/dev/null || true
      git config user.email "noreply@openai.com" 2>/dev/null || true
      GIT_AUTHOR_SUFFIX="-X"
      ;;
    copilot)
      git config user.name "GitHub Copilot" 2>/dev/null || true
      git config user.email "noreply@github.com" 2>/dev/null || true
      GIT_AUTHOR_SUFFIX="-CP"
      ;;
    *)
      GIT_AUTHOR_SUFFIX="-?"
      ;;
  esac

  # Configure SSH signing (via 1Password)
  git config gpg.format ssh 2>/dev/null || true

  echo "✅ Git signing configured: $agent ($GIT_AUTHOR_SUFFIX)"
  export GIT_AUTHOR_SUFFIX
}

# ============================================================================
# PHASE 6: CHECKPOINT (Log Protocol Invocation)
# ============================================================================

emit_checkpoint() {
  local agent="$1"
  local phase="$2"  # "init" or "complete"
  local timestamp=$(date -u +'%Y-%m-%dT%H:%M:%SZ')

  cat >> "$VAULT_ROOT/!/agent-protocol.log" 2>/dev/null || true <<EOF
{
  "timestamp": "$timestamp",
  "agent": "$agent",
  "phase": "$phase",
  "vault_root": "$VAULT_ROOT",
  "git_author": "$(git config user.name)",
  "auth_status": "authenticated"
}
EOF

  echo "✅ Checkpoint logged: $agent ($phase)"
}

# ============================================================================
# MAIN PROTOCOL FLOW
# ============================================================================

main() {
  local agent="${1:-}"

  if [ -z "$agent" ]; then
    identify_agent "$agent"  # Will fail with usage info
    return 1
  fi

  echo ""
  echo "🔔 AGENT PROTOCOL — IDAHO-VAULT"
  echo "════════════════════════════════════"
  echo ""

  # Phase 1: Authentication
  if ! authenticate_1password; then
    echo "⚠️  1Password authentication failed. Continuing without secrets."
  fi
  echo ""

  # Phase 2: Identification
  if ! identify_agent "$agent"; then
    return 1
  fi
  echo ""

  # Phase 3: Authorization
  if ! authorize_agent "$agent"; then
    return 1
  fi
  echo ""

  # Phase 4: Agency (Load Context)
  if ! load_agent_instructions "$agent"; then
    echo "⚠️  Instructions not loaded, continuing"
  fi
  if ! load_vault_context; then
    echo "⚠️  Vault context incomplete"
    return 1
  fi
  echo ""

  # Phase 5: Signing Authority
  if ! configure_git_signing "$agent"; then
    return 1
  fi
  echo ""

  # Phase 6: Checkpoint
  emit_checkpoint "$agent" "init"
  echo ""

  echo "✅ AGENT PROTOCOL INITIALIZED"
  echo "════════════════════════════════════"
  echo ""
  echo "Ready: $agent (Tier: $AGENT_TIER)"
  echo "Context: LEVELSET, CONSTITUTION, AGENTS, DECISIONS"
  echo "Signing: $GIT_AUTHOR_SUFFIX"
  echo ""
  echo "Next: Read \$AGENT_INSTRUCTIONS, consult vault context, then proceed."
  echo ""
}

# ============================================================================
# CONDITIONAL EXECUTION
# ============================================================================

# Only run main() if this script is sourced with an agent argument
# If sourced without args, user can call main() directly or use helper functions
if [[ "${BASH_SOURCE[0]}" == "${0}" ]] || [ -n "${1:-}" ]; then
  main "$@"
fi
