---
title: "Authentication"
source: "https://www.home-assistant.io/docs/authentication/"
author:
  - "[[Home Assistant]]"
published:
created: 2026-04-29
description: "Documentation on authentication in Home Assistant."
tags:
  - "clippings"
---
The authentication system secures access to Home Assistant.

## Login screen

You are greeted with a log in screen, asking you for username and password.

![Screenshot of the login screen, when logging in from within the local network](https://www.home-assistant.io/images/docs/authentication/login-outside-local-network.png)

## User accounts

When you start Home Assistant for the first time, the *owner* user account is created. This account has some special privileges and can:

- Create and manage other user accounts.
- Configure integrations and other settings (coming soon).

> [!warning] :host{display:inline-block;vertical-align:-0.125em}span,svg{display:block} Warning
> For the moment, other user accounts will have the same access as the owner account. In the future, non-owner accounts will be able to have restrictions applied.

> [!note] :host{display:inline-block;vertical-align:-0.125em}span,svg{display:block} Note
> If you want to manage users and you’re an owner but you do not see “Users” in your main configuration menu, make sure that **Advanced Mode** is enabled for your user in your profile.

### Your account profile

Once you’re logged in, you can see the details of your account on the [**User profile**](https://my.home-assistant.io/redirect/profile) page by selecting on the circular at the very bottom of the sidebar.

![Screenshot of the profile page](https://www.home-assistant.io/images/docs/authentication/profile.png)

You can:

- Change your password.
- Enable or disable [multi-factor authentication](https://www.home-assistant.io/docs/authentication/multi-factor-auth/).
- Delete **Refresh tokens**. These are created when you log in from a device. Delete them if you want to force the device to log out.
- Create [Long-lived access tokens](https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token) so scripts can securely interact with Home Assistant.
- Define language and other locale settings.
- Log out of Home Assistant.

> [!note] :host{display:inline-block;vertical-align:-0.125em}span,svg{display:block} Note
> Unused refresh tokens will be automatically removed. A refresh token is considered unused if it has not been used for a login within 90 days. If you need a permanent token, then we recommend using [Long-lived access tokens](https://developers.home-assistant.io/docs/auth_api/#long-lived-access-token).

### Securing your login

*Make sure to choose a secure password!* At some time in the future, you will probably want to access Home Assistant from outside your local network. This means you are also exposed to random black-hats trying to do the same. Treat the password like the key to your house.

As an extra level of security, you can turn on [multi-factor authentication](https://www.home-assistant.io/docs/authentication/multi-factor-auth/).

## Adding a person to Home Assistant

If you have administrator rights, you can [add a person to Home Assistant](https://www.home-assistant.io/integrations/person/#adding-a-person-to-home-assistant) and create them a user account.

## Changing display or username

To learn how to change a display or username, refer to [setting up basic information](https://www.home-assistant.io/docs/configuration/basic/).

## Other authentication techniques

Home Assistant provides several ways to authenticate. See the [Auth providers](https://www.home-assistant.io/docs/authentication/providers/) section.

## Troubleshooting

### Authentication failures from 127.0.0.1

If you’re seeing authentication failures from `127.0.0.1` and you’re using the `nmap` device tracker, you should [exclude the Home Assistant IP](https://www.home-assistant.io/integrations/nmap_tracker#exclude) from being scanned.

### Bearer token warnings

Under the new authentication system you’ll see the following warning logged when the [legacy API password](https://www.home-assistant.io/docs/authentication/providers/#legacy-api-password) is supplied, but not configured in Home Assistant:

```txt
WARNING (MainThread) [homeassistant.components.http.auth] You need to use a bearer token to access /blah/blah from 192.0.2.4
```

If you see this, you need to add an [`api_password`](https://www.home-assistant.io/integrations/http/#api_password) to your `http:` configuration.

### Bearer token informational messages

If you see the following, then this is a message for integration developers, to tell them they need to update how they authenticate to Home Assistant. As an end user you don’t need to do anything:

```txt
INFO (MainThread) [homeassistant.components.http.auth] You need to use a bearer token to access /blah/blah from 192.0.2.4
```

### Lost owner password

If you lose the password associated with the owner account, you need to [start a new onboarding process](https://www.home-assistant.io/docs/locked_out/#to-prepare-the-system-to-start-a-new-onboarding-process).

### Error: invalid client id or redirect URL

![Screenshot of Error: invalid client id or redirect url](https://www.home-assistant.io/images/docs/authentication/error-invalid-client-id.png)

You have to use a domain name, not IP address, to remote access Home Assistant otherwise you will get `Error: invalid client id or redirect url` error on the login form. However, you can use the IP address to access Home Assistant in your home network.

This is because we only allow an IP address as a client ID when your IP address is an internal network address (such as `192.168.0.1`) or loopback address (such as `127.0.0.1`).

If you don’t have a valid domain name for your Home Assistant instance, you can modify the `hosts` file on your computer to fake one. On Linux edit the `/etc/hosts` file, and add following entry:

```text
12.34.56.78 homeassistant.home
```

Replace `12.34.56.78` with your Home Assistant’s public IP address.

This will allow you to open Home Assistant at `http://homeassistant.home:8123/`

### Stuck on loading data

Some ad blocking software, such as Wipr, also blocks WebSockets. If you’re stuck on the Loading data screen, try disabling your ad blocker.