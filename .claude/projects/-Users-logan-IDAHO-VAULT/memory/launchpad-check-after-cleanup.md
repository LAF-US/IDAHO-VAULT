---
name: launchpad-check-after-cleanup
description: "Logan wants a Launchpad sanity check at the end of every app-cleanup pass on the Mac"
metadata:
  type: feedback
---

At the end of each cleaning/uninstall loop on the MacBook, run a Launchpad sanity
check — removed apps commonly leave ghost icons behind.

**Why:** Deleting an .app does not always update Launchpad's database, so the icon
lingers and clicking it fails. Logan asked for this as a standing step (2026-08-18).

**How to apply:** Look for a UUID-named Launchpad DB in
`~/Library/Application Support/Dock/*.db` and check its `apps` table for bundle IDs
that no longer resolve. If the DB is absent, Launchpad rebuilds itself from
`/Applications` and no ghosts are possible. To force a rebuild:
`defaults write com.apple.dock ResetLaunchPad -bool true && killall Dock`
(this resets custom Launchpad arrangement). See [[macbook-hardware-ceiling]].
