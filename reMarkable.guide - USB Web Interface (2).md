---
title: "USB Web Interface"
source: "https://remarkable.guide/tech/usb-web-interface.html"
author:
published:
created: 2026-04-27
description: "There is an optional web interface that can be turned on that allows you upload and export files from the device. Contents: Enable the interface, API- GET http://10.11.99.1/documents/, GET http://1..."
---
There is an optional web interface that can be turned on that allows you upload and export files from the device.

## Enable the interface

See the official [Transferring files using a USB cable](https://support.remarkable.com/s/article/Transferring-files-using-a-USB-cable) article for up to date information.

1. Open the Menu from the main page.
2. Select “Settings”.
3. Select “Storage”.
4. Toggle “USB web interface” on.

## API

The USB Web Interface exposes the following API endpoints that can be used to interact with the xochitl filesystem.

### GET http://10.11.99.1/documents/

Get the document and folders list for the root folder. This will also respond to POST requests.

**Example:**

```bash
curl \
  --silent \
  http://10.11.99.1/documents/ \
| jq -r 'map({(.ID): {VissibleName,Type}}) | add'
```

### GET http://10.11.99.1/documents/{guid}

Get the documents and folders list for a specific folder. This will also respond to POST requests.

**Example:**

```bash
guid=fd2c4b2c-3849-46c3-bf2d-9c80994cc985
curl \
  --silent \
  "http://10.11.99.1/documents/$guid" \
| jq -r 'map({(.ID): {VissibleName,Type}}) | add'
```

### GET http://10.11.99.1/download/{guid}/pdf

Download the PDF for a specific document.

**Example:**

```bash
guid=fd2c4b2c-3849-46c3-bf2d-9c80994cc985
curl \
  -I "http://10.11.99.1/download/$guid/pdf"
```

### GET http://10.11.99.1/download/{guid}/rmdoc

Download the raw notebook archive for a specific document. This was added in v3.9.

**Example:**

```bash
guid=fd2c4b2c-3849-46c3-bf2d-9c80994cc985
curl \
  -I "http://10.11.99.1/download/$guid/rmdoc"
```

### POST http://10.11.99.1/upload

Upload a document to the last folder that was listed.

**Example:**

```bash
file=Get_started_with_reMarkable.pdf
curl \
  'http://10.11.99.1/upload' \
  -H 'Origin: http://10.11.99.1' \
  -H 'Accept: */*' \
  -H 'Referer: http://10.11.99.1/' \
  -H 'Connection: keep-alive' \
  -F "file=@$file;filename=$(basename "$file");type=application/pdf"
```

### GET http://10.11.99.1/log.txt

Download the xochitl log file found at `/home/root/log.txt`.

**Example:**

```bash
curl \
  --silent \
  --remote-name \
  --remote-header-name \
  'http://10.11.99.1/log.txt'
```

### GET http://10.11.99.1/thumbnail/{guid}

Download the thumbnail for a specific document (latest page opened).

**Example:**

```bash
guid=fd2c4b2c-3849-46c3-bf2d-9c80994cc985
curl \
  -I "http://10.11.99.1/thumbnail/$guid"
```

### POST 'http://10.11.99.1/search/{keyword}'

Search for documents matching a specific keyword. This endpoint is currently under development, and may not work as expected.

**Example:**

```bash
keyword="planning"
curl \
  -X POST \
  "http://10.11.99.1/search/$keyword" \
| jq -r 'map({(.ID): {VissibleName,Type}}) | add'
```

## External links

- Make the usb web interface available immediately after starting the device: [webinterface-onboot](https://github.com/rM-self-serve/webinterface-onboot)
- Make the usb web interface available over wifi: [webinterface-wifi](https://github.com/rM-self-serve/webinterface-wifi)
- Add an upload button to the usb web interface: [webinterface-upload-button](https://github.com/rM-self-serve/webinterface-upload-button)
- The usb web interface is likely using this to serve itself: [reMarkable/qtwebapp](https://github.com/reMarkable/qtwebapp)