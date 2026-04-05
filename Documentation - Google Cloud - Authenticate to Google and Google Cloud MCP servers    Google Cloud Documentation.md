---
source: https://docs.cloud.google.com/mcp/authenticate-mcp#create-oauth-client
author:
- Google
published: null
created: 2026-03-28
date created: Saturday, March 28th 2026, 2:18:45 pm
date modified: Saturday, March 28th 2026, 2:18:55 pm
related:
- '2026-03-28'
- ADC
- API
- CLI
- Cloud
- Google
- Grant
- IAM
- MCP
- agent
- libraries
- sign
authority: LOGAN
---
Google and Google Cloud remote Model Context Protocol (MCP) servers implement the [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) for HTTP-based transports. Generally, your AI applications must authenticate to access these servers. This document describes the supported authentication methods.

Some Google and Google Cloud MCP server endpoints don't require authentication. In such cases, no credentials are necessary.

Services that require a principal for Identity and Access Management (IAM) don't support [Standard API key credentials](https://docs.cloud.google.com/docs/authentication/api-keys#standard-api-keys) for authentication, but services that don't use IAM, like Google Maps, do accept API keys.

The terms *AI application* and *agent* are used interchangeably throughout this document, and refer to any program that can instantiate an [MCP client](https://modelcontextprotocol.io/docs/learn/client-concepts).

## How tool calling and authentication work

When your AI application calls an MCP tool, it must authenticate to the MCP server hosting the tool, using the authentication method you supply. If you use your own credentials, actions taken by the AI application through tool calling are attributed to you. Additionally, the AI application has the same permissions as you do on all resources.

For production environments, choose one of the following authentication methods:

- To create a separate identity for your AI application, choose one of the following methods:
	- [Create a service account](https://docs.cloud.google.com/mcp/authenticate-mcp#create-sa-application)
		- Use an [agent identity](https://docs.cloud.google.com/agent-builder/agent-engine/agent-identity)
- To let your AI application authenticate on your behalf without sharing your credentials, [create an OAuth client ID and credentials](https://docs.cloud.google.com/mcp/authenticate-mcp#create-oauth-client).
- For services that don't require a principal, you can also use [API keys](https://docs.cloud.google.com/mcp/authenticate-mcp#api-keys-services-that-dont-require-principal).

## User identity

For testing purposes, you can authenticate your AI application to Google and Google Cloud MCP servers using your own Google Cloud identity.

### Set up user identity authentication for MCP servers

Your setup method depends on your environment. The most common options are described in the following sections.

For more options and information, see [Authentication methods](https://docs.cloud.google.com/docs/authentication).

#### Local development environment

To set up credentials for a local development environment, use one of the following ways:

- [User credentials and ADC for MCP servers](https://docs.cloud.google.com/mcp/authenticate-mcp#user-credentials-adc-mcp-servers)
- [Service account impersonation](https://docs.cloud.google.com/mcp/authenticate-mcp#sa-impersonation)

#### User credentials and ADC for MCP servers

To use your own identity for local development, provide your user credentials to [Application Default Credentials](https://docs.cloud.google.com/docs/authentication/application-default-credentials) (ADC). Running the Google Cloud CLI command `gcloud auth application-default login` creates a local credential file. ADC automatically finds and uses this file to authenticate requests to Google Cloud services, including MCP servers.

If you use this method, you might encounter an authentication error when you try to authenticate to MCP servers. For more information about this error and how to address it, see [User credentials not working](https://docs.cloud.google.com/docs/authentication/troubleshoot-adc#user-creds-client-based).

#### Service account impersonation

In most cases, you can use your user credentials to authenticate from a local development environment. If that is not feasible, or if you need to test the permissions assigned to a service account, you can use service account impersonation.

When you use service account impersonation, you start with an authenticated principal (your user account or a service account) and request short-lived credentials for a service account that has the authorization that your use case requires. You must have the `iam.serviceAccounts.getAccessToken` permission, which is included in the [Service Account Token Creator](https://docs.cloud.google.com/iam/docs/roles-permissions/iam#iam.serviceAccountTokenCreator) (`roles/iam.serviceAccountTokenCreator`) IAM role.

You can set up the gcloud CLI to use service account impersonation by using the [`gcloud config set` command](https://docs.cloud.google.com/sdk/gcloud/reference/config):

```
gcloud config set auth/impersonate_service_account SERVICE_ACCT_EMAIL
```

Replace `SERVICE_ACCT_EMAIL` with the service account email.

For select languages, you can use service account impersonation to create a local ADC file for use by client libraries. This approach is supported only for the Go, Java, Node.js, and Python client libraries—it is not supported for the other languages. To set up a local ADC file with service account impersonation, use the [`--impersonate-service-account` flag](https://docs.cloud.google.com/sdk/gcloud/reference#--impersonate-service-account) with the [`gcloud auth application-default login` command](https://docs.cloud.google.com/sdk/gcloud/reference/auth/application-default/login):

```
gcloud auth application-default login --impersonate-service-account=SERVICE_ACCT_EMAIL
```

For more information about service account impersonation, see [Use service account impersonation](https://docs.cloud.google.com/docs/authentication/use-service-account-impersonation).

#### Create an OAuth client ID for your AI application

Create an OAuth client ID and client secret to permit your AI application to authenticate to Google and Google Cloud remote MCP servers. When configured, the AI application can access resources as if it were you, inheriting your permissions. This is achieved through OAuth tokens, so your actual user credentials are never shared with or stored in the AI application.

To create a client ID and client secret, follow the instructions in [Obtain OAuth 2.0 credentials from the Google API Console](https://developers.google.com/identity/protocols/oauth2#1.-obtain-oauth-2.0-credentials-from-the-dynamic_data.setvar.console_name.).

## Agent identity

For production workloads, create a separate agent identity, instead of using your identity, to ensure observability and security. Only grant your agent identity the minimum permissions necessary, and consider using Identity and Access Management attributes to [prevent read-write MCP tool use](https://docs.cloud.google.com/mcp/prevent-read-write-tool-use) on important resources.

The following sections describe how to set up a separate identity, or principal, for your agent. The agent principal can be granted separate roles to control the AI application's access to resources.

### Set up an agent identity to authenticate to MCP servers

Your authentication setup depends on your environment. The most common options are described in the following sections.

For more options and information about authentication, see [Authentication methods](https://docs.cloud.google.com/docs/authentication).

#### Create a service account for your AI application

You can use a service account as the identity for your agent if your AI application is hosted on Google Cloud. The service account can use the metadata server for a virtual machine (VM) instance to fetch an access token for authentication.

To set up a VM and attach a service account for your AI application, follow the instructions to set up a workload [on Google Cloud](https://docs.cloud.google.com/mcp/authenticate-mcp#on-gcp).

If your AI application isn't hosted on Google Cloud, then follow the instructions for [On-premises or on a different cloud provider](https://docs.cloud.google.com/mcp/authenticate-mcp#on-prem).

#### Create an agent identity

If you are using Vertex AI Agent Engine to deploy your agent, then you can [create an agent identity](https://docs.cloud.google.com/agent-builder/agent-engine/agent-identity#create-agent-identity).

### On Google Cloud

To authenticate a workload running on Google Cloud, you use the credentials of the service account attached to the compute resource where your code is running, such as a [Compute Engine virtual machine (VM) instance](https://docs.cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances#using). This approach is the preferred authentication method for code running on a Google Cloud compute resource.

For most services, you must attach the service account when you create the resource that will run your code; you cannot add or replace the service account later. Compute Engine is an exception—it lets you attach a service account to a VM instance at any time.

Use the gcloud CLI to create a service account and attach it to your resource:

1. [Install](https://docs.cloud.google.com/sdk/docs/install) the Google Cloud CLI. After installation, [initialize](https://docs.cloud.google.com/sdk/docs/initializing) the Google Cloud CLI by running the following command:
	```
	gcloud init
	```
	If you're using an external identity provider (IdP), you must first [sign in to the gcloud CLI with your federated identity](https://docs.cloud.google.com/iam/docs/workforce-log-in-gcloud).
2. Set up authentication:
	1. Ensure that you have the Create Service Accounts IAM role (`roles/iam.serviceAccountCreator`) and the Project IAM Admin role (`roles/resourcemanager.projectIamAdmin`). [Learn how to grant roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access).
		2. Create the service account:
		```
		gcloud iam service-accounts create SERVICE_ACCOUNT_NAME
		```
		Replace `SERVICE_ACCOUNT_NAME` with a name for the service account.
		3. To provide access to your project and your resources, grant a role to the service account:
		```
		gcloud projects add-iam-policy-binding PROJECT_ID --member="serviceAccount:SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com" --role=ROLE
		```
		Replace the following:
		- `SERVICE_ACCOUNT_NAME`: the name of the service account
				- `PROJECT_ID`: the project ID where you created the service account
				- `ROLE`: the role to grant
		4. To grant another role to the service account, run the command as you did in the previous step.
		5. Grant the required role to the principal that will attach the service account to other resources.
		```
		gcloud iam service-accounts add-iam-policy-binding SERVICE_ACCOUNT_NAME@PROJECT_ID.iam.gserviceaccount.com --member="user:USER_EMAIL" --role=roles/iam.serviceAccountUser
		```
		Replace the following:
		- `SERVICE_ACCOUNT_NAME`: the name of the service account
				- `PROJECT_ID`: the project ID where you created the service account
				- `USER_EMAIL`: the email address for a Google Account
3. Create the resource that will run your code, and attach the service account to that resource. For example, if you use Compute Engine: Create a Compute Engine instance. Configure the instance as follows:
	- Replace `INSTANCE_NAME` with your preferred instance name.
		- Set the `--zone` flag to the [zone](https://docs.cloud.google.com/compute/docs/zones#available) in which you want to create your instance.
		- Set the `--service-account` flag to the email address for the service account that you created.
	```
	gcloud compute instances create INSTANCE_NAME --zone=ZONE --service-account=SERVICE_ACCOUNT_EMAIL
	```

For more information about authenticating to Google APIs, see [Authentication methods](https://docs.cloud.google.com/docs/authentication).

### On-premises or on a different cloud provider

The preferred method to set up authentication from outside of Google Cloud is to use workload identity federation. For more information, see [Set up ADC for on-premises or another cloud provider](https://docs.cloud.google.com/docs/authentication/set-up-adc-on-premises) in the authentication documentation.

## API keys for services that don't require a principal

Services that don't require a principal can use API keys for authentication.

To create an API key for an AI application, do the following:

1. In the Google Cloud console, go to the **APIs & Services > Credentials** page.
	[Go Credentials](https://console.cloud.google.com/projectselector2/apis/credentials?supportedpurview=project)
2. Click **Create credentials** and then select **API key**.
3. In the **API key created** dialog, click **Edit API key**.
	1. Edit the API Key **Application restrictions**. Application restrictions limit an API key's usage to specific websites, IP addresses, Android applications, or iOS applications. You can set one application restriction per key.
		2. Edit the API key **API restrictions**. API restrictions specify the enabled APIs that the key can call.
4. Click **Save**.

Your AI application can use the API key to authenticate to Google and Google Cloud services. To keep your API key secure, follow the [best practices for securely using API keys](https://support.google.com/googleapi/answer/6310037).