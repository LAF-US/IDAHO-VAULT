---
name: transcript-synthesis
description: Synthesize multiple transcript versions (Adobe, YouTube, SRT) into a single, accurate vault-standard document.
---

## When to Use
- When multiple transcript variants exist for a single media file (e.g., `.txt`, `.csv`, `.json`, `.srt`, and YouTube-generated).
- When the user asks to "SYNTHESIZE, GENTLY" or "CROSS-CHECK accuracy".
- When a transcript contains phonetic errors, "garbletext", or generic speaker labels (e.g., "Speaker 1").

## Procedure
1. **Locate Artifacts**: Use `glob` to find all files sharing the media base name (e.g., `**/*IDEX_Artifacts-Bites-All*`).
2. **Normalize for Comparison**:
    - Extract raw spoken text from each variant.
    - Strip metadata: timestamps (e.g., `00;00;00;05`), speaker labels (e.g., `Speaker 3`), and sequence numbers.
3. **Identify Authority**:
    - Compare segments across versions.
    - Choose the most plausible wording based on context (e.g., "Northwest Ordinance" vs. "Northwest Orient Ordinance").
    - Use human-provided corrections (if any) as the primary authority.
4. **Standardize Speaker Names**:
    - Map generic labels (Speaker 1, Speaker 2) to actual names using provided notes or historical context (e.g., Speaker 2 -> Pat -> Pem).
5. **Reformat to Vault Standard**:
    - Apply the standard formatting: `[HH:MM:SS] Speaker Name: Text`.
    - Follow examples from reference files (e.g., `ARCHIVAL-FIND.md`).
    - Use `\n` line breaks between timestamped segments for readability.
6. **Final Write**: Save the synthesized result to a new file (e.g., `BaseName_Transcript_Synthesized.md`).

## Pitfalls and Fixes
- **Phonetic Errors**: Transcription engines often mishear proper nouns (e.g., "Rigby" as "rugby"). Cross-reference with vault entities to correct.
- **Timecode Mismatch**: YouTube timecodes (HH:MM:SS) may differ slightly from Adobe Premiere (HH;MM;SS;FF). Align based on the first spoken word.
- **Truncated Files**: Always use `read_file` with `start_line` if a transcript is large to ensure you have the complete text.

## Verification
- The synthesized transcript uses standardized names throughout.
- Obvious "garbletext" has been replaced by contextually correct terms.
- Timecodes are consistently formatted as `[HH:MM:SS]`.
