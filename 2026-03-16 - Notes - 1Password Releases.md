---
source: "https://releases.1password.com/windows/stable/#changelog"
author:
  - "[[Dave]]"
published: 2026-03-16
created: 2026-03-30
---
![1Password 8 for Windows](https://releases.1password.com/windows/stable/HeroUnlocked.png)

1Password 8 for Windows

[Download 1Password for Windows](https://downloads.1password.com/win/1PasswordSetup-latest.msixbundle)

The [1Password Support Community](https://www.1password.community/?utm_source=releasenotes) 💌 is a great place to leave feedback and discuss changes with the team.

Subscribe to the [RSS feed](https://releases.1password.com/windows/stable/index.xml) for 1Password for Windows release notes.

---

### What's new

- We’ve fixed an issue that could prevent the app from opening and cause a blank screen or error message.!35848

- You can now connect additional browsers installed outside of `C:\Program Files`, making it easier to use browsers installed at the user level.
- We’ve fixed an issue that could cause the 1Password app to crash for some customers enforcing settings through an MDM solution. #PA-852!35562
- We’ve fixed an issue where a list of your SSH keys could be returned in an incorrectly sorted order.!35625
- The setting to use system accent colors has been removed in order to offer a more consistent design experience. #KNOX-615!35307

- We’ve improved error handling when 1Password first opens to prevent the app from displaying a blank screen.

- We’ve improved localization for a number of our supported languages. If you’d like to suggest a localization improvement, [contact 1Password Support](https://1password.com/contact-support).!34965!34966!35028
- We’ve fixed an issue where the Windows Hello prompt could appear behind other windows or seem unresponsive. #DV-446!34963
- We’ve fixed an issue where the multi-factor authentication prompt could be missing when trying to unlock the app. #AUTH-2056\] \[#AUTH-2005!35083
- If you load an empty `.env` file in **Developer** > **Environments**, it will now show a message saying no variables were found. #DG-7!35144
- We’ve fixed an issue that could cause 1Password to crash when you signed in to a device. #PA-346!35258
- We’ve fixed an issue that could block in-app updates if the MDM setting for automatic updates was enabled for MSI installs. #PA-941!35295

- 1Password now supports a wider set of custom trusted browsers on Windows. #PA-901!34408
- We’ve added a new developer setting to enable SDK integrations, so you can authenticate SDKs with authorization prompts from the 1Password desktop app. #39275
- We’ve fixed an issue where a prompt to turn on two-factor authentication couldn’t be selected. #AUTH-160!34473
- We’ve fixed an issue where the Windows Hello prompt could appear behind other windows or seem unresponsive. #DV-446!34963

- We’ve fixed an issue where Windows Hello prompts could appear behind app and browser windows. #RO-800

- We’ve Fixed an issue with an unclickable prompt when being asked to enable two-factor authentication during sign-in.!34473
- You now only see the Windows Passkeys setup prompt if an unlocked account has the setting “Passkey item support” enabled. #FS-4434!34387
- We’ve improved localization for a number of our supported languages. If you’d like to suggest a localization improvement, [contact 1Password Support](https://1password.com/contact-support).!34435!34438!34441
- We’ve added settings to reduce lag and choppy performance on some high refresh rate G-SYNC monitors. #PA-874!34142
- We’ve fixed intermittent connection issues between the MSIX version of 1Password for Windows and the browser extension. #PA-878!34036
- We’ve fixed an issue where `op-ssh-sign-wsl.exe` could fail to translate Windows Subsystem for Linux (WSL) paths to Windows paths, causing Git commit signing to fail in WSL. #PA-883!34113
- We’ve fixed an issue where one-time password fields from Bitwarden login items didn’t import correctly. #SET-12!34140
- We’ve updated the account icon shown in the authentication prompt when using the CLI or SDK desktop app integrations to have rounded corners.!34185
- We’ve fixed an issue where the step to download the 1Password extension was missing from Guided Setup for individual and family accounts. #SET-344!34198
- We’ve fixed an issue where selecting the **Create vault** button multiple times could cause multiple vaults to be created. #DA-1725!34305
- We’ve fixed an issue where items containing files could be duplicated or moved into accounts where file storage was turned off. #DA-1723!34342
- We’ve fixed an issue that prevented ADMX templates from being ingested and applied in Microsoft Intune. #PA-895!34518

- We’ve fixed an issue that caused the 1Password app to become unresponsive for 30 seconds after you turned on passkey support.

- You can now [connect additional browsers](https://support.1password.com/additional-browsers/?windows) to 1Password under **Settings** > **Browser** > **Add Browser**.
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!33713!33789!33830
- We’ve fixed an issue on Windows 10 where 1Password would always open on startup if you used the MSIX installer, even if you set it as hidden. #PA-872!33851

- If duplicates are detected when you import environment variables, you can now choose to ignore, overwrite, or keep both. #DG-70!33012
- When you view an Environment in 1Password, updated wording now distinguishes between temporarily revealing variables and changing their default visibility. #DG-43!33057
- Large Type no longer disappears when the display zoom is set above 100%. #DA-106!32944
- We’ve fixed an issue that caused comma-separated URLs in code blocks within Secure Notes to change when you saved them. #DA-19!33266
- In-app updates are now blocked for MSIX system-wide installs and Microsoft Intune-managed deployments to avoid issues tracking 1Password’s install state, update failures, and de-provisioning. #PA-859!33354

- There are new unlock settings and presets available for the 1Password app, including **Unlock with device**. You can manage these settings in the app under **Settings** > **Security**.
- You can now use, save, and sync passkeys across devices using 1Password as a third-party passkey provider. To get started, make sure you’ve [installed the MSIX version of 1Password](https://support.1password.com/cs/1password-msix-installer/#what-to-know).
- We’ve added group policy support using ADMX templates. #PA-844!32934
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!32874!32914
- We’ve fixed an issue where 1Password would open in front of other windows after a silent MSIX update. #PA-848!33000

- You now see breadcrumb navigation on the SSH Agent and CLI pages. #DG-18!32687
- We’ve made visual improvements to the background of the sidebar, authorization prompt, and Quick Access.!32726
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!32590!32802!32801!32632
- We’ve fixed an issue that could prevent you from unlocking the app if it was closed during sign-in. #FRAM-11!32618
- Icons now load significantly faster across 1Password. #38351!32684
- You now see a more accurate progress bar for Guided Setup.!32729
- We’ve fixed an issue where the initial launch when you opened the app was affected by network conditions.!32741
- We’ve fixed an issue where some non-resizable windows could get stuck in large sizes.!32803

- We’ve made visual improvements to the 1Password system tray icon. #40246!32495
- We’ve made visual improvements to the 1Password taskbar icon for the MSIX app. #40245!32494
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!32539!32552
- We’ve fixed an issue where date formatting was lost when you copied and pasted from a date field. #38653!32479

- 1Password can now stay unlocked for more than 40 minutes when biometry is disabled by admin policy, and we’ve improved the resilience of authenticated sessions overall. #32197
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!16511!32126!32167
- You can now press `Enter` to submit creating, renaming, and deleting Developer Environment forms. #36512!32329
- You can now select the drag-and-drop area on the Developer Environments page to import a variable. #40062!32330
- We’ve fixed an issue where the MSI install could fail for some users due to an unsigned script. #40153!32462
- We’ve fixed an issue that could cause a Windows Hello prompt to appear when you uninstalled 1Password. #39933!32157

- JSON Web Tokens stored in concealed item fields can now be decoded and viewed. #35434!31573
- We’ve added breadcrumbs to the Developer Environment pages to improve navigation. #38953!32010
- Previous versions of 1Password Developer Environment variables can now be viewed and restored. #39335!32181!32107
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!32044!32012!31985
- We’ve fixed an issue where MDM-managed devices couldn’t unlock the app with approved biometric methods. #36642!31866
- The taskbar icon now displays correctly in light mode for the MSIX version of 1Password for Windows. #39729!31989
- We’ve fixed an issue where a banner for an app update was shown incorrectly when you used the App Installer. #39815!32046
- The “Scan QR code” button now works as expected when you create or edit an item. #39060!32108
- We’ve fixed an issue where an account password and Secret Key prompt appeared incorrectly when you changed the email address of an SSO account. #39875!32119
- We’ve fixed an issue that could cause the MSI installer to fail. #40153!32462

- The “Sign in with \[your identity provider\]” button now works as expected when you try to reauthenticate your account using SSO in the app.!35399
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!31596!31694!31597!31834
- We’ve fixed an issue where selecting the back button after saving edits to Developer environment variables caused an extra empty field to appear. #38291!31602
- We’ve fixed an issue where you could get multiple re-authentication prompts if your SSO email was changed. #39344 #39345!31816
- We’ve fixed an issue where the sorting for an item list wasn’t maintained after you navigated away from the list. #38821!31578
- We’ve updated our dependencies to fix some bugs and improve the app’s stability.

- Localization has been improved for a number of our supported languages using new translations from Crowdin.!31426!31251!31250!31422
- The SSH agent now suppresses approval prompts for requests from background applications regardless of the “Remember key approval” setting. #38748!31240
- We’ve fixed an issue where SSO users were unable to unlock their accounts after an email change. #35758!31307
- We’ve fixed an issue with incorrect banners saying Git commit signing must be reconfigured.!31387
- We’ve fixed an issue where you’d see an error if you selected “View” from the “Restore item” prompt. #39058!31453

- Localization has been improved for a number of our supported languages using new translations from Crowdin.!31215!31214
- We’ve fixed an issue where the “Item created in \[vault name\]” notification could incorrectly appear after editing an item. #38685!31237
- We’ve fixed an issue where 1Password would suggest to save a new passkey in existing login items, potentially causing some passkeys to be incorrectly overwritten. #38754!31241

- Localization has been improved for a number of our supported languages using new translations from Crowdin.!30882
- We’ve added op-ssh-sign-wsl.exe for WSL integration with MSIX. #38242!31029
- op-ssh-sign can now also sign non UTF-8 payloads.!31003
- We’ve fixed an issue where shortcuts and quick actions in Quick Access didn’t work properly. #38465!31005

- Localization has been improved for a number of our supported languages using new translations from Crowdin.!30581!30645
- The message you see when you encounter an unrecoverable error is now easier to understand. #23149!30689
- We’ve fixed an issue for family organizers and administrators where the Shared vault could appear twice in the list of vaults for some people in the Manage Accounts screen. #35806!30340
- We’ve fixed an issue that could prevent you from viewing documents that didn’t upload correctly. #38178!30819
- We’ve fixed an issue where search results would show missing lines in an item if the line contained an accented version of one of the search terms. #38070!30796

- Localization has been improved for a number of our supported languages using new translations from Crowdin.!30328!30549
- We’ve updated some wording in the Autofill Behavior menu. “Only fill on this exact domain” is now “Only fill on this exact host”, and ports are now included in the description. #26458

- You’ll now see separate tabs for SSH Keys, Bookmarks, and Activity Log under **Developer** > **SSH Agent** in the app. #37257!30136
- You’ll now see separate tabs for Get Started and Activity Log under **Developer** > **CLI** in the app. #37264!30160
- When you select **New Item** > **Login**, the focus will now default on the title. #34260!30216
- We’ve fixed an issue where focus would shift between date fields. #37107!30098
- The date picker now uses localization for date format only, and not for language. #28051!30133
- We’ve fixed an issue where Developer Watchtower onboarding didn’t fill the full app window. #37654!30254
- We’ve fixed an issue where a tag could be deleted if you selected **Rename Tag**, didn’t make any changes, then you selected **Save**. #37480!30252

- You can now use, save, and sync passkeys across devices using 1Password as a third-party passkey provider. To get started, make sure you’ve installed the [MSIX beta](https://www.1password.community/discussions/1password/beta-release-new-msix-installer-for-1password-for-windows/155230).
- We’ve added a new setting, “Autofill username when creating a new login”, under **Settings** > **General**. When turned off, 1Password won’t autofill the username field for new items created manually in the app. #657!29868
- We’ve fixed an issue where you could incorrectly be notified of an app update. #37396
- We’ve fixed an issue where the wrong item list was shown when selecting the “View” button after deleting or archiving an item. #37217
- We’ve fixed an issue where the MSI installer could sometimes ignore the option to disable in-app updates. #37450!30027
- We’ve fixed an issue that could cause individual account names to appear twice in the Profile view. #37472!30062

- You now see an error message if you try to import items in a shared collection from Bitwarden. #36165
- We’ve fixed an issue that could cause search errors in non-English languages. #36272

- We’ve released version 8.10.75 to fix an issue with the release deployment of version 8.10.74. Both versions contain the same improvements to the 1Password app.
- Family account owners now see a prompt to invite family members in Guided Setup. #35005!28124
- We’ve made visual improvements to the Developer pages so they no longer use the full width of the app on larger displays. #36656!29333

- Family account owners now see a prompt to invite family members in Guided Setup. #35005!28124
- We’ve made visual improvements to the Developer pages so they no longer use the full width of the app on larger displays. #36656!29333

- The MSI installer now supports in-app updates, turned on by default. Administrators can turn them off during deployment using `MANAGED_UPDATE=1`. #36156
- MSI deployments can now use the `MANAGED_INSTALL=1` flag to remove per-user 1Password installs. #33193
- We’ve improved the reliability of the connection between the app and browser extension.!29149
- We’ve fixed an issue that prevented 1Password from opening after updates were deployed with the MSI installer. #27597
- We’ve fixed an issue where 1Password wouldn’t unlock after a new user was confirmed in the app. #31549
- We’ve fixed an issue where using “Open and Fill” in the app could cause websites to reload repeatedly. #36284

- We’ve made general improvements and fixed various bugs for a better 1Password experience.

- If you’re an administrator, you can now view an Item Usage report by going to an item’s details and selecting **More options** > **Go to Item Usage Report**. #35199!28456
- You can now select the **Help** button beside the New Item button to find additional resources, like tutorial videos, the community forum, and latest releases.!28202

- You can now add locations to your items and see them on the Home screen of 1Password mobile apps when you’re nearby.
- We’ve added default expiry alerts based on the category of an item. #34229
- If you have 6 or more keys enabled in the SSH agent, you’ll see a warning callout in the SSH Agent page about [too many authentication failures](https://developer.1password.com/docs/ssh/agent/advanced#ssh-server-six-key-limit). #35398
- You can now configure a custom command to open bookmarked SSH URLs.!28118
- We’ve added passkey and location search filter suggestions. You can see these when you enter an equals sign “=” in the search bar. #34965
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!28091
- We’ve made improvements to username suggestions. If you have an Identity item saved in your vault, the email address from that item will be your suggested username.!28179
- We’ve fixed a rare issue where the SSH agent failed to start on Windows. #29999

- Localization has been improved for a number of our supported languages using new translations from Crowdin.!27851!28073
- We’ve fixed a typo in the placeholder text for countries with a postal code in their address format. #34369!27878
- We’ve made visual improvements to the graphic on the Watchtower card for recovery codes. #35129!27974
- We’ve improved the visual quality of Wi-Fi sharing QR codes. #34656!28074
- The date field in item details now only allows you to input numbers. #19450!27782

- You can now import items from Bitwarden using the 1Password app.
- Guided Setup is now only shown for accounts that have been active for under six months. #34559!27686
- Guided Setup is now automatically dismissed when you complete all the tasks. #34561!27697
- In [Labs](https://support.1password.com/labs/), you can now enter `=location` in the search bar to find items that have a location in their item details.!27590
- We’ve fixed an issue where using a template with no fields could create an item stuck in the Offline Changes section. #33011!27634
- We’ve fixed an issue that caused broken links in Watchtower “Compromised website” banners. #34578!27699
- We’ve fixed an issue where the “Change password on website” button could open an incorrect URL. #34685!27701 #27750!27818
- We’ve fixed an issue that could prevent Watchtower from updating and displaying categories correctly. #34768!27746
- We’ve fixed an issue where you couldn’t remove an item from the list of ignored alerts. #32513!27854
- Localization has been improved for a number of our supported languages using new translations from Crowdin. #27809 #27811
- We’ve fixed an issue where guest accounts, which don’t support recovery keys, could still see recovery options. #34592!27681
- We’ve fixed an issue where you’d still see the option to “Open and fill” a password, even if you had AutoFill set to “Never fill on this website”. #24696!27657
- Multiple installations of 1Password no longer conflict. Now, only one instance can be launched at a time. #34038!27663

- You can now set up expiry alerts for items. In edit mode, select “+add more” > “Date”. After setting the expiry date, select “Set expiry alert” and choose an alert schedule from the dropdown menu.
- Localization has been improved for a number of our supported languages using new translations from Crowdin. #27164 #27155
- The commit signing helper for WSL (op-ssh-sign-wsl) can now be used on Windows ARM64.!27310
- You can now search for passkeys. Enter `=passkey` in your search bar to view all your items that contain a passkey. #30066
- When you select a password strength from Watchtower’s Overall Password Strength bar, you’ll now see a list of items with that password strength. #14056
- Label fields are now left blank if you don’t add a custom label. #33629
- You’ll now see a loading indicator when you sign in to a single sign-on (SSO) or passkey account on the desktop app. #34291
- The LastPass importer can now handle newer private key encodings. #34286
- We’ve made improvements to the sizing options for the “create new vault” pop-up. #33919
- We’ve fixed an issue where some of the Watchtower scores could be cut off. #23028
- We’ve fixed an issue where the same item could appear in both regular search and smart search results in quickfind. #27168
- We’ve fixed an issue where a file could be lost if an item was moved during the upload. #24336
- We’ve fixed an issue where some words weren’t fully highlighted when searched in Secure Notes. #30603
- We’ve fixed an issue in the SSH agent where connecting to older SSH servers (OpenSSH < 7.2) with an RSA key would fail!27252
- We’ve fixed an issue where spaces were not properly formatted after a Secure Note was saved. #34364 #17312
- We’ve fixed an issue where release channels couldn’t be changed in the app for business accounts with a release channel policy. #34499
- We’ve fixed an issue where recently deleted item lists could change order. #33961
- We’ve fixed an issue where you wouldn’t see a dialog when a 1Password app version had expired and needed to be updated.!27538
- Concealed fields (like password and credit card) are now shown in edit mode when “Always show passwords and full credit card numbers” is turned on in Settings > Security. #12863 #34593
- We’ve fixed an issue where a plus symbol didn’t format correctly when used as a bullet point in Secure Notes. #25808
- We’ve fixed an issue where older fields in 1Password 7 wouldn’t show their entire contents. #33620
- We’ve fixed an issue where the timestamp for an item wouldn’t update after it was archived. #34618
- We’ve fixed an issue with searching for accented characters when linking a related item. #23582
- We’ve fixed an issue where a Right-Shift keybind could be triggered in Discord when 1Password was unlocked.!27597!27313

- Guided Setup is now only shown for accounts that have been active for under two years.
- SSH keys in the PKCS#8 format that are encrypted with 3DES can now be imported.
- We’ve made visual improvements to the “Sign in with Identity Provider” prompt. #22611
- You’ll now see a descriptive error message if you try to export when you’re offline. #33645
- Username suggestions are now based on the vault that you’re creating a new item in.
- You can now search within search results. #30188
- We’ve made visual improvements to the SSH and CLI Activity Logs.
- We’ve fixed an issue where Secure Notes weren’t displayed properly when Markdown formatting was turned off in Settings. #33725
- When you export SSH private keys or public keys, you can now choose the desired name and location. #13268
- The Developer Activity Log can now be viewed with more than 10 entries and includes filter options. #33229
- You’ll now see “Connect” when you hover over ssh:// URls on items. #33773
- We’ve made some visual improvements to the Developer experience pages (SSH Agent, CLI, Developer Watchtower). #33513
- We’ve fixed an issue where empty Document items could cause an export to fail with the error message “Export failed check your internet connection and try again”. #32588
- If you have your language set to Deutsch, you’ll now see a “Dismiss” button on the “1Password is trying to unlock the browser extension” prompt.
- We’ve fixed an issue where archived and deleted items were sometimes included in search results. #34075
- We’ve fixed an issue where you weren’t able to rename nested tags. #16417
- We’ve fixed an issue where the Guided Setup progress shown on your Home screen didn’t match your actual progress. #33467
- You’ll now see an alert if you try to dismiss the import items prompt while offline. #34133
- We’ve fixed an SSH agent issue that caused JetBrains IDEs to ask for approval for each SSH request. #33404
- We’ve resolved an issue where the LastPass importer couldn’t decode newer private keys. #34286
- We’ve fixed an issue where you couldn’t connect to older SSH servers (OpenSSH 7.2 or earlier) with RSA keys when using the SSH agent.!27252

- 1Password can now remember tag selection when reopening the app. #27370
- We’ve fixed an issue where some features being gradually released or enabled through Labs were unavailable in the app. #32828
- Localization has been improved for a number of our supported languages using new translations from Crowdin.
- We’ve added an “Other Options” dropdown to the “Set Up Another Device” screen. You’ll now see the option to use an automatic sign-in link or view account details. #32184
- The LastPass importer can now recover from failed imports and reuse already imported folders. #33702
- You’ll now see a notification when your items are about to expire. #26616
- We’ve made visual improvements to the found accounts list on the Sign In page. #32938
- We’ve made visual improvements to the Developer Activity Log code blocks. #32925
- When you turn off the SSH Agent, you’ll no longer see the number of available SSH keys. #33464
- We’ve fixed an issue where language settings wouldn’t save during your first sign in. #33239
- We’ve fixed an issue where plain text notes wouldn’t show line breaks.!26701
- You’ll now be able to fill your passwords with Auto-Type on the command line.!26453

- You can now delete SSH keys directly from the Developer Watchtower. #33234
- We’ve made visual improvements to the Welcome page. #25037
- We’ve made improvements to the category and website search results in the “+ New item” page. #33029 #33029
- We’ve simplified the item creation process by displaying fewer categories when you select “+ New item” in the app. #33026
- Localization has been improved for a number of our supported languages using new translations from Crowdin.
- We’ve fixed an issue where you could get an error if you tried to search 1Password with the search bar empty.
- We’ve fixed an issue where you could get an error if you tried to sign in to the app with SSO. #32331
- We’ve fixed an issue where some features being gradually released or enabled through Labs were unavailable in the app.

- When you export or copy an SSH key with a passphrase, the passphrase is now automatically included with the SSH Key item. #32674
- We’ve improved the message you see when you try to leave the recovery code setup or replacement process. #29284
- We’ve made visual improvements to the empty “Items in wrong account” Watchtower list. #27275
- We’ve improved the wording for the require password settings. #32631
- We’ve fixed an issue where you wouldn’t see search highlighting for secure notes when the “Format secure notes using Markdown” setting was turned off. #30979
- We’ve fixed an issue where the Auto-lock policy wasn’t reflected correctly in the app. #32977
- We’ve made visual improvements to the device enrollment prompt. #32972
- We’ve fixed a visual issue on the lock screen where icons weren’t rounded. #30875
- The 1Password Developer experience is now available in the sidebar, which helps you discover, configure, and use our bundle of tools designed to simplify security of developer credentials. To enable the experience, navigate to Settings > Developer and select “Show 1Password in the sidebar.”
- You’ll now be able to use OneLogin as an SSO provider in the LastPass importer. #33126
- Watchtower now remains selected in the sidebar when you navigate to one of the Watchtower lists, like Password Strength or Vulnerable Passwords. #14254
- We’ve made visual improvements to the Watchtower item menu. #13284
- The Lastpass importer will now use the same redirect URL regardless of which SSO provider you use during the import.
- We’ve fixed an issue where vault and device text were shortened unnecessarily. #26594
- We’ve fixed an issue where the “Sign in with Okta” page could remain after you successfully signed in. #32648
- We’ve fixed an issue where if you right-clicked any account in Manage Accounts > Accounts, it highlighted the top account. #31231
- We’ve added self-update support to the Windows ARM version of 1Password. #32082

- We’ve added support to display auto-lock policies in days or weeks in the app. #32843
- We’ve improved how VoiceOver reads the Watchtower page. #25535 #25443
- Localization has been improved for a number of our supported languages using new translations from Crowdin.
- We’ve removed mention of “desktop app” from the Security Settings in Safari on iOS. #27532
- We’ve fixed an issue where searching in Labs could disrupt the grouping of available features for testing. #32708

- You can now sign in to 1Password securely by using a QR code. This simplifies the process of setting up new devices without needing to manually enter your account password or Secret Key.
- Guided Setup is now available for Individual and Family accounts. You’ll be able to use the step-by-step guide to help you set up autofill, practice the basics, import your passwords, and access your passwords everywhere.
- You can now view item history and restore previous versions of items in the desktop apps. #27574
- When confirming your recovery code, you can now select and drag text into the “Enter your recovery code” field. #32510
- We’ve added arrow symbols next to accounts on the Manage Accounts screen to indicate they can be clicked. #31322
- We’ve made improvements to the sidebar so screen readers can announce the current selection. #31040
- The “Your Details” heading now wraps words that are too long. #24252
- Localization has been improved for a number of our supported languages using new translations from Crowdin.
- We’ve removed the import and extension pages from the essential setup flow. #31389
- When installing the app, the MSI now removes previous user installs to prevent potential disruptions in functionality. #28662 #28552
- We’ve added localization support for the memorable password generator. #30248
- We’ve made visual improvements to the Watchtower Overall Password Strength meter. #15612
- We’ve made visual improvements to the Watchtower banners you see in your items. #27061
- We’ve updated the wording from “Feedback and Support” to “Support Community” in the Help button dropdown. #31477
- We’ve improved the message you see when you try to leave the recovery code setup or replacement process. #29284
- We’ve made visual improvements to the guided sign-in screens. #32363 #31694
- We’ve fixed an issue where you couldn’t cancel while importing items. You’ll now see the “Importing Items” screen until the import is completed. #32476
- We’ve fixed an issue where 1Password could return to the foreground while you were using the extension. #31951
- We’ve fixed an issue where if you had multiple accounts, an account with the auto-lock setting enabled could lock the app even if that account wasn’t unlocked. #32168
- We’ve fixed an issue where 1Password could return to the foreground while you were using your browser. #32186
- We’ve fixed an issue where the “Set Up Another Device” screen didn’t show your selected account in the account dropdown. #31833
- We’ve fixed an issue where search filters wouldn’t work for categories or tags that contained spaces (for example, secure notes). #15420
- We’ve fixed an issue where 1Password could fail to start due to an issue reported by Windows' Device Guard. #32427
- We’ve fixed an issue where you couldn’t see the password history for some item types. #17252
- We’ve fixed a visual issue where the Wi-Fi QR code didn’t fill the window when you selected “Open in new window”. #32509
- We’ve fixed an issue when importing from LastPass where private items were imported during a permissions-only import. #32515
- You’ll now see suggestions for open Windows apps in Quick Access.!22682

- We’ve fixed an issue where 1Password could fail to start due to an issue reported by Windows' Device Guard. #32427

We’re excited to share that we’ve updated the release number formatting for the 1Password browser extension! This change aligns our browser extension with the 1Password apps, so you’ll now see the same release number across all platforms. Plus, both the extension and apps will be released on the same date, for a consistent and streamlined experience.

- We’ve enhanced search capabilities to help you find items faster than ever.
- You can now search within a list of items, such as a vault or category. #29739 #29764 #29735
- We’ve made improvements to the item sharing experience.
- We’ve updated the preview image you see when you receive a shared item link. #27623
- Pending invitations are now included in the invite count shown by the Invite People banner. #29492
- You’ll now see a message in Settings > Security if your app’s auto-lock settings are managed by an account administrator. #31297
- We now save fields more reliably for credit cards and identity items. #29369
- The “Grant access to your account” message will now display the device name instead of the operating system when enrolling a trusted device. #29952
- If you’re a Guest user, you’ll no longer see the banner in the sidebar that prompts you to import your passwords or migrate data. #31147
- You can now import login items with encrypted URLs from LastPass. #31130
- We’ve made visual improvements to the Autofill Behavior options. #31011
- We’ve made accessibility improvements to the found accounts list on the Sign in modal. #9182
- We’ve made accessibility improvements to the contrast of the close button for the Sign In page. #27811
- You’ll now see the correct message on the the unlock screen when you’ve been locked out after multiple failed biometric sign-in attempts. #31367
- We’ve fixed an issue that prevented shared items from loading if there was content in the Notes field. #31318
- We’ve fixed a visual issue when you opened shared items where elements on the page were spaced too far apart. #31393
- We’ve fixed an issue in the search results where you’d see a dash in an item’s subtitle. #31354
- We’ve fixed an issue that prevented certain proxy types from connecting in 1Password. #31475

- Reduced the chances of all authenticated settings being reset due to old or invalid settings. #31311 #31863
- We fixed an issue where the 1Password app would steal focus from browser windows if the 1Password browser extension was installed but not signed in. #29392
- We fixed an issue where the “Connect with 1Password in the browser” setting could automatically turn back on after being turned off.!25121
- Settings are now reset after you reset 1Password from Advanced Settings or sign out of all accounts in the app. #24261!25173
- You can now import login items with encrypted URLs from LastPass. #31130

- We’ve temporarily removed the Setting Reset message to address edge cases.

- This release contains an important security update that enforces additional integrity protections for the setting file. [See the accompanying article for more information.](https://support.1password.com/kb/202408c/) #31863
- We’ve made visual improvements to the Wi-Fi sharing QR code. #30408
- We’ve fixed an issue where signing in with your Emergency Kit could take you out of the sign-in flow if the email address didn’t match, instead of prompting you to update the email address. #30387
- We’ve fixed an issue where search highlight could make links in items non-clickable. #29811
- You can now search “favorite” and “favorites” to find items. #28471
- Saving an item with the same password as before will no longer affect password history. #30584
- We’ve made accessibility improvements to tooltips. You’ll now be able to dismiss a tooltip without moving the mouse pointer and they are readable to screen readers. #27780
- We’ve added a loading spinner after a 3-second delay for slow internet connections when generating a sign-in QR code. #29889
- We’ve made visual improvements to the search in lists. #30745
- We’ve fixed an issue where you’d see unrelated notes when you opened an item from a search result. #29883
- You’ll now see the correct error message when you try to sign in to an account that is already added to your app. #29503
- We’ve improved the accessibility of tooltips in the app. #27777
- You’ll now see the option to share when you right-click an item in the apps. #22527
- We’ve moved Developer settings up higher in the Settings sidebar. #30707
- We’ve updated the accessibility labels for sidebar options in the app. #25431
- We’ve fixed an issue where importing permissions from a LastPass account caused duplicate vaults in 1Password. #30792
- We’ve added a link to the documentation for browser connection security in Settings > Browser. #30746
- We’ve updated some wording in the Migrate from 1Password 7 prompt. #31203
- If you’re using a guest account, you’ll no longer see the Profile section. #31149
- We’ve updated the sidebar background color to work better when when Dark Mode is turned on or off. #31184
- When you install 1Password 8 for the first time, you’ll no longer be prompted to migrate from 1Password 7. #29860

If you feel generous and have a couple of minutes, seeing your 1Password review on [GetApp](https://www.getapp.com/security-software/a/1password/) would be really cool.

- QR codes for Wi-Fi will now be generated in Wireless Router items! Family and friends can scan your QR code and automatically connect to your Wi-Fi network. You can manage your QR code display settings in Settings > Security in the 1Password app.
- You can now search for passkeys. #22295
- The “Last checked for updates on” date and time in Settings > About now uses the ICU format. #28065
- Uploading a new document to an existing document item no longer replaces the title. #15079
- The import guide will now be hidden if all of your unlocked accounts are frozen. #28674
- We’ve made improvements to the accessibility labels on the Lock Screen’s password field and the reveal/conceal buttons.
- We’ve added accessibility labels to the “Manage Accounts” and “Subscribe now” buttons.
- You’ll now only see the vault selection highlighted for Accounts and Vaults.
- We’ve made visual improvements to the prompts you see when you sign in on a new device. #28671
- Localization has been improved for a number of our supported languages using new translations from Crowdin.
- We’ve fixed an issue that could prevent an unusable recovery key from being shown in Account Management.
- We’ve fixed an issue where resizing the lock screen window could obstruct part of the Sign in with SSO button label. #29420
- You can now search within a list of items, such as a vault or category. #29739 #29764 #29735
- We’ve added a lock screen message explaining that biometric unlock is not available after multiple failed attempts. #23968
- The lock option will now be more visible in the menu bar. #29537
- You’ll now be able to import items using a CSV file from Chrome. We’ve also improved the import guides for Chrome, iCloud, and Safari to increase readability. #29899
- You’ll now see the total number of deleted items at the bottom of the list in Recently Deleted. #11719
- We’ve made accessibility improvements to the password generator. #27753 #27807
- We’ve made visual accessibility improvements to the toggle button in the password generator and the radio button in the Autofill Behavior dialog. #27817 #27757
- We’ve made visual accessibility improvements to the “Create” button for creating a new vault. #27783
- We’ve fixed an issue where closing a window during the window fading animation could cause the app to crash. #28644
- We’ve fixed an issue where you couldn’t select “Show locked accounts” when navigating with your keyboard. #24384
- We’ve fixed an issue where the notes field was always shown when searching, even if it was unrelated to the search. #29788
- We’ve fixed an issue where search results didn’t have a space between item titles and the text found in item notes. #29678
- We’ve fixed a visual issue with the loading animation for signing in with a QR code. #30054
- We’ve fixed an issue where the item list count wasn’t updating when you filtered a list. #29736
- We’ve fixed an issue where Guest accounts were incorrectly labeled as Team Members. #30181
- We’ve fixed a visual issue with the tooltip for the Reveal Password and Reveal Secret Key buttons on the Enter account details page. #27794
- The password generator will now save the last password type you used. #30346
- We’ve fixed an issue where Progressive insurance was listed twice in New Item search results. #30309
- We’ve fixed an issue where the main window could go blank if you opened an item in a new window and clicked on the item’s tag. #28910
- You can now view the sharing history of an item in the 1Password app. Select the ellipsis button when viewing an item, then select View Sharing History. #29833
- We’ve fixed an issue where Security settings would be reset or disabled after updating the app.!24141
- We’ve removed the beta tag from Settings > Developers > Watchtower. #29884

If you feel generous and have a couple of minutes, seeing your 1Password review on [GetApp](https://www.getapp.com/security-software/a/1password/) would be really cool.

- We’ve addressed an issue in how 1Password for Windows validates incoming connections from browsers and the 1Password CLI. Credits to Secfault Security.

- You can now generate [recovery codes](https://support.1password.com/recovery-codes/) for family accounts in the app. In Manage Accounts, choose your account > Sign-in & Recovery.
- The banner encouraging you to import items now only displays if you have fewer than 7 items across all of your unlocked accounts. #29547
- We’ve improved localization for a number of our supported languages using new translations from Crowdin.!23211
- You’ll now see tailored device enrollment instructions depending on the last device you used for SSO authentication.!23093
- Localization has been improved for a number of our supported languages using new translations from Crowdin. #29586
- We’ve fixed an issue with 1Password file import where you’d see duplicate alerts if you tried to import without permission to create vaults. #29599
- When you save conflicting information in an item, some of the item’s metadata that used to be erased will now be preserved. #18666
- We’ve fixed an issue where credit card numbers that included letters wouldn’t display consistently. #28733
- We’ve fixed a typo in New item > Getting started in the Credit cards section. #28158
- We’ve fixed an issue where in some cases shared folders were not being imported from LastPass. #29367
- We’ve made visusal improvements to the sign-in address field. #29000
- We’ve fixed an issue where the Continue button wasn’t working correctly on the CSV file import page. #29402
- It’s now easier to manage the date in an item.!23364
- We’ve fixed an issue that prevented 1Password uninstaller from completing the uninstall process. #27704
- We’ve enabled local resource integrity checks on Windows. #18207

If you feel generous and have a couple of minutes, seeing your 1Password review on [GetApp](https://www.getapp.com/security-software/a/1password/) would be really cool.

- We’ve fixed an issue that caused the app to crash when editing a date item using an unsupported language locale.!23364

- We’ve improved the experience of creating an item sharing link.
- When you search in notes, you’ll now see highlighted matched terms.!22722!22622
- We’ve added recovery codes for Individual accounts. You can now create a recovery code in Manage Account > Sign-In & Recovery and store it somewhere safe to prevent account lockouts in the future.
- When sharing an item, you’ll now be able to edit the recipients' email addresses. #27898
- If you try to import data and create a vault without vault creation permissions, you’ll now see a prompt to use the web importer instead. #28796
- If you import items but they are only partially transferred, you’ll now see a message about the items with missing data. #28493
- We’ve fixed an issue where you couldn’t open an item in a new window. #28985
- We’ve fixed an issue where closing the sign-in prompt while signed in to a previously used account would lock you out of the app. #28197
- We’ve removed an unnecessary scrollbar on the screen you see when you unlock 1Password. #28560
- We’ve made visual improvements to the unlock prompt on Windows 11.!22572
- You’ll now be able to use snap layouts in the title bar of the app.!22275
- We’ve fixed an issue where the wrong Shared vault icon was shown on a person’s details view in the app.!22729
- You can now sign in to 1Password with SSO when you’re using a proxy. #26046
- We’ve fixed the error message displayed when trying to sign back into a recovered account that had previously signed in with SSO. #24543
- We’ve fixed an issue where passwords were missing in Password items imported from 1Password 7. #29056
- We’ve fixed an issue where the text box to re-enter a recovery code was resizable. #29106
- We’ve improved the import options screen by adding a search field and a default import option if you can’t find the import method you’re searching for. #28658
- We’ve fixed an issue where the verification screen would not dismiss after entering your verification code when signing in with SSO. #22256
- We’ve fixed an issue where family accounts subscribed through the apps would see the wrong family account limits in an error message when trying to invite additional family members above their account limit. #28723
- We’ve fixed an issue where a user’s role (such as Family Organizer) was only shown in the Your Details screen and not in a Person Detail screen. #22171
- We’ve fixed an issue that prevented viewing or exporting older items in 1Password 8. #19328
- We’ve fixed an issue where choosing the back arrow button on a person’s details screen you back to the Account Overview screen instead of the People screen. #22579
- We’ve fixed an issue where the prompts to get started with 1Password would appear over the list of accounts during sign-in. #28237
- We’ve fixed an issue that prevented signing in to an account with SSO when using a proxy. #29259

- When you share an item, you’ll now see options to either copy the item link or share it.!21708
- You’ll now see a banner on deleted items with an option to restore or permanently delete the item. #24433
- The pop-up to help you import items into 1Password now has buttons to help you learn how to import from browsers and other password managers. #27860 #28669!22008
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!22337
- We’ve improved the formatting on the Credits & Acknowledgements page in Settings > About.!21905
- You can now unlock the 1Password browser extension and Quick Access from a new pop-up, without the need to navigate to the 1Password app.!21230
- We’ve improved the in-app messaging when you copy the link to a shared item.!22133
- We’ve improved the reliability of 1Password updates and the specificity of error messages related to updates when they occur. #26426
- The search bar will now change when you adjust the size of the window.!19566
- The prompt for Windows Hello will now display in front of the lock screen. #28467
- When you edit a field in the auto-saved web form details section of an item, removing a field’s contents will no longer hide the field. #18483
- We’ve fixed an issue where you may have been unable to manage your accounts if one of your accounts was offline. #28284
- If you have Settings > Labs > “Add locations to items” turned on, the Maps header in the Privacy settings is no longer displayed in all capital letters. #27990
- The list of users shown when you share a vault will no longer visually flicker when first loading up the list. #24146
- We’ve fixed an issue where the Manage Accounts pop-up would close after you signed out of an account. #28196
- We’ve fixed an issue where you wouldn’t be prompted to download the 1Password browser extension when first setting up the app.!22308
- We’ve fixed a visual issue where the messaging on an empty item list was displaying incorrectly as a banner.!22306

- You can now quickly and easily log in to apps using auto-type. Turn this on in Settings > Labs > “Auto-type”. The next time you’re in an app that you want to fill your username and password in, open Quick Access, select a Login item, and press Enter on your keyboard to fill it.!21390
- You can now enter a zip code when adding an address in Barbados to an Identity item. #22221
- You can now choose from more formats when you export an SSH key. #22454
- Additional spaces at the end of an username will no longer be factored into results in the “Items in another account” Watchtower category. #28000
- The verification code that appears when you set up a new trusted device is now entirely uppercase to make the characters clearer.!20369
- Biometrics are no longer required to turn on integration with 1Password CLI. #26315
- We’ve increased the height of the Settings window so you can see more settings.!21716
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!21543!21378!21831
- Created and modified dates for items are now formatted according to your operating system’s language settings and standards specified by the [Unicode Consortium](https://cldr.unicode.org/).!21525
- 1Password will no longer restart silently if an update is available when you quit the app. #27702
- We’ve fixed an issue when importing from LastPass that caused a “Failed to find private vault” error. #27270
- We’ve fixed an issue that caused some LastPass items to be imported as “unknown items”. #27550
- We’ve fixed an issue in the LastPass importer that prevented regular users from seeing admin options if they had “administrator” permissions on any LastPass folders. #28089
- We’ve fixed an issue where you couldn’t clear a search query after editing and saving an item in the list of results. #22782
- The Credits & Acknowledgements link in the About settings now works properly again.!21619
- We’ve fixed an issue where using certain tags could result in visual issues or cause the app to become unresponsive. #28117 #28220
- We’ve fixed an issue that caused the app to display an incorrect location in Add & Remove Programs when it was installed with the MSI. #24115
- We’ve fixed an issue where menu options for the app, such as New Item or Lock 1Password, wouldn’t always be available. #14893

- We’ve fixed an issue where team members with the permission to administer folders in LastPass couldn’t see some options when importing data into 1Password.!21704

- When searching, the search dropdown now highlights the content from note items or fields beside item titles for easier skimming. #24426
- More types of items are now supported when you import data from LastPass.!21375
- If you want to import your LastPass data, and you sign into LastPass with Entra ID, the redirect URI has been updated from `onepassword://import/login/sso` to `http://127.0.0.1:18255/import/redirect`. #26626
- “What’s New” is no longer shown when you set up the app for the first time.!20982
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!21197
- We’ve updated the icons used for the 1Password browser extension in the list of trusted devices and browsers. #26284
- We’ve improved the descriptions and suggestions shown for items in the “Items in another account” Watchtower category. #24303 #24019
- “Authentication codes” are now properly referred to as “one-time passwords” throughout the app. #22013
- 1Password now unlocks a bit faster if you’re signed in to multiple accounts in the app. #26921
- We’ve made some improvements to the pop-up you see if you’re prompted to share your usage data with 1Password.!20898
- We’ve fixed an issue that prevented the 1Password.com, Emergency Kit, and Setup Code sign in methods from working properly when setting up the app. #26913
- We’ve fixed an issue that could cause you to be asked for a verification code after reauthorizing a trusted device with your identity provider. #26038

- Search is now able to use the text in Secure Notes to display matches in the dropdown results under the search bar. #24421
- Watchtower now includes [insights about developer credentials](https://developer.1password.com/docs/watchtower/) to help diagnose and remediate security issues found with SSH keys stored on disk.!20284
- The cache for app and website icons will now be removed when you turn off the icons. #9801
- The app will now be locked when you ignore the prompt to sign in with SSO after your session has expired. #26785
- We’ve fixed an issue that caused the “Delete all duplicates” button in Watchtower to also delete ignored items. #26226
- We’ve fixed an issue that prevented signing in with SSO after your 1Password account’s sign-in address was changed. #25913
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!20908
- 1Password now uses more system-provided exclusion formats from Windows to let other apps know that the clipboard contains sensitive content.!20533
- We’ve fixed some issues that prevented signing in to LastPass with Azure SSO during import. #23641
- We’ve incorporated some fixes for how dates are handled when you import items from LastPass. #26544
- We’ve fixed an issue that caused the LastPass import options screen to be blank when you’re an admin but don’t have any shared folders. #26736
- The “Delete other duplicates” button in Watchtower banners now takes into account if you’re viewing a list of duplicate items that have been marked as ignored. #26285
- We’ve made accessibility-focused improvements in Settings > Labs. #22743
- We’ve fixed an issue that could cause the app to crash if you used Ctrl + Alt + F to filter a list of search results. #26121
- We’ve fixed an issue that caused app and website icons to show in some places when they were turned off. #18541
- App and website icons now display properly in both item list and item details views. #18063

- We’ve fixed an issue where an account that unlocks with SSO could be removed from the 1Password app if the app locks when you’re prompted to sign in with your identity provider. #26785

- We’ve added an option to [“Configure for WSL”](https://developer.1password.com/docs/ssh/integrations/wsl/) when setting up Git commit signing.!20216
- You can now sign in to your LastPass account using Google Workspace SSO to import your data. #24522
- We’ve fixed an issue where an inaccurate message related to permissions could be displayed when importing data from LastPass. #24097
- We’ve fixed an issue that could prevent you from importing from LastPass if your Okta email address was different from your LastPass email address. #26206
- You’ll now see a warning when you try to remove your own viewing permissions from a vault. #24182 #24857
- We’ve updated the description of CSVs when exporting your data. #15742
- When you select “Open and fill” in the 1Password app, the Login item’s UUID included in the URL is now encrypted. #21885
- Resetting 1Password in Settings > Advanced now removes an additional database file. #24468
- If you export your 1Password information, the status of the export will now be communicated more clearly when using a screen reader. #11860
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!20174!20452!20407
- We’ve fixed an issue where the offline indicator wouldn’t properly reflect when accounts that unlock with SSO were offline. #24786

- Items imported from LastPass now show a red Watchtower banner to remind you to update the passwords. #23338
- You can now map LastPass user email addresses to 1Password users when importing your data. #23839
- The LastPass importer will now check for a feature on some 1Password accounts that limits vault access management to people in the Owners group. #24669
- We’ve fixed an issue that occurred when signing in to the LastPass importer with SSO. #24238
- 1Password now unlocks faster when you’re signed in to accounts with many vaults.!19340
- You can now select and copy item titles when viewing an item. #5218
- We’ve improved the labels of buttons for screen readers when viewing the Profile screen. #24095
- We’ve fixed an issue that prevented items from being selected again after they were deselected. #24064
- In Secure Notes, Markdown ruled lines and code blocks will now fill the available space in the window. #22972
- We’ve fixed the error that appears when you try to sign in to an account without being connected to the internet. #15347
- We’ve fixed an issue that prevented adding new trusted devices with SSO in some cases.!19632
- If you delete all items with duplicates in Watchtower, you’ll now see details about the Watchtower category instead of just a blank list of items. #24215
- We’ve improved the phrasing shown on the pop-up when you grant access to another device if you sign in with SSO. #22789 #23907
- Sign-in address validation accuracy has been improved when adding an account to the app. (*Thanks, Secfault Security!*) #24344
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!19623!19987
- We’ve fixed an issue where you could be prompted to enter a password when signing in to a previously used account after you switched to unlock with SSO. #22773
- We’ve updated the icon on the “Items in the wrong account” Watchtower card. #24287
- We’ve fixed an issue that caused accounts that unlock with SSO to not unlock. #24036
- We’ve fixed an issue where malicious local software could have been able to confuse the app, resulting in the wrong vault key being used to process an item. *(Thanks, Secfault Security!)* #23293
- We’ve removed some undesirable words from the password generator. #22639
- We’ve fixed an issue that caused 1Password to lock immediately after unlocking it in some cases. #23790
- We’ve fixed an issue that prevented importing 1Password Unencrypted Export files when some of the items inside were corrupted. #15999
- When you use the 1Password browser extension to edit or open the item in a new window, the main window for the 1Password app will now open properly. #24066
- If you use 1Password to [sign Git commits](https://developer.1password.com/docs/ssh/git-commit-signing/), you’ll now see a clearer error message if you try to commit changes when 1Password isn’t running. #23569
- We’ve fixed an issue where attempting to unlock the 1Password browser extension wouldn’t put the 1Password app in focus when biometrics weren’t available. #24507
- We’ve fixed an issue where certain items with some empty fields wouldn’t show up as duplicates in Watchtower. #24387
- We’ve fixed visual alignment in the device and vault lists in Manage Accounts > People. #24523
- When you set up the app for the first time and sign in to your account, a prompt to import your items will now only be shown if you have fewer than 10 items in your account. #24412
- Group section titles in Watchtower items with duplicates are now formatted the same as group titles elsewhere in the app. #24386

- You can now choose a default identity and credit card item in the app. Choose Profile in the sidebar to get started.!19438!19449 #24203!19579!19548!19544!19519
- You can now control which family members have access to your vaults right in the app! Add family members, remove family members, and edit permissions for every vault you control. #24169 #22751 #22755!19027 #23776 #22853 #23759 #23868
- You can now see a list of your duplicate items in the app. Choose “Items with duplicates” in your Watchtower dashboard to see or delete all of your duplicates.!18925 #23645 #23774!19091!18983!18993!18980!18964!18920!18850!19138!18968
- We’ve added 1 day and 1 week options to the “Require password” setting. #13742
- We’ve added a Give Feedback button for active experimental features in Settings > Labs.!19266
- We’ve updated the error message shown if you choose “Sign in with SSO” and try to sign in to a 1Password account that unlocks with a password. #22574
- We’ve fixed an issue that prevented exporting your data as a CSV file while offline. #19195
- When you import using your LastPass administrator account, you’ll now see administrative tool options to help with the import, such as only importing folder permissions.!19324
- The “Select your default details” experiment in 1Password Labs has concluded.!19528
- We’ve redesigned the authorization prompts for the 1Password command-line tool.!18855 #23633
- If you already have an account that unlocks with SSO, you’ll now see an error when you try to sign in to another one.!18757
- We’ve rolled back some recent changes related to how de-duplication works when importing from LastPass in a team or business account.!19403 #23838
- We’ve updated the information shown when you edit an item’s autofill behavior. #20135
- We’ve made improvements to prevent accounts from being added to the app while it’s locked. #23767
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!19592!19217
- We’ve fixed an issue where updated permissions weren’t applied properly for subsequent LastPass imports. #23951
- Folder names are no longer included in the metadata vault when you import your LastPass data. #23818
- You’ll now see a warning that your Secret Key may be included when you export your data as a 1PUX file.
- We’ve fixed an issue where choosing to unlock 1Password using your password in Quick Access would lead to a second biometric or system authentication prompt. #23433
- We’ve fixed an issue where queued SSH authentication prompts would automatically get denied. #23524
- We’ve fixed an issue where the names of the Personal, Private, and Shared vaults weren’t properly translated into some supported languages. #23260
- We’ve made security improvements to how user-supplied icons for items are handled in the app. #24143
- You’ll now see a warning when permissions aren’t properly imported from LastPass. #22460
- The metadata vault is no longer localized when you import from LastPass. #24163
- We’ve made additional improvements for how data from LastPass is imported.!19568
- We’ve made security improvements to how information is handled in memory. #23453

- 1Password will now check for items that support passkeys. You can manage this setting in Settings > Privacy. #21747
- You can now deauthorize trusted devices in the app. In Manage Accounts, choose your account > Your Details and click Deauthorize beside an unused device to remove it.!18789!18806!18807!18792
- 1Password now detects authenticated HTTP proxies more reliably.!18905
- The dropdown menu options in Settings > Labs > “Select your default details” are now sorted alphanumerically. #23313
- You’ll now see if an account added to the app is currently frozen in Settings > Labs. #23474
- The SSH Key item category is now prioritized when creating a new item if you have developer-related items in your Private vault. #22840
- Closing the biometric or system authentication prompt to unlock 1Password Quick Access will no longer bring the main app window to the foreground. #13923
- Clicking the close button (X) on the previously used accounts list after signing in will now complete the sign in attempt.!18924
- You can now allow 1Password to prevent your device from sleeping when viewing a field in Large Type. Adjust this setting in Settings > Security. #23443
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!19146!19119
- We’ve fixed an issue where the app would show an error if you clicked New Item and chose an item type that isn’t Login in the 1Password browser extension. #23479
- We’ve fixed an issue that showed some categories in the sidebar even when you don’t have items in those categories. #13984
- If you quit 1Password before you finish the initial setup flow, reopening the app will present the setup flow again to allow you to finish it. #7296 #23705
- We’ve fixed an issue that didn’t allow switching to unlock with SSO. #22440
- We’ve fixed an issue that prevented copying the secret reference to the password fields in Password items if the CLI integration was enabled. #23712
- We’ve fixed an issue where a warning prompt wouldn’t be displayed when navigating away from an item while you’re editing it. #23692
- We’ve fixed an issue that suppressed SSH signing requests from background requests such as git.!19195
- We’ve reversed the order of the auto-lock options in Settings > Security. #15540
- We’ve fixed an issue that could prevent the “Hold key to toggle revealed fields” option from working properly after 1Password was closed and reopened. #22935
- We’ve fixed an issue that made it difficult to select Security Questions when adding a field to an item. #21083
- Items imported from LastPass will now show metadata details in the notes field. #23241
- We’ve fixed an issue where some items wouldn’t be imported from LastPass when team members didn’t have the Create Vaults permission. #23557
- If you use Duo with push notifications for multi-factor authentication in your LastPass account, you can now successfully import your data. #23291
- Permissions are now more restrictive for the `LastPass Imported Shared Folders Metadata` vault in team and business accounts when you import your LastPass data. #23588
- We’ve fixed an issue where it wasn’t possible to drag and drop the contents of a date field into another application. #23254
- You’ll now see the search filters you were previously using when you press Ctrl + F in the search result lists. #11280 #9884

- This release contains an important security update related to displaying images. Please see the accompanying [security advisory](https://support.1password.com/kb/202309/).!19379

- We’ve updated our internal libraries to benefit from general improvements, bug fixes, and more.

- Introducing labs: A space where you can explore and test new features. Open Settings, choose Labs, and click “Select your default details” to get started.
- When viewing any field in Large Type, your screen won’t sleep.!18356
- The password generator will no longer create some easy-to-guess 4- and 6-digit PIN codes. #12456
- When you delete a tag, the app no longer attempts to remove the tag from deleted items.!18574
- We’ve updated the title and description for the command-line interface integration in Settings > Developer. #21114
- Nested quote blocks (`>`) in notes using Markdown are now indented less dramatically to allow for more space.!18538
- We’ve reordered the sections in New Item > “Developer tools” to put SSH at the top. #22839
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!18357!18693
- We’ve updated the link to learn more about connecting the command-line interface. #22638
- The “Learn more…” item banner for Shell Plugins now changes depending on the item you’re viewing.!18388
- The View Tagged Items button is now hidden if you started an import during setup. #20114
- You’ll now see a message if your account is frozen when you try to import your data. #19833
- Backticks for Markdown are no longer shown in the item list for Secure Notes when the note begins with them. #18717
- We’ve added some information to [diagnostics reports](https://support.1password.com/diagnostics/) to help troubleshoot offline items. #22355
- 1Password now applies more correct and safe validations to the names of files downloaded from your vaults. *(Thanks, Secfault Security!)*!18445
- You can now test signing in to your LastPass account using Azure SSO to import your data. [Contact 1Password Support](https://support.1password.com/contact/) if you experience any issues. #21446 #22415
- The LastPass importer now supports Never URLs and will turn off autofill for items whose URL matches a Never URL. #20029
- We’ve overhauled how LastPass import de-duplication works for team accounts. A shared vault now keeps track of imported data instead of creating a lock file in your LastPass account for each imported folder. If you need help importing shared folders and permissions, [contact 1Password Support](https://support.1password.com/contact/). #23173
- Additional fields in LastPass items are now imported to the main section of the item in 1Password. #20093
- The LastPass importer now converts Health Insurance and Insurance Policy items to Secure Notes in 1Password. #23259
- Passkey fields are now ignored when exporting with 1Password Unencrypted Export (1PUX). #22771
- We’ve fixed an issue that caused buttons to not use the operating system accent color. #23226
- We’ve improved support for importing previously unknown item types from LastPass, such as basic authentication.!18459
- We’ve fixed an issue with Okta SSO in the LastPass importer.!18620
- We’ve fixed an issue that caused column headers in the app to be misaligned. #12161
- We’ve fixed an issue that caused the LastPass import to fail when signing in with SSO.!18572
- We’ve removed “Learn more” links for some shell plugins that aren’t yet released.!18614
- We’ve fixed some visual spacing issues in the importer. #22989
- We’ve fixed an issue that caused three backticks to not render as a code block in Markdown. #15518
- We’ve fixed an issue that caused the public key store to be cleared when unlocking an account with the SSH Agent. #22844
- We’ve fixed an issue that prevented a new code from appearing after entering an incorrect one when setting up a new trusted device with SSO. #22916
- We’ve fixed a typo on the screen to delete your account.!18609
- We’ve fixed an issue that prevented dragging and dropping passwords from filling fields correctly. #22617
- We fixed an issue where clicking “Sign in with SSO” on the lock screen wouldn’t display the appropriate error if you signed in as a user in your identity provider that wasn’t tied to the corresponding 1Password account. #22662
- When you import your LastPass data, the first password in form fields is now added to the main password field if a main password isn’t specified in the LastPass item. #20217
- We’ve added a note after importing LastPass data to clarify that folder sharing permissions may need to be manually edited after importing from the same account more than once. #22461
- We’ve added a message after importing LastPass data to let you know when folders owned by linked accounts aren’t imported. #23046
- We’ve fixed an issue where you couldn’t import your data if your LastPass account uses Duo for multi-factor authentication.!18840

- You can now [use 1Password to sign in to sites](https://support.1password.com/sign-in-with-provider/) with your Amazon, Discord, or Slack account. #18049 #18051 #22536
- You can now see the vaults a family member has access to from Manage Accounts. #21561
- The LastPass importer will now save unknown items. #22292
- We’ve added proxy support to the LastPass importer. #19741
- Imported sub-folder items from LastPass are now tagged with parent the folder name. #22421
- You can now import from LastPass to your Personal or Private vault without having vault creation permissions. #22088
- The LastPass importer now has an option to only import permissions of shared folders and create a vault with shared folder mapping on it.!17532!17630
- LastPass imported folder data is now stored as a Secure Note in the Shared vault to help larger teams see what was imported.!17256
- We’ve fixed some issues that caused permissions on shared vaults to not be updated correctly when importing from LastPass. #22203 #22194 #22342
- We’ve fixed an issue that caused the Import Finished screen to not show correct vault icons. #16181
- We’ve improved support for Duo and LastPass authenticator during the import process. #21445
- We’ve fixed some issues with using SSO to sign in to LastPass during import.!17921
- We’ve improved the error message in the LastPass importer when signing in to your LastPass account with SSO. #22225
- We’ve fixed a LastPass import issue by adding support for multibyte characters in LastPass item fields. #22280
- The importer now shows the name of the file you’re importing instead of its full path. #16107
- We’ve added some additional logging to help diagnose LastPass importer issues.!18150
- Your name and profile picture will now be displayed when you set up another device using the Setup Code. #14801
- We’ve improved the error message displayed when you can’t invite more people to your family account.!18139
- We’ve added more descriptive errors when inviting family members and/or guests.!17992
- We’ve improved the error that displays when you’re using a 1Password database from a newer version of the app, which now prompts you to contact 1Password Support for help.!17592
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!18244!17946
- We’ve added headers and better organization in Manage Accounts. #22550 #22464
- You can import Login items containing passkeys with 1Password Unencrypted Export (1PUX) if they are exported with the same version. #19935
- The Deleted Items list no longer refreshes on every click.!18347
- We’ve fixed an issue where the SSO migration banner conflicted with clicking the account in Manage Accounts. #22668
- We’ve fixed an issue that could prevent some people from migrating to SSO. #20378
- We’ve fixed an issue that prevented custom sections from being deleted when editing an item. #22566
- We’ve fixed an issue with text alignment in SSH agent auth prompts. #22431
- We’ve fixed an issue that caused the two-factor authentication prompt for your 1Password account to display after locking the app. #21620
- We’ve fixed an issue that caused all actions to be title case in Quick Access. #21203
- We’ve removed the invitation modal and moved user management to the overflow menu. #20827
- We’ve fixed an issue that caused the connection between the app and browser extension to be inconsistent. #20871 #22487
- The multi-factor authentication prompt for your 1Password account will now disappear when the timeout expires. #22056
- The What’s New count now shows the correct color in dark mode.!18017
- We’ve fixed an issue that caused the Manage Account modal to show a blank screen. #22246
- We’ve updated the color of the Suspended status indicator in Manage Account > People.!17884
- Item usage data will now be tracked when you use fill an item with “type in”. #21036

- We’ve fixed an issue that could prevent the app from connecting to the browser extension for some people. #22451
- We’ve fixed an issue that could cause a memory leak in the app. #22495

- If you’re a family organizer, you can now invite and confirm family members directly in the apps. #21558
- You’ll now see a banner about [1Password Shell Plugins](https://developer.1password.com/docs/cli/shell-plugins) on API Credential items. #21496
- We’ve updated the design and details included in the SSH authentication prompt so you can learn more about the request. #20679
- We’ve removed the note about needing SSH keys to be in a Private vault from Settings > Developer because they can now be stored elsewhere.!17726
- The LastPass importer now supports Yubikey for two-factor authentication on your LastPass account. #20761
- If your device is offline, you’ll now see an Offline Items list in the sidebar if you’ve made changes that aren’t yet saved in your 1Password account. #21366
- You can now choose custom icons for your vaults directly in the app.!15099
- You can now [create the config file for the 1Password SSH agent](https://developer.1password.com/docs/ssh/agent/config/).!17947!17828 #21955
- You can now see the progress when you import your LastPass data. #22094
- You can now reset the app in Settings > Advanced. #7378
- SSH-related options are now sorted together in the actions menu when viewing the details of an SSH key. #22188
- We’ve improved the error message that’s shown if your shared folders fail to import from LastPass. #20796
- We’ve fixed an issue that caused TLS certificates with misformed serial numbers preventing connections from working. #12845 #16670
- We’ve improved the import feature to prevent it from timing out while syncing your information. #20640
- We’ve updated the color of the banner for items that may be in the wrong account.!17702
- We’ve fixed an issue that caused items imported from LastPass to show the wrong Watchtower banner. #21739
- We’ve fixed an issue with multi-factor authentication in the LastPass importer. #21897
- We’ve fixed some incorrect punctuation of labels in Settings. #17043
- We’ve fixed an issue that could cause the importing from LastPass to fail if you sign into LastPass using SSO. #22142
- We’ve fixed an issue with importing data from a LastPass account containing a lot users with access to the same shared folder. #22070
- We’ve fixed an issue that could cause importing a 1PUX file to fail.!17864

- You can now move an item directly from the Watchtower banner that says it’s stored in the wrong account. #21157
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!16976
- The LastPass importer will now import permissions from shared folders in LastPass business accounts. #21448 #21426
- The LastPass importer will now prevent duplicate items and attachments when importing shared folders.!17096!17283
- The LastPass importer now imports application items as Login items. #20279
- The “missing agent config” message in the 1Password SSH agent is now logged on a debug level to prevent notification noise.!17434
- We’ve fixed an issue that caused the welcome screen to stop working after you signed out of all your accounts. #21454
- The main app window will now retain its size and position after your computer is restarted. #14755
- Field labels on the Enter Account Details screen are now title case. #20303
- We’ve fixed an issue that caused the main app window to reset if it was snapped and then an item was moved, duplicated, or deleted. #19709 #13256
- We’ve fixed background app detection for some SSH clients that used winssh-pageant.exe. #21275
- You’ll now see a warning if you may be about to save a new item in the wrong 1Password account.!17309!17431
- We’ve updated the phrasing used to describe the new “Items in another account” category in Watchtower.!17489
- We’ve fixed an issue where the Export Items permission was required to move an item out of a shared vault. #12573
- Items shared with you in LastPass are now included when you import your data. #21519
- User group permissions for shared folders are now included when importing from LastPass. #21450
- We’ve improved the way the app handles a specific “500” status that can occur when you import item attachments from LastPass.!17397
- You can now copy [secret references](https://developer.1password.com/docs/cli/secret-references/) by clicking the dropdown menu beside a field when viewing item details. #20817
- Prompts to authenticate using the 1Password SSH agent no longer put initial focus on the “Approve for all applications” checkbox. #21469
- We’ve fixed an issue where you could experience errors with the 1Password SSH agent when setting it up for the first time.!17405
- We’ve improved the import feature to prevent it from timing out while syncing your information. #20640!17555

- We’ve updated the names and descriptions for each of the Watchtower categories.!16810 #7151 #15460
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!16887!16717
- We’ve fixed an issue where denying a prompt to sign in with SSO wouldn’t inform you that the request was denied on the new device. #20795
- We’ve fixed an issue that could cause someone to get stuck when trying to migrate to sign in with SSO. #20803
- You can now import your LastPass data if you sign in to LastPass with SSO, currently only Okta is supported. #20048
- To prevent duplicates when importing from LastPass, items in the “Shared with me” section will not be imported. #20862
- Errors with the LastPass importer now direct customers to click on the `support+LPimporter@1Password.com` email address to reach 1Password Support. #20773 #20757
- We’ve improved the error message displayed if you have too many failed login attempts when you try to import your LastPass data. #20810
- We’ve improved the error message displayed if 1Password can’t connect to LastPass.com when you try to import your data. #20811
- We’ve fixed an issue that could cause a “MissingFileName” error when importing certain LastPass items. #20268
- We’ve fixed an issue that could cause a “failed to convert data to a number” error when importing data from LastPass. #20491
- We’ve improved the design and functionality of the SSH authentication prompt. #20933
- Focus will now return to the original window after you approve an authentication prompt for SSO. #20331
- The Imported from LastPass section in Watchtower is now hidden if you’ve never imported LastPass data. #20884
- We’ve fixed an issue when attempting to use an RSA key via the SSH agent.!16931
- The SSH agent now validates that the requested public key corresponds to the private key before signing any commits. #20638
- We’ve fixed an issue where dismissing the two-factor authentication prompt in the app did not properly cancel the request. #20971
- We’ve fixed an issue where after completing the account migration to use SSO, all secondary devices would be required to sign out instead of completing the migration.!16921
- We’ve moved the clear search button to the right side of the item list. #14250
- We’ve updated some of the visual branding for 1Password.!17031
- Watchtower will now warn about items that may have been saved into the wrong account. #21155
- When you fill an item in a browser, you’ll now see a prompt for authentication if your 1Password account requires it after you unlock the app. #20670 #18637
- We’ve fixed an issue that prevented permanently deleting more than 49 items from Recently Deleted. #17690
- We’ve changed the order of the options in Watchtower > Share My Score. #14301
- We’ve added a new error for when attachments imported from LastPass can’t be decoded properly. #21047
- You’ll now see a message in the LastPass importer when you sign in with SSO if your identity provider isn’t supported. #20931
- In the LastPass importer, we’ve improved the experience of signing in to your account with SSO.!17091 #21171
- In the LastPass importer, we’ve added an error message for when a password reset has been requested in the LastPass account. #21010
- In the LastPass importer, an item with a field that can’t be imported will be tagged so you can review it after the import has completed. #21048
- You’ll now see an in-app notification when you copy the app version from Settings > About. #18805
- We’ve fixed an issue that caused the sidebar toggle to only work on the second click.!17059
- You’ll now see an in-app notification when this device has been deauthorized from your 1Password account. #13381 #12844
- The offline indicator will now display consistently after closing and reopening the main app window. #21209 #21234
- We’ve fixed an issue that caused the vault icon selector to not stay in focus when selecting an icon. #13394
- We’ve fixed an issue that caused the “Sign in with” feature to show when there are iframes for different login domains such as Twitter. #19088
- The SSH agent will now be more conservative when detecting background apps to prevent false positives. #21275
- If you use the 1Password SSH agent and you’ve received multiple SSH requests at the same time, each prompt now must be approved by you one at a time. #21492

- We’ve implemented a change to make sure the connection between the 1Password app and browser extension continues to work properly in the upcoming versions of Microsoft Edge, Chrome, and other Chromium-based browsers. #21031

- We’ve improved the design and functionality of the SSH auth prompt.!16697
- Search filters like `=untagged` can now be used without keywords. #19917
- We’ve fixed an issue that caused the New Vault and Collections screens to not update after unlocking another account. #19982 #18880
- You can now adjust the order of websites and apps tied to an item. #12996
- We’ve improved the accessibility experience when changing the order of fields or sections in an item. #19241!16399
- Field names in the Set Up Another Device pop-up are now lowercase. #15330
- We’ve fixed a localization issue to make sure that the search bar shows “Search in all accounts” in all supported languages when All Accounts is selected. #19034
- We’ve made many improvements related to how fields in LastPass items are mapped to their corresponding fields in 1Password items when you import your data.
- We’ve made additional improvements related to the accuracy of our LastPass importer and reduced the amount of unknown LastPass account metadata that’s imported. #20139 #20314
- We’ve fixed an issue where checkbox fields in LastPass items weren’t properly imported. #19890
- We’ve fixed an issue where empty LastPass folders would be imported as Login items with `https://group` in the website field. #19692
- We’ve fixed an issue where pressing the Escape key wouldn’t close certain pop-ups. #13546
- When you delete a vault, you’ll now be shown the next available vault in your account or collection. #19925
- We’ve fixed an issue where the app would be slow to unlock when the 1Password SSH agent was turned on. #20254
- The button to reveal a Secret Key or password field is now displayed when the field is in focus. #13310
- We’ve fixed a visual issue where the “add more” button when creating or editing an item didn’t have rounded edges.!16472
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!16511
- When you import your LastPass data, your personal items will now be imported into your Personal or Private vault with tags that align with your LastPass folders. #20226
- We’ve made some improvements to how we handle error messages when you try to import your LastPass data. #20312
- We’ve made additional improvements to the account information we include in the Imported Unknown Data vault when you import your LastPass data. #20380
- 1Password version information is now more consistent across all of our executable files' properties. #18563 #19208

- SSH commit signing now supports Git version 2.40. #20587

- We’ve made several under-the-hood improvements related to copying information from item fields. #5218 #17651
- We’ve fixed an issue where you couldn’t enter your new Secret Key in the app if prompted. #18081
- We’ve fixed an issue where pressing the Escape key would close multiple pop-ups in the app instead of just the visible pop-up.!16280
- We’ve improved the LastPass importer to import items even if it contained data that couldn’t be decrypted. We now tag them with `!-repair-items-lastpass`, so that customers can review the items manually and compare it to their LastPass counterpart. #20076
- We’ve fixed an issue where the list of accounts in the pop-up to create a new vault wasn’t updated when another account was unlocked. #19982 #18880
- We’ve fixed a visual issue where some tooltips in the app would adjust in size after being displayed.!16239
- We’ve fixed a small visual issue related to the tooltip for the Reveal Password button on the lock screen when using a keyboard to navigate.!16239
- You can now use the app to type in iTunes windows, like to sign in using your Apple ID. #19397
- We’ve fixed an issue where deauthorizing a specific device and updating your sign-in details at the same time wouldn’t remove the local copy of the data on that device. (*Thanks, Michael Rops!*) #19697
- Search filters like `=untagged` can now be used without keywords. #19917
- We’ve fixed an issue that caused the New Vault and Collections screens to not update after unlocking another account. #19982 #18880

- You can now reorder sections and fields when editing an item. #5958
- We’ve made some speed improvements to 1Password Unencrypted Export (1PUX), so it’ll only compress necessary files during the export. #11137
- Results in the search bar now show the keyboard shortcut needed to open the item details. #9430!15686
- The SSH agent will now show an “Unknown app” auth prompt for apps that aren’t supported instead of rejecting the request. #18060 #19296
- We’ve added an option to install 1Password CLI from the 1Password menu.!16010
- We’ve improved the design and accessibility of the autofill behavior settings.!15803
- We’ve made a few visual tweaks to the icon used in beta releases of the app.!16021
- We’ve updated some translations.!14945
- We’ve improved the default width of Large Type windows to show six characters to work better with one-time password. #14039
- You’ll now see a note when autofill behaviors have been customized for an item. #18424
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!15984
- 1Password will now automatically repair any duplicated internal section and/or field IDs when you edit and save an item.!16137
- 1Password now suggests more Microsoft items when saving a login with “Sign in with”.!16068
- We’ve improved the accessibility of tooltips in the app. #18887 #17741
- We’ve improved the performance of some animations.!16080
- We’ve fixed an issue where you wouldn’t be prompted to update your sign-in details if you tried to sign in using outdated credentials. #19341
- We’ve fixed a small spacing issue with text in the About screen in Settings. #17812
- We’ve fixed an issue where clicking the 1Password icon in the system tray wouldn’t work when the “Show a menu” option was chosen in Settings. #13538
- We’ve fixed an issue where logins with a [supported sign-in provider](https://support.1password.com/sign-in-with-provider/) wouldn’t show up in full search results. #15916
- We’ve fixed an issue where you could still see a prompt to authenticate with two-factor authentication when the app was locked. #18882 #8956
- We’ve fixed an issue that allowed clicking other accounts on the Sign In screen while one is trying to complete sign in. #15796
- We’ve fixed an issue that caused notifications to not appear on items opened in new windows. #18535
- We’ve fixed a rare issue that caused the app to stop you from signing in after you’ve completed account recovery.!15860
- We’ve fixed an issue where ampersands (&) weren’t displayed correctly in account menus. #12240 #9123
- We’ve fixed an issue where you wouldn’t be prompted for two-factor authentication on an account when first setting up the app. #19280
- We’ve fixed an issue where the SSH agent’s default approval setting wasn’t “Application” or saved after the app was closed.!15990 #19284
- We’ve fixed the documentation link for how to turn off the OpenSSH Authentication Agent. #19200
- We’ve fixed an issue that caused navigation history to be lost when sorting or changing categories.!16062
- We’ve fixed an issue that caused MFA with a security key to not work on nested subdomains of 1password.com, such as ent.1password.com. #19384
- We’ve fixed an issue that caused new shortcuts and some other settings to not be applied until restarting the app. #18857
- We’ve fixed incorrect op-ssh-sign arg parsing in the SSH agent. #19505
- We’ve redesigned the app toast notifications to be more consistent. #13150
- If you import your data from LastPass when first setting up the app, you’ll be taken by to the tips shown when you sign in to the app for the first time. #19520
- We’ve improved how notes fields in items are processed when importing from LastPass. #19754
- We’ve fixed an issue where logins imported from LastPass could become Secure Note items.!16286
- We’ve fixed an issue where the LastPass importer would group the country and phone number into a single field. #19696
- We’ve fixed an issue that could cause the LastPass import process to fail if an item had a form field with the `Select` type. #19881
- We’ve fixed an issue where trying to import data from a LastPass account with a higher password iteration count would fail. #19710
- Unknown LastPass account metadata is now combined into a single item with multiple fields called “Imported Unknown Data” instead of separate items. #19755
- We’ve fixed a few issues that could cause a LastPass import to fail. #19704 #19689
- We’ve fixed an issue where you may have seen a blank pop-up after canceling a LastPass import. #19694

- You can now directly import your data from LastPass without saving an unencrypted CSV to your computer. #19309 #19310 #19383

- We’ve fixed an issue that prevented creating any type of item in a business account when file storage was turned off in the account’s security settings. #19357

- We’ve added an offline indicator to let you know if 1Password is unable to connect to 1Password.com due to network issues.!15511!15497!15671!15594
- If your account has been recovered, and you try to unlock the app, you’ll now be asked to enter your new Secret Key and password. #18300
- We’ve updated the default option for the [SSH agent](https://developer.1password.com/docs/ssh/agent) to ask for approval from “application and terminal session” to “application” when setting it up for the first time. #17731
- We’ve updated the item details overflow menu’s label to have a proper description when using the app with a screen reader. #18632
- We’ve added proper localization support for dates and times.!14849
- We’ve fixed an issue where clicking or tapping View after moving more than one item would take you to the item details for one of the items instead of showing the list of moved items in the vault. #15436
- We’ve fixed an issue where checking for updates to the app wasn’t possible when it was locked. #18788
- We’ve fixed an issue where the pop-up shown when you click New Item wouldn’t display the proper animation when closed.!15674
- We’ve fixed an issue where restarting your Mac would change the selected choice for the “Require password” option in the Security settings.!15651
- We’ve fixed an issue where in-app notifications were dismissed too quickly. #18862
- We’ve fixed an issue that caused the New Vault popup to not update when opened once, then again from a different account. #!15728
- We’ve fixed an issue that would sometimes cause the main app window to not respond to any inputs after clicking and dragging an item field. #13788
- We’ve fixed an issue that where the floating message to let you know that the app is offline would quickly appear then disappear if you clicked the offline indicator button. #18802
- We’ve fixed an issue that could result in a repeating “Authentication timeout” prompt if you use Duo. #17939
- When you show the search results for a query with no matching items, the sort button will now be hidden. #18055
- We’ve fixed a crash that occurred when manually locking 1Password and being in a country that is blocked by the firewall settings on your 1Password account. #18828
- We’ve fixed an issue that caused tapping Search when already viewing the Search tab to show a blank screen. #18738
- We’ve fixed an issue where tapping View after moving an item would cause you to switch from the collection you were viewing to the account it’s in.!15274

Here’s the full list of changes in this release:

- You can now choose a default vault to save new items in.!15000!15405
- We’ve added an indicator to let you know if 1Password is unable to connect to 1Password.com due to network issues.!15511!15497!15671
- You can now choose to encrypt your SSH keys when exporting them.!15031
- We’ve added Okta to the list of “Sign in with” providers. #16402
- We’ve updated the Duo prompt to make it clear that dismissing the prompt will lead to the app being offline. #18298
- User settings are now restored if MDM is turned off. #18156
- We’ve updated some of the wording in the setup flow. #18318
- We’ve improved the screen reader support when first getting started in the app. #11347
- Private SSH keys will now be shown and copied in the OpenSSH format instead of PCKS8.!14006
- We’ve updated some translations.!15463
- We’ve improved the error message that you’ll see if you try to add a second user from the same team or family account. #17830
- A prompt to enter credentials is now displayed when a proxy from a PAC file requires authentication. #18506
- The sign-in address field is now automatically populated with `https://my.1password.com` if you choose “Enter account details” when adding an account. #12638
- When you open the Set Up Another Device pop-up, you’ll now see the full Secret Key if you reveal the field. #7228!15174
- We’ve made some improvements to the list of previously used accounts shown when you add a new account, including automatically scrolling down to display error messages. #15831 #14620
- We’ve improved the text colors used to show how many days are left in a trial. #15181
- When you show the search results for a query with no matching items, the sort button will now be hidden. #18055
- We’ve made some design improvements throughout the app. #18162
- We’ve updated the icon of the beta version of the app to better distinguish it from the production version.!14364
- We’ve removed support for Secure Desktop.!15379
- We’ve fixed a crash on startup for some users when they tried to launch 1Password 8 on a corporate device. #16275
- We’ve fixed an issue that could result in a repeating “Authentication timeout” prompt if you use Duo. #17939
- We’ve fixed an issue that wouldn’t allow the calendar in the date picker to be used with a keyboard when editing an item. #9043
- We’ve fixed an issue where opening Quick Access when first setting up the app would stop the setup flow from continuing properly. #11350
- We’ve fixed an issue where text in a text field wouldn’t be read out properly when navigating with a screen reader. #9637
- We’ve fixed a distorted cursor at scale sizes larger than 1 when dragging and dropping item details. #12337
- We’ve fixed an issue where an item details wouldn’t refresh automatically after changing specific app settings, such as toggling Markdown formatting or always showing passwords and credit card numbers. #18429
- We’ve fixed an issue where dragging and dropping a password wouldn’t work properly if the password contained emojis. #18394
- We’ve fixed an issue where signing in to a 1Password account that’s already in the app would prompt you to sign in again. #18111
- We’ve fixed an issue where the Settings screen wouldn’t refresh after settings were changed via MDM. #18594!15505

- You can now copy the version number of the app in the About section in Preferences. #16010
- We’ve added animations when you open pop-ups in the app, like when you click the New Item button.!14346
- We’ve made a number of improvements in the way proxies are supported in the app. #14366
- The unlock animation has been sped up.!14362
- We’ve improved the screen reader support for the pop-up you see when moving items to a different vault. #16031 #3074
- We’ve updated the default icon used for Visa cards.!14137
- We’ve fixed an issue where the password field on the lock screen wouldn’t always be in focus automatically when opening the app.!14359
- We’ve improved the way that the app scans QR codes when setting up a one-time password field in an item. #10148 #15731
- You’ll now see an error message if 1Password is unable automatically configure your `.gitconfig` file to set up commit signing. #17206
- We’ve made some adjustments to the size of items shown in dropdown menus.!14134
- We’ve updated the 1Password icon used on the lock screen, for the All Accounts button, and in the About section in Preferences.!14443
- We’ve reorganized the Advanced section in Preferences to make them easier to navigate through. #17329
- Authentication prompts are now automatically closed if the SSH request times out. #17156
- We’ve improved the error messages displayed if commit signing doesn’t work as expected.!14709
- We’ve fixed a visual issue that could occur when zooming all the way in on the lock screen. #16281
- We’ve fixed some issues related to the alphabetical sorting of items when symbols are included at the beginning of the title.!14623
- We’ve updated the description for where you can find Recently Deleted items when you’re deleting an item. #17354
- We’ve fixed an issue where items couldn’t be saved in a vault if the permission to archive items wasn’t granted. #15904
- We’ve corrected the label used to refer to Traditional Chinese. #17521
- We’ve fixed an issue where “\\n” would be displayed at the end of the Password Strength summary in Watchtower in languages other than English. #17591
- We’ve fixed an issue in the item catalogue where items with a period (.) in the title couldn’t be focused when using keyboard navigation. #16335
- We’ve fixed an issue that caused the Manage Accounts window to be slow. #17442
- We’ve fixed a few design issues with the welcome tour. #17512 #17348
- We’ve fixed an issue where the sidebar wouldn’t display properly at certain zoom levels. #16394
- We’ve improved the icon size and text alignment in the sidebar of the Manage Collections window.!14624

- We’ve fixed an issue where the app window appears to be blank if the PC is configured with a pure black accent color. Thanks to Leonard B. for reporting and helping us find the issue on their system. #17021

- You can now use the 1Password SSH agent to automatically configure Git commit signing for your SSH keys. #17039
- You can now rename tags by right-clicking them in the sidebar. #9335
- You can now copy the sharing link for an item when viewing the sharing history. #13199 #13198
- You can now turn off two-factor authentication for your 1Password account from the 1Password app. #7403 #16888
- 1Password will now use the accent color you’ve chosen for your operating system. ✨!13226
- Partial (substring) matches will now show up in search results. #9056 #14001
- The 1Password SSH agent now supports SHA1 signatures. #12998
- The agent.sock file is now deleted when you turn off the SSH agent. #15303
- You can now choose how often your account password is required when you unlock with Windows Hello. #17009
- The “close window” keyboard shortcut now only closes a window instead of a modal.!13752
- You can now import SSH keys from older 1Password export files that don’t include the key metadata. #16477
- We’ve added Opera’s new browser signature to fix the integration with the 1Password browser extension. #16141
- We’ve updated the button after creating a Document item to say “Add File” instead of “Add Document”.!13653
- We’ve updated the way we refer to “Wireless Router” items in a few places throughout the app, like in the sidebar. #16258
- We’ve lightly updated the appearance of the checkmark icon used when signing into a previously used 1Password account. #14338
- We’ve added a + icon before the Add File button when creating a new Document item.!13813
- We’ve improved proxy detection support and now verify IP addresses instead of DNS hostnames only. #15726
- Importing an item that has a missing file attachment now adds a notice to the item’s details view that the file is missing. #16260
- We’ve updated Dutch, German, and several other translations and localized some buttons.!14124!13604!13992!13990 #16590 #16434!13816
- We’ve made some general performance improvements.!14049 #15283
- We’ve increased the file upload timeout so you can upload larger files. #17045
- We’ve made some improvements to vulnerable password checks in Watchtower. #17017
- We’ve fixed an issue where holding down the up or down arrow key wouldn’t scroll an item list. #16267
- We’ve fixed an issue where dragging an item wouldn’t be properly offset from your cursor. #16246
- We’ve fixed a visual issue that with highlighted tabs when the app window was narrow and at the max zoom level. #15792
- We’ve fixed an issue that caused escape characters () to appear on either side of certain words in non-English translations. #16270
- We’ve fixed an issue where the scroll position wouldn’t reset when switching between item lists. #6852
- We’ve fixed some crashes. #15812 #15024
- We’ve updated support to the SSH agent for the latest version of Git for Windows.!13765
- We’ve fixed an issue where editing an item with a long text field could show a light-colored scroll bar next to the field when Dark Mode was turned on. #16766
- Checking for an update no longer relies on the Windows registry to verify details about the installation directory. #12186 #15911
- We’ve fixed a sticky checkmark on the sign in popup. #16552
- We’ve fixed an issue in the Import modal where if you added an export file but decided to replace it with another one, cancelling that action would remove the previously chosen file in the modal. #16002
- We’ve fixed an issue where clearing a month/year date field would show “NaN”. #16389
- We’ve fixed an issue where a field in an item with two matching section identifiers could not be deleted.!12449
- We’ve improved 1Password’s Windows Hello implementation to be less likely to reset after restarting your computer.!13970
- We’ve fixed an issue where the scroll position was reset when deleting or deselecting items. #16756
- We’ve fixed an issue with the MSI installer where it would create an empty `%SYSTEMDRIVE%\APPDIR` directory. #16658

- You can now import a 1Password Unencrypted Export (1PUX), CSV export file from 1Password, or a CSV export of your iCloud Passwords via Safari. #8586
- We’ve added Dutch to the list of supported languages and updated some of the other translations.!13409
- You can now configure the SSH agent to ask for authorization once per application or per app session. #15801
- An MSI Installer is available for enterprise customers, please [contact our business support team](https://1password.com/contact-us/) for more information.!13220
- You’ll now be warned if you attempt to share an item that contains the sign in details for your 1Password account.!13373
- Selecting a vault is now more accessible with the keyboard when you select an item to move it. #2594
- When you open a modal, you can now see the default selection highlighted with a blue focus ring. #11746
- The font size for one-time passwords has been increased to match the size of other text fields. #15903
- If you use the export feature in the app, all vault icons will now be included in the exported data. #15975
- If you have an individual 1Password account, you can now view the sharing history for an item. #12504
- In the “Move this item to” popup, we’ve changed the Cancel button to an X for consistency. #8742
- The description of vulnerable passwords in Watchtower is now localized. #16208
- We’ve fixed an issue that could cause the app to crash when trying to sync after changing your account password. #13714 #15810
- We’ve fixed an issue where the keyboard shortcuts to copy item fields to your clipboard would copy the field values from the previously viewed item if you switched the item shown in the main app window using Quick Access or search. #15830
- We’ve fixed an issue where setup codes from 1Password 7 for iOS wouldn’t read properly by [1Password 8](https://1password.com/products/) if your account’s email address contained a plus symbol (`+`). #15875
- We’ve fixed an issue that would cause the General section in Preferences to flash when turning dark mode on or off. #12477
- We’ve fixed an issue with the SSH agent that could cause multiple prompts to be shown for the same authorization request. #16037
- We’ve corrected the French term used to describe a period (`.`) as a separator in the password generator. #15101
- We updated the tooltip shown when hovering over the Help button. #11635
- Using the keyboard shortcut to switch vaults or collections now works for locked vaults and it will bring up the unlock view for that vault.!13529
- We’ve fixed an issue that caused the Cancel button to not appear on the “Get a link to share this item” popup. #16130
- Watchtower will now automatically update if you change the collection you’re viewing.!13577

- You can now sort items by frequently and recently used. #4042
- You can now change how long your session remains active when using the 1Password SSH Agent. #15872 #15874
- Watchtower will now warn you when API Credential items are about to expire or when they’ve expired. #15438
- If collapsed, vaults and tags in the sidebar will temporarily expand if you drag an item over them. #14908
- Quick Access now displays better suggestions for open apps. #15172
- Search now treats `+` and `&` as word boundaries to better support searching for email addresses that contain these characters.!12584
- You can now open Settings using the 1Password icon in the notification area. #1604
- Changing the language in the app now updates the onboarding screen shown when no accounts are signed in without having to close and reopen the app first.!13098
- Changing the language in the app now updates the item, export, create vault, item sharing history, and proxy authentication modals if they were displayed without having to reopen them first. #15231!13068!13140!13133
- The title of the Settings window now updates when changing the language in the app. #15342
- Passwords containing 6 digits or fewer are no longer considered PINs and will be checked by Watchtower. You can click Ignore in the Watchtower banner to dismiss PINs. #15052
- We’ve updated the title of the language selector in settings. #15312
- When you choose a language, the list will now be displayed in your current language. #11216
- When you share an item, the icon will now be displayed clearly. #15522
- We’ve improved the way sessions are cached when using JetBrains IDEs with the SSH agent. #15379
- We’ve optimized and restored the menu animations to the app.!12893
- We’ve redesigned the Watchtower loading screen and security score. #15178 #15179
- The “delete share link” icon now has a tooltip on hover. #11970
- We’ve fixed an issue that would cause files to be downloaded again even when there was a local copy available. #15610
- We’ve fixed an issue that could cause items with Watchtower warnings that have been ignored to remain in the ignored section in Watchtower.!12532
- We fixed an issue where the names of vaults and items wouldn’t truncate properly in the sidebar and item list. #13930 #15661
- We’ve fixed an issue that could cause the title bar of the app to shift out of view when changing the icon for a vault. #15716
- We’ve fixed an issue where it wasn’t possible to scroll in the modal to create a new vault.!13165
- We’ve fixed an issue that could cause a large number of SSH agent authentication prompts to show up at once, or could render the SSH agent unusable from certain apps or terminal sessions if an earlier prompt timed out. #15488
- We’ve fixed an issue that could cause authentication prompts to pop up more often than they should when using Git Bash. #13699
- We’ve fixed an issue that would allow vaults to be created without a name. #14798
- We’ve fixed a crash that would occur when setting the app’s language. #14713
- We’ve fixed an issue where the checkmark wouldn’t be positioned correctly when changing a vault’s icon. #15447
- We’ve fixed an issue that could prevent modals from opening after attempting to move an item to a different vault.!12897
- We’ve fixed an issue that could cause the text in longer account names to overflow in the sidebar. #12858
- We’ve fixed an issue where the wrong scroll bar would appear when adding a date field to an item while dark mode was turned on. #15359
- We’ve fixed an issue where the delete button wouldn’t fill the full height in a multi-line field when editing an item. #15363
- We’ve fixed an issue that could cause extra spacing to appear when turning on “Show debugging tools” in Advanced preferences. #15477
- We’ve fixed an issue that prevented scrolling in the search box.!12988
- We’ve fixed an issue that allowed the copy password shortcut to work within the vaults where you don’t have permission to reveal the password. #15714
- We’ve fixed an issue that caused Watchtower vulnerable password checks to not be immediately performed on newly added accounts. #14728
- Non-numeric characters are no longer excluded from the credit card number field. #5599
- We’ve fixed an issue where sharing an item wouldn’t show all available options in the “Available to” menu. #15877
- Pressing the Escape key on modals now dismisses them reliably. #15062 #14739
- We’ve fixed an issue that caused the sign in modal to stay open after you’ve signed in. #15767
- We’ve fixed the reported crashes submitted to us. Thank you for submitting them! #15697 #15782

We replaced our code signing certificate to address an issue with the previous certificate, which was inadvertently revoked. This release is otherwise identical to 8.7.1. #15802

- We’ve added language options for Korean and Japanese back to the app, along with updating other translations from Crowdin. #13744
- You can now right-click items to permanently destroy them in the Recently Deleted list. #14180 #10482
- If you open an item in a new window, you’ll now see a toast notification when you perform actions like copying the contents of a field.!12458
- We’ve introduced limits in the number of consecutive authentication prompts that will be shown when using the SSH agent. #14442
- We’ve added additional animations to the lock screen.!12224
- The location of the unlock checkmark on the lock screen shown when you unlock the app now changes depending on if you’re signed in to one or multiple 1Password accounts.!12222
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!12007,12320
- We’ve made under-the-hood design improvements to the sign-in modals shown when you open the app for the first time.!12594
- Diagnostic reports now include information about how frequently the SSH agent prompts you to authenticate. #14014
- You can now search for items using their UUID. #12859
- Closing the sign in modal before clicking Done will now immediately cancel the in-progress sign in attempt. #14164 #14715
- Changing the language in the app now updates the keyboard shortcuts, move and duplicate item, and locked account modals if they were displayed without having to reopen them first.!12846
- We’ve made a light visual improvement to the lock screen when Dark Mode is turned on. #15325
- We’ve localized the 1Password menu in the task bar. #15102
- We’ve removed a potentially offensive word from the password generator word list. #10558
- You can now drag items to the left side of the app’s main window to temporarily display the sidebar if it’s hidden.!12191
- If you attempt to move or duplicate an item in the Archive list, vaults where you don’t have permission to archive items can no longer be chosen. #14786
- If you attempt to duplicate an item in the Archive list to a vault where you don’t have permission to archive items, you can no longer select the option to delete the duplicate item. #14785
- Clicking outside of a modal will no longer dismiss it from view. #6827
- We’ve fixed an issue where Quick Access would show app and website icons even if the setting to show rich icons was turned off. #14677
- We’ve fixed an issue when creating a new item where the vault selector would show an empty message for frozen accounts.!12447
- We’ve fixed an issue where the password history button wouldn’t work when viewing an item in a new window. #10272
- The app now displays the specific item date fields in the format you’ve chosen in your operating system’s settings.!12170
- We’ve fixed an issue with the sizing and placement of the callout on the Watchtower dashboard that’s shown when a collection is selected.!12333
- We’ve fixed a few visual issues in the password generator that could cause text to be unnecessarily truncated. #13822 #13844
- We’ve fixed a visual issue that would cause the search box to flash when clicking the button to clear the search field. #13919
- We’ve fixed a visual issue related to the focus ring for selected items in the sidebar. #14493
- We’ve fixed a visual issue that could cause empty space in the list of vaults shown when moving or duplicating an item if the list was filtered. #14550
- We’ve improved the way that we use word “item” (singular or plural) in the modal shown before you delete a vault. #14110
- If originally opened by 1Password in your browser, the app will now no longer close when Firefox is quit. #14770
- Changing your Windows keyboard layout will no longer require you to restart 1Password for keyboard shortcuts to continue working with the updated layout. #13698
- We’ve fixed an issue where clicking the buttons to create new items for categories other than logins wouldn’t work. #14894
- We’ve fixed an issue where the options to cut or copy were unavailable when editing password fields in items.!12703
- We’ve fixed an issue that could cause the app to use high CPU usage when your computer wasn’t connected to the internet. #14608
- When you edit an item, the app now fetches the latest version of the item from your local database instead of a cached version of the item. #3132
- Pressing Shift + Tab will now place focus on the first available option, such as in the item catalog after you click New Item.!12537
- We’ve fixed an issue where the inner border of drop-down menus was hidden when dark mode was turned on. #14906
- We’ve fixed an issue that caused Quick Access to incorrectly show All Accounts selected after unlocking instead of remembering the account or collection selected in the previous session.!12448
- We’ve fixed an issue where the SSH agent would reject all connection attempts after biometric unlock times out. #15173
- We’ve fixed an issue where focusing the button for a specific field would have a focus ring on both the button and the field instead of just the button. #14492
- The password generator is now scrollable when the window is smaller.!12763
- We’ve fixed a few visual issues where elements would appear on top of each other. #15266 #14477
- We’ve fixed an issue that caused the focus ring on the password history field to be cut off on the top. #14477
- We’ve improved the comma detection on international keyboard layouts when using the comma to add multiple tags to the item. #15158
- One-time password fields no longer shift when hiding and restoring the timer animation.!12809
- The app is now more compatible with TLS interception solutions used in some corporate environments.!12826
- We’ve fixed an issue where the banner to move an SSH key out of a shared vault could result in the item being moved to the Personal or Private vault in different account signed into the app. #15270
- We’ve fixed an issue where drop-down menus could still be clicked even when disabled. #15336
- We’ve fixed an issue where the Feedback menu wouldn’t update when the language was changed in the app. #15307
- We’ve fixed an issue in Preferences where dragging the scroll bar to the bottom wouldn’t scroll all the way down. #15306
- We’ve fixed an issue that caused the [1Password extension](https://1password.com/downloads/windows/#browsers) to hang the first time the 1Password icon in the Firefox toolbar was clicked if “Connect with 1Password in the browser” was turned on in the app. #14742
- We’ve fixed an issue that could cause the app to crash if memory access protections failed on computers in some corporate environments. #13465
- We’ve fixed a rare issue where if the app was in stuck in a log loop (fixed in previous updates), it would also prevent the app’s ability to auto-lock itself. #14454

- You can now click the 1Password logo on the lock screen to submit your password. #14095
- You can now edit and delete vaults in the app. #13945
- The names of item categories in the sidebar are now localized.!12400
- We’ve added 4 and 8 hour options to the “Lock after the computer is idle for” security setting.!11737
- You can now search filenames to find file attachments and document items.!11694
- You can now adjust the density and zoom level of the app in the Appearance settings.!11865!11893
- When viewing an empty shared vault, you’ll now see pictures of the users and groups it’s shared with. #12940
- We’ve updated the All Accounts icon, as well as icons throughout the sidebar. ✨!12089
- Tooltips now have animations. ✨!11328
- You can now view a list of your items sorted by their password strength in Watchtower.!11521
- We’ve added a sorting option to Watchtower’s Password Strength item list. #14239
- Settings now opens in its own window. #13009
- We’ve improved the way we retain the positions of our app windows. #14066
- We’ve improved the screen reader experience by adding the appropriate titles to app windows. #13772
- We’ve improved performance by temporarily stopping Quick Access when 1Password is locked.!11469
- Unlocking the 1Password app will also load Quick Access in the background for quicker access.!11755
- Search results in Quick Access will now be refreshed when you change the account, collection, or vault you’re searching. #13155 #13189
- Search results will update when switching between accounts or collections.!11762
- Search when linking an item will now include full item titles, not just what they start with. #7598
- You’ll now always be taken to the All Items list when switching to a different account or collection. #8169 #12413
- We’ve updated the design for when you sign in to a new 1Password account.!10895
- When signing in to multiple accounts, the button under the list of accounts now displays the word “Done” instead of “Sign In”.!12005
- We’ve updated the wording on a sign in option to “Enter account details”. #14246
- We’ve improved the design of the 1Password account sign in menu. #13476
- We’ve improved the wording on the sign in popup. #13695
- The biometric icons on the unlock view are color-matched to fit the rest of the app.!12116
- We’ve added tooltips to the sort and biometric unlock buttons and removed the tooltip from the New Item button. #12396 #6635
- Tooltips will now hide when they’re no longer in view.!12262
- Category icons now look clearer throughout the app.!11795
- We’ve increased the contrast of usernames in the item list to make them easier to read. #13210
- Date headers in the item list are now localized. #12666
- We now use sentence-style capitalization for item catalog articles. #13260
- We’ve improved the design of empty item lists and details.!11099
- The setting to change what clicking the 1Password icon in the menu bar or tray does will now show all available options. #12582
- We’ve updated the illustration displayed in the About screen. #13916
- Resolving the issue for an item in Watchtower no longer deselects it in the item list. #6872
- The sidebar will now show unknown or deleted item templates as “Others”. #13231
- We’ve added some animations to the sidebar when expanding and collapsing sections.!11916
- We now remove duplicate email addresses if you paste in a list of email addresses when preparing to share an item. #13229
- We’ve updated links to 1Password Developer Documentation to be more specific. #13380
- SSH Key items in non-private vaults will display an informative banner explaining that they need to be in the private vault to use them with 1Password SSH Agent. #13982
- You can now reveal an SSH key passphrase when you’re typing it into the prompt.!12165
- We’ve removed the system tray step from the setup flow.!12160
- Password strength is no longer shown on PIN codes. #14174
- We’ve updated the keyboard shortcut to view the Keyboard Shortcuts modal to be Ctrl + Shift + Forward Slash (/). #11820
- We’ve added Show 1Password and other shortcuts to the shortcuts list (Ctrl + /). #5335
- We’ve fixed the issue where using the Backspace shortcut didn’t follow the “Archive and Don’t Ask Again” setting. #9779
- We’ve fixed an issue where the app menu button didn’t display when setting up 1Password for the first time. #13789
- We’ve fixed an issue where the sign-in options menu wasn’t displayed if one account was found. #13691
- Date fields will now be consistent after your time zone changes. #12492
- We’ve fixed an issue that prevented syncing when several very large items are changed at the same time. #14467
- Drag and drop now includes all selected items, not just visible ones.!11479
- We’ve fixed the height of the dragged items image when dragging and it now respect the interface’s density setting.!12008
- We’ve fixed the hover state for the item’s custom icon picker. #13820
- We’ve fixed issues that prevented the app from being controlled by computers with touch interfaces.!11818!11879
- We’ve improved how keyboard shortcuts work with non-US keyboard layouts. #12850
- We’ve fixed an issue that caused the search status bar to be misaligned when the sidebar was hidden. #14213
- We’ve fixed an issue where the “Choose an item” modal for linking related items was resizing based on the results instead of remaining a fixed size. #13720
- The banner image in the item catalog articles now resizes properly. #13331
- We’ve fixed an issue where the item list’s context menu is not dismissed when locking 1Password. #13486
- Dropdown menus will now close when opening a modal, such as when you open the New Item dialog. #13988
- We’ve fixed an issue that prevented selecting some items when holding Shift and pressing arrow keys. #13532
- We’ve fixed an issue where selecting multiple items with the Shift and arrow keys could result in the items becoming deselected. #13924
- We’ve fixed an issue that prevented saving an item when only the month was filled in the date field. #6315
- We’ve fixed an issue where the strength of a password wouldn’t be calculated if it contained Unicode characters. #13996
- We’ve fixed an issue where tooltips didn’t display correctly. #13526
- The icon for a suspended 1Password account is now aligned properly in the vault selector. #13464
- The 1Password SSH Agent is now more resilient against errors and will prompt for authorizations more reliably. #13547
- We’ve fixed an issue that prevented 1Password from importing OpenSSH private keys exported from PuTTY. #13510
- We’ve fixed an issue where certain biometric settings disappeared in the Security settings when biometrics are temporarily unavailable. #13304
- We’ve fixed an issue where changing the language in the app would not adjust the language used in the item view area when no item was selected.!11706
- We’ve improved the way certain warnings are displayed when viewing the *Browser* or the *Developer* settings. #12094 #13535
- The SSH Agent no longer prompts you to unlock twice. #14143
- We now clear out cached information about the system’s integrity state when “Use the Trusted Platform Module with Windows Hello” is turned off. #14025
- The installation progress bar now has a maximum width to avoid taking up the entire width of large monitors, especially ultrawide monitors. #13801
- We’ve fixed an issue that caused the app size to be calculated incorrectly in Windows' Apps & Features list. #13949
- We’ve fixed an issue where 1Password in your browser could get stuck on loading or unlocking screens the first time you connect it with the app. #14020
- The proxy authentication modal will now present itself again if it was closed due to losing focus. #14308
- We’ve fixed an issue where the auto-lock monitor logging would create very large log files. #14161
- The registry is now only updated when 1Password for Windows successfully updates. #13420

- We’ve added a new toggle for “Auto-detect network settings” under Advanced settings if you have a proxy but need a direct connection for network connectivity. #12632!11601
- We’ve improved how the prompt to unlock with Windows Hello appears if you use multiple displays. If you open Quick Access, the prompt will pop up on the active display. If you open the main app window, the prompt will pop up on the display where the app window is located. #9448 #13228!11569
- 1Password now supports using the [Trusted Platform Module (TPM) with Windows Hello to unlock 1Password](https://support.1password.com/windows-hello/#manage-your-settings) on more systems than before, including AMD’s firmware TPMs and virtual TPMs in certain virtualization solutions on supported setups. #13307!11739
- We’ve made some adjustments that should allow some customers to use the Trusted Platform Module with Windows Hello more consistently.!11666
- Closing 1Password now dismisses the Windows Hello prompt. #13306!11569
- The prompt to unlock with Windows Hello should now appear faster on some devices.!11454
- We’ve updated our internal libraries to the latest versions for general improvements and fixes.!11546
- We’ve made changes to help prevent the app from crashing on startup on certain systems. #11668
- 1Password will now check for supported Windows Hello features before enabling the setting to prevent crashes on older versions of Windows 10. #13705!11698
- We’ve implemented a different fix for the issue where customers could see a blank app window if their Windows account names had symbols or spaces in it. #13223

1Password now includes full support for SSH keys, providing the easiest and most secure way for developers to manage SSH keys and use Git in their daily workflow.

Together with our new command-line tool, authorizing services and securing your development toolchains is easier then ever.

See our [SSH and Git, meet 1Password](https://blog.1password.com/1password-ssh-agent/) and [Your CLI wish is our command](https://blog.1password.com/1password-cli-2.0/) announcement posts for full details.

Here’s the full list of changes in this release:

- For Windows computers with TPM, Windows Hello can now be used for unlocking after you quit the app or restart your computer without entering your account password.!11028
- You can now show Categories in the sidebar. #9299
- You can now hide Tags in the sidebar.!10916
- You can now hide the sidebar in the app.!10961!11036!10957
- You can now choose to ignore Watchtower warnings and suggestions for item by clicking Ignore after expanding the banner.!11354
- You can now scan a QR code directly from the “Two-factor authentication available” banner on an item. #12441
- You can now filter the items displayed in lists with Ctrl + Alt + F.!10533
- You can now use the Page Up and Page Down keys to navigate sections the item list. #1546
- You can now change what happens when you click 1Password in the menu bar. #10768
- You can now drag and drop multiple lines of text into multi-line fields, such as an address. #12606
- New text fields added to items now support multiple lines of text.!11138
- You can now open our Developer Documentation site from Preferences > Developers. #12315
- We’ve added new icons and illustrations that display in empty lists and other scenarios where there’s no information to show. #12149
- We’ve added all-new backgrounds that display when viewing an empty list of items, like in a new vault with no items added. #12942
- The dropdown menu to adjust your sorting order now shows the total number of items in the list. #10674
- After changing your password, 1Password will now check for a new account password before rejecting it as an incorrect password. #11834 #4511
- You can now share items with any email address across a domain. To view an item, the recipient can verify their email address at the specified domain.
- If you change your language in the app, creating a new item will now display the names of item categories and default fields in your chosen language.!11064
- Localization has been improved for a number of our supported languages using new translations from Crowdin.!11255
- We’ve improved some Italian translations in the interface. #11195 #11215
- Watchtower now updates properly after changing your language in the app. #11210
- Switching between accounts or collections while Watchtower is open will no longer switch to the All Items view. #12735
- The item list in Watchtower no longer resets to a private vault item list when switching accounts or collections. #13050
- We’ve updated the design of the cards shown in Watchtower. #12726 #12736
- Images displayed throughout the app now load much faster. #12085
- Rich icons are now reloaded less often.!10978
- Collapsed sections in the sidebar now have better visibility, keyboard navigation, and accessibility. #8971
- In the sidebar, Archive and Recently Deleted now stay at the bottom when there’s extra space. #12365
- Hovering over truncated text in the sidebar now displays a tooltip with all of the text. #8349
- We’ve improved the experience when dragging items to the sidebar when you don’t have permissions to modify an item. #9609
- When a category is selected in the sidebar, the name of the category will be shown in the app’s title when multitasking.!11072
- Quick Access now shows the default actions for each item in the list if you hover over it with your mouse cursor.!11407
- We’ve improved the accuracy of suggested items shown in Quick Access. #10753 #12834
- Quick Access is now positioned in the center of the screen more consistently.!10899!10866
- We’ve made improvements to the visual experience of opening the main app window if it was closed. #12085 #8874
- The order of items is now remembered after you close the app. #11317
- The lock screen has received updates to improve the visual experience while zoomed in. #5608
- The lock screen has received some visual improvements for customers who are signed into five or more 1Password accounts. #13015
- We’ve made a number of smaller visual improvements to the lock screen related to the password field and buttons. #12997
- We’ve improved the experience for keeping Windows Hello in focus when using it to unlock 1Password. #12091
- We’ve improved experience of using dropdowns throughout the app, such as keeping them open when resizing the app window. #12220!11021
- We’ve made some improvements to the experience of changing the password tied to an item in the app. #6163
- We’ve improved the way that email addresses are displayed when viewing the history of a shared item. #12042
- If you try to share an item, you’ll now be presented with the limitations enforced by your account’s administrators, such as how many times an item can be viewed. #13151
- The design of the confirmation dialog when moving an item has been improved.!10725
- We’ve added a View button to the to the confirmation after deleting an item. #11796
- We’ve added contextual hints to help you when you can’t find something. #12380
- Added an icon to the No Results screen when searching.!10860
- The design of an empty item list has been improved. #12147
- If you’re viewing a list of items, but don’t have a specific item selected, you’ll now see a new design in the empty item view space on the right. #12939
- The item details column now displays helpful information when nothing is selected. #12148
- The tray icon is now always responsive, even when multiple clicks are performed in quick succession.!10970
- If the 1Password icon is hidden from the system tray, the “Click the icon to” option in Settings will be now disabled. #12583
- You can now use non-ASCII global keyboard shortcuts.!10920
- You can now use the Escape key to hide the password field for expanded accounts when viewing a list of existing accounts to add to the app. #10563
- Unlabeled buttons are no longer readable by screen readers. #12065
- 1Password now automatically unlocks and shows contextual information when the CLI is authorized. #11673
- Accessing secrets with command-line tool extends the validity of the session.!10679
- We’ve fixed an issue where Watchtower would show an empty password strength section while a viewing a collection with no items in the selected vaults. #13048
- We’ve fixed an issue that could cause the app to visually flicker when changing some settings while Watchtower was open.!11412
- We’ve fixed an issue where the names of collections could appear unaligned when switching among your accounts and collections. #12472
- We’ve corrected the color of the icon shown beside a locked account when switching among your accounts and collections in the app. #13080
- We’ve fixed an issue where the color of the chevron in the category picker was the wrong color. #11638
- We’ve updated the quality of the icon shown when you have no recently deleted items after clicking Recently Deleted in the sidebar. #13297
- We’ve fixed an issue where text couldn’t be dragged and dropped into the fields when signing into an account. #12648
- We’ve fixed an issue where text in a field couldn’t be dragged and dropped into a remote Windows session window (RDP). #12728
- The message displayed when copying a gender field to the clipboard has been corrected to show “Copied gender”. #8412
- We’ve fixed an issue related to the formatting of certain URLs when viewing an item. #12558
- We’ve fixed an issue where adding a username to a Password item would show web form details. #12979
- We’ve fixed an issue where clicking the reveal password button when unlocking the app wouldn’t return focus to the password field.!11067
- We’ve fixed an issue with creating an new item from a custom template with fields that contained the same title. #12434
- The first tag is no longer selected by default when adding a tag to an item. #12559
- Tag suggestions no longer include tags from deleted items. #12449
- We’ve removed text ligatures to avoid ambiguity when reading revealed passwords. #12574
- We’ve fixed an issue that could cause the same item to be suggested more than once in Quick Access.!11316
- We’ve fixed an issue where Quick Access didn’t open on the active display. #12590
- We’ve fixed an issue where Quick Access was dismissed on unlock. #10246
- We’ve fixed an issue that caused the lock screen to flicker. #12085
- We’ve made a slight update to the phrasing used when signing in to an account. #8526
- We’ve updated the message that’s displayed when you sign out of a 1Password account in the app. #9221
- Logs no longer display the names of files when they’re attached to items. #12916
- We’ve fixed an issue where customers would see a blank app window if they had certain symbols in their Windows account name. #13223

You can now search for untagged items using `=untagged` to quickly find items you haven’t organized yet. This joins our `=vault:$name`, `=tag:$name`, `=category:$name`, and `=favorite` advanced search scope options.

![Screenshot of the untagged advanced search scope in action](https://releases.1password.com/img/rn/b8.5.0.10-untagged-advanced-search-scope.png)

There’s a new Developers section under preferences. It’s a bit sparse at the moment 😂 and yes it is a *little* bit mean of me to tease you like this, but it’s something I’m incredibly excited about and couldn’t wait to share. Something cool is coming soon and I think you’re going to love it. 🤘

![Screenshot of the new Developer section under Settings](https://releases.1password.com/img/rn/b8.5.0.10-developer-preferences-window-coming-soon.png)

Other notable callouts include some huge improvements to export (you can select a specific account and the export now includes all files) along with improvements to the biometric unlock experience when opening the app.

We added support for changing vault collections within Quick Access. With today’s release you can now switch between them using the Ctrl+1 through Ctrl+9 keyboard shortcuts.

![1Password Quick Access window with a custom collection selected using the new keyboard shortcuts](https://releases.1password.com/img/rn/b8.4.0.46-quick-access-hero-custom-collection.png)

We also improved our network stack to support custom corporate network setups that use various security protections. This was the top reported issue with [1Password 8](https://1password.com/products/) on Windows so we’d love to [hear from you](https://1password.community/categories/desktop-betas) if it solved the connection issues for your setup.

By popular demand you can now add your 2FA secrets to an item by scanning QR codes from within the main app, in addition to [saving QRCodes in your browser](https://support.1password.com/one-time-passwords/#set-up-two-factor-authentication-for-a-website). Add a one-time password and then click the QR code icon to scan an image anywhere on your screen or from your clipboard.

![An item being edited with a QRCode scanner icon shown on a one-time password field](https://releases.1password.com/img/rn/b8.5.0.79-scan-2fa-qrcodes-in-app.png)

While scrolling through item lists you’ll now find the number of entries being shown included at the end of the list.

![An item list scrolled to the very end, revealing the number of items in the list](https://releases.1password.com/img/rn/b8.5.0.79-item-counts.png)

And Quick Access now always remembers your selected account or collection, including across application restarts.

![Quick Access with the account and collection selection open](https://releases.1password.com/img/rn/b8.5.0.79-quick-access-collection-selection.png)

You can now view the history of items shared using our password secure sharing tool, [Psst!](https://blog.1password.com/psst-item-sharing/). After you’ve shared an item you’ll now find a `View history` button in the sharing window.

![The sharing window for an item showing who it is being shared with along with the new View history button](https://releases.1password.com/img/rn/b8.5.0.83-item-sharing-details-view-history.png)

The history enables you to see when you shared an item, who you shared it with, and how many times they have viewed it. You can also delete entries to expire the share link immediately. Here’s how my pie recipe looked after I shared it during Thanksgiving.

![The sharing history for my pie recipe after I shared it with my newsletter subscribers](https://releases.1password.com/img/rn/b8.5.0.83-item-sharing-history.png)

Watchtower banners for items with a compromised, vulnerable, or weak password now include a button to take you to the website to change that password.

![A Watchtower banner pointing out that an item has a weak or vulnerable password, along with a Change Password button](https://releases.1password.com/img/rn/b8.5.0.102-change-password.png)

A new Appearance section has been added to Preferences, allowing you to choose between light and dark themes. And it gives us plenty of room to add some customizations for the sidebar in a future beta. 🙂

![Preferences window with new Appearance tab selected](https://releases.1password.com/img/rn/b8.5.0.102-apperance-preferences.png)

Tags can also be deleted directly from the sidebar. This is super convenient and will automatically update all items that have this tag.

![A screenshot of the sidebar with a tag selected along with a context menu with the Delete menu item highlighted](https://releases.1password.com/img/rn/b8.5.0.102-delete-tag-from-sidebar.png)

Here’s the full list of changes in this release:

- We’ve improved our network stack to support custom corporate network setups that uses various security protections. (Let us know if this resolves any connection issues you were experiencing before!)!7382
- The option to export login and password items to a CSV file has now been added. #11825
- Document items, attachments and archived items are now included when performing an export. #10956 #10954
- We’ve added an option to temporarily display hidden fields with a keyboard shortcut (`Ctrl+Alt`).!10077
- We’ve added a new search scope (`=untagged`) to locate items without tags applied. #10134
- The total number of items is now shown at the bottom of lists in all Watchtower categories. #12064
- Quick Access now supports changing vault collections independently from the main 1Password window.!10092
- Quick Access now supports using keyboard shortcuts (`Ctrl+1` - `Ctrl+9`) to switch among accounts and collections. #11036
- Quick Access now detects more running apps for displaying suggested items. #11516
- Quick Access now remembers the account or collection selection after restarting the app. #11667
- Quick Access now preserves search terms when switching collections. #11969
- Expanding the Watchtower banner on an item with a compromised, vulnerable, or weak password now presents a button to take you to the website to change that password. #12154 #12153
- Installing 1Password will now display a progress bar during installation. #11330 #11106
- The app’s main window now temporarily fades into the background when dragging and dropping fields from items.!10360
- QR codes for two-factor authentication can now be scanned from your screen or clipboard when editing an item. #5963!10486
- The number of items in a list can now be viewed by scrolling to the bottom of the list. #10673
- You can now view the history of items shared using [Psst!](https://blog.1password.com/psst-item-sharing/) as well as delete actively shared links.
- The button to reveal the password on the lock screen will remain visible once toggled on, even if the password field is empty.!10555
- You can now right-click on a tag in the sidebar to delete it.!10434
- We’ve added a Developers section to Settings.!10016
- An Appearance section has been added to Settings.!10674
- We’ve improved the experience when showing item suggestions in Quick Access. #10807
- We now label keyboard shortcuts using Ctrl instead of Control in Quick Access and settings.!9831
- Using Quick Access to view an item in 1Password will now bring the app to the foreground if already open. #9455
- In Quick Access, we’ve improved how we present the text that indicates where an item is located. #11789
- Quick Access and the main 1Password app now show collections in the same order. #11048 #12099
- Quick Access now sorts suggested items for running apps in alphabetical order. #11573
- We’ve improved the experience of enabling biometric unlock when launching the app for the first time.!10050
- We’ve made a number of improvements surrounding focus for both the 1Password app and other apps while using Quick Access.!10573
- We’ve added the ability to choose a specific account when exporting. #11113
- Entering your account password is now required when exporting data.!10040
- The app won’t automatically lock when performing an export now. #10947
- Exports can now be canceled after being started. #11116 #10945
- Partially exported files are now automatically deleted if an export halts. #10955
- We’ve updated the alert dialog that’s shown when exporting to match our current design specifications. #11118
- We’ve improved the message displayed when preparing to export data. #11569
- Users are now informed if an export fails, along with why it may have happened. #11119
- Additional metadata is now included when exporting items containing [Masked Email](https://1password.com/fastmail/) addresses. #9463
- Exported data files now contain a prefix of “1PasswordExport” to indicate what they contain. #2223
- We’ve improved the way we handle exporting items that include one-time passwords. #11953
- We’ve improved the biometric unlock experience when opening the app.!9977!9880!9991
- Searching within a vault no longer displays the scope syntax outside the search bar.!9739
- We’ve made improvements to how the item list renders when searching.!9957
- We’ve improved localization for several of our supported languages.!10018 #11159
- The Tab key can now be used to navigate through existing accounts when signing in. #10339
- We’ve improved the experience when using a keyboard to navigate between articles in the item catalog. #10942
- We’ve reduced CPU usage when the app is locked or idle. #11353
- We’ve improved the design when viewing deleted Document items to clarify the file itself cannot be accessed. #11311
- It’s now possible to toggle hardware acceleration on and off in Advanced settings. #3764 #6066
- We’ve fixed an issue where information copied to the clipboard wouldn’t be cleared after 90 seconds. #11557
- The typography and spacing for text within the main app window has been adjusted.!10270
- Search now includes results for section and field titles within items. #7775
- Diagnostic information and logs no longer record the username associated with a user’s computer. #10833
- We’ve improved the accessibility experience of signing into the app with a new account and when existing accounts are found. #10511 #11452
- We’ve updated the design of the onboarding screen when launching the app for the first time. #10462
- The search field is now given focus when opening the app. #7945
- The experience of using Windows Hello with 1Password has been improved when switching to another application without completing the unlock. #11226 #11332
- Using Windows Hello to unlock 1Password now has additional text to explain why the prompt is shown.!10322
- We’ve improved the speed at which potential network issues are reported when downloading larger files.!10442
- We’ve improved the accessibility experience related to the custom icon button when editing an item. #11790
- Users with accounts that have Duo enabled can now sign into the app. #11393
- We’ve made a several improvements to ensure the fields and selections in the app remain in focus, such as when dragging the window by the toolbar or switching to another window then back to 1Password.!10411
- The keyboard shortcuts window now correctly reflects any user-made changes to the default keyboard shortcuts. #11386
- We’ve improved the visual experience when authenticating an account with two-factor authentication enabled. #11873
- Tooltips in the app are now fully opaque.!10556
- We’ve updated the reveal all characters button when viewing an item in large type to support localization.!10567
- We’ve updated a few links for the libraries we use listed in our credits and acknowledgements. #12016
- We’ve improved the way focus in fields is handled when manually signing into an account after opening the app for the first time.!10682
- We’ve improved the experience and accessibility when adjusting the length of a password using the password generator. #11933
- We’ve improved the experience for configuring keyboard shortcuts for non-US keyboard layouts.!10310
- We’ve updated the design of the window shown when you sign in by importing an [Emergency Kit](https://support.1password.com/emergency-kit/).!10659
- We’ve made some visual tweaks when moving items across vaults or accounts.!10754
- We’ve slightly increased the spacing between lines in the sidebar.!10761
- Extra whitespace is no longer shown at the bottom of the window when changing a vault’s icon. #12128 #8056
- We’ve adjusted the shade of red shown in a few places throughout the app, such as in the countdown indicator for one-time passwords.!10706
- The last used collection is now restored after quitting and reopening the app. #12068
- When in a collection, new items now save to the first vault in the selected collection by default. #7756
- The release channel selections no longer use all capital letters. #7169
- There are now limits on how far you can zoom in and out in the app.!10674
- We’ve fixed an issue where clicking on a tag from the drop-down list would not apply the tag to the item. #11571
- Using Secure Desktop when unlocking the app now works reliably.!9840
- Search results are now scoped to the selected account and collection!9961
- When using search, entering a scope without a query won’t display suggestions. #11035
- We’ve resolved an issue where locking the app could result in lost changes when editing an item. #10876 #7918
- We’ve fixed an issue where choosing a field suggestion when creating a new item could close the modal. #11292
- The hint bar in Quick Access no longer displays two options for “Copy Password” when viewing a Password item. #10983
- In Quick Access, a keyboard shortcut is no longer displayed to show Quick Access if one is not defined in Settings. #11976
- Using Quick Access to open an item in the app will now bring the main app window to the foreground if already open. #12095
- Date fields copied from items in Quick Access are now displayed correctly when pasted. #11964
- We’ve fixed an issue where using keyboard shortcuts to switch collections wouldn’t work in Quick Access. #12090
- Tags are now shown when viewing recently deleted items. #11326
- We’ve fixed an issue where using the Return or Enter key when adding a tag wouldn’t apply it to the item. #11331
- We’ve fixed an issue where scrolling wasn’t possible when creating a new item.!10001
- We’ve fixed an issue where the Save button could become hidden when creating an item.!10032
- We’ve fixed an issue where the Save button was incorrectly enabled for Document Items that didn’t yet have a file. #11027
- We’ve fixed a visual issue related to creating a new item from the item catalog. #11415
- It’s now possible to scroll in alert dialogs if they exceed the height of the app window. #4608
- Icons in the sidebar have been properly aligned. #10959
- We’ve fixed the width of dropdown menus throughout the app. #11300
- We’ve fixed an issue where viewing an item field in Large Type could result in overlapping characters.!9869
- We’ve fixed an issue where the left arrow button didn’t work properly when using the item catalog. #11147
- We’ve fixed an issue with false positive results in our diagnostics report related to address exceptions for proxy servers. #11070
- We’ve fixed an issue with editing labels that offer suggestions, such as with security questions.!10199
- Creating a new Document item now specifies how a file can be uploaded. #11061
- The keyboard shortcut to Open & Fill an item in a browser now works properly within the app. #11064
- We’ve resolved an issue where locking the app while editing an item could result in losing changes. #11473 #11465
- The app’s main window will not jump to the foreground if it automatically locks while open in the background.!10182
- We’ve fixed an issue where downloaded files wouldn’t be included in exports.!10251
- We’ve fixed an issue with the spacing of placeholder text in text fields.!10289
- The back button in the app now works properly when creating a new item started from 1Password in your browser. #11885
- We’ve fixed an issue where revealing a concealed field would open the main app window when viewing an item in its own window. #11412
- We’ve fixed an issue where a revealed field would stay visible after editing and saving an item. #11477
- Items with long, single-line titles and fields now wrap and truncate properly when viewed. #8482
- When using the app with multiple accounts, “Vaults” is now always shown as the label in the sidebar when only one account is unlocked. #11891
- We now use `http` as the default scheme when proxy settings without a defined scheme are detected. #11866
- We’ve fixed an issue with the warning icon not displaying properly in a banner while in light mode. #9407
- We’ve fixed the contrast of the text in the About section in Settings.
- We’ve fixed an issue that could prevent text from being copied from certain fields. #11974
- We’ve fixed an issue that could prevent text from being pasted into one-time password fields.!10559
- Tags are now properly applied when editing an item after entering a comma. #11821
- We’e added proper padding to the tabs in the dialog box for setting up another device.!10521
- We’ve fixed an issue with where the option to unlock with biometrics was shown even after entering an incorrect password multiple times.!8824
- Creating a new item when viewing a collection now suggests the first vault you have the permission to create items in for saving. #7756
- We’ve fixed a visual issue with selecting the button to back out of search results via keyboard navigation. #11966
- We’ve fixed a visual issue with the field to add a tag being longer than necessary. #11200
- We’ve fixed an issue where changing the language in the app wouldn’t update the sidebar options in Settings.!10639
- We’ve fixed a crash for restricted user setups by changing how we open process with certain rights. #12306
- The 1Password icon in the notification area now shows its unlocked state when enabled while the app is unlocked. #6007
- We’ve fixed an issue where selecting a country in an address field wouldn’t always adjust the available fields for the address. #12060
- Clicking the back button after adding your first account no longer results in a blank screen. #11510
- We’ve adjusted the link provided to learn about what’s new when using a beta release. #11033

- Optimized an animation to reduce CPU usage. #10236
- We fixed a race condition that could lead to increased CPU usage while idle. #11353

- Everything is new! 😎