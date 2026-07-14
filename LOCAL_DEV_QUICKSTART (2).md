# Local Dev Quickstart

Last checked: 2026-05-07

## Machine Profile

- OS: Windows
- Shell: PowerShell Core 7.6.1
- Home/workspace: `C:\Users\loganf`
- Main project area: `C:\Users\loganf\Documents`
- Fast search: `rg`
- Editor CLI: `code`

## Core Tools

- Git: `git --version`
- Git LFS: `git lfs version`
- GitHub CLI: `gh --version`
- 1Password CLI: `op --version`
- Node: `node --version`
- npm: `npm --version`
- Python: `python --version`
- uv: `uv --version`

Current checked versions:

- Git 2.49.0
- Git LFS 3.6.1
- GitHub CLI 2.89.0
- 1Password CLI 2.33.1
- Node 24.14.1
- npm 11.12.1
- Python 3.13.3
- uv 0.11.2

## GitHub CLI

Verify:

```powershell
gh auth status
gh api user --jq .login
```

If `gh` reports an invalid token immediately after a successful browser login, check for dead proxy variables:

```powershell
Get-ChildItem Env: | Where-Object { $_.Name -match 'proxy|PROXY' }
```

In this Codex shell, proxy variables may point at `127.0.0.1:9`. Clear them for GitHub network commands:

```powershell
Remove-Item Env:HTTP_PROXY,Env:HTTPS_PROXY,Env:ALL_PROXY,Env:GIT_HTTP_PROXY,Env:GIT_HTTPS_PROXY -ErrorAction SilentlyContinue
```

If Windows Credential Manager keeps a stale GitHub CLI token, clear only the GitHub CLI entries:

```powershell
cmdkey /delete:gh:github.com:loganfinney27
cmdkey /delete:gh:github.com:
gh auth logout -h github.com -u loganfinney27
gh auth login -h github.com -w --insecure-storage
```

`--insecure-storage` stores the token in `C:\Users\loganf\AppData\Roaming\GitHub CLI\hosts.yml` instead of Windows Credential Manager.

## 1Password CLI

Configured account:

- `my.1password.com`
- `loganfinney27@gmail.com`

Verify:

```powershell
op account list
op vault list --account my.1password.com
```

If access fails:

1. Open and unlock the 1Password desktop app.
2. Go to Settings > Security and enable Windows Hello.
3. Go to Settings > Developer and enable 1Password CLI integration.
4. Retry:

```powershell
op signin --account my.1password.com
op vault list --account my.1password.com
```

Note: `op whoami` may still report "account is not signed in" even when explicit `--account my.1password.com` commands work.

## Secret Handling Rule

Never dump plaintext secrets to repo files, audit reports, logs, screenshots, or terminal summaries.

Use 1Password for targeted reads only:

```powershell
op read "op://<vault>/<item>/<field>" --account my.1password.com
```

Pipe or assign secret values directly into the command that needs them. Do not write secret values into tracked files. If a local file must contain secrets, use ignored paths such as `.env`, `.env.*`, `.op/openrouter.env`, or `secrets/`.

The `IDAHO-VAULT` repo has a pre-commit and CI secret-pattern guard. It reports only file path, line number, and rule name; it must not print matched secret values.

## Local Projects

### IDAHO-VAULT

Path:

```powershell
C:\Users\loganf\Documents\IDAHO-VAULT
```

Remote:

```powershell
https://github.com/LAF-US/IDAHO-VAULT.git
```

Useful checks:

```powershell
git -C C:\Users\loganf\Documents\IDAHO-VAULT status --short
git -C C:\Users\loganf\Documents\IDAHO-VAULT branch --show-current
uv --directory C:\Users\loganf\Documents\IDAHO-VAULT sync
```

Project notes:

- Python/CrewAI project declared in `pyproject.toml`.
- Requires Python `>=3.10,<3.14`.
- Root package path is `src/idaho_vault`.
- The repo is large and vault-like; avoid broad recursive listings unless needed.
- Treat untracked files under `!\` as user-owned until explicitly classified.

### IR-Court-Tracker

Path:

```powershell
C:\Users\loganf\LFPython\IR-Court-Tracker
```

Useful check:

```powershell
python C:\Users\loganf\LFPython\IR-Court-Tracker\main.py
```

Project notes:

- Small Python scraper folder.
- Not a Git repo at the checked path.
- `main.py` currently imports modules that are not all present in the visible `scraper` folder, so expect setup or missing-file work before it runs cleanly.

## Missing Or Optional

- Docker is not on PATH.
- Go is not on PATH.
- Rust is not on PATH.
- Global Git `user.email` is set; verify `user.name` before committing:

```powershell
git config --global user.name
git config --global user.email
```

Set the name if needed:

```powershell
git config --global user.name "Logan Finney"
```
