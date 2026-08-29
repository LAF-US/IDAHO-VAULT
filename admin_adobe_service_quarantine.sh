#!/bin/zsh
set -u

Q="/Users/logan/.local/state/startup-cleanup/2026-07-03-adobe-service-quarantine"

move_path() {
  local src="$1"
  if [ -e "$src" ] || [ -L "$src" ]; then
    local dst="$Q$src"
    /bin/mkdir -p "$(/usr/bin/dirname "$dst")"
    /bin/mv "$src" "$dst"
  fi
}

# Stop/disable non-Acrobat Adobe service layer. Acrobat ARMDC helpers are intentionally left alone.
/bin/launchctl bootout system/Adobe_Genuine_Software_Integrity_Service 2>/dev/null || true
/bin/launchctl bootout system/com.adobe.acc.installer.v2 2>/dev/null || true
/bin/launchctl disable system/Adobe_Genuine_Software_Integrity_Service 2>/dev/null || true
/bin/launchctl disable system/com.adobe.acc.installer.v2 2>/dev/null || true

/bin/launchctl bootout gui/501 /Library/LaunchAgents/com.adobe.AdobeCreativeCloud.plist 2>/dev/null || true
/bin/launchctl bootout gui/501 /Library/LaunchAgents/com.adobe.ccxprocess.plist 2>/dev/null || true
/bin/launchctl bootout gui/501 /Library/LaunchAgents/com.adobe.GC.Invoker-1.0.plist 2>/dev/null || true
/bin/launchctl bootout gui/501 /Users/logan/Library/LaunchAgents/com.adobe.AAM.Updater-1.0.plist 2>/dev/null || true
/bin/launchctl bootout gui/501 /Users/logan/Library/LaunchAgents/com.adobe.GC.Invoker-1.0.plist 2>/dev/null || true
/bin/launchctl disable gui/501/com.adobe.AdobeCreativeCloud 2>/dev/null || true
/bin/launchctl disable gui/501/com.adobe.ccxprocess 2>/dev/null || true
/bin/launchctl disable gui/501/com.adobe.GC.Scheduler-1.0 2>/dev/null || true
/bin/launchctl disable gui/501/com.adobe.AAM.Updater-1.0 2>/dev/null || true

move_path "/Library/LaunchAgents/com.adobe.AdobeCreativeCloud.plist"
move_path "/Library/LaunchAgents/com.adobe.ccxprocess.plist"
move_path "/Library/LaunchAgents/com.adobe.GC.Invoker-1.0.plist"
move_path "/Library/LaunchDaemons/com.adobe.acc.installer.v2.plist"
move_path "/Library/LaunchDaemons/com.adobe.agsservice.plist"
move_path "/Library/PrivilegedHelperTools/com.adobe.acc.installer.v2"

move_path "/Applications/Utilities/Adobe Application Manager"
move_path "/Applications/Utilities/Adobe Sync"
move_path "/Applications/Utilities/Adobe Genuine Service"

move_path "/Library/Application Support/Adobe/AdobeGCClient"
move_path "/Library/Application Support/Adobe/Adobe OS Extension"
move_path "/Library/Application Support/Adobe/Adobe Desktop Common"
move_path "/Library/Application Support/Adobe/Creative Cloud Libraries"

move_path "/Users/logan/Library/LaunchAgents/com.adobe.AAM.Updater-1.0.plist"
move_path "/Users/logan/Library/LaunchAgents/com.adobe.GC.Invoker-1.0.plist"

/usr/sbin/chown -R logan:staff "$Q" 2>/dev/null || true
