# Snapshot file
# Unset all aliases to avoid conflicts with functions
unalias -a 2>/dev/null || true
shopt -s expand_aliases
# Check for rg availability
if ! (unalias rg 2>/dev/null; command -v rg) >/dev/null 2>&1; then
  function rg {
  local _cc_bin="${CLAUDE_CODE_EXECPATH:-}"
  [[ -x $_cc_bin ]] || _cc_bin=$(command -v claude 2>/dev/null)
  if [[ ! -x $_cc_bin ]]; then command rg "$@"; return; fi
  if [[ -n $ZSH_VERSION ]]; then
    ARGV0=rg "$_cc_bin" "$@"
  elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ "$OSTYPE" == "win32" ]]; then
    ARGV0=rg "$_cc_bin" "$@"
  elif [[ $BASHPID != $$ ]]; then
    exec -a rg "$_cc_bin" "$@"
  else
    (exec -a rg "$_cc_bin" "$@")
  fi
}
fi
export PATH='/c/Users/loganf/bin:/mingw64/bin:/usr/local/bin:/usr/bin:/bin:/mingw64/bin:/usr/bin:/c/Users/loganf/bin:/c/Program Files (x86)/Common Files/Intel/Shared Libraries/redist/intel64/compiler:/c/WINDOWS/system32:/c/WINDOWS:/c/WINDOWS/System32/Wbem:/c/WINDOWS/System32/WindowsPowerShell/v1.0:/c/WINDOWS/System32/OpenSSH:/c/JupyterLab:/c/Users/loganf/scoop/apps/openjdk/current/bin:/c/Users/loganf/.codex/tmp/arg0/codex-arg0uoTk6q:/c/Users/loganf/scoop/persist/nodejs-lts/bin/node_modules/@openai/codex/node_modules/@openai/codex-win32-x64/vendor/x86_64-pc-windows-msvc/path:/c/Program Files (x86)/Common Files/Intel/Shared Libraries/redist/intel64/compiler:/c/WINDOWS/system32:/c/WINDOWS:/c/WINDOWS/System32/Wbem:/c/WINDOWS/System32/WindowsPowerShell/v1.0:/c/WINDOWS/System32/OpenSSH:/c/JupyterLab:/c/Users/loganf/scoop/apps/1password-cli/current:/c/Users/loganf/scoop/apps/nodejs-lts/current/bin:/c/Users/loganf/scoop/apps/nodejs-lts/current:/c/Users/loganf/scoop/shims:/c/Users/loganf/AppData/Local/Microsoft/WindowsApps:/c/Users/loganf/AppData/Local/GitHubDesktop/bin:/cmd:/c/Users/loganf/AppData/Local/Programs/Microsoft VS Code/bin:/c/Users/loganf/AppData/Local/Programs/Obsidian:/c/Users/loganf/AppData/Local/Microsoft/WinGet/Packages/BurntSushi.ripgrep.MSVC_Microsoft.Winget.Source_8wekyb3d8bbwe/ripgrep-15.1.0-x86_64-pc-windows-msvc:/c/Users/loganf/AppData/Local/Microsoft/WinGet/Packages/MistralAI.MistralVibe.ACP_Microsoft.Winget.Source_8wekyb3d8bbwe:/c/Users/loganf/AppData/Local/Programs/Ollama:/c/Users/loganf/.vscode/extensions/anthropic.claude-code-2.1.114-win32-x64/resources/native-binary:/c/Users/loganf/AppData/Local/Google/CloudSDK/google-cloud-sdk/bin:/bin:/c/Users/loganf/AppData/Local/Microsoft/WinGet/Packages/Anthropic.ClaudeCode_Microsoft.Winget.Source_8wekyb3d8bbwe:/c/Users/loganf/AppData/Local/Programs/Python/Python313:/mingw64/bin:/usr/bin/vendor_perl:/usr/bin/core_perl:/c/Users/loganf/AppData/Roaming/Claude/local-agent-mode-sessions/skills-plugin/3c7fe224-4f1f-4c0f-bbbd-e986bfeb6dcf/c761f06c-c4b2-466b-bdf9-4892c2194414/bin'
