---
source: "https://docs.codacy.com/codacy-api/examples/creating-repository-api-tokens-programmatically/"
author:
  - "[[support@codacy.com (Codacy Support)]]"
published: 2024-05-08
created: 2026-08-10
---
To create new [repository API tokens](https://docs.codacy.com/codacy-api/api-tokens/) for your Codacy repositories programmatically, use the Codacy API endpoint [createRepositoryApiToken](https://app.codacy.com/api/api-docs#createrepositoryapitoken). You can also list all repository API tokens for a repository using the endpoint [listRepositoryApiTokens](https://api.codacy.com/api/api-docs#listrepositoryapitokens).

For example, if you're [setting up coverage](https://docs.codacy.com/coverage-reporter/) for all your repositories and prefer not to use a single account API token that grants the same permissions as an administrator, you need to create an individual repository API token for each repository.

## Example: Creating a repository API token for a single repository

This example creates a new repository API token for a repository and outputs the new token string.

The example script:

1. Defines the [account API token](https://docs.codacy.com/codacy-api/api-tokens/#account-api-tokens) used to authenticate on the Codacy API, the Git provider, the organization name, and the repository name passed as an argument to the script.
2. Calls the endpoint [createRepositoryApiToken](https://app.codacy.com/api/api-docs#createrepositoryapitoken) to create a new repository API token and uses [jq](https://github.com/stedolan/jq) to obtain only the created token string.
```js
#!/bin/bash

CODACY_API_TOKEN="<your account API token>"
GIT_PROVIDER="<your Git provider>" # gh, ghe, gl, gle, bb, or bbe
ORGANIZATION="<your organization name>"
REPOSITORY=$1

curl -sX POST "https://app.codacy.com/api/v3/organizations/$GIT_PROVIDER/$ORGANIZATION/repositories/$REPOSITORY/tokens" \
     -H "api-token: $CODACY_API_TOKEN" \
| jq -r ".data | .token"
```

Example usage and output

```js
$ ./create-token.sh website
<new repository API token>
```

## Example: Creating repository API tokens for all repositories in an organization

This example creates new repository API tokens for all the repositories in an organization and outputs a comma-separated list of repository names and corresponding token strings.

The example script:

1. Defines the [account API token](https://docs.codacy.com/codacy-api/api-tokens/#account-api-tokens) used to authenticate on the Codacy API, the Git provider, and the organization name.
2. Calls the endpoint [listOrganizationRepositories](https://api.codacy.com/api/api-docs#listorganizationrepositories) to retrieve the list of repositories in the organization.
3. Uses [jq](https://github.com/stedolan/jq) to select only the name of the repositories.
4. Asks for confirmation from the user before making any changes.
5. For each repository, calls the endpoint [createRepositoryApiToken](https://app.codacy.com/api/api-docs#createrepositoryapitoken) to create a new repository API token and uses jq to obtain only the created token string.
6. Outputs a comma-separated list of the repository names and the corresponding new token strings.
7. Pauses a few seconds between requests to the Codacy API to avoid rate limiting.
```js
#!/bin/bash

CODACY_API_TOKEN="<your account API token>"
GIT_PROVIDER="<your Git provider>" # gh, ghe, gl, gle, bb, or bbe
ORGANIZATION="<your organization name>"

repositories=$(curl -sX GET "https://app.codacy.com/api/v3/organizations/$GIT_PROVIDER/$ORGANIZATION/repositories" \
                    -H "api-token: $CODACY_API_TOKEN" \
               | jq -r ".data[] | .name")

count=$(echo "$repositories" | wc -l)
read -p "Create repository tokens for $count repositories? (y/n) " choice
if [ "$choice" = "y" ]; then
    echo "$repositories" | while read repository; do
        echo -n "$repository,"
        curl -sX POST "https://app.codacy.com/api/v3/organizations/$GIT_PROVIDER/$ORGANIZATION/repositories/$repository/tokens" \
             -H "api-token: $CODACY_API_TOKEN" \
        | jq -r ".data | .token"
        sleep 2 # Wait 2 seconds
    done
else
    echo "No changes made.";
fi
```

Example output:

```js
chart,<new repository API token>
docs,<new repository API token>
website,<new repository API token>
[...]
```

> [!important] Important
> For the sake of simplicity, the example doesn't consider paginated results obtained from the Codacy API. [Learn how to use pagination](https://docs.codacy.com/codacy-api/using-the-codacy-api/#using-pagination) to ensure that you process all results returned by the API.

## Example: Listing the repository API tokens for a repository

This example lists all repository API tokens created for a repository.

The example script:

1. Defines the [account API token](https://docs.codacy.com/codacy-api/api-tokens/#account-api-tokens) used to authenticate on the Codacy API, the Git provider, the organization name, and the repository name passed as an argument to the script.
2. Calls the endpoint [listRepositoryApiTokens](https://api.codacy.com/api/api-docs#listrepositoryapitokens) to list the repository API tokens available on the repository and uses [jq](https://github.com/stedolan/jq) to obtain only the token strings, or exit with a non-zero status if the repository doesn't have any repository API tokens created yet.
```js
#!/bin/bash
CODACY_API_TOKEN="<your account API token>"
GIT_PROVIDER="<your Git provider>" # gh, ghe, gl, gle, bb, or bbe
ORGANIZATION="<your organization name>"
REPOSITORY=$1

curl -sX GET "https://app.codacy.com/api/v3/organizations/$GIT_PROVIDER/$ORGANIZATION/repositories/$REPOSITORY/tokens" \
     -H "api-token: $CODACY_API_TOKEN" \
| jq -er ".data[] | .token"
```

Example usage to obtain only the repository API token created most recently for the repository:

```js
$ ./list-tokens.sh website | head -n 1
<last repository API token created>
```

## See also

- [API tokens](https://docs.codacy.com/codacy-api/api-tokens/)