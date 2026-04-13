# Action Automation & Theme Alignment

The vault requires three primary fixes to restore stability:
1. Routing automated operations out of branch-protected collision paths.
2. Fixing the Linear gateway's API footprint so webhooks do not fail with HTTP 400s.
3. Resetting the Obsidian ROYGBIV theme to anchor to the most recently worked Daily Note, as requested.

## User Review Required
> [!IMPORTANT]
> - By transitioning scraper and preservation workflows to PRs, these will now require manual merge approvals. If you prefer `linear-pr-sync` to auto-merge them, we will need to add a label step.
> - The ROYGBIV fallback will be cached in `.obsidian/plugins/roygbiv-day-accent/data.json` so it perfectly persists between Obsidian restarts. 

## Proposed Changes

### Obsidian Plugin: ROYGBIV Theme 
We will shift from `new Date().getDay()` fallback to a persistent `settings.lastActiveDayIndex` cached state.

#### [MODIFY] main.js (file:///c:/Users/loganf/Documents/IDAHO-VAULT/.obsidian/plugins/roygbiv-day-accent/main.js)
- Inject `this.settings = Object.assign({ lastActiveDayIndex: new Date().getDay() }, await this.loadData())` into `onload()`.
- Add `this.saveData(this.settings)` call upon resolving a valid daily-note.
- Swap the fallback in `applyDayClass()` to `this.settings.lastActiveDayIndex`. 

### Pipeline: Branch Protection Enforcement 
A bare `git push` violates `main` branch protections. The following workflows will have their standard git operations swapped to branching operations paired with a `gh pr create` terminal string. 

#### [MODIFY] idaho-leg-scraper.yml (file:///c:/Users/loganf/Documents/IDAHO-VAULT/.github/workflows/idaho-leg-scraper.yml)
- Change bare push to `git checkout -b idaho-leg-scraper-$(date)` -> `gh pr create`.

#### [MODIFY] wayback-preserve.yml (file:///c:/Users/loganf/Documents/IDAHO-VAULT/.github/workflows/wayback-preserve.yml)
- Change bare push to `git checkout -b wayback-preserve-$(date)` -> `gh pr create`.

#### [MODIFY] wayback-audit.yml (file:///c:/Users/loganf/Documents/IDAHO-VAULT/.github/workflows/wayback-audit.yml)
- Change bare push to `git checkout -b wayback-audit-$(date)` -> `gh pr create`.

### Linear Gateway API Stabilization
Linear GraphQL relies on specific Input types. Standard attachments are created using the `attachmentLinkCreate` mutation rather than `attachmentCreate`, which is generating the 400 HTTP exception.

#### [MODIFY] linear_gateway.py (file:///c:/Users/loganf/Documents/IDAHO-VAULT/.github/scripts/linear_gateway.py)
- Refactor the LinkPR mutation syntax to point directly to `attachmentLinkCreate` to ensure payload acceptance via Webhook integration. 

## Open Questions

- Does the ROYGBIV plugin need to check for `-1` default values or rely entirely on standard 0-6 array values? (Assuming 0-6).
- Should the auto-generated PRs from the scraper and wayback scripts have an `auto-merge` designation applied to them (i.e. `gh pr create ... --label "auto-merge"`), or are you manually inspecting them?

## Verification Plan

### Automated Tests
- N/A

### Manual Verification
- We will trigger an ad-hoc action from `.github/workflows/idaho-leg-scraper.yml` to confirm a PR generates without any `Protected branch hook declined` strings. 
- We will open Obsidian (or inspect its local properties) to verify `dayIndex` retention is functional post workspace refresh.
