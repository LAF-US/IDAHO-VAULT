# Adobe Service-Layer Quarantine

Date: 2026-07-03

Purpose: Quarantine the non-Acrobat Adobe service layer while preserving Adobe Acrobat DC, Acrobat Distiller, Adobe Acrobat Reader, and Acrobat ARMDC helper/update support.

Preserved:

- `/Applications/Adobe Acrobat DC/Adobe Acrobat.app`
- `/Applications/Adobe Acrobat DC/Acrobat Distiller.app`
- `/Applications/Adobe Acrobat Reader.app`
- `/Library/LaunchAgents/com.adobe.ARMDCHelper.cc24aef4a1b90ed56a725c38014c95072f92651fb65e1bf9c8e43c37a23d420d.plist`
- `/Library/LaunchDaemons/com.adobe.ARMDC.Communicator.plist`
- `/Library/LaunchDaemons/com.adobe.ARMDC.SMJobBlessHelper.plist`
- `/Library/PrivilegedHelperTools/com.adobe.ARMDC.Communicator`
- `/Library/PrivilegedHelperTools/com.adobe.ARMDC.SMJobBlessHelper`

Disabled / booted out where present:

- `gui/501/com.adobe.AdobeCreativeCloud`
- `gui/501/com.adobe.ccxprocess`
- `gui/501/com.adobe.GC.Scheduler-1.0`
- `gui/501/com.adobe.AAM.Updater-1.0`
- `system/Adobe_Genuine_Software_Integrity_Service`
- `system/com.adobe.acc.installer.v2`

Moved into this quarantine:

- `/Library/LaunchAgents/com.adobe.AdobeCreativeCloud.plist`
- `/Library/LaunchAgents/com.adobe.ccxprocess.plist`
- `/Library/LaunchAgents/com.adobe.GC.Invoker-1.0.plist`
- `/Library/LaunchDaemons/com.adobe.acc.installer.v2.plist`
- `/Library/LaunchDaemons/com.adobe.agsservice.plist`
- `/Library/PrivilegedHelperTools/com.adobe.acc.installer.v2`
- `/Applications/Utilities/Adobe Application Manager`
- `/Applications/Utilities/Adobe Sync`
- `/Applications/Utilities/Adobe Genuine Service`
- `/Library/Application Support/Adobe/AdobeGCClient`
- `/Library/Application Support/Adobe/Adobe OS Extension`
- `/Library/Application Support/Adobe/Adobe Desktop Common`
- `/Library/Application Support/Adobe/Creative Cloud Libraries`
- `/Users/logan/Library/LaunchAgents/com.adobe.AAM.Updater-1.0.plist`
- `/Users/logan/Library/LaunchAgents/com.adobe.GC.Invoker-1.0.plist`

Post-check:

- Live Adobe launch roster only showed Acrobat helper/update launch items.
- Process list only showed Acrobat `AdobeResourceSynchronizer`.
- Acrobat DC and Reader still reported version `26.001.21563`.

Notes:

- The large user-level Adobe media/cache payloads under `/Users/logan/Library/Application Support/Adobe` were not moved in this pass.
- Creative Cloud Files folders were not touched.
- This quarantine is reversible by moving paths back to their original locations with administrator privileges where needed.
