# Adobe Launchpad Cleanup

Date: 2026-07-03

Purpose: Remove stale non-Acrobat Adobe icons from Launchpad after the Adobe service-layer quarantine.

Launchpad DB backup:

- `/Users/logan/.local/state/startup-cleanup/2026-07-03-adobe-launchpad-cleanup/Launchpad-DB-Backup/db.before-adobe-launchpad-cleanup`

Removed Launchpad rows:

- `AAM Registration Notifier` / `com.adobe.AAMRegistrationNotifier` (2 rows)
- `AASIapp` / `com.adobe.AASIapp`
- `AdobeGCClient` / `com.adobe.gcclient`
- `AdobeIPCBroker` / `com.adobe.AdobeIPCBroker`
- `Core Sync` / `com.adobe.accmac`
- `Setup` / `com.adobe.Installers.Redirector` (2 rows)
- `Uninstall Product` / `com.Adobe.Uninstall Product` (2 rows)
- `adobe_licutil` / `com.adobe.adobe_licutil` (3 rows)
- `AdobeCleanUpUtility` / `GoCart.gcuninstaller`

Preserved Launchpad rows:

- `Adobe Acrobat` / `com.adobe.Acrobat.Pro`
- `Acrobat Distiller` / `com.adobe.distiller`
- `Adobe Acrobat Reader` / `com.adobe.Reader`

Post-check:

- Launchpad DB showed only Acrobat-family Adobe rows.
- Dock was restarted by killing PID `591`; Dock relaunched as PID `12256`.
