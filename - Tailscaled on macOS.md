---
title: "- Tailscaled on macOS"
source: "https://github.com/tailscale/tailscale/wiki/Tailscaled-on-macOS"
author:
published:
created: 2026-07-03
description: "The easiest, most secure way to use WireGuard and 2FA. - Tailscaled on macOS · tailscale/tailscale Wiki"
aliases:
  - "- Tailscaled on macOS"
linter-yaml-title-alias: "- Tailscaled on macOS"
date created: Friday, July 3rd 2026, 2:58:41 am
date modified: Friday, July 3rd 2026, 7:58:18 pm
---

# - Tailscaled on macOS

There are [multiple ways to use Tailscale on macOS](https://tailscale.com/kb/1065/macos-variants/). The recommended way is to always install the **Standalone variant**, available for [download](https://tailscale.com/download/) from the Tailscale website.

This page is about how to use the open source, non-GUI `tailscaled` and `tailscale` binaries. This is only recommended for advanced users.

## Requirements

## Install Go

Install Go 1.25 (or whatever the most recently released Go version is) from [https://golang.org/dl/](https://golang.org/dl/) or Homebrew, etc. Tailscale always requires the most recent Go version and doesn't support older ones.

## Compile Tailscale

Run:

```
go install tailscale.com/cmd/tailscale{,d}@main
```

That'll put the binaries in `$(go env GOPATH)/bin`, so likely `$HOME/go/bin`. You can copy or symlink those binaries into your `$PATH`, or make your `$PATH` include that directory.

You can also compile from a specific release version. For example to build from the source code used for Tailscale 1.38.2, use:

```
go install tailscale.com/cmd/tailscale{,d}@v1.38.2
```

### Run the tailscaled (daemon)

```
sudo $HOME/go/bin/tailscaled
```

Or, to run it in the background under launchd so it starts at system boot:

```
sudo $HOME/go/bin/tailscaled install-system-daemon
```

That copies the binary to `/usr/local/bin` and installs a plist in `/Library/LaunchDaemons/com.tailscale.tailscaled.plist` and starts `com.tailscale.tailscaled`.

(to stop/uninstall, use: `sudo tailscaled uninstall-system-daemon`)

### Use the tailscale CLI tool

See [https://tailscale.com/kb/1080/cli](https://tailscale.com/kb/1080/cli) (but ignore the `/Applications/Tailscale.app/Contents/MacOS/Tailscale` part; that's the path to the GUI's CLI)

```
tailscale up       # (any optional arguments)
tailscale status
```

Enjoy.

## Comparison to GUI version

Compared to the GUI version of Tailscale, running `tailscaled` instead has the following differences:

- `tailscaled` on macOS is less tested.
- the App Store version uses the Apple Network Extension API; `tailscaled` uses the `/dev/utun` TUN interface
- MagicDNS works, but you need to set `100.100.100.100` as your DNS server yourself. It doesn't change your DNS config.
- `tailscaled` can run at system boot before any user has logged in (e.g. letting you VNC to your computer after a power outage)
- is fully open source (Tailscale GUI parts aren't open source on non-free operating systems)

Refer to the [comparison](https://tailscale.com/kb/1065/macos-variants) available in the Tailscale KB for more details.

## Installing tailscaled from homebrew

If you don't want to build it yourself, you can also use homebrew:

```
$ brew install --formula tailscale
$ sudo brew services start tailscale
$ sudo tailscale up
$ sudo tailscale status
```

See [https://github.com/tailscale/tailscale/issues/10558](https://github.com/tailscale/tailscale/issues/10558) for background. Thanks to @DilumAluthge!
