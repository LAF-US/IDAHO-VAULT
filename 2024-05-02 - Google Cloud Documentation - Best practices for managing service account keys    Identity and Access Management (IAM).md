---
source: "https://docs.cloud.google.com/iam/docs/best-practices-for-managing-service-account-keys?_gl=1%2Adwksfq%2A_ga%2AMTA3ODU3MTkyOS4xNzc0MzE5ODcx%2A_ga_WH2QY8WWF5%2AczE3NzcwNjgxMzEkbzIxJGcxJHQxNzc3MDY4NjQyJGoxNiRsMCRoMA.."
author:
published: 2024-05-02
created: 2026-04-24
---
Unlike user accounts, service accounts don't have passwords. Instead, service accounts use RSA key pairs for authentication. If you know the private key of a service account's key pair, you can use the private key to [create a JWT bearer token](https://developers.google.com/identity/protocols/oauth2/service-account#httprest) and use the bearer token to request an access token. The resulting access token reflects the service account's identity and you can use it to interact with Google Cloud APIs on the service account's behalf.

Because the private key lets you authenticate as the service account, having access to the private key is similar to knowing a user's password. The private key is known as a *service account key*. The key pairs used by service accounts fall into two categories, [Google-managed and user-managed](https://docs.cloud.google.com/iam/docs/service-account-creds#key-types).

Service account keys can become a security risk if not managed carefully. You should [choose a more secure alternative for authentication](https://docs.cloud.google.com/docs/authentication#auth-decision-tree) whenever possible. The main threats are related to service account keys are:

- **Credential leakage**: Service account keys might inadvertently end up in places where they are not supposed to be stored. A bad actor can use a leaked service account key to authenticate and gain a foothold in your environment.
- **Privilege escalation**: If a bad actor gets access to a poorly secured service account key, they might be able to use the key to escalate their privileges.
- **Information disclosure:** Service account keys might inadvertently disclose confidential metadata.
- **Non-repudiation:** By authenticating using a service account key and letting the service account carry out operations on their behalf, a bad actor might conceal their identity and actions.
- **Malicious credential configurations:** A bad actor could provide a malicious credential configuration to circumvent your security defenses.

The best way to mitigate these threats is to [avoid user-managed service account keys](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts#service-account-keys) and to use [other methods to authenticate service accounts](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts#using_service_accounts) whenever possible. You can also use [IAM Conditions](https://docs.cloud.google.com/iam/docs/conditions-overview) and [VPC Service Controls](https://docs.cloud.google.com/vpc-service-controls/docs/service-perimeters) to restrict what resources can potentially be accessed by a compromised service account.

For situations where you can't use [more secure alternatives to service account keys](https://docs.cloud.google.com/docs/authentication#auth-decision-tree), this guide presents best practices for managing, using, and securing service account keys.

## Protecting against credential leakage

Like a username and password, service account keys are a form of credential. If a user can access a valid service account key, they can use it to authenticate and access the resources the respective service account has been granted access to.

To bad actors, service account keys can be even more valuable than a leaked password. Attempting to sign in by using a leaked password is unlikely to succeed if the user account has been configured to use [2-step verification](https://support.google.com/a/answer/9176657) and [login challenges](https://support.google.com/a/answer/6002699). In contrast, authenticating by using a leaked service account key is likely to succeed as service accounts are not subject to any additional sign-in verifications.

Bad actors might look for service account keys in a variety of places, including:

- Source code repositories of open source projects
- Public Cloud Storage buckets
- Public data dumps of breached services

In addition to public locations, bad actors might look for service account keys in private locations they've compromised. Examples include:

- Email inboxes
- File shares
- Backup storage
- Temporary file system directories

An effective way to lower the risk of leaking service account keys is to reduce the number of keys in circulation and to disincentivize the creation of new keys. The following sections describe how you can limit the number of service account keys in circulation, and what other measures can help you limit the risk of leaking service accounts.

**Best practices**:

[Provide alternatives to creating service account keys](#alternatives).  
[Use organization policy constraints to limit which projects can create service account keys](#orgpolicy-constraints).  
[Don't leave service account keys in temporary locations](#temp-locations).  
[Don't pass service account keys between users](#pass-between-users).  
[Don't submit service account keys to source code repositories](#code-repositories).  
[Don't embed service account keys in program binaries](#embed-in-binaries).  
[Use insights and metrics to identify unused service account keys](#insights).  
[Rotate service account keys to reduce security risk caused by leaked keys](#rotate-keys).  
[Use expiry times to let keys expire automatically](#key-expiry).  
[Use organization policy constraints to automatically disable leaked keys](#orgpolicy-leaked-keys).

### Provide alternatives to creating service account keys

Make sure that users in your organization are aware of alternatives and can justify the additional risk and management overhead of using a service account key:

- Educate your developers on [more secure alternatives to service account keys](https://docs.cloud.google.com/docs/authentication#auth-decision-tree)
- Establish a process to help developers decide on the appropriate authentication method for their use case before creating a new service account key.
- Use [organization policy constraints](https://docs.cloud.google.com/resource-manager/docs/organization-policy/understanding-constraints) to prevent creating new service account keys, and allow exceptions only for projects that have demonstrated that they cannot use a more secure alternative.

### Use organization policy constraints to limit which projects can create service account keys

Given the [more secure alternatives to service account keys](https://docs.cloud.google.com/docs/authentication#auth-decision-tree), it's best to consider the use of service account keys as an exception rather than the norm.

To prevent unnecessary usage of service account keys, use [organization policy constraints](https://docs.cloud.google.com/resource-manager/docs/organization-policy/org-policy-constraints):

- At the root of your [organization's resource hierarchy](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization), apply the [Disable service account key creation](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts#disable_service_account_key_creation) and [Disable service account key upload](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts#disable_service_account_key_upload) constraints to establish a default where service account keys are disallowed.
- When needed, [override](https://docs.cloud.google.com/resource-manager/docs/organization-policy/understanding-hierarchy#disallow_inheritance) one of the constraints for selected projects to re-enable service account key creation or upload.

Modifying organization policy constraints requires the `orgpolicy.policy.set` permission. Because neither the Owner (`roles/owner`) nor the Editor (`roles/editor`) role includes this permission, constraints can also be effective in non-production environments where some principals might have Owner or Editor access to projects.

### Don't leave service account keys in temporary locations

When you create a service account key by using the Google Cloud console, most browsers immediately download the new key and save it in a download folder on your computer. You should immediately move the key to the location where you want to store it. Make sure you're not accidentally leaving a copy in the download folder or the recycle bin of your computer.

You can reduce the risk of accidentally leaving copies of service account keys in temporary locations [by using the Google Cloud CLI](https://docs.cloud.google.com/sdk/gcloud/reference/iam/service-accounts/keys/create): The `gcloud iam service-accounts keys create` command lets you write the service account key file straight to the location where you need it. Also, on most operating systems, the gcloud CLI automatically adjusts file permissions so that the file is only accessible by you.

### Don't pass service account keys between users

When you deploy an application that requires a service account key, you might not have the permission to create a service account key yourself. Instead, you might have to request a different person to create a service account key for you.

In scenarios where multiple users are involved in the creation and deployment of a service account key, there is an increased risk that copies of the key remain in mailboxes, chat histories, or other locations. Whenever a handover between users is necessary, it can be more secure to upload a service account key:

1. As the user deploying the application, create a self-signed certificate that uses an RSA 2048-bit key pair on the target machine. To create the certificate, you can use `openssl`, `certutil`, `New-SelfSignedCertificate`, or other operating system tools.
2. Pass the certificate file to the user who has the permission to upload the certificate while keeping the private key on the target machine. When passing the certificate, make sure that it can't be replaced or tampered with, but you don't need to keep it confidential.
3. As the user who has the necessary permissions to manage service account keys, [upload the certificate](https://docs.cloud.google.com/iam/docs/keys-upload) to associate it with a service account.

By following this process, you avoid passing the private key and instead only exchange public information between users.

### Don't submit service account keys to source code repositories

Service account keys are credentials, and must be protected from unauthorized access. If you submit a service account key to a source code repository, there is an increased risk that the key becomes accessible to unauthorized users and bad actors:

- Bad actors might scan the source code of public source repositories for leaked keys.
- In the future, you might decide to turn a private source repository into a public repository, without checking it for keys first.
- Other team members might store copies of the source code on their workstation.

When you work on code that uses a service account key, always store the service account key separate from the source code to reduce the risk of accidentally submitting the key to the source repository. In many cases, you can further reduce this risk by not using service account keys at all during development and [using your personal credentials instead of service account keys](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts#development) instead.

Additionally, set up your source control system so that it detects accidental submissions of service account keys:

- If you use [Cloud Source Repositories](https://docs.cloud.google.com/source-repositories), [enable key detection](https://docs.cloud.google.com/source-repositories/docs/detecting-security-keys#enable_security_key_detection) to block `git` push operations that contain private keys and to notify users.
- If you use GitHub, [enable secret scanning for your repositories](https://docs.github.com/en/code-security/secret-scanning/enabling-secret-scanning-features/enabling-secret-scanning-for-your-repository).
- Use Security Command Center [anomaly detection](https://docs.cloud.google.com/security-command-center/docs/concepts-security-sources#anomaly_detection) to surface information about leaked credentials.
- If your source control management system doesn't support automatic scanning, use an open-source tool like [truffleHog](https://github.com/dxa4481/truffleHog) to scan your source code for secrets by using a [pre-commit hook](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks), by adding a step to continuous integration pipeline, or both.

### Don't embed service account keys in program binaries

Service account keys are strings that match a certain pattern, and they can be identified even if embedded in other files or binaries. If a bad actor has access to the binary, they can extract any service account keys that are embedded in the binary.

Program binaries for server-side applications might be hosted in artifact repositories or they might be copied to developer workstations for debugging purposes. Keeping service account keys separate from the program binaries helps ensure that a user who can access the binary does not implicitly get access to service account credentials.

- For client-side applications such as tools, desktop programs, or mobile apps, don't use service accounts. Instead, let users authenticate with their own credentials. For example, you could use the [OAuth-consent flow](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts#user-consent).
- For server-side applications, don't embed service account keys into the binary. Instead, keep the keys separate from the application binary.

### Use metrics to identify unused service account keys

To minimize the number of valid service account keys in circulation, it's best to disable keys as soon as they aren't needed anymore, then delete the keys when you're certain that they are no longer needed.

If you're unsure whether a key is still in use, you can check its usage with service account insights and authentication metrics:

- [Service account insights](https://docs.cloud.google.com/iam/docs/managing-insights) let you identify service accounts that have not been used in the past 90 days.
- By monitoring the **Key Authentication Events** metric, you can [find out when a service account key was last used](https://docs.cloud.google.com/iam/docs/service-account-monitoring#view-metrics-single-key) and how often it was used to authenticate a service account.

Because service accounts belong to a Google Cloud project, insights and metrics must be tracked individually for each project.

### Rotate service account keys to reduce security risk caused by leaked keys

Although you can reduce the probability of accidentally leaking a service account key, it can be difficult to eliminate the risk completely.

Key rotation is the process of replacing your existing keys with new keys and then invalidating the replaced keys. We recommend that you routinely rotate all keys that you manage, including your service account keys.

Rotating service account keys can help reduce the risk posed by leaked or stolen keys. If a key is leaked, it might take bad actors days or weeks to discover the key. If you regularly rotate your service account keys, there's a higher chance that the leaked keys will be invalid by the time a bad actor gets them.

Having an established process for rotating service account keys also helps you act quickly if you suspect that a service account key has been compromised.

If you generated the public/private key pair yourself, stored the private key in a hardware security module (HSM), and [uploaded the public key to Google Cloud](https://docs.cloud.google.com/iam/docs/keys-upload), then you might not need to rotate the key on a regular schedule. Instead, you can rotate the key if you believe that it might have been compromised.

### Use expiry times to let keys expire automatically

By default, service account keys that you create and download from IAM don't have an expiry time and stay valid until you delete them. Setting an expiry time for service account keys can limit your security risk by reducing the lifetime of the persistent credential. However, there are other risks associated with setting expiry times; for example, setting an expiry time can cause workloads to fail when their keys expire.

Use expiry times when you need temporary access to a system that requires a service account key. For example, use expiry times when you're doing the following:

- Developing code in a non-production environment for an application that can only authenticate with service account keys
- Using a third-party tool that can only authenticate with service account keys

Avoid using expiry times for these scenarios:

- Production workloads. In production, an expired service account key could cause an accidental outage. Instead, use keys that do not expire, and manage their lifecycle with key rotation.
- Non-production workloads that need permanent access, such as a continuous integration (CI) pipeline.
- Key-rotation systems that prevent a key from being used after a specified amount of time. To learn about recommended key rotation strategies, see [Service account key rotation](https://docs.cloud.google.com/iam/docs/key-rotation).

To limit the validity of service account keys, you can [configure an expiry time](https://docs.cloud.google.com/iam/docs/service-account-creds#key-expiry) for newly created keys in your project, folder, or organization. The expiry time does not apply to existing keys.

Alternatively, you can [upload a service account key](https://docs.cloud.google.com/iam/docs/keys-upload) and specify a **Valid To** date in the X.509 certificate file. After the expiry date passes, the key can't be used for authentication. However, it stays associated with the service account until you delete it.

### Use organization policy constraints to automatically disable leaked keys

Even if you follow all of the best practices for service account keys, it's possible for your service account keys to be leaked.

To help manage leaked credentials, ensure that the [Service Account Key Exposure Response constraint](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts#disable-exposed-keys) is set to `DISABLE_KEY`. If you set the constraint to this value, Google Cloud will automatically disable any leaked keys that it detects.

If a key is disabled because it was leaked, the following fields are added to the key's metadata:

- `"disable_reason": "SERVICE_ACCOUNT_KEY_DISABLE_REASON_EXPOSED"`: indicates that the key was disabled because it was exposed.
- `"extended_status": "SERVICE_ACCOUNT_KEY_EXTENDED_STATUS_KEY_EXPOSED"` ": indicates that the key was once publicly exposed. This value persists even if you re-enable the key.
- `"extended_status_message": "LINK_TO_EXPOSURE"`: if available, the metadata contains a link to the place where the key was detected, which you can use for remediation.

These keys [can be re-enabled](https://docs.cloud.google.com/iam/docs/keys-disable-enable#enabling) if required to mitigate an outage. However, we recommend disabling them again as soon as possible, because publicly exposed keys present a security risk, even if the initial exposure is removed.

To learn about other best practices for managing compromised credentials, see [Handling compromised Google Cloud credentials](https://docs.cloud.google.com/docs/security/compromised-credentials).

## Protecting against privilege escalation

Using service account keys can expose you to privilege escalation attacks if the keys are less well secured than the resources they grant access to.

As an example, suppose a bad actor has already gained a foothold in your environment and now tries to access certain Google Cloud resources. They might still lack the permissions to access these resources, but their privileges might suffice to access a service account key that is stored on a VM, file share, or another less secure location. By authenticating using the service account key, the bad actor can assume the identity of the service account. The service account might let the bad actor access resources they previously did not have access to, thereby escalating the bad actor's privileges.

Because a service account key indirectly grants access to resources on Google Cloud, you must consider the key itself to be as valuable, and as much worth protecting, as the resources themselves.

The following sections describe best practices for protecting service account keys and reducing the risk of unauthorized access and resulting privilege escalation.

**Best practices**:

[Avoid storing keys on a file system](#file-system).  
[Use an HSM or TPM to store keys](#tpm).  
[Use a software-based key store](#software-keystore).  
[Don't store keys in Secret Manager or other cloud-based secret stores](#secret-manager).  
[Don't use the Editor role in projects that allow service account key creation or upload](#editor-role).  
[Avoid using service account keys for domain-wide delegation](#domain-wide-delegation).

### Avoid storing keys on a file system

Service account keys created by using the Google Cloud console or the gcloud CLI are JSON files, and you can copy these files to the file system of the machine where they are needed. But storing service account keys as files on a file system can expose you to several risks, including:

- Some file systems such as NTFS use inherited permissions by default. Unless disabled, a permission added to a parent folder might inadvertently cause a key file to become more widely accessible and visible to unauthorized users.
- In a virtualized environment, bad actors might be able to undermine file system security by accessing the underlying virtual disk.
- File system access and permission changes are often not audit-logged. If file permissions are inadvertently changed and the key becomes visible to unauthorized users, it might be difficult to analyze when and by whom these changes were made.
- Files can be easily copied and thus exfiltrated if a bad actor gains access.

Whenever possible, avoid storing service account keys on a file system. If you can't avoid storing keys on disk, make sure to restrict access to the key file, configure file access auditing, and encrypt the underlying disk.

### Use an HSM or TPM to store keys

When you create a service account key by using the Google Cloud console or the gcloud CLI, the private key is generated by Google Cloud and then revealed to you. Many security risks associated with service account keys stem from the fact that the private key is, temporarily or permanently, available in clear text and can therefore be difficult to protect.

Instead of letting Google Cloud generate a key pair, you can use a hardware security module (HSM) or Trusted Platform Module (TPM) to create and manage keys:

1. Use a HSM or TPM to generate a RSA key pair.
2. Use the key pair to create a self-signed certificate.
3. [Upload the certificate](https://docs.cloud.google.com/iam/docs/keys-upload) as a service account key.
4. Let the application use the HSM or TPM's signing API to sign the JWT for authenticating the service account.

An HSM or TPM lets you use a private key without ever revealing the key in clear text. Using an HSM or TPM to manage service account keys therefore helps you enforce access control while also mitigating the risk of keys being copied to other systems.

Some platforms provide abstractions that let you take advantage of a TPM without having to directly interact with it. For example, Windows lets you manage TPM-protected keys by using the CryptoNG API in combination with the `Microsoft Platform Crypto Provider`.

Service account keys managed by a TPM are unique to a physical or virtual machine. You can still let multiple machines share a service account by associating each machine's key with a common service account.

### Use a software-based key store

In situations where using a hardware-based key store isn't viable, use a software-based key store to manage service account keys. Similar to hardware-based options, a software-based key store lets users or applications use service account keys without revealing the private key. Software-based key store solutions can help you control key access in a fine-grained manner and can also ensure that each key access is logged.

The security of a software-based key store typically depends on how its master key is protected. Before you use a software-based key store, make sure to review the following:

- How the master key is secured at rest,
- How the unsealing process works, and who is able to initiate it,
- How keys are protected from being extracted from memory,
- How the key store is protected from being undermined if a bad actor gains shell access or hypervisor access to the underlying system.

### Don't store keys in Secret Manager or other cloud-based secret stores

We don't recommend using Google Cloud's Secret Manager to store and rotate service account keys. This is because, to access Secret Manager secrets, your application needs an identity that Google Cloud can recognize. If your application already has an identity that Google Cloud can recognize, then your application can use that identity to authenticate to Google Cloud instead of using a service account key.

The same concept applies for other cloud-based secret management services, like Azure KeyVault and AWS Secret Manager. If an application already has an identity that these cloud providers can recognize, your application would be able to use that identity to authenticate to Google Cloud instead of using a service account key.

### Don't use the Editor role in projects that allow service account key creation or upload

A key difference between the Editor (`roles/editor`) and Owner (`roles/owner`) basic roles is that the Editor role doesn't let you change IAM policies or roles. With the Editor role, you therefore can't easily extend your own access or grant other users access to project resources.

The limitations of the Editor role can be undermined if a project contains service accounts. Because the Editor roles grant permission to create or upload service account keys, a bad actor can create new keys for existing service accounts and use these keys to either escalate their own access, or to hand the keys to other users to obtain access to project resources.

Instead of using the Editor role, or any other basic role, it's best to use the more narrowly defined predefined roles, or to create custom roles that only grant necessary permissions.

If you need to use the Editor role, [disable service account key upload](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts#disable_service_account_key_upload) and [key creation](https://docs.cloud.google.com/resource-manager/docs/organization-policy/restricting-service-accounts#disable_service_account_key_creation) by using organization policy constraints to help ensure that the Editor role can't be abused for privilege escalation.

### Avoid using service account keys for domain-wide delegation

Domain-wide delegation lets you impersonate a user so that you can [access a user's data without any manual authorization on their part](https://developers.google.com/admin-sdk/directory/v1/guides/delegation). Although examples illustrating the use of domain-wide delegation commonly suggest the use of service account keys, using service account keys is not necessary to perform domain-wide delegation.

When using domain-wide delegation, avoid service account keys and use the [`signJwt` API](https://docs.cloud.google.com/iam/docs/reference/credentials/rest/v1/projects.serviceAccounts/signJwt) instead:

1. Authenticate a service account by using an [attached service account](https://docs.cloud.google.com/iam/docs/attach-service-accounts), [Workload Identity Federation for GKE](https://docs.cloud.google.com/kubernetes-engine/docs/how-to/workload-identity#authenticating_to), or [Workload Identity Federation](https://docs.cloud.google.com/iam/docs/workload-identity-federation) first.
2. [Construct a JWT](https://developers.google.com/identity/protocols/oauth2/service-account#jwt-auth) and use the `sub` claim to specify the email address of the user for which you're requesting delegated access.
3. Use the [`signJwt` API](https://docs.cloud.google.com/iam/docs/reference/credentials/rest/v1/projects.serviceAccounts/signJwt) to sign the JWT.
4. [Pass the signed JWT](https://developers.google.com/identity/protocols/oauth2/service-account#jwt-auth) to the OAuth2 Token resource to obtain an access token.

By following this approach, you avoid having to manage a service account key, resulting in a setup that can be secured more easily.

## Protecting against information disclosure threats

**Best practices**:

[Avoid disclosing confidential information in uploaded X.509 certificates](#confidential-information).

### Avoid disclosing confidential information in uploaded X.509 certificates

For each service account key, IAM lets you download a X.509 certificate from the endpoint `https://www.googleapis.com/service_accounts/v1/metadata/x509/ACCOUNT_EMAIL`. This endpoint is public and doesn't require authentication.

For Google-owned and managed keys and user-managed keys that you created by using the Google Cloud console or the gcloud CLI, the X.509 certificates are created automatically and only contain basic metadata such as the email address and expiry date.

For uploaded service account keys, the X.509 certificate provided by the public endpoint is the same certificate as the one you uploaded. If the certificate you uploaded contained any optional attributes (such as address or location information embedded in the common name), then this information also becomes publicly accessible. A bad actor might use this information to learn more about your environment.

To avoid disclosing confidential information, don't add any optional attributes to uploaded X.509 certificates and use a generic `Subject`.

## Protecting against non-repudiation threats

When you notice suspicious activity affecting your Google Cloud resources and want to analyze its origins, you need data that lets you reconstruct the chain of events that led to the suspicious activity. The primary source of data to perform such analysis are typically audit logs.

Analyzing audit logs can become more difficult when service accounts are involved. If an activity was initiated by a service account, the log entry contains the service account's email address, but you also need to find out which user or application was using the service account at the time.

The following sections contain best practices for using service account keys in a way that helps you track their usage.

**Best practices**:

[Use a dedicated service account for each application](#dedicated-service-accounts).  
[Use a dedicated key for each machine that runs an application](#dedicated-keys).

### Use a dedicated service account for each application

All audit log records contain a `principalEmail` field that identifies the principal that initiated the activity. If you share a service account key across multiple applications, then it can be difficult to identify which application performed an activity because audit log records contain the same `principalEmail` value.

Instead of sharing a key among multiple applications, create a dedicated service account for each application. That way, the `principalEmail` field lets you identify the application associated with a service account which can help you reconstruct the chain of events that led to a suspicious activity.

### Use a dedicated key for each machine that runs an application

If you run multiple copies of the same application across multiple machines, then the `principalEmail` field might let you identify the application, but not the machine where a particular activity originated from.

To help you narrow down the potential sources of suspicious activity, create individual keys for each copy of the application. That way, you can use the `serviceAccountKeyName` field that many services add to audit log records to distinguish which machine an activity originated from.

## Protecting against malicious credential configurations

Some credential configurations contain URLs and file paths that, if not appropriately validated by a workload, could cause the workload to use malicious endpoints.

**Best practices**:

[Validate keys acquired from an external source before using them to authenticate to Google APIs](#validate-external-creds).

### Validate keys acquired from an external source before using them to authenticate to Google APIs

When you accept a service account key from an external source, you must validate the key before using it. If you don't validate the key, a malicious actor could use the key to cause your workload to access malicious endpoints.

If your system expects only service account keys, make sure that the value of the `type` field is `service_account`.

For more information, see [Security requirements when using credential configurations from an external source](https://docs.cloud.google.com/docs/authentication/external/externally-sourced-credentials).

## What's next

- Read more about [best practices for working with service accounts](https://docs.cloud.google.com/iam/docs/best-practices-service-accounts).
- Review our [best practices for using service accounts in deployment pipelines](https://docs.cloud.google.com/iam/docs/best-practices-for-using-service-accounts-in-deployment-pipelines).