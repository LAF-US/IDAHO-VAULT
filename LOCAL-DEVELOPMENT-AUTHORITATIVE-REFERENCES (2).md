---
updated: 2026-05-07
status: active
authority: LOGAN
scope:
  - local-development
  - python
  - jupyter
  - windows-storage
---
# Local Development Authoritative References

This note records the local machine facts checked on 2026-05-07 and the authoritative web references used for Python, Jupyter, and Windows disk tooling.

## Local Python And Jupyter State

Checked locally before installs/downloads:

```text
Python: 3.13.3
pip: 26.0.1
JupyterLab: 4.4.0
Notebook: 7.4.0
IPython: 9.1.0
ipykernel: 6.29.5
```

Global commands exist:

```powershell
jupyter
jupyter-lab
ipython
```

Registered kernels:

```text
python3 -> C:\Users\loganf\AppData\Local\Programs\Python\Python313\share\jupyter\kernels\python3
```

`IDAHO-VAULT` has a project `.venv` using Python 3.13.3, but that `.venv` does not currently include `jupyter` or `ipykernel`.

## Project Python Constraint

`pyproject.toml` currently declares:

```toml
requires-python = ">=3.10,<3.14"
```

That means Python 3.13 is in range for this repo. Python 3.14 is current upstream, but should not be used for this repo until the project constraint is intentionally changed and dependencies are verified.

## Jupyter Guidance

Global Jupyter can open notebooks today:

```powershell
cd C:\Users\loganf\Documents\IDAHO-VAULT
jupyter lab
```

This will use the global `python3` kernel unless a project-specific kernel is added later.

Cleaner future project setup, only when installs/downloads are intentionally allowed:

```powershell
cd C:\Users\loganf\Documents\IDAHO-VAULT
uv add --dev jupyterlab ipykernel
uv run python -m ipykernel install --user --name idaho-vault --display-name "IDAHO Vault"
uv run jupyter lab
```

## Windows Disk Utility Equivalents

Safe inspection commands:

```powershell
Get-Volume
Get-Disk
Get-PhysicalDisk
Get-PSDrive
```

Repair or destructive commands require deliberate intent:

```powershell
diskpart
chkdsk /f
Repair-Volume -OfflineScanAndFix
Optimize-Volume
Clear-Disk
Initialize-Disk
Format-Volume
```

`diskpart` is the closest Windows CLI equivalent to macOS Disk Utility for disk, partition, volume, and virtual disk management, but it is powerful and should be treated as an administrative tool.

## Secret Handling Rule

Never dump plaintext secrets to repo files, audit reports, logs, screenshots, or terminal summaries.

Use 1Password for targeted reads only, and pass secrets directly into the command that needs them. Do not write secret values into tracked files.

The repo now includes a secret-pattern guard in:

```text
.github/scripts/check_secret_patterns.py
.githooks/pre-commit
.github/workflows/secret-pattern-policy.yml
```

The guard reports only file path, line number, and rule name. It must not print matched secret values.

## Authoritative Web References

Python:

- Python downloads and active releases: https://www.python.org/downloads/
- Python 3.13 release notes: https://docs.python.org/3/whatsnew/3.13.html
- Python 3.14 and 3.13 maintenance release announcement: https://blog.python.org/2026/02/python-3143-and-31312-are-now-available/

Jupyter:

- Project Jupyter install page: https://jupyter.org/install
- Project Jupyter documentation: https://docs.jupyter.org/en/latest/index.html
- JupyterLab installation docs: https://jupyterlab.readthedocs.io/en/stable/getting_started/installation.html

Windows storage and disk tools:

- `Get-Disk`: https://learn.microsoft.com/en-us/powershell/module/storage/get-disk
- `Get-Volume`: https://learn.microsoft.com/en-us/powershell/module/storage/get-volume
- `Get-PhysicalDisk`: https://learn.microsoft.com/en-us/powershell/module/storage/get-physicaldisk
- `Repair-Volume`: https://learn.microsoft.com/en-us/powershell/module/storage/repair-volume
- `Optimize-Volume`: https://learn.microsoft.com/en-us/powershell/module/storage/optimize-volume
- `diskpart`: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/diskpart
- `chkdsk`: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/chkdsk
