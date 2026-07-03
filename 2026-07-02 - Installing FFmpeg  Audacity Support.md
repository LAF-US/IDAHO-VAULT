---
title: "Installing FFmpeg | Audacity Support"
source: "https://support.audacityteam.org/basics/installing-ffmpeg"
author:
published: 2026-07-02
created: 2026-07-03
description: "FFmpeg allows you import/export additional audio file formats into/from Audacity"
---
Due to patent restrictions, FFmpeg cannot be distributed with Audacity itself. However, FFmpeg is required to import and export a variety of audio formats, including M4A and WMA.

**Note:** In previous versions of Audacity, LAME was required to export MP3 files. It is now included with Audacity by default on Windows and macOS. Make sure you are using the latest version of Audacity if you're getting any LAME errors.

You can download and install FFmpeg as follows:

<iframe src="https://iframely.net/2dy2hRe" allowfullscreen="" allow="accelerometer *; clipboard-write *; encrypted-media *; gyroscope *; picture-in-picture *; web-share *;"></iframe>

#### Recommended installer

1. Download the FFmpeg installer from [https://lame.buanzo.org/ffmpeg.php](https://lame.buanzo.org/ffmpeg.php) For most computers, the 64-bit Windows version is correct. For native Windows ARM build go to [https://github.com/tordona/ffmpeg-win-arm64](https://github.com/tordona/ffmpeg-win-arm64).
2. Run the installer. You can ignore the "unknown publisher" warning.
3. Read and accept the license
4. Select the location to install FFmpeg. By default FFmpeg will be installed into **C:\\Program Files\\FFmpeg for Audacity**
5. Finish the installation
6. Restart Audacity

Audacity should now automatically detect FFmpeg and allow you to use it.

#### Installing using WinGet

FFmpeg for Audacity is also available on WinGet:

```
winget install --id=Buanzo.FFmpegforAudacity  -e
```

#### Other FFMPEG builds

**Note:** Audacity does not support work-in-progress (i.e., master branch) builds of FFmpeg. Choose the FFmpeg version that matches your Audacity release.

If you prefer a manual installation of FFmpeg you can download a ZIP file from a different source:

- [https://github.com/BtbN/FFmpeg-Builds/releases](https://github.com/BtbN/FFmpeg-Builds/releases)
- [https://www.gyan.dev/ffmpeg/builds/#release-builds](https://www.gyan.dev/ffmpeg/builds/#release-builds)
- Windows ARM64: [https://github.com/tordona/ffmpeg-win-arm64](https://github.com/tordona/ffmpeg-win-arm64)
- Or by compiling it from source as described here: [https://trac.ffmpeg.org/wiki/CompilationGuide](https://trac.ffmpeg.org/wiki/CompilationGuide)

**Note:**

- Not all FFmpeg versions are supported on all releases.
	- Audacity prior 3.1 only supports avformat-55.dll.
	- Audacity 3.1 and later supports avformat-55.dll, avformat-57.dll and avformat-58.dll.
	- Audacity 3.2 and later also supports avformat-59.dll.
	- Audacity 3.3 and later also supports avformat-60.dll.
	- Audacity 3.5 and later also supports avformat-61.dll.
	- Audacity 3.7 and later also supports avformat-62.dll.
	- You can check which dll is in which FFmpeg release [here](https://ffmpeg.org/download.html#releases).
- Make sure you download full FFmpeg copies, not just the avformat-\*.dll's individually. Further, make sure to download or build the **shared** versions as only those contain.dll's.
- Different versions of FFmpeg may have different codecs enabled in them. In particular, AMR (narrowband) is not featured in the recommended installer.

#### Manual installation

If you have installed FFmpeg from a different source, or installed it in a different location, you'll need to tell Audacity where to find it. To do this:

1. Go to **Edit > Preferences > Libraries**
2. Click on the **Locate...** button.
3. **If the following message appears**, Audacity has automatically identified FFmpeg:
	![](https://support.audacityteam.org/~gitbook/image?url=https%3A%2F%2F2387260374-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F-MhmBVzGzh8SctWQ6jPR%252Fuploads%252FrcSz9YFN39uFg0qnNQZR%252Fimage.png%3Falt%3Dmedia%26token%3D5658bf67-32b6-4175-b412-8010320ca5e4&width=768&dpr=3&quality=100&sign=7204efe4&sv=2)
	You can click **No** as Audacity already knows where to find FFmpeg.
	If this message **does not appear**, proceed with the next steps.
4. In this dialog window, click **Browse...** to locate the avformat-\*.dll from the FFmpeg folder you downloaded/installed elsewhere
	![](https://support.audacityteam.org/~gitbook/image?url=https%3A%2F%2F2387260374-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F-MhmBVzGzh8SctWQ6jPR%252Fuploads%252FrE2im0sfVkoWPopRtk6M%252Fimage.png%3Falt%3Dmedia%26token%3D2a7b0a9f-326b-4ddd-bf6b-faf422f0257f&width=768&dpr=3&quality=100&sign=fa380606&sv=2)
5. Once you've found it, click **Open**, then **OK**, then **OK** again to close the preferences.

Last updated