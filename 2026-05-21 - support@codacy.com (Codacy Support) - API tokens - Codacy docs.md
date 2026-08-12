---
source: "https://docs.codacy.com/codacy-api/api-tokens/#repository-api-tokens"
author:
  - "[[support@codacy.com (Codacy Support)]]"
published: 2026-05-21
created: 2026-08-10
---
## API tokens

Codacy provides **account** and **repository** -level API tokens that allow you to:

- [Upload coverage data](https://docs.codacy.com/coverage-reporter/) to Codacy
- Upload to Codacy the results of [running client-side analysis tools](https://docs.codacy.com/repositories-configure/local-analysis/client-side-tools/)
- [Authenticate when using the Codacy API](https://docs.codacy.com/codacy-api/using-the-codacy-api/#authenticating-requests)
- [Authenticate with the Codacy Cloud CLI](https://docs.codacy.com/codacy-cloud-cli/#authentication)

The sections below provide details about the two types of API tokens and instructions on how to generate and revoke them.

> [!warning] Warning
> **Never write API tokens to your configuration files** and keep your API tokens well protected, as they grant owner permissions to your projects on Codacy.
> 
> It's a best practice to store API tokens as environment variables. Check the documentation of your CI/CD platform on how to do this.

## Generating and revoking account API tokens

Account API tokens are defined at the **Codacy user account level**. Each account API token authorizes access to the same organizations, repositories, and operations as the [roles and permissions of the owner of the account](https://docs.codacy.com/organizations/roles-and-permissions-for-organizations/).

> [!important] Important
> **If you're using an account API token to upload coverage** be sure to [check the roles](https://docs.codacy.com/organizations/roles-and-permissions-for-organizations/) that your Git provider account must have to authorize uploading coverage to Codacy.
> 
> Use a dedicated service account to integrate Codacy with your repositories. This prevents disruption of service if the user who created an account API token loses access to the repositories, which may happen when a user leaves the team or the organization.

You can create new account API tokens programmatically [using the Codacy API](https://docs.codacy.com/codacy-api/examples/creating-repository-api-tokens-programmatically/) or using the Codacy UI:

1. Open your account, tab **Access management**.
2. Click the button **Create API token** under **Account API tokens**.
3. Select an expiration date from the modal options. You can select between a range of 7 days to 90 days, create a custom expiration date, or create a token with no expiration.

![Creating an account API token](https://docs.codacy.com/codacy-api/images/codacy-api-tokens-account.png)

![Creating an account API token modal](https://docs.codacy.com/codacy-api/images/codacy-api-tokens-account-modal.png)

> [!tip] Tip
> You can create multiple account API tokens. This can be useful to have a more flexible control by revoking only a specific token.

When you have tokens created, you can view them inside the tokens table. By hovering a token, you are able to copy its value.

![Creating an account API token modal](https://docs.codacy.com/codacy-api/images/codacy-api-tokens-account-table.png)

To delete an account API token, click the trash icon in the Actions column of the table. After this, all applications or services using that token to access the Codacy API will fail to authenticate and will receive the reply `{"error":"not found"}`.

## Generating and revoking repository API tokens

Repository API tokens are defined on **individual repositories**. Each repository API token only authorizes access to the corresponding repository.

You can create new repository API tokens programmatically [using the Codacy API](https://docs.codacy.com/codacy-api/examples/creating-repository-api-tokens-programmatically/) or using the Codacy UI:

1. Open your repository **Settings**, tab **Integrations**.
2. Click the button **Create API token** under **Repository API tokens**.
	> [!tip] Tip
	> You can create multiple (up to 100) API tokens per repository. This can be useful to have a more flexible control by revoking only a specific token.
	![Creating a repository API token](https://docs.codacy.com/codacy-api/images/codacy-api-tokens-repository.png)

To revoke a repository API token, click the **X** next to the token. After this, all applications or services using that token to access the Codacy API will fail to authenticate and will receive the reply `{"error":"not found"}`.