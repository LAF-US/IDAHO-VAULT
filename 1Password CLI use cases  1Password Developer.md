---
source: https://developer.1password.com/docs/cli/use-cases/#secrets
author: null
published: null
created: 2026-03-30
related:
- 1Password
- '2026-03-30'
- CLI
- GitHub
- Grant
- format
- sign
- syntax
- web
- window
authority: LOGAN
---
## Use cases

1Password CLI allows you to securely provision secrets in development environments, use scripts to manage items and provision team members at scale, and authenticate with biometrics in the terminal.

## Eliminate plaintext secrets in code

![An item open in the 1Password app with the option to copy a secret reference selected.](https://developer.1password.com/img/cli/use-case-secret-reference-top.png)

An item open in the 1Password app with the option to copy a secret reference selected.

With 1Password CLI, you can store secrets securely in your 1Password vaults then use [secret references](https://developer.1password.com/docs/cli/secret-references/) to load them into [environment variables](https://developer.1password.com/docs/cli/secrets-environment-variables/), [configuration files](https://developer.1password.com/docs/cli/secrets-config-files/), and [scripts](https://developer.1password.com/docs/cli/secrets-scripts/) without putting any plaintext secrets in code.

Secret references are dynamic – if you update your credentials in 1Password, the changes will be reflected in your scripts without needing to update the script directly. You can also [use variables within secret references](https://developer.1password.com/docs/cli/secret-reference-syntax#externally-set-variables) to pass different sets of secrets for different environments using the same file.

For example, you can use a secret reference in place of your plaintext GitHub Personal Access Token in a `github.env` file:

![An environment file using a plaintext secret and the same file using a secret reference.](https://developer.1password.com/img/cli/use-case-secret-reference.png)

An environment file using a plaintext secret and the same file using a secret reference.

Then use [`op run`](https://developer.1password.com/docs/cli/reference/commands/run/) to pass the file with the token provisioned from 1Password to your application or script when you need it. The script will run with the token provisioned, without the token ever appearing in plaintext.

 <video controls=""><source type="video/mp4" src="https://developer.1password.com/videos/secret-references-in-scripts.mp4"> <source type="video/webm" src="https://developer.1password.com/videos/secret-references-in-scripts.webm"></video>

### Learn more

## Automate administrative tasks

![1password.com open to show the people who have access to a vault alongside a terminal window displaying the same information.](https://developer.1password.com/img/cli/use-case-it-top.png)

1password.com open to show the people who have access to a vault alongside a terminal window displaying the same information.

With 1Password CLI, IT administrators can set up scripts to automate common tasks, like [provisioning users](https://developer.1password.com/docs/cli/provision-users/), [managing permissions](https://developer.1password.com/docs/cli/grant-revoke-vault-permissions/), [managing items](https://developer.1password.com/docs/cli/reference/management-commands/item/), and generating custom reports.

For example, this script will loop through each vault the person who runs the script has access to and provide:

- the vault name
- the number of items in the vault
- the last time the vault's contents were updated
- the users and groups that have access to the vault along with their permissions

vault\_details.sh

#!/usr/bin/env bash

for vault in $(op vault list --format=json | jq --raw-output '.\[\].id')

do

echo ""

echo "Vault Details"

op vault get $vault --format=json | jq -r '.|{name, items, updated\_at}'

sleep 1

echo ""

echo "Users"

op vault user list $vault

sleep 1

echo ""

echo "Groups"

op vault group list $vault

sleep 1

echo ""

echo "End of Vault Details"

sleep 2

clear

echo ""

echo ""

done

### Learn more

See our [repository of example 1Password CLI scripts](https://github.com/1Password/solutions) for inspiration for your own projects. You'll find scripts that can help you:

To learn more about how to accomplish these tasks with 1Password CLI, see the following guides:

- [Create items](https://developer.1password.com/docs/cli/item-create/)
- [Add and remove team members](https://developer.1password.com/docs/cli/provision-users/)
- [Grant and revoke vault permissions](https://developer.1password.com/docs/cli/grant-revoke-vault-permissions/)

## Sign in to any CLI with your fingerprint

 <video><source type="video/mp4" src="https://developer.1password.com/videos/aws.mp4"> <source type="video/webm" src="https://developer.1password.com/videos/aws.webm"></video>

With our [shell plugin ecosystem](https://developer.1password.com/docs/cli/shell-plugins/), you can use 1Password to securely authenticate all your command-line tools. Store your CLI access credentials in your 1Password vaults then sign in to your CLIs with your fingerprint instead of entering your credentials manually or storing them in an unencrypted format on your computer.

Shell plugins unlock the ability to securely share credentials between team members. Store a token in a shared 1Password vault, and all people with access to the vault will be able to sign in with them. And you can use shell plugins across [multiple environments](https://developer.1password.com/docs/cli/shell-plugins/environments/), so you don't have to spend time signing in and out between projects.

For example, the [ngrok shell plugin](https://developer.1password.com/docs/cli/shell-plugins/ngrok/) can securely tunnel the local app to the internet for a web development project running on your computer. The ngrok authtoken is not stored anywhere on the computer. When the ngrok CLI is run, the shell plugin provisions the authtoken as an environment variable for the ngrok binary to consume, and when the process exits, the environment variable is cleared.

 <video controls=""><source type="video/mp4" src="https://developer.1password.com/videos/shell-plugin-demo.mp4"> <source type="video/webm" src="https://developer.1password.com/videos/shell-plugin-demo.webm"></video>

### Learn more

Get started with one of our most popular shell plugins:

Or choose a plugin from [our library of more than 40 command-line tools](https://developer.1password.com/docs/cli/shell-plugins/) to get started with. If the tool you want to use isn't supported yet, you can [build your own plugin](https://developer.1password.com/docs/cli/shell-plugins/contribute/).

You can also:

- [Test shell plugins](https://developer.1password.com/docs/cli/shell-plugins/test/)
- [Use shell plugins to switch between environments](https://developer.1password.com/docs/cli/shell-plugins/environments/)
- [Use shell plugins with multiple accounts](https://developer.1password.com/docs/cli/shell-plugins/multiple-accounts/)