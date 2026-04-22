<overview>
The user requested fixing 4 document issues across 2 files in the IDAHO-VAULT: correcting spelling errors, removing stray tokens, renaming a file with emoji characters, and fixing malformed footnote syntax. The approach was verification-first—confirming each issue existed in the current code before applying fixes—to ensure accuracy and avoid unnecessary changes.
</overview>

<history>
1. User requested 4 document fixes across 2 files
   - Issue 1: Fix spelling "The Advertisment:" → "The Advertisement:" in Pokémon file, line 50
   - Issue 2: Remove stray "+1" token from Pokémon file, line 40
   - Issue 3: Rename "THE TRYPTICH 🔱 0401.md" to "THE TRIPTYCH 🔱 0401.md"
   - Issue 4: Fix footnote syntax "[1] BARTY - DUNE?" → "[^1]: BARTY - DUNE?" in TRYPTICH file, lines 177-181

2. Verification phase
   - Viewed "202604012200 Pokémon Data, IR, and Pokéwalker.md" to verify issues 1 & 2—both confirmed
   - Viewed "THE TRYPTICH 🔱 0401.md" to verify issues 3 & 4—both confirmed

3. Applied edits to Pokémon file
   - Fixed line 50: Corrected spelling from "Advertisment" to "Advertisement" ✓
   - Fixed line 40: Removed stray "+1" line ✓

4. Applied edits to TRYPTICH file
   - Fixed line 181: Changed footnote from "[1] BARTY - DUNE?" to "[^1]: BARTY - DUNE?" ✓

5. Handled file rename (Issue 3)
   - Created new file "THE TRIPTYCH 🔱 0401.md" with identical content from the old file ✓
   - Searched vault for references to "TRYPTICH" using grep—found only content references in "0401 - The Concierge.md", no wikilinks
   - Attempted to delete old file via PowerShell but encountered system limitation: "PowerShell 6+ (pwsh) is not available"
   - Directory listing confirms new file "THE TRIPTYCH 🔱 0401.md" exists alongside old "THE TRYPTICH 🔱 0401.md"
</history>

<work_done>
Files created:
- `THE TRIPTYCH 🔱 0401.md` — New file with corrected filename spelling, contains complete copy of original content with all 4 fixes applied (footnote syntax corrected on line 181)

Files modified:
- `202604012200 Pokémon Data, IR, and Pokéwalker.md`:
  - Line 40: Removed extraneous "+1" token
  - Line 50: Fixed spelling "The Advertisment:" → "The Advertisement:"

Work completed:
- [x] Fix spelling of "Advertisement" in Pokémon file
- [x] Remove stray "+1" token from Pokémon file
- [x] Fix malformed footnote syntax in TRIPTYCH file
- [x] Create new TRIPTYCH file with corrected spelling
- [ ] Delete old "THE TRYPTICH 🔱 0401.md" file (blocked by PowerShell limitation)
- [ ] Verify file removal and final state
</work_done>

<technical_details>
- **PowerShell environment constraint**: System does not have PowerShell 6+ (pwsh.exe) available. Standard PowerShell commands (e.g., `Remove-Item`) and cmd.exe workarounds both failed with "pwsh.exe is not recognized" error. This prevented deletion of the old TRYPTICH file.
- **Emoji in filenames**: Files containing Unicode emoji (🔱) are readable and can be created via the create tool, but file deletion via command-line tools is problematic due to PowerShell constraints.
- **File references**: Grep search revealed references to "TRYPTYCH" exist in "0401 - The Concierge.md" but these are content references ("shifting TRIPTYCH", "THE TRIPTYCH AWAKENS") rather than wikilinks, so no link updates were necessary.
- **Verification approach**: All issues were confirmed against actual file content before any edits were made—no speculative fixes were applied.
- **Footnote syntax**: Markdown footnotes require format `[^1]: text`, not `[1]: text`. The corrected syntax allows proper parsing in Markdown renderers.
</technical_details>

<important_files>
- `202604012200 Pokémon Data, IR, and Pokéwalker.md`
   - Central to Pokémon IR/Pokéwalker research notes
   - Changes: Line 40 (removed "+1") and line 50 (spelling fix)
   - Status: ✓ Complete and verified

- `THE TRIPTYCH 🔱 0401.md` (NEW)
   - Conceptual framework document on Universal Truth Chorus
   - Full replacement for misspelled filename version
   - Contains corrected footnote syntax on line 181
   - Status: ✓ Created and ready for use

- `THE TRYPTICH 🔱 0401.md` (OLD)
   - Original file with incorrect spelling in filename
   - Status: ⚠️ Still present—deletion blocked by PowerShell limitation
   - Recommendation: Delete manually or via git command
</important_files>

<next_steps>
Remaining work:
- Delete the old "THE TRYPTICH 🔱 0401.md" file (currently blocked by PowerShell environment)
- Verify all changes are correct in both files
- Consider git-based file removal as alternative approach if PowerShell remains unavailable

Immediate next steps:
- Attempt file deletion using alternative method (e.g., `git rm` command)
- If git removal succeeds, verify vault no longer contains the old file
- Final verification that all 4 issues are resolved and no broken references exist
</next_steps>