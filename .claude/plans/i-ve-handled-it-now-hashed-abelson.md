# Jailbreak plan — iPod touch 4th gen, iOS 6.1.6

## Context

Goal is sentimental recovery: run old games that no longer exist on modern
devices. Two obstacles were reported — the device's App Store will not load, and
the Mac has no iTunes. Both are symptoms, not the problem. The problem is that a
2011 device on a 2014 OS cannot complete a modern TLS handshake and cannot be
served by current Apple tooling. Jailbreaking is the route around both: it
restores certificate trust and gives filesystem-level app installation.

An earlier pass in this session produced wrong answers from search summaries and
an unauthorized binary download. This plan is rebuilt from primary sources read
end to end, with sourcing marked per claim.

## Verified facts about this specific setup

Observed by command on this machine:

- Host OS: **macOS 12.7.6** (build 21H1320) — `sw_vers`
- Device enumerates over USB: Product ID `0x129e`, Vendor `0x05ac`, 480 Mb/s,
  serial `807f9593…` — `system_profiler SPUSBDataType`. macOS talks to it; no
  iTunes or driver install is needed on macOS for that to be true.

Read from primary documentation:

- **Aquila** jailbreaks all 32-bit devices on **iOS 4.3 – 7.1.2**, is
  **untethered**, and requires "a computer with 64-bit Windows or macOS."
  (ios.cfw.guide/installing-aquila)
- Aquila's macOS procedure is: extract zip, plug in device, **double-click
  `aquila`**, wait for "Done" and reboot. The iOS 7 pre-reboot caveat is
  explicitly scoped — *"does not apply to iOS 4.3 to 6.1.6."* (same page)
- **aquila-app** is the same jailbreak as a sideloadable IPA; jailbreak runs on
  launch, device reboots, Cydia appears. Built with **Xcode 13.4.1 on macOS
  Monterey 12.6**. (aquila-app README)
- **Legacy iOS Kit** supports **macOS 10.11+, 12.6+ recommended**; its
  "Jailbreak Device" (ramdisk) path is untethered and loses no data, **but
  requires working Home and Power buttons to enter DFU**. (LiK README;
  Jailbreaking-with-Legacy-iOS-Kit)
- Onboard SHSH blobs: iPod touch 4 is a **supported** device, but dumping
  "requires the device to be in Normal mode, **jailbroken**, and with OpenSSH
  installed." (Saving-onboard-SHSH-blobs)
- App install needs **AppSync Unified** for unsigned/cracked IPAs; signed IPAs
  do not. For iOS 5+, AppSync comes from `https://lukezgd.github.io/repo/`.
  Preferred installer is **appinst** over ideviceinstaller. (Install-IPA-AppSync;
  App-Management)
- App dumping (`Dump App as IPA`) needs jailbreak + OpenSSH; output lands in
  `saved/applications`. (App-Management)
- LiK backups use `idevicebackup2` and are **limited — they do not include
  apps**, only some app data and settings. (Data-Management)
- Certificate errors on older macOS are addressed by installing the "Signed iOS
  Bundle (iOS 5+)" from `http://tlsroot.litten.ca` **in Safari** (LiK How-to-Use).
  That host returns HTTP 200 and serves DER-encoded root CA bundles — verified
  by `curl`.

## Why Aquila is the primary route

The two candidate methods differ in where they attack, and that determines the
hardware they demand:

- **Aquila** is a userland-plus-kernel chain — its credits name a ddi race
  condition, a sandbox patch, an amfid bypass, and CVE-2014-4461 (aquila README).
  It needs the device merely booted and connected. **No DFU. No button presses.**
- **Legacy iOS Kit's ramdisk method** enters DFU to load a patched ramdisk, so it
  **hard-requires a working Home button and Power button**.

**Update (confirmed by Logan):** the Home and Power buttons work and the device
is in good physical condition. That removes the hardware objection, so the
ramdisk method is available as a genuine fallback rather than being ruled out.

Aquila still leads, on two remaining grounds: it is one double-click with no DFU
timing to get right, and its supported range (4.3–7.1.2) states this device's
version unambiguously, where Legacy iOS Kit's range carries an unenumerated
"with some exceptions." Legacy iOS Kit stays essential for everything after the
jailbreak — blobs, app install, app dumping, SSH, backups — and is now also the
documented Plan B if Aquila fails.

## Plan

**Phase 0 — before touching anything**

1. Confirm exact version at Settings → General → About → Version. This plan
   assumes 6.1.6; if it reads lower, the Aquila range still covers it.
2. Settings → General → Passcode Lock → **turn passcode off**.
3. Pull irreplaceable photos/videos off with **Image Capture** (built into
   macOS, needs no iTunes). Note that LiK backups exclude apps, so this is the
   step that actually protects personal media.

**Phase 1 — jailbreak with Aquila**

4. Download Aquila for macOS from its releases; **extract the zip** first.
5. Plug in the iPod, double-click `aquila`, leave it alone until it reports Done
   and the device reboots.
6. Success condition: **Cydia on the home screen.**
- *Fallback if Aquila fails:* Legacy iOS Kit → `Jailbreak Device` (ramdisk).
  Buttons are confirmed working, so DFU entry is available. Set LiK up per
  Phase 3 step 10 first.

**Phase 2 — restore trust, then capabilities**

7. In Cydia, install **OpenSSH** (needed by every later step) and change the
   default root password from `alpine`. LiK's SSH access uses port `6414`.
8. Install updated root CAs so Cydia and the App Store can negotiate TLS —
   `http://tlsroot.litten.ca`, "Signed iOS Bundle (iOS 5+)", opened in **Safari
   on the iPod**.
9. Add AppSync Unified from `https://lukezgd.github.io/repo/`.

**Phase 3 — Legacy iOS Kit for everything else**

10. Set up LiK:
    - `xcode-select --install`
    - `git clone --filter=blob:none https://github.com/LukeZGD/Legacy-iOS-Kit`
      (shallow `--depth 1` clones are explicitly unsupported)
    - drag `restore.sh` into Terminal, Return; first run pulls dependencies
11. **Save onboard SHSH blobs** now — this is only possible post-jailbreak with
    OpenSSH present, which is why it is not step 1. Needs the matching IPSW from
    ipsw.me.
12. Retry the App Store on the device. Whatever it will still serve from the
    purchase history is free and legitimate.
13. For anything it won't serve: `App Management → Install IPA (appinst)`.
14. Once games are on the device, `App Management → Dump App as IPA` to archive
    them properly into `saved/applications`.

## Verification

- **Jailbreak:** Cydia present and opens; device survives a reboot with Cydia
  still working (this is what "untethered" should mean here).
- **TLS:** Cydia refreshes sources without SSL errors; App Store renders.
- **SSH:** `Data Management → Connect to SSH` succeeds on port 6414.
- **Install path:** one known-good IPA installs and launches.
- **Blobs:** a saved blob file exists for 6.1.6.
- **Rollback:** if the jailbreak fails, the device is recoverable by restoring
  to 6.1.6 — the only signed version it can take.

## Known unknowns — not established, do not assume

- Legacy iOS Kit's README says jailbreak support runs 3.1.3–9.3.4 "with some
  exceptions" and never enumerates them. No document was found naming iPod
  touch 4 + 6.1.6 explicitly for the ramdisk path. Aquila's stated range is
  unambiguous; that asymmetry is a reason to prefer it.
- theapplewiki is behind a Cloudflare challenge and was not read. Any claim
  about the A4 bootrom or limera1n is therefore **unsourced here** and is
  omitted from this plan deliberately.
- Whether installing the CA bundle actually revives this device's App Store is
  untested — plausible from the failure mode, not verified.
- Whether the specific games wanted still exist in the purchase history, or
  anywhere retrievable, is unknown until Phase 2 completes.
- Battery condition. Old cells fail abruptly under sustained USB load.

## Explicitly out of scope

No downloads, no execution, nothing written to the device without a go-ahead per
step. The archive.org p0sixspwn binary referenced earlier in the session is not
part of this plan and should not be used — Aquila is maintained, documented, and
covers the same device and version.
