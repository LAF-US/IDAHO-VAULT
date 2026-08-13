---
title: "Set up Obsidian Sync"
source: "https://obsidian.md/help/sync/setup"
author:
published:
created: 2026-08-13
description: "Set up Obsidian Sync - Obsidian Help"
---
You purchased Obsidian Sync and are ready to get started. This guide will help you set up and adjust your Obsidian Sync settings for daily use.

## Set up Obsidian Sync for the first time

In this section, you'll create a new [remote vault](https://obsidian.md/help/sync/vault-types) and connect it to an existing local vault. You don't need to create a new, empty local vault to use Obsidian Sync for this purpose.

> [!info] Is your current vault in an iCloud, OneDrive, Dropbox, or other syncing folder? If yes, or you are unsure, please read this and Switch to Obsidian Sync before proceeding.
> 

**Prerequisites**

- An Obsidian account. If you don't have one, [sign up now](https://obsidian.md/auth?returnto=%2Faccount%2Fsync#signup).
- An active Obsidian Sync [subscription](https://obsidian.md/help/sync/plans). If you don't have one, subscribe from [your account dashboard](https://obsidian.md/account/sync).
- **Recommended**: A [backup system](https://obsidian.md/help/backup) in place for your Obsidian files. A syncing service is not a backup.

### Log in with your Obsidian account

1. Open **[Settings](https://obsidian.md/help/settings)**.
2. In the sidebar, select **General**.
3. Under **Account → Your Account**, select **Log in**.
4. In **Email**, enter your email.
5. In **Password**, enter your password.
6. Select **Login**.

### Enable Obsidian Sync

1. Open **[Settings](https://obsidian.md/help/settings)**.
2. In the sidebar under **Options**, select **Core Plugins**.
3. Toggle **Sync**.

### Create a new remote vault

1. Open **[Settings](https://obsidian.md/help/settings)**.
2. In the sidebar, select **Sync**.
3. Next to **Remote vault**, select **Choose**.
4. Select **Create new vault**.
5. In **Vault name**, enter the name of the remote vault.
6. In **Region**, choose your server [region](https://obsidian.md/help/sync/setup#Regional%20sync%20servers) for your remote vault.
7. In **Encryption password**, choose a password for your vault. This creates an end-to-end encrypted vault. The vault password is separate from your Obsidian account and can be different for each of your vaults. For more information, refer to [Security and privacy](https://obsidian.md/help/sync/security).
8. Select **Create**.

### Connect to a remote vault

1. Select **Connect** next to your newly created vault.
2. Enter the password you configured for the vault in the **Encryption password** field if you opted into [end-to-end encryption](https://obsidian.md/help/sync/security#What%20does%20end-to-end%20encryption%20mean?).
3. Select **Unlock vault**.
4. **Do not start syncing yet.** Check your sync settings in [adjust Obsidian Sync settings](https://obsidian.md/help/sync/setup#Adjust%20Obsidian%20Sync%20settings).
	- If you wish to start syncing immediately, move onto [begin syncing with Obsidian Sync](https://obsidian.md/help/sync/setup#Begin%20syncing%20with%20Obsidian%20Sync).
5. If you haven't already, close or dismiss the pop-up window prompting you to **Exclude Folders** and **Start Syncing**. Proceed to the next step.

#### Adjust Obsidian Sync settings

1. Navigate to **[Settings](https://obsidian.md/help/settings)** → **Sync** if needed.
2. If a device name has not been added, add one to make reading your Sync logs easier!
3. Toggle the settings under **Selective Sync** and **Vault configuration sync** to indicate which items should be synced to and from the remote vault.
	- **Note**: If you recently disconnected from a remote vault and are reconnecting without an application restart, some settings may already be toggled on.
4. If you make changes to any settings, restart Obsidian completely.
5. Once Obsidian is restarted, return to **[Settings](https://obsidian.md/help/settings)** → **Sync**.

#### Begin syncing with Obsidian Sync

If you are beginning syncing after connecting to a remote vault, you will see a **Start Syncing** button. Select this button to begin syncing.

If you are beginning syncing after adjusting Obsidian Sync's settings and restarting the application, you will see a **Resume** button within Sync's settings. Select this button to begin syncing.

> [!done] Syncing status
> When Obsidian Sync completes, a green circle with a checkmark appears in the bottom-right corner (desktop) or in the right sidebar (mobile). The Sync log will also display "Fully Synced" as one its most recent message.
> 
> For more details on sync statuses, refer to [Status icon and messages](https://obsidian.md/help/sync/messages).

To connect other devices to your newly created and synced remote vault, move onto [Sync a remote vault on another device](https://obsidian.md/help/sync/setup#Sync%20a%20remote%20vault%20on%20another%20device).

To learn more about settings and files, move onto [Sync settings and selective syncing](https://obsidian.md/help/sync/settings).

## Sync a remote vault on another device

In this section, you have already created a remote vault, and uploaded data to it. Now, you want to connect your other devices to it.

**Prerequisites**

- An Obsidian account. If you don't have one, [sign up now](https://obsidian.md/account#mode=signup).
- An active Obsidian Sync subscription. If you don't have one, subscribe from [your account dashboard](https://obsidian.md/account).
- Sync enabled within the [Core plugins](https://obsidian.md/help/plugins) settings.
- An active remote vault. If you have not yet made one, please create a [remote vault](https://obsidian.md/help/sync/setup#Create%20a%20new%20remote%20vault) first.
- **Recommended**: A [backup system](https://obsidian.md/help/backup) in place for your Obsidian files on your most-used device. A syncing service is not a backup.

### Sync your vault from the vault switcher

If you have freshly installed Obsidian, when you open the program you will be presented with the [Vault switcher](https://obsidian.md/help/manage-vaults). To create a new local vault from the contents of a remote vault, you will want to perform the following steps.

1. Open Obsidian (assuming this is your first time opening it)
2. Select one of the options depending upon your installation:
	1. **Desktop**: In the section that says Open vault from Obsidian Sync, choose **Setup**
		2. **Mobile/Tablet**: **Setup Obsidian Sync**
3. Login with your Obsidian User account
	1. If [2FA](https://obsidian.md/help/2fa) is set up, enter your 2FA code.
4. You will be asked to choose which remote vault you want to sync to this device. Select **Connect**.
5. You will be asked to choose a name for the local vault that will be created on the device to hold this data. Enter the name of your choice.
	1. If you use [Obsidian URI](https://obsidian.md/help/uri) s, you will want to use the same name as the local vault on your other device.
6. Select **Create**.
7. The remove vaults window will pop-up momentary as Obsidian Sync connects to your server and validates the subscription. It will then present you a *Setup Connection* window.
	1. It is highly recommended that you close or swipe down from this window, and [adjust Obsidian Sync settings](https://obsidian.md/help/sync/setup#Adjust%20Obsidian%20Sync%20settings) first.
		2. If you change any Sync Settings, please reload or restart Obsidian.

### Sync your vault from Obsidian Settings

If you have already created a local vault on this device, and you want to connect this local vault to a remote vault, the instructions are very similar to [Set up Obsidian Sync for the first time](https://obsidian.md/help/sync/setup#Set%20up%20Obsidian%20Sync%20for%20the%20first%20time).

### Log in with your Obsidian account

1. Open **[Settings](https://obsidian.md/help/settings)**.
2. In the sidebar, select **General**.
3. Under **Account → Your Account**, select **Log in**.
4. In **Email**, enter your email.
5. In **Password**, enter your password.
6. Select **Login**.

### Enable Obsidian Sync

1. Open **[Settings](https://obsidian.md/help/settings)**.
2. In the sidebar under **Options**, select **Core Plugins**.
3. Toggle **Sync**.

#### Connect to a remote vault

1. Open **[Settings](https://obsidian.md/help/settings)**.
2. In the sidebar, select **Sync**.
3. Next to **Pick remote vault**, click **Choose**.
4. Click **Connect** next to the remote vault you want to connect to.
5. In **Encryption password**, enter the password for your vault, if you have one.
6. You will be prompted to start Syncing. It is recommended to wait and adjust your sync settings first. If you do want to sync the entire vault to the device as is, you may **Start Syncing**.

> [!warning] If the vault on your device already contains some notes (not recommended), you'll be warned that those notes will be merged before proceeding. Conflicts will be resolved through Sync's conflict resolution.
> 

#### Adjust Obsidian Sync settings

1. Navigate to **[Settings](https://obsidian.md/help/settings)** → **Sync** if needed.
2. If a device name has not been added, add one to make reading your Sync logs easier!
3. Toggle the settings under **Selective Sync** and **Vault configuration sync** to indicate which items should be synced to and from the remote vault.
	- **Note**: If you recently disconnected from a remote vault and are reconnecting without an application restart, some settings may already be toggled on.
4. If you make changes to any settings, restart Obsidian completely.
5. Once Obsidian is restarted, return to **[Settings](https://obsidian.md/help/settings)** → **Sync**.

#### Begin syncing with Obsidian Sync

If you are beginning syncing after connecting to a remote vault, you will see a **Start Syncing** button. Select this button to begin syncing.

If you are beginning syncing after adjusting Obsidian Sync's settings and restarting the application, you will see a **Resume** button within Sync's settings. Select this button to begin syncing.

> [!done] Syncing status
> When Obsidian Sync completes, a green circle with a checkmark appears in the bottom-right corner (desktop) or in the right sidebar (mobile). The Sync log will also display "Fully Synced" as one its most recent message.
> 
> For more details on sync statuses, refer to [Status icon and messages](https://obsidian.md/help/sync/messages).

To connect other devices to your newly created and synced remote vault, move onto [Sync a remote vault on another device](https://obsidian.md/help/sync/setup#Sync%20a%20remote%20vault%20on%20another%20device).

To learn more about settings and files, move onto [Sync settings and selective syncing](https://obsidian.md/help/sync/settings).

## Manage your remote vaults

You have created and connected to a remote vault. You may have also synced this remote vault to multiple devices. This section goes over some of the other common instructions you may need in managing this remote vault.

### Disconnect from a remote vault

1. Open Obsidian's **[Settings](https://obsidian.md/help/settings)**.
2. Select **Sync** in the sidebar.
3. Click the **Disconnect** button next to Remote vaults.

You are now disconnected from the remote vault and are no longer syncing on this device.

### Delete a remote vault

> [!tip] Deleting a remote vault will not delete your local data on your device.
> 

1. Open **[Settings](https://obsidian.md/help/settings)**.
2. In the sidebar, select **Sync**.
3. Select **Manage** next to Remote vaults. A window will open with your list of remote vaults.
4. Select the trash can icon next to the remote vault you want to delete.
5. Confirm the deletion by selecting the red **Delete** button.
6. Your remote vault has been deleted.

> [!info] If there is no trash can icon visible you may need to first disconnect from the remote vault. Once disconnected, select the Choose button to open the list of remote vaults.
> 

### Regional sync servers

Obsidian Sync lets you choose the hosting location for your remote vault. If you're using version `1.4.16` or older of Obsidian, the location will be automatically chosen for you.

If you're unsure where your current vault's region is, check out [Where can I find my current Sync server and where is it hosted?](https://obsidian.md/help/sync/security#Where%20can%20I%20find%20my%20current%20Sync%20server%20and%20where%20is%20it%20hosted?) for guidance.

![sync-regional-sync-servers.png#interface](https://publish-01.obsidian.md/access/f786db9fac45774fa4f0d8112e232d67/Attachments/sync-regional-sync-servers.png)

sync-regional-sync-servers.png#interface

After selecting a location, your data center **cannot** be moved to a different server without re-uploading your data. To change regions, follow the [follow vault Sync regions guide](https://obsidian.md/help/sync/region).

> [!abstract] Sync regions
> **Automatic**: Your data center is chosen based on your IP location, at the time when you first set it up.
> 
> **Asia**: Singapore  
> **Europe**: Frankfurt, Germany  
> **North America**: San Francisco, USA  
> **Oceania**: Sydney, Australia

## Next steps

Here are some suggested documents to read next.

- Explore more about [selecting files and settings to sync](https://obsidian.md/help/sync/settings).
- Learn what happens if your remote vault [fill up](https://obsidian.md/help/sync/version-history).
- [Collaborate on a shared vault](https://obsidian.md/help/sync/collaborate) with another Obsidian Sync user.
- Check out the [Sync FAQ](https://obsidian.md/help/sync/faq) for some answers to common questions.

<iframe allow="clipboard-write; web-share" src="chrome-extension://cnjifjpddelmedmihgijeibhnjfabmlf/side-panel.html?context=iframe"></iframe>