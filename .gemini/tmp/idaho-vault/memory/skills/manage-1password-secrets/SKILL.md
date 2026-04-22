---
name: manage-1password-secrets
description: Implement 1Password secret management in GitHub Actions workflows to eliminate plaintext credentials.
---

## When to Use
Use this skill when you need to update a GitHub Actions workflow to fetch secrets (API keys, tokens, etc.) from 1Password instead of using GitHub Repository Secrets directly. This aligns with the IDAHO-VAULT security policy defined in `VAULT-CONVENTIONS.md`.

## Procedure

1.  **Identify the Secret**: Determine which secret needs to be migrated and its path in 1Password. (Typical path: `op://vault-operations/<secret-name>/credential`).
2.  **Verify Prerequisites**: Ensure the workflow has access to `secrets.OP_SERVICE_ACCOUNT_TOKEN`.
3.  **Update Workflow Steps**: Replace the direct secret usage with a "Load Secrets from 1Password" step.

### Workflow Pattern

```yaml
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Install 1Password CLI
        run: |
          # 1Password CLI is usually pre-installed on GitHub-hosted runners.
          op --version

      - name: Load Secrets from 1Password
        id: op-load-secrets
        run: |
          # Authenticate to 1Password using the service account token
          echo "${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}" | op signin --raw

          # Fetch the secret
          SECRET_VALUE=$(op read "op://vault-operations/<item-name>/<field-name>")
          
          # Mask the secret in logs
          echo "::add-mask::$SECRET_VALUE"
          
          # Set as environment variable for subsequent steps
          echo "<ENV_VAR_NAME>=$SECRET_VALUE" >> $GITHUB_ENV

          # Sign out
          op signout
        env:
          OP_SERVICE_ACCOUNT_TOKEN: ${{ secrets.OP_SERVICE_ACCOUNT_TOKEN }}

      - name: Next Step
        env:
          # Use the environment variable set in the previous step
          MY_SECRET: ${{ env.<ENV_VAR_NAME> }}
        run: |
          # Run your command/script
          python3 my_script.py
```

## Pitfalls and Fixes

- **Impasse on `source !/agent.sh`**: If instructed to run the agent protocol locally via `source !/agent.sh`, acknowledge that `run_shell_command` uses PowerShell and does not support `source` (a bash command), and environment variables do not persist between tool calls.
- **Missing OP_SERVICE_ACCOUNT_TOKEN**: symptom -> `op signin` fails -> fix -> ensure the token is provisioned in GitHub Secrets and passed to the step.
- **Incorrect Secret Reference**: symptom -> `op read` returns error -> fix -> verify the path format `op://<vault>/<item>/<field>`.

## Verification

1.  Check the workflow logs: the 1Password CLI should report its version.
2.  Check for the `::add-mask::` output in logs (it should be hidden).
3.  Verify the script/command correctly receives the environment variable.