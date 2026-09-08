---
source: "https://developer.1password.com/docs/environments/read-environment-variables/"
author:
published:
created: 2026-04-20
---
## Programatically read 1Password Environments Beta

You can programatically retrieve environment variables from [1Password Environments](https://developer.1password.com/docs/environments) using [1Password SDKs](#sdks) or [1Password CLI](#cli). Both tools support local authentication with the 1Password desktop app or automated authentication with service accounts scoped to specific Environments.

## Choose your configuration

### Tool options

- **1Password CLI**: Best for quick testing, shell scripts, CI/CD pipelines, Infrastructure as Code, build tools and task runners.
- **1Password SDKs**: Best for native integrations with Go, Python, or JavaScript applications.

### Authentication options

- **Local authentication with the 1Password desktop app**: Authenticate in the same way you unlock your [1Password desktop app](https://1password.com/downloads/), like with biometrics or your 1Password account password. Requires minimal setup with no token management. Enables human-in-the-loop approval for sensitive workflows.
- **1Password Service Accounts**: Authenticate using a [service account token](https://developer.1password.com/docs/service-accounts/) scoped to the Environments you want to fetch. Best for shared building, automated access, and headless server authentication. Enables you to follow the [principle of least privilege](https://csrc.nist.gov/glossary/term/least_privilege) in your project.

### Decision guide

Use the table below to find the best tool and authentication method for your specific use case.

| Use case | Recommended tool | Authentication method | Why this approach |
| --- | --- | --- | --- |
| **Local development** on your machine | [CLI](#cli) or [SDK](#sdks) | Desktop app | Uses existing 1Password account credentials, making it seamless for individual developers working locally. No token management. |
| **Quick testing** and exploration | [CLI](#cli) | Desktop app | Fastest way to test. Uses existing 1Password account credentials with minimal setup required. |
| **Desktop applications** | [SDK](#sdks) | Desktop app | Better integration with application code. Desktop app authentication allows end users to authenticate with their own 1Password accounts. |
| **Shell scripts** and automation tasks | [CLI](#cli) | Desktop app or service account | 1Password CLI is designed for shell scripting. Use 1Password desktop app for personal scripts, service accounts for shared/automated scripts. |
| **CI/CD pipelines** (GitHub Actions, GitLab CI, etc.) | [CLI](#cli) | Service account | Service accounts provide non-interactive authentication perfect for automated workflows. 1Password CLI is lightweight and easy to integrate into pipeline scripts. |
| **Application runtime** (production services) | [SDK](#sdks) | Service account | 1Password SDKs offer native language integration with better error handling and type safety. Service accounts enable secure, automated access without user interaction. |
| **Server-side applications** | [SDK](#sdks) | Service account | 1Password SDKs offer robust error handling and connection pooling. Service accounts enable headless server authentication. |
| **Docker containers and Kubernetes** | [SDK](#sdks) or [CLI](#cli) | Service account | Service accounts work well in containerized environments. Choose 1Password SDKs for application containers, 1Password CLI for init containers or sidecars. |
| **Infrastructure as Code** (Terraform, Pulumi, etc.) | [CLI](#cli) | Service account | 1Password CLI can be easily invoked from IaC tools. Service accounts enable automated infrastructure provisioning. |
| **Build tools and task runners** | [CLI](#cli) | Desktop app or service account | 1Password CLI integrates easily with build tools like Make, Gradle, or npm scripts. Use 1Password desktop app for developer builds. Service accounts support shared building. |

## Get an Environment's ID

To fetch environment variables from a 1Password Environment, you'll need its unique identifier (ID). You can get an Environment's ID in the [1Password desktop app](https://1password.com/downloads/):

1. Open and unlock the 1Password desktop app, then navigate to **Developer** > **View Environments**.
2. Select **View environment** next to the Environment you want to fetch.
3. Select **Manage environment** > **Copy environment ID**.

## Read Environments with 1Password SDKs

### Before you get started

To use this feature, you'll need to install the beta version of the Go, JS, or Python SDK:

Then [follow the steps](https://developer.1password.com/docs/sdks#get-started) to set up your project to authenticate with your 1Password desktop app or a service account token.

### Get environment variables

With [1Password SDKs](https://developer.1password.com/docs/sdks), you can retrieve environment variables from your 1Password Environments using the `get_variables()` function with the [Environment's ID](#get-an-environments-id).

The function returns a `GetVariablesResponse` object that contains a list of the environment variables stored in the Environment.

Each environment variable in the response contains the environment variable's name (for example, `DB_HOST`), value, and whether the value is hidden by default.

> [!-secondary] -secondary
> note
> 
> By default, 1Password Environment variables have **"Hide value by default"** turned on. To change this, open an Environment, select the verticle ellipsis next to the variable, then select **Show value by default**.

#### Examples

## Read Environments with 1Password CLI

With [1Password CLI](https://developer.1password.com/docs/cli), you can retrieve environment variables from your 1Password Environments with `op environment read` and pass them to an application or script using `op run --environment`.

### Before you get started

Before you get started, install the [latest beta build of 1Password CLI](https://app-updates.agilebits.com/product_history/CLI2#beta), version `2.33.0-beta.02` or later. Then choose your authentication method:

- **Local authentication with the 1Password desktop app**: Authenticate in the same way you unlock your [1Password desktop app](https://1password.com/downloads/), like with biometrics or your 1Password account password. To set up local authentication, [turn on the 1Password CLI desktop app integration](https://developer.1password.com/docs/cli/get-started#step-2-turn-on-the-1password-desktop-app-integration).
- **Service account**: Authenticate using a service account token that can only access the Environments you want to fetch. To authenticate using a service account token, [create a new service account](https://start.1password.com/developer-tools/infrastructure-secrets/serviceaccount/) with read access to the appropriate Environments. Then export your service account token:

### Get environment variables

To read environment variables from a 1Password Environment, use `op environment read` with the [Environment's ID](#get-an-environments-id). 1Password CLI will return a list of environment variables for the Environment formatted as key-value pairs.

op environment read <environmentID>

#### Examples

To get the environment variables for a local development Environment with the ID `blgexucrwfr2dtsxe2q4uu7dp4`:

op environment read blgexucrwfr2dtsxe2q4uu7dp4

See result...

DB\_HOST=localhost

DB\_USER=admin

API\_KEY=sk-abc123

After you fetch the Environment, you can pipe the results to other tools. For example:

op environment read blgexucrwfr2dtsxe2q4uu7dp4 | grep DB\_

### Pass environment variables to an application or script

To pass environment variables from a 1Password Environment to an application or script, use [`op run`](https://developer.1password.com/docs/cli/reference/commands/run) with the `--environment` flag and the [Environment's ID](#get-an-environments-id), then pass the results to the application or script. 1Password CLI runs the application or script as a subprocess with your secrets loaded into the environment for the duration of the process.

op run --environment <environmentID> -- <command>

> [!-secondary] -secondary
> note
> 
> By default, 1Password Environment variables have **"Hide value by default"** turned on. Hidden variables are automatically concealed in stdout and stderr output. To change this, open an Environment, select the verticle ellipsis next to the variable, then select **Show value by default**. Or use the `--no-masking` flag with `op run`.

#### Use with environment variables from multiple sources

You can also use `op run` with multiple environments, or in combination with `.env` files or shell environment variables. When the same environment variable exists in multiple sources, 1Password CLI gives them the following precedence:

1. 1Password Environments (highest priority)
2. Environment files
3. Shell environment variables (lowest priorities)

If the same variable exists in multiple 1Password Environments, the last Environment specified takes precedence.

#### Examples

To run the `printenv` command with the environment variables from a 1Password Environment loaded into the environment:

op run --environment blgexucrwfr2dtsxe2q4uu7dp4 -- printenv

See result...

DB\_HOST=localhost

DB\_USER=admin

API\_KEY=sk-abc123

To run a script provisioned with the environment variables from an Environment:

op run --environment blgexucrwfr2dtsxe2q4uu7dp4 --./my-script.sh

## Learn more

- [Access secrets from 1Password through local.env files](https://developer.1password.com/docs/environments/local-env-file)
- [Use 1Password's agent hook to validate local.env files from 1Password Environments](https://developer.1password.com/docs/environments/agent-hook-validate)
- [Sync secrets from 1Password to AWS Secrets Manager](https://developer.1password.com/docs/environments/aws-secrets-manager)