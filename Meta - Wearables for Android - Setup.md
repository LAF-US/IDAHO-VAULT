---
title: "Setup"
source: "https://wearables.developer.meta.com/docs/develop/dat/getting-started-toolkit/#sdk-for-android-setup"
author:
published:
created: 2026-06-18
description: "This getting started topic provides guidance on how to start using the Meta Wearables Device Access Toolkit, including supported platforms, hardware requirements, mobile device setup, and setting up your developer environment for both iOS and Android."
---
Updated: Jun 5, 2026

## Overview

The Wearables Device Access Toolkit supports iOS and Android mobile platforms, with the same OS version requirements as the Meta AI app (iOS 15.2+ and Android 10+).

Xcode 14.0+ is supported for iOS. Android Studio Flamingo or newer is supported for Android.

## Hardware requirements

Currently, the SDK supports the Ray-Ban Meta (Gen 1 and Gen 2), Ray-Ban Meta Optics, and Meta Ray-Ban Display glasses. You can test with a simulated device using [Mock Device Kit](https://wearables.developer.meta.com/docs/develop/dat/mock-device-kit/), or directly with a device. Detailed version support of the Meta AI app and glasses firmware is located in the [Version Dependencies](https://wearables.developer.meta.com/docs/develop/dat/version-dependencies/) page.

## Setting up your glasses

1. Ensure your versions of the Meta AI app and glasses software are in line with the version dependencies [outlined here](https://wearables.developer.meta.com/docs/develop/dat/version-dependencies). Follow the instructions below to verify your current glasses version.
2. Connect your glasses to the Meta AI app.
3. Enable [developer mode](https://wearables.developer.meta.com/docs/develop/dat/getting-started-toolkit#enable-developer-mode-in-the-meta-ai-app) in the Meta AI app. Developer mode allows your unpublished app to register and interact with your AI glasses without the need to submit it for publishing review. Your app appears under **Meta AI settings** > **App connections** > **Developer mode apps**. It also enables testing via invite-only [release channels](https://wearables.developer.meta.com/docs/develop/dat/set-up-release-channels).

### Verify glasses software version

1. In the Meta AI app, go to the Devices tab (the glasses icon at the bottom of the app), and select your device.
2. Tap the gear icon to open **Device settings**.
3. Tap **General** > **About** > **Version**.
4. You should have the minimum supported version or above installed on your glasses, as outlined [here](https://wearables.developer.meta.com/docs/develop/dat/version-dependencies/).
5. If your version is below minimum support requirements, update your glasses software.

### Enable developer mode in the Meta AI app

1. On your iOS or Android device, select **Settings** > **App Info**, and then tap the **App version** number five times to display the toggle for developer mode.
2. Select the toggle to enable **Developer Mode**.
3. Click **Enable** to confirm.

**iOS**

![Image of enabling developer mode on an iOS device](https://scontent.fboi1-1.fna.fbcdn.net/v/t39.2365-6/559205454_1850889009172150_8783518501745032329_n.png?_nc_cat=109&ccb=1-7&_nc_sid=e280be&_nc_ohc=lENAw7ANPSQQ7kNvwETP1Kr&_nc_oc=Adq2a7uJ_WPfEeVdgjAAFawOmJyuQiPV9f7Pwas0P0a6Wa7iWU3EXp5JZCVMLd_aYXc&_nc_zt=14&_nc_ht=scontent.fboi1-1.fna&_nc_gid=jmu52KmTpMmcRSaS40Eflw&_nc_ss=7b289&oh=00_Af9IOA-P8U5rD3aNGHIiPqCnoF6JwD_dgUpFoeptlz6pGg&oe=6A4E7D0D)

**Android**

![Image of enabling developer mode on an android device](https://scontent.fboi1-1.fna.fbcdn.net/v/t39.2365-6/560041248_1850888972505487_6549169074798622417_n.png?_nc_cat=110&ccb=1-7&_nc_sid=e280be&_nc_ohc=qyl2wQ1XwqkQ7kNvwE0uavl&_nc_oc=AdpTrlbEkWaO8a6H6imQANd2DetgK_MCt-QKqOQLG9CPBDhkNdYNCDAI36xvVRSFCrI&_nc_zt=14&_nc_ht=scontent.fboi1-1.fna&_nc_gid=jmu52KmTpMmcRSaS40Eflw&_nc_ss=7b289&oh=00_Af8g069In7fCwXcEDYoby9ChowMJ8GoL1ZAOmYSCg5K9VA&oe=6A4E7FEA)

English (US)