---
title: "Configuring two-factor authentication"
source: "https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication"
author:
published:
created: 2026-04-20
description: "You can choose among multiple options to add a second source of authentication to your account."
date created: Monday, April 20th 2026, 12:53:17 pm
date modified: Monday, April 20th 2026, 12:54:11 pm
---

You can configure two-factor authentication (2FA) using a TOTP app on mobile or desktop or via text message. After you have configured 2FA using a TOTP app or via text message, you can then also add security keys as alternate 2FA methods.

We strongly recommend using a time-based one-time password (TOTP) application to configure 2FA, and security keys as backup methods instead of SMS. TOTP applications are more reliable than SMS, especially for locations outside the United States. Many TOTP apps support the secure backup of your authentication codes in the cloud and can be restored if you lose access to your device.

After you configure 2FA, your account will enter a 28-day check up period. You can leave the check up period by successfully performing 2FA in those 28 days. Otherwise, you will be prompted to perform 2FA in an existing GitHub session on the 28th day. If you cannot perform 2FA to pass the checkup, you must use the provided shortcut to reconfigure your 2FA settings and retain access to GitHub.

If you're a member of an enterprise with managed users, you cannot configure 2FA for your managed user account account unless you're signed in as the setup user. For users other than the setup user, an administrator must configure 2FA on your identity provider (IdP).

## Configuring two-factor authentication using a TOTP app

A time-based one-time password (TOTP) application automatically generates an authentication code that changes after a certain period of time. These apps can be downloaded to your phone or desktop. We recommend using cloud-based TOTP apps. GitHub is app-agnostic when it comes to TOTP apps, so you have the freedom to choose any TOTP app you prefer. Just search for `TOTP app` in your browser to find various options. You can also refine your search by adding keywords like `free` or `open source` to match your preferences.

