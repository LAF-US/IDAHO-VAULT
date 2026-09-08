# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
shopt -s expand_aliases
# Check for rg availability
if ! (unalias rg 2>/dev/null; command -v rg) >/dev/null 2>&1; then
  function rg {
  local _cc_bin="${CLAUDE_CODE_EXECPATH:-}"
  [[ -x $_cc_bin ]] || _cc_bin=/c/Users/loganf/.local/bin/claude.exe
  if [[ ! -x $_cc_bin ]]; then command rg ${1+"$@"}; return; fi
  if [[ -n ${ZSH_VERSION:-} ]]; then
    ARGV0=rg "$_cc_bin" ${1+"$@"}
  elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    ARGV0=rg "$_cc_bin" ${1+"$@"}
  else
    (exec -a rg "$_cc_bin" ${1+"$@"})
  fi
}
fi
# Shadow pkill to refuse patterns matching the CLI process
unalias pkill 2>/dev/null || true
function pkill {
  if [ -n "${CLAUDE_PID:-}" ] && [ -r "/proc/${CLAUDE_PID}/comm" ]; then
    local _cc_skip="" _cc_a
    local -a _cc_probe=()
    for _cc_a in ${1+"$@"}; do
      if [ -n "$_cc_skip" ]; then _cc_skip=""; continue; fi
      case "$_cc_a" in
        --signal) _cc_skip=1 ;;
        --signal=*|-e|--echo) ;;
        -[0-9]*) ;;
        -[PUGOF]?*) _cc_probe+=("$_cc_a") ;;
        -[ABCDEFGHIJKLMNOPQRSTUVWXYZ][ABCDEFGHIJKLMNOPQRSTUVWXYZ0-9]*) ;;
        *) _cc_probe+=("$_cc_a") ;;
      esac
    done
    if command pgrep ${_cc_probe[@]+"${_cc_probe[@]}"} 2>/dev/null | command grep -qx "${CLAUDE_PID}"; then
      printf 'pkill: refusing to run — this pattern matches the Claude CLI process (PID %s). Narrow the pattern, or target your own children with `pkill -P $$ ...`.\n' "${CLAUDE_PID}" >&2
      return 1
    fi
  fi
  command pkill ${1+"$@"}
}
export PATH='/c/Users/loganf/bin:/mingw64/bin:/usr/local/bin:/usr/bin:/bin:/mingw64/bin:/usr/bin:/c/Users/loganf/bin:/c/Program Files (x86)/Common Files/Intel/Shared Libraries/redist/intel64/compiler:/c/WINDOWS/system32:/c/WINDOWS:/c/WINDOWS/System32/Wbem:/c/WINDOWS/System32/WindowsPowerShell/v1.0:/c/WINDOWS/System32/OpenSSH:/c/JupyterLab:/c/Users/loganf/scoop/shims:/c/Users/loganf/scoop/apps/nodejs-lts/current:/c/Users/loganf/scoop/apps/nodejs-lts/current/bin:/c/Users/loganf/scoop/apps/1password-cli/current:/c/Users/loganf/AppData/Local/Microsoft/WindowsApps:/cmd:/bin:/c/Users/loganf/AppData/Local/Programs/Microsoft VS Code/bin:/c/Users/loganf/AppData/Local/Programs/DockerDesktop/resources/bin:/c/Users/loganf/AppData/Local/Microsoft/WinGet/Packages/SST.opencode_Microsoft.Winget.Source_8wekyb3d8bbwe:/c/Users/loganf/AppData/Local/Microsoft/WinGet/Packages/MistralAI.MistralVibe.ACP_Microsoft.Winget.Source_8wekyb3d8bbwe:/c/Users/loganf/AppData/Local/Programs/Ollama:/c/Users/loganf/AppData/Local/Programs/Python/Python313:/mingw64/bin:/usr/bin/vendor_perl:/usr/bin/core_perl:/c/Users/loganf/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/3c7fe224-4f1f-4c0f-bbbd-e986bfeb6dcf/c761f06c-c4b2-466b-bdf9-4892c2194414/bin'
