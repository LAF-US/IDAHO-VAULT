---
source: "https://developer.1password.com/docs/ssh/agent/config/"
author:
published:
created: 2026-04-20
---
The 1Password SSH agent config file is a [TOML file](https://toml.io/en/) you can create that gives you more fine-grained control over the behavior of the SSH agent.

With the agent config file, you can:

- [Choose which keys are available to the SSH agent](#add-individual-keys) from any of your vaults and accounts, not just your Personal, Private, or Employee vault.
- Specify the order the agent uses to offer your keys to SSH servers, to prevent running into the [six-key authentication limit](https://developer.1password.com/docs/ssh/agent/advanced#ssh-server-six-key-limit) on most servers.
- Create different agent configurations for each machine, to customize how you use the SSH agent on each device.

The SSH agent config file (`~/.config/1Password/ssh/agent.toml`) is unique to 1Password. It's separate from the SSH *client* config file ([`~/.ssh/config`](https://linux.die.net/man/5/ssh_config)) and the SSH *server* config file ([`/etc/ssh/sshd_config`](https://linux.die.net/man/5/sshd_config)) and can be used alongside them.

## Requirements

1. [Sign up for 1Password.](https://1password.com/pricing/password-manager)
2. Install and sign in to 1Password for [Mac](https://1password.com/downloads/mac), [Windows](https://1password.com/downloads/windows), or [Linux](https://1password.com/downloads/linux).
3. [Import or generate SSH keys in 1Password.](https://developer.1password.com/docs/ssh/manage-keys/)
4. [Set up the 1Password SSH Agent.](https://developer.1password.com/docs/ssh/get-started#step-3-turn-on-the-1password-ssh-agent)

## About the SSH agent config file

The SSH agent config file is an optional configuration file that allows you to override the [default behavior](#agent-configuration-options) of the 1Password SSH agent on your Mac, Windows, or Linux machine. It doesn't alter your SSH agent settings or other SSH config files on your computer — only which keys the agent can access and in which order to make them available to servers.

The agent config file is saved locally on your machine and isn't synced to the 1Password servers. If you use 1Password with multiple workstations, you can sync or share the agent config file using your own method (for example, using Git) the same way you do with other dotfiles. Or you can create separate agent config files for each machine.

You can [remove the agent config file](#remove-the-ssh-agent-config-file) at any time to return to the default agent configuration.

### Agent configuration options

If there's no agent config file on your machine, 1Password will use the default SSH agent configuration, which allows the agent to make any SSH key item in your default [Personal](https://support.1password.com/1password-glossary#personal-vault), [Private](https://support.1password.com/1password-glossary#private-vault), or [Employee](https://support.1password.com/1password-glossary#employee-vault) vault available to offer to SSH servers.

If you want to customize how the SSH agent is configured, you can [create the SSH agent config file](#create-the-ssh-agent-config-file) to override the default agent behavior, then [modify the file](#modify-the-ssh-agent-config-file) to specify which keys the SSH agent has access to and the order you want them offered to the server.

### File syntax and structure

#### TOML syntax

The SSH agent config file uses the [TOML file syntax](https://toml.io/en/v1.0.0) to identify which SSH keys the SSH agent can access and when it can access them.

Each entry in the file requires an `[[ssh-keys]]` header and one or more key-value pairs to indicate the item, vault, and/or account name or ID for the SSH key item. For example:

\# Add my Git authentication key from my Work vault

\[\[ssh-keys\]\]

item = "Git Authentication Key"

vault = "Work"

\# Add my Git signing key from my Work vault

\[\[ssh-keys\]\]

item = "Git Signing Key"

vault = "Work"

\# Then add all keys from my Private vault

\[\[ssh-keys\]\]

vault = "Private"

account = "Wendy Appleseed's Family"

> [!-info] -info
> TOML syntax rules

#### File structure

The SSH agent config file is made up of sections. A section is defined by the `[[ssh-keys]]` header followed by one or more key-value pairs for the intended SSH key or set of keys to be made available to the SSH agent.

The order of the `[[ssh-keys]]` sections in the agent config file determine the order the agent offers your keys to SSH servers. This helps to minimize the number of authentication attempts the SSH agent makes so you don't run into the [six-key limit](https://developer.1password.com/docs/ssh/agent/advanced#ssh-server-six-key-limit) (`MaxAuthTries`) that is the default for most SSH servers.

Here's an example of an SSH agent configuration file with entries for two specific SSH keys:

\# My GitHub SSH key for my Work account

\[\[ssh-keys\]\]

item = "GitHub SSH key - Work"

vault = "Private"

account = "AgileBits"

\# Shared GitHub SSH key for the Demo account

\[\[ssh-keys\]\]

item = "GitHub SSH Key - Demo"

vault = "Demo"

account = "AgileBits"

With this configuration, if you try to SSH into a GitHub repository in your `Work` account, the SSH agent will offer your work SSH key to the server first because it's the first key entry in the file. If the key is a match, 1Password will ask you to [authorize the request](https://developer.1password.com/docs/ssh/get-started#step-6-authorize-the-ssh-request).

If you try to SSH into a GitHub repository in your `Demo` account instead, the agent will still offer your work key to the server first, then your demo SSH key. With only two SSH keys in the file, it's unlikely that you'd be at risk of running into any server limits. However, if you have six or more SSH keys listed in your agent config file before the demo key, or if your agent config file includes multiple SSH keys for the same host, you can also modify the SSH client config file (`~/.ssh/config`) to [match your SSH keys to individual hosts](https://developer.1password.com/docs/ssh/agent/advanced#match-key-with-host) or specify [which SSH key each of your GitHub repositories uses](https://developer.1password.com/docs/ssh/agent/advanced#use-multiple-git-identities-on-the-same-machine).

## Create the SSH agent config file

### From the 1Password app

You can use the 1Password desktop app to create the SSH agent config file for you. The file will include entries to allow the SSH agent to access all the keys in any of your Personal, Private, or Employee vaults, similar to the [default configuration](#agent-configuration-options) used by the agent when no agent config file exists.

For example, if you're signed in to a 1Password account with a default Private vault, you'll see an entry like this added to the agent config file:

\[\[ssh-keys\]\]

vault = "Private"

You can then choose to [modify the file](#modify-the-ssh-agent-config-file) to adjust which keys the agent offers to SSH servers in which order.

To create the agent config file from 1Password:

### From the terminal

You can also choose to create the SSH agent config file yourself from the terminal. The file won't include any entries for your SSH keys — including any keys in your default Personal, Private, or Employee vault(s) — until you add them.

When you create the file at the specified path, 1Password will detect it and override the default agent behavior, even if the agent config file is empty. Make sure to [modify the agent config file](#modify-the-ssh-agent-config-file) after you create it, to add any SSH keys items you need from any of your vaults or accounts.

You can create the SSH agent config file on your machine at the specified path:

## Modify the SSH agent config file

You can make your SSH keys available to the SSH agent by adding `[[ssh-keys]]` sections to the agent config file for any combination of individual keys, vaults, and accounts you have access to in 1Password, including shared and custom vaults.

Your `[[ssh-keys]]` entries can be as specific or as broad in scope as you'd like, where you'll use at least one or more of the following key-value pairs to act like a series of queries on your SSH key items:

- item: "The item name or ID"
- vault: "The vault name or ID"
- account: "The account name sign-in address or ID"

These key-value pairs work like `WHERE` / `AND` clauses and operators, where the more data you include, the more specific your query becomes.

If the SSH agent finds more than one key match per entry, the keys will be added in ascending order according to when the item was created (from the oldest to the most recent). To control the exact order, you can add additional `[[ssh-keys]]` sections to the agent config file.

Before you modify the agent config file, make sure you're familiar with the [file syntax and structure](#file-syntax-and-structure), to ensure the SSH agent behaves as you expect it to.

You don't need to restart the SSH agent each time you edit the agent config file. Your saved changes will be immediately available to the agent.

### Add individual keys

You can add an `[[ssh-keys]]` section for an individual SSH key by including an `item` key-value pair in the entry. Include additional key-value pairs if you want to further specify which vault or account the SSH key is in. For example:

\# Add my Git authentication key from my Work vault

\[\[ssh-keys\]\]

item = "Git Authentication Key"

\# Then add my Git signing key from my Work vault

\[\[ssh-keys\]\]

item = "Git Signing Key"

vault = "Work"

account = "ACME, Inc."

### Add all keys in a vault

You can add an `[[ssh-keys]]` section for all the SSH keys in a vault by including the `vault` key-value pair in the entry. You can include an `account` key-value if you want to specify which 1Password account the key is in, but don't include an `item` key-value pair or only that item will be added. For example:

\# Add all keys from my Work vault

\[\[ssh-keys\]\]

vault = "Work"

\# Then add all keys from the Private vault in my family account

\[\[ssh-keys\]\]

vault = "Private"

account = "Wendy Appleseed's Family"

If you add or remove SSH keys from the vault, access to the keys will be added to, or removed from, the SSH agent without needing to modify the agent config file later.

### Add all keys in an account

You can add an `[[ssh-keys]]` section for all the SSH keys in a 1Password account by including the `account` key-value pair in the entry. Don't include the `item` or `vault` key-value pairs or you'll only add SSH keys for that item or vault. For example:

\# Add all keys from my family account

\[\[ssh-keys\]\]

account = "Wendy Appleseed's Family"

\# Then add all keys from my work account

\[\[ssh-keys\]\]

account = "ACME, Inc."

Instead of the account name, you can also use the [sign-in address](https://support.1password.com/1password-glossary#sign-in-address) as the `account` value (sign-in addresses can include `https://` at the start, but it's not required). For example:

\# Add all keys from my family account

\[\[ssh-keys\]\]

account = "my.1password.com"

\# Then add all keys from my work account

\[\[ssh-keys\]\]

account = "https://acme.1password.com"

If you add or remove SSH keys from the account, access to the keys will be added to, or removed from, the SSH agent without needing to modify the agent config file later.

### Filter keys

You can use the `[[ssh-keys]]` entries as filters in the agent config file to progressively add keys for the SSH agent to access in your preferred order.

When you have multiple 1Password accounts, like a work account and a family account, you can progressively filter the `[[ssh-keys]]` entries down by 1Password account. If you have any specific items or vaults that you want the SSH agent to offer to servers first, you can include those as well. For example:

\# Add my Git signing key from my Work vault

\[\[ssh-keys\]\]

item = "Git Signing Key"

vault = "Work"

account = "ACME, Inc."

\# Then add all keys from the Private vault in my family account

\[\[ssh-keys\]\]

vault = "Private"

account = "Wendy Appleseed's Family"

\# Then add all keys from the Private vault in my work account

\[\[ssh-keys\]\]

vault = "Private"

account = "ACME, Inc."

\# Then add all remaining keys from any vault in my family account

\[\[ssh-keys\]\]

account = "Wendy Appleseed's Family"

### Use IDs as values

Using the name of an item, vault, or account in the agent config file makes it easier to identify what the entry is for. However, you might choose to use an ID in place of a name if:

- **You don't want your item, vault, or account names stored in plaintext on disk.** [This metadata is encrypted](https://support.1password.com/1password-privacy#data-saved-in-1password:~:text=Your%20metadata%20is%20private) by default in 1Password, but the agent config file on your device is unencrypted.
- **You expect the name of an item, vault, or account to be updated periodically.** IDs are the most stable way to reference an item. An item's ID only changes if you move it to a different vault.

An example entry with an item ID:

\# Add my signing key from my Private vault

\[\[ssh-keys\]\]

item = "hhaeohhhc7iksdbadbx5pxyb6m"

To find and copy an item ID, go to the [**Advanced** settings](onepassword://settings/advanced) in the 1Password app and turn on **Show debugging tools**. Find the item you want and select it, then select > **Copy UUID**. Then paste the UUID value in the config file entry.

You can also [use 1Password CLI to find the IDs for your items, vaults, and accounts](https://developer.1password.com/docs/cli/reference#unique-identifiers-ids).

## Remove the SSH agent config file

If you no longer want to use the SSH agent configuration file, you can delete the file or move it to another location. The 1Password SSH agent will then use the [default configuration](#agent-configuration-options) again.

## Get help

To get help or provide feedback, use the `#ssh-agent-config` channel on the [1Password Developers Slack workspace](https://developer.1password.com/joinslack). This channel is used as the primary means of communication about the agent config file and is where we'll post updates and help answer questions.

### Errors in the agent config file

If there's an error in the agent config file, the SSH agent will stop running and will notify you of the error in the [Developer settings](onepassword://settings/developers) of the 1Password app. Make sure each entry [uses the correct syntax](#file-syntax-and-structure).

If you don't see an error message in 1Password but you're seeing an authentication error in your SSH client or having trouble using the SSH agent, check the values from your key-value pairs. If you make any typos in an item, vault, or account name value, the SSH agent won't be able to make a key match. Entries without key matches are not considered errors and will be ignored.

If you're not able to use a specific key with the SSH agent and it's in the agent config file with the correct syntax and values, you can also check that the SSH key hasn't been archived or deleted. Any archived or deleted SSH Key items will be ignored, even if you specify them by ID.

To see the list of all keys the SSH agent can access, you can run the `ssh-add -l` command, with the `SSH_AUTH_SOCK` environment variable set to the agent socket path:

## Learn more

- [Get started with 1Password for SSH & Git](https://developer.1password.com/docs/ssh/get-started/)
- [Advanced use cases](https://developer.1password.com/docs/ssh/agent/advanced/)
- [Manage SSH keys](https://developer.1password.com/docs/ssh/manage-keys#generate-an-ssh-key)
- [SSH client compatibility](https://developer.1password.com/docs/ssh/agent/compatibility/)
- [About 1Password SSH Agent security](https://developer.1password.com/docs/ssh/agent/security/)