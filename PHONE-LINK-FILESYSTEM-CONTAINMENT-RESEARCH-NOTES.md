---
title: Phone Link filesystem containment — research notes
author: Manus AI
status: research note
scope: Windows path handling and containment considerations for local Phone Link intake tooling
sources: Microsoft Learn
updated: 2026-08-22
---

# Phone Link filesystem containment — research notes

## Purpose and scope

This note records a narrow research review of filesystem-containment concerns relevant to the repository’s local Phone Link intake and autosweep utilities. It is **not** a replacement for the implementation, a Windows security guarantee, or operating guidance for third-party files. Its purpose is to preserve the rationale for resolving a configured source and destination to trusted filesystem locations before moving files.

## Findings

| Concern | Microsoft documentation | Practical implication for local intake tooling |
|---|---|---|
| Navigation segments and path normalization | Windows path canonicalization removes navigation elements such as `.` and `..`; Microsoft recommends the newer PathCch APIs instead of the legacy `PathCanonicalize` API.[1] [2] | A containment check should compare resolved path components rather than rely on raw input strings or simple textual prefixes. |
| Reparse points and links | Microsoft documents that reparse points can change ordinary file-operation behavior and are used for linked files and mounted folders.[3] [4] | Source and destination decisions should account for link/reparse behavior rather than treating a displayed path as an immutable physical location. |
| Final resolved location | `GetFinalPathNameByHandle` reports the final fully resolved path of an opened file or directory; Microsoft’s example shows a symbolic link resolving to its target.[5] | A native Windows integration that must make handle-bound authorization decisions can verify the final opened object, not merely a pre-open spelling of its path. |
| Path-form edge cases | Microsoft notes that canonicalization behavior differs for forward slashes, extended-length forms, and path-segment normalization.[2] | Cross-platform tooling should avoid assuming a single string form represents a path identity. Windows-specific wrappers need explicit tests for drive, UNC, slash, and long-path forms. |

## Design observations

The Python watcher on `main` (`.github/scripts/phone_link_auto_sweep.py`) uses resolved paths and a component-aware containment rule. That claim covers the Python code only: the PowerShell path (`!/PHONE-LINK/phone-link-auto-sweep.ps1`), which `!/PHONE-LINK/START-PHONE-LINK-SWEEP.cmd` launches directly and which therefore remains a user-facing entry point rather than a compatibility shim, still builds its destination with `Join-Path` and calls `Move-Item` with no canonical destination validation, and this note records it as an unresolved security gap rather than as covered. The intake script carries the same containment code, but the 2026-08-21 cleanup (063cdaa24) moved it from `.github/scripts/` to `scripts_scripts/phone_link_intake.py` without adjusting its root anchor, so `Path(__file__).resolve().parents[2]` pointed one directory above the repository, and `phone-link-intake.bat` still launched the old path. This PR corrects the anchor to `parents[1]` for the new location and repoints the launcher; the correction was checked by importing the module and comparing its resolved root with the repository root. The regression tests that validated the original change (`tests/test_phone_link_contract.py`) were deleted from `main` on 2026-08-26 (e43ee3f57) and are not restored here. The component-aware rule is a stronger boundary than a `startswith` comparison because same-prefix siblings, such as `C:\vaultx` versus `C:\vault`, do not represent the same directory relationship. Both Python entry points maintain a fixed repository-root destination model rather than accepting arbitrary destination roots.

Microsoft’s reparse-point documentation is a useful caution for this design: a path can carry behavior that is not obvious from its name alone. The current Python-level approach is appropriate for a small local tool because it resolves paths before evaluating containment. If the tool’s privilege, automation scope, or deployment surface expands, a Windows-native wrapper should consider handle-bound verification of the final opened object as a further hardening measure.[3] [5]

The research does not recommend weakening the existing containment checks for compatibility. Where an operator needs a new source or destination, the safer course is to define that location explicitly and add coverage for the resolved-path boundary rather than permitting arbitrary environment or command-line paths.

## Review questions retained for future work

The following questions are intentionally recorded rather than answered by this note. They require implementation-specific testing on the intended Windows environment.

| Question | Why it remains open |
|---|---|
| How should the tool behave when a configured source crosses a junction or network share? | Reparse and SMB behavior depends on the final filesystem/provider and the chosen API surface.[3] [5] |
| Does the local Windows launch path need a handle-bound final-path check? | The Python code is local and resolves paths before comparing, and with this PR both Python entry points anchor to the repository that contains them; the PowerShell path, which `START-PHONE-LINK-SWEEP.cmd` launches directly, performs no destination validation today (see Design observations), so any answer applies to it first. A native-handle policy would need a separate design and test plan. |
| Which long-path and UNC forms are supported by the actual Phone Link folder configuration? | Microsoft documents distinct normalization and extended-path behavior; the repository should test the configurations it intends to support.[2] |

## References

[1] [Microsoft Learn — PathCanonicalizeA function](https://learn.microsoft.com/en-us/windows/win32/api/shlwapi/nf-shlwapi-pathcanonicalizea)

[2] [Microsoft Learn — PathAllocCanonicalize function](https://learn.microsoft.com/en-us/windows/win32/api/pathcch/nf-pathcch-pathalloccanonicalize)

[3] [Microsoft Learn — Reparse Points and File Operations](https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-points-and-file-operations)

[4] [Microsoft Learn — Reparse points](https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-points)

[5] [Microsoft Learn — GetFinalPathNameByHandleA function](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfinalpathnamebyhandlea)
