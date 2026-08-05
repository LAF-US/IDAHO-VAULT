<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# https://developer.1password.com/docs/environments/read-environment-variables/

The page describes **1Password Environments (beta)** as a way to organize project environment variables separately from vault items, then use them in local `.env` files, agents/IDEs, terminal workflows, SDKs, or AWS Secrets Manager [^1_1]. It also explains that you can create an environment in the 1Password desktop app, add variables by importing an existing `.env` file or creating them manually, and share or manage access for team members [^1_1].

## What the page covers

- Local `.env` file support without writing plaintext secrets to disk [^1_1].
- Agent hook validation for supported IDEs and agents [^1_1].
- Programmatic access through 1Password CLI or SDKs [^1_1].
- AWS Secrets Manager sync [^1_1].
- Team sharing and access control [^1_1].


## Setup basics

You need 1Password installed on Mac, Windows, or Linux, and 1Password Developer turned on in the desktop app [^1_1]. To create an environment, open **Developer > View Environments**, then choose **New environment** and name it [^1_1].

## Variable handling

Variables are stored as name/value pairs like standard environment variables, and 1Password returns values exactly as entered [^1_1]. The page notes that values containing spaces should be quoted and special characters escaped, just like in a normal `.env` file [^1_1].

## Practical note

The docs caution that if you share an Environment and read it outside 1Password, you should review the values carefully because 1Password will return exactly what was stored [^1_1].

Would you like the exact CLI/SDK steps for reading the environment variables programmatically?
<span style="display:none">[^1_2][^1_3][^1_4][^1_5][^1_6][^1_7][^1_8][^1_9]</span>

<div align="center">⁂</div>

[^1_1]: https://developer.1password.com/docs/environments/

[^1_2]: https://www.1password.community/discussions/developers/export-specific-secret-value-as-an-environment-variable/86806/replies/86807

[^1_3]: https://www.youtube.com/watch?v=W0SNYmdVD0o

[^1_4]: https://developer.1password.com/docs/environments/local-env-file/

[^1_5]: https://1password.com/blog/1password-environments-env-files-public-beta

[^1_6]: https://developer.1password.com/docs/cli/environment-variables/

[^1_7]: https://developer.1password.com/docs/sdks/environments/

[^1_8]: https://developer.1password.com/docs/cli/secrets-environment-variables/

[^1_9]: https://www.1password.community/discussions/developers/introducing-new-env-file-support-in-1password/162994


---

# https://developer.1password.com/docs/cli/

The URL `https://developer.1password.com/docs/cli/` points to the **main documentation hub for the 1Password CLI** (`op`), which is 1Password’s command‑line tool for managing secrets, vaults, users, and integrations programmatically [^2_1][^2_2]. In practice that page serves as a landing index that links down to “Get started,” “App integration,” “Command reference,” “Environments,” and other sub‑sections.

## What the CLI docs cover

- **Installation and sign‑in**: How to install `op` on Mac, Windows, and Linux, and how to sign in using your 1Password account (including SSO and app‑based integration) [^2_1][^2_3][^2_4].
- **Command structure**: The CLI uses a noun‑verb pattern; top‑level commands like `account`, `vault`, `item`, `environment`, `plugin`, and `inject` group related operations [^2_2].
- **Secrets and automation**: You can read item fields, generate or update passwords, list or create items, inject secrets into config files, and load `.env`‑style secrets from 1Password Environments [^2_2][^2_5].


## Key workflows you’ll see there

- Enabling “Integrate with 1Password CLI” in the 1Password desktop app so you can sign in with Touch ID / Windows Hello / system auth [^2_3][^2_6].
- Using `op item get`, `op item edit`, `op environment` and shell plugins to pull secrets into scripts or local tools without hard‑coding them [^2_2][^2_5].
- Managing teams and access (`group`, `user`, `events-api`) via the CLI for automation pipelines and CI/CD [^2_2][^2_7].

If you tell me what you want to do (e.g., load env vars into a script, sync to AWS Secrets Manager, or automate vault/user setup), I can walk you through the exact `op` commands and patterns.
<span style="display:none">[^2_10][^2_11][^2_12][^2_13][^2_14][^2_8][^2_9]</span>

<div align="center">⁂</div>

[^2_1]: https://developer.1password.com/docs/cli/get-started/

[^2_2]: https://developer.1password.com/docs/cli/reference/

[^2_3]: https://developer.1password.com/docs/cli/app-integration/

[^2_4]: https://developer.1password.com/docs/cli/sign-in-sso/

[^2_5]: https://developer.1password.com/docs/cli/secrets-environment-variables/

[^2_6]: https://developer.1password.com/docs/cli/reference/commands/signin/

[^2_7]: https://1password.com/developers/cli

[^2_8]: https://developer.1password.com

[^2_9]: https://developer.1password.com/llms-cli.txt

[^2_10]: https://www.youtube.com/watch?v=rle97m_vKuE

[^2_11]: https://support.1password.com/developer/

[^2_12]: https://1password.com/downloads/command-line

[^2_13]: https://releases.1password.com/developers/cli/

[^2_14]: https://github.com/robertknight/1pass

