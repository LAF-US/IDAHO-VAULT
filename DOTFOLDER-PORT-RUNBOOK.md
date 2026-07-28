# Dotfolder Port Runbook

This is the employer-laptop evacuation tool for preserving home dotfolders in the Vault. The implementation is the root-visible Python script `dotfolder_reconcile.py`; there is no shell launcher for this workflow.

## Rules

- Dry-run first. Do not run `--apply` until the dry-run output makes sense.
- `SNAPSHOT` preserves the machine: it copies home-only files into the Vault and leaves home files in place.
- `RETIRE` is later cleanup: it moves or deletes home files only after preservation is confirmed.
- Secret-looking files are salvaged, then classified. They must stay out of Git unless Logan explicitly promotes them.
- The local containment manifest is ignored scratch: `.tmp/dotfolder-containment/manifest.local.json`.

## Commands

From the Vault root:

```text
python -B dotfolder_reconcile.py --all --snapshot --force --quiet
python -B dotfolder_reconcile.py --all --snapshot --force --apply --quiet
python -B dotfolder_reconcile.py --all --retire --force --apply --quiet
```

If Windows does not resolve `python`, use `py -3` with the same arguments.

## Expected Flow

1. Run the `SNAPSHOT` dry-run and inspect counts for home-only files, conflicts, sensitive paths, and unavailable paths.
2. Run `SNAPSHOT --apply` only after the dry-run is acceptable.
3. Inspect the containment summary and local manifest.
4. Move the hydrated Vault to the portable drive later; this script does not automate drive relocation or rclone backup.
5. Run `RETIRE --apply` only when the laptop is ready for final cleanup.

## Git Safety

Hydrated cargo remains present in the working tree until Logan chooses disposition. Git ignore rules and the secret-pattern guard are expected to keep private/runtime cargo out of commits by default, including `.home`, hash-suffixed `.home.<sha>`, and Windows duplicate names such as `name (2).json`.