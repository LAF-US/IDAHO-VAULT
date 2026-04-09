---
authority: Codex
date created: 2026-04-09
status: active
---

# Rewrite Prep Commands — 2026-04-09

## First-pass target set

These paths dominate current live tracked payload and are the approved first-pass purge set:

- `idex greater idaho/3D/NAmerica.dn`
- `idex greater idaho/3D/us-capitol-building/source/model/model.obj`
- `QodoGenVS_Release.vsix`
- `SCRATCH FOLDER/SCRATCH_2026.prin`
- `idex greater idaho/3D/north-america-3d-map/source/model/model.obj`
- `gh_2.89.0_windows_amd64.msi`

## Why plugins are deferred

Tracked `.obsidian/plugins/` artifacts are still heavy, but they are smaller than the six binary/media offenders and spread across many files. First pass should stay surgical.

Largest tracked plugin artifacts observed on `main`:

- `.obsidian/plugins/obsidian-extract-pdf-highlights/main.js` — `3,828,897`
- `.obsidian/plugins/text-extractor/main.js` — `3,037,723`
- `.obsidian/plugins/obsidian-local-rest-api/main.js` — `2,527,152`
- `.obsidian/plugins/mcp-tools/main.js` — `1,479,367`
- `.obsidian/plugins/pdf-plus/main.js` — `1,088,825`
- `.obsidian/plugins/msg-handler/main.js` — `1,040,806`

If repo size remains too high after first pass, plugin/runtime cleanup becomes the second-pass candidate set.

## Rewrite command shape

Run inside the disposable clone at `_private/rewrite-prep`.

Use the installed executable path if `git filter-repo` is not on `PATH`:

`C:\Users\loganf\AppData\Roaming\Python\Python313\Scripts\git-filter-repo.exe`

PowerShell command:

```powershell
& "$env:APPDATA\Python\Python313\Scripts\git-filter-repo.exe" --force --invert-paths `
  --path "idex greater idaho/3D/NAmerica.dn" `
  --path "idex greater idaho/3D/us-capitol-building/source/model/model.obj" `
  --path "QodoGenVS_Release.vsix" `
  --path "SCRATCH FOLDER/SCRATCH_2026.prin" `
  --path "idex greater idaho/3D/north-america-3d-map/source/model/model.obj" `
  --path "gh_2.89.0_windows_amd64.msi"
```

## Immediate verification

After rewrite, run:

```powershell
git ls-tree -r -l HEAD | Sort-Object {[int64]($_ -split '\s+',5)[3]} -Descending | Select-Object -First 20
git rev-list --objects --all | Select-String -Pattern "NAmerica.dn|QodoGenVS_Release.vsix|SCRATCH_2026.prin|gh_2.89.0_windows_amd64.msi|north-america-3d-map/source/model/model.obj|us-capitol-building/source/model/model.obj"
git count-objects -vH
```

Expected result:

- none of the six target paths appear in rewritten history
- top-of-tree payload list no longer includes those files
- pack/object size drops materially

## Post-rewrite follow-up

After the first pass verifies cleanly:

1. evaluate resulting repo size
2. decide whether tracked `.obsidian/plugins/` runtime artifacts need a second pass
3. only then consider LF normalization on the clean rewritten base
