# Adobe User Cache-State Quarantine

Date: 2026-07-03

Purpose: Quarantine high-confidence user-level Adobe media cache, CEP/CSXS cache, logs, WebKit state, and saved application state while preserving Acrobat and user content folders.

Moved into this quarantine:

- `/Users/logan/Library/Application Support/Adobe/Common/Media Cache Files`
- `/Users/logan/Library/Application Support/Adobe/Common/Media Cache`
- `/Users/logan/Library/Application Support/Adobe/Common/Peak Files`
- `/Users/logan/Library/Application Support/Adobe/Common/Team Projects Cache`
- `/Users/logan/Library/Application Support/Adobe/Common/Team Projects Local Hub`
- `/Users/logan/Library/Application Support/Adobe/Premiere Pro`
- `/Users/logan/Library/Application Support/Adobe/dynamiclinkmediaserver`
- `/Users/logan/Library/Caches/CSXS`
- `/Users/logan/Library/Caches/Adobe_CCXProcess.node`
- `/Users/logan/Library/Caches/Adobe`
- `/Users/logan/Library/Caches/com.adobe.Photoshop`
- `/Users/logan/Library/Caches/com.adobe.PremierePro.14`
- `/Users/logan/Library/Caches/com.adobe.PremiereRush1.5`
- `/Users/logan/Library/Caches/com.adobe.InDesign`
- `/Users/logan/Library/Caches/com.adobe.illustrator`
- `/Users/logan/Library/Caches/com.adobe.lightroomCC`
- `/Users/logan/Library/Caches/com.adobe.ame.application.14`
- `/Users/logan/Library/Logs/CreativeCloud`
- `/Users/logan/Library/Logs/CSXS`
- `/Users/logan/Library/Logs/AdobeDownload`
- `/Users/logan/Library/Logs/AdobeVulcan`
- `/Users/logan/Library/Logs/Adobe Illustrator 24`
- `/Users/logan/Library/Saved Application State/com.adobe.InDesign.savedState`
- `/Users/logan/Library/Saved Application State/com.adobe.Photoshop.savedState`
- `/Users/logan/Library/Saved Application State/com.adobe.PremierePro.14.savedState`
- `/Users/logan/Library/Saved Application State/com.adobe.PremierePro.CC12.savedState`
- `/Users/logan/Library/Saved Application State/com.adobe.PremiereRush1.5.savedState`
- `/Users/logan/Library/Saved Application State/com.adobe.ame.application.14.savedState`
- `/Users/logan/Library/Saved Application State/com.adobe.lightroomCC.savedState`
- `/Users/logan/Library/WebKit/com.adobe.InDesign`
- `/Users/logan/Library/WebKit/com.adobe.Photoshop`
- `/Users/logan/Library/WebKit/com.adobe.PremierePro.14`
- `/Users/logan/Library/WebKit/com.adobe.ccd.helper`
- `/Users/logan/Library/WebKit/com.adobe.illustrator`
- `/Users/logan/Library/WebKit/com.adobe.lightroomCC`

Preserved:

- `/Users/logan/Library/Application Support/Adobe/Acrobat`
- `/Users/logan/Library/Application Support/Adobe/AcroCef`
- `/Users/logan/Library/Application Support/Adobe/com.adobe.ARMDCHelper`
- `/Users/logan/Library/Application Support/Adobe/OOBE`
- `/Users/logan/Library/Application Support/Adobe/Creative Cloud Libraries`
- `/Users/logan/Creative Cloud Files`
- `/Users/logan/Creative Cloud Files  avid4@idahoptv.org A5AC8FDA59D3C96E0A495C84@AdobeID`

Post-check:

- This quarantine measured about `27G`.
- `/Users/logan/Library/Application Support/Adobe` dropped from about `43G` to about `18G`.
- The remaining large user Adobe support folder is `/Users/logan/Library/Application Support/Adobe/Creative Cloud Libraries` at about `17G`; it was left for human review.
- Live Adobe launch/process state remained Acrobat-only.

Restore by moving paths back to their original locations.