1. Download a TOTP app of your choice to your phone or desktop.
2. In the upper-right corner of any page on GitHub, click your profile picture, then click **Settings**.
3. In the "Access" section of the sidebar, click **Password and authentication**.
4. In the "Two-factor authentication" section of the page, click **Enable two-factor authentication**.
5. Under "Scan the QR code", do one of the following:
	- Scan the QR code with your mobile device's app. After scanning, the app displays a six-digit code that you can enter on GitHub.
		- If you can't scan the QR code, click **setup key** to see a code, the TOTP secret, that you can manually enter in your TOTP app instead.
	![Screenshot of the "Setup authenticator app" section of the 2FA settings. A link, labeled "setup key", is highlighted in orange.](https://docs.github.com/assets/cb-23826/mw-1440/images/help/2fa/ghes-3.8-and-higher-2fa-wizard-app-click-code.webp)
6. The TOTP application saves your account on GitHub.com and generates a new authentication code every few seconds. On GitHub, type the code into the field under "Verify the code from the app."
7. Under "Save your recovery codes", click **Download** to download your recovery codes to your device. Save them to a secure location because your recovery codes can help you get back into your account if you lose access.
8. After saving your two-factor recovery codes, click **I have saved my recovery codes** to enable two-factor authentication for your account.
9. Optionally, you can configure additional 2FA methods to reduce your risk of account lockout. For more details on how to configure each additional method, see [Configuring two-factor authentication using a security key](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication#configuring-two-factor-authentication-using-a-security-key) and [Configuring two-factor authentication using GitHub Mobile](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication#configuring-two-factor-authentication-using-github-mobile).

### Manually configuring a TOTP app

If you are unable to scan the setup QR code or wish to setup a TOTP app manually and require the parameters encoded in the QR code, they are:

- Type: `TOTP`
- Label: `GitHub:<username>` where `<username>` is your handle on GitHub, for example `monalisa`
- Secret: This is the encoded setup key, shown if you click "Setup key" during configuration
- Issuer: `GitHub`
- Algorithm: The default of SHA1 is used
- Digits: The default of 6 is used
- Period: The default of 30 (seconds) is used

## Configuring two-factor authentication using text messages

If you're unable to configure a TOTP app, you can also register your phone number to receive SMS messages.

Before using this method, be sure that you can receive text messages. Carrier rates may apply.

1. In the upper-right corner of any page on GitHub, click your profile picture, then click **Settings**.
2. In the "Access" section of the sidebar, click **Password and authentication**.
3. In the "Two-factor authentication" section of the page, click **Enable two-factor authentication**.
4. Complete the CAPTCHA challenge, which helps protect against spam and abuse.
5. Under "Verify account", select your country code and type your mobile phone number, including the area code. When your information is correct, click **Send authentication code**.
6. You'll receive a text message with a security code. On GitHub, type the code into the field under "Verify the code sent to your phone" and click **Continue**.
	- If you need to edit the phone number you entered, you'll need to complete another CAPTCHA challenge.
7. Under "Save your recovery codes", click **Download** to download your recovery codes to your device. Save them to a secure location because your recovery codes can help you get back into your account if you lose access.
8. After saving your two-factor recovery codes, click **I have saved my recovery codes** to enable two-factor authentication for your account.
9. Optionally, you can configure additional 2FA methods to reduce your risk of account lockout. For more details on how to configure each additional method, see [Configuring two-factor authentication using a security key](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication#configuring-two-factor-authentication-using-a-security-key) and [Configuring two-factor authentication using GitHub Mobile](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication#configuring-two-factor-authentication-using-github-mobile).

## Configuring two-factor authentication using a passkey

Passkeys allow you to sign in securely to GitHub in your browser, without having to input your password.

If you use two-factor authentication (2FA), passkeys satisfy both password and 2FA requirements, so you can complete your sign in with a single step. If you don't use 2FA, using a passkey will skip the requirement to verify a new device via email. You can also use passkeys for sudo mode and resetting your password. See [About passkeys](https://docs.github.com/en/authentication/authenticating-with-a-passkey/about-passkeys).

1. You must have already configured 2FA via a TOTP mobile app or via SMS.
2. In the upper-right corner of any page on GitHub, click your profile picture, then click **Settings**.
3. In the "Access" section of the sidebar, click **Password and authentication**.
4. Under “Passkeys”, click **Add a passkey**.
5. If prompted, authenticate with your password, or use another existing authentication method.
6. Under “Configure passwordless authentication”, review the prompt, then click **Add passkey**.
7. At the prompt, follow the steps outlined by the passkey provider.
8. On the next page, review the information confirming that a passkey was successfully registered, then click **Done**.

## Configuring two-factor authentication using a security key

Not all FIDO authenticators can be used as passkeys, but you can still register those authenticators as security keys. Security keys are also WebAuthn credentials, but unlike passkeys they don't require user validation. Since security keys only need to verify user presence, they only count as a second factor and must be used in conjunction with your password.

Registering a security key for your account is available after enabling 2FA with a TOTP application or a text message. If you lose your security key, you'll still be able to use your phone's code to sign in.

1. You must have already configured 2FA via a TOTP mobile app or via SMS.
2. Ensure that you have a WebAuthn compatible security key inserted into your device.
3. In the upper-right corner of any page on GitHub, click your profile picture, then click **Settings**.
4. In the "Access" section of the sidebar, click **Password and authentication**.
5. Next to "Security keys," click **Add**.
	![Screenshot of the "two-factor methods" section of the 2FA settings. A gray button labeled "Add" is outlined in orange.](https://docs.github.com/assets/cb-33660/mw-1440/images/help/2fa/add-security-keys-option.webp)
6. Under "Security keys," click **Register new security key**.
7. Type a nickname for the security key, then click **Add**.
8. Following your security key's documentation, activate your security key.
9. Confirm that you've downloaded and can access your recovery codes. If you haven't already, or if you'd like to generate another set of codes, download your codes and save them in a safe place. For more information, see [Configuring two-factor authentication recovery methods](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication-recovery-methods#downloading-your-two-factor-authentication-recovery-codes).

## Configuring two-factor authentication using GitHub Mobile

You can use GitHub Mobile for 2FA when signing into your GitHub account in a web browser. 2FA with GitHub Mobile does not rely on TOTP, and instead uses public-key cryptography to secure your account.

Once you have configured a TOTP application, or SMS, you can also use GitHub Mobile to authenticate. If, in the future, you no longer have access to GitHub Mobile, you will still be able to use security keys or TOTP applications to sign in.

1. You must have already configured 2FA via a TOTP mobile app or via SMS.
2. Install [GitHub Mobile](https://github.com/mobile).
3. Sign in to your GitHub account from GitHub Mobile.
4. Ensure GitHub Mobile can send push notifications. If you have not opted in to push notifications, you can turn them on within notification settings in GitHub Mobile.

After signing in and turning on push notifications, you can now use your device for 2FA.

## Further reading

- [About two-factor authentication](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/about-two-factor-authentication)
- [Configuring two-factor authentication recovery methods](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication-recovery-methods)
- [Accessing GitHub using two-factor authentication](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/accessing-github-using-two-factor-authentication)
- [Troubleshooting two-factor authentication issues](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/troubleshooting-two-factor-authentication-issues)
- [Recovering your account if you lose your 2FA credentials](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/recovering-your-account-if-you-lose-your-2fa-credentials)
- [Managing your personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)