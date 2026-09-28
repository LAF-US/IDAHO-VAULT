# Obsidian Plugin Modes

These files are local mode snapshots for `.obsidian/community-plugins.json`.

They exist to make plugin recovery repeatable while the broader historical desktop stack remains under review.

## Important context

- `restricted-recovery.json` reflects the current low-risk startup set.
- `desktop-pre-troubleshoot-2026-04-11.json` reflects the plugin list backed up before the 2026-04-11 recovery reduction.
- The older agentic record still refers to a historical 49-plugin desktop state. That count is not reconstructed here as an authoritative JSON because the local repo record and the historical note still disagree.

## Use

List modes:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\set-obsidian-plugin-mode.ps1 -List
```

Show current enabled plugins:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\set-obsidian-plugin-mode.ps1 -ShowCurrent
```

Apply a mode:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\set-obsidian-plugin-mode.ps1 -Mode restricted-recovery
```

The script refuses to switch while Obsidian is running unless `-AllowWhileRunning` is passed.
