[Action Required] Transition your scripts and workflows from gsutil to gcloud storage before Mar 2027

Hello Logan,

We’re writing to inform you that starting March 2027, Google Cloud will no longer include the gsutil command-line tool in the default Google Cloud CLI installation package.

We strongly encourage all users to transition to gcloud storage, our modern and fully supported CLI for Google Cloud Storage that offers enhanced performance and advanced features. Users who install or update the Google Cloud CLI after this change takes effect will not receive gsutil by default. If you wish to continue using gsutil, you will need to install it separately.

We’ve provided additional details below to help you understand these changes and take any necessary actions.

What you need to know
Key changes after March 2027:

New installations: If you install or update the Google Cloud CLI after March 2027, the system will not install gsutil by default. We will continue to distribute gsutil separately. You must download it explicitly via the PyPI channel, as it will no longer form part of the default gcloud bundle.
Existing installations: The impact of updating your Google Cloud CLI version after March 2027 depends on the installation method:
Installations via Docker, Snap, or similar methods (Environment replacement): If you use installation methods like the official Docker or Snap images, which replace the entire environment upon update, updating to a Google Cloud CLI version released after March 2027 will result in gsutil no longer being present in the environment. This will immediately break any scripts or CI/CD pipelines relying on the bundled gsutil. To avoid disruption, you must modify your Dockerfile, Snap configuration, or similar setup to explicitly install gsutil separately through PyPI.
Installations via APT, RPM, Tarball, or other methods: If you installed the Google Cloud CLI using methods such as APT, RPM, or by extracting a tarball, when you update the Google Cloud CLI after March 2027, the last version of gsutil that was bundled will remain on your system. However, this version of gsutil will no longer receive updates through the Google Cloud CLI. To access newer gsutil versions or to ensure functionality in new environments, you will need to switch to a standalone installation.
Script compatibility: Existing scripts that use gsutil will continue to function with the PyPI version of gsutil. Note that standalone gsutil does not automatically share credentials with the gcloud CLI. If you switch to the standalone version, you must configure authentication separately (e.g., via gsutil config or by defining credentials in a Boto configuration file).
Future updates: To access updated versions of gsutil moving forward, you must switch to a standalone installation.
We strongly recommend migrating your scripts and workflows from gsutil to gcloud storage to ensure long-term support and access to the latest features.

What you need to do
Action required:

Migrate your workflows: Transition your scripts and workflows from gsutil to gcloud storage before March 2027. Refer to the Transitioning from gsutil to gcloud storage guide for detailed instructions, command equivalents, and migration tips.
Standalone installation (Optional): If you must continue using gsutil in new environments, Docker and Snap like environments or installations after the deadline, you must install gsutil separately. (Note: Standalone installation requires a Python environment and pip. If your environment restricts access to PyPI, or if you have any concerns, reach out to Google Cloud Support.)
If you already use gcloud storage, you do not need to take any action.

Impacted customers/accounts:

Your affected projects are listed below:

idaho-vault
We’re here to help
We understand that making this change may require some planning and we're here to support you during this process. If you have any questions or require assistance, please reach out to Google Cloud Support.

Thanks for choosing Google Cloud Storage.

– The Google Cloud Team