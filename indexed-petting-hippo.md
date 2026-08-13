# Plan: Save IDEX Transcripts to Vault

## Context
Logan needs two clean transcripts from IDEX_Artifacts-Bites-All saved as vault files, with `[MM:SS]` timecode markers at the start of each paragraph chunk. These are for copy/pasting into Word docs for human colleagues.

## Files to Create
1. **IDEX_Artifacts-Bites-All_FRANKLIN.md** — Transcript #1, 10:19–34:52 (Franklin segment)
2. **IDEX_Artifacts-Bites-All_PIERCE.md** — Transcript #2, 34:52–1:15:28 (Pierce segment)

## Format
- Clean flowing text, no speaker labels
- `[MM:SS]` timecode at the start of each paragraph chunk (derived from the original CSV start times)
- No frame-level precision, no SRT formatting

## Source
- `IDEX_Artifacts-Bites-All.csv` (original, speaker-attributed, paragraph-chunked) — rows 28–84 for Franklin, rows 85–216 for Pierce

## Verification
- Confirm files render in Obsidian
- Spot-check timecodes against source CSV
