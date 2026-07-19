---
title: "Get Started with the Shade Python SDK | Developers"
source: "https://academy.shade.inc/developers"
author:
published: 2026-02-27
created: 2026-04-20
description: "Easily manage and interact with your data in Shade via our Python SDK"
date created: Monday, April 20th 2026, 11:59:52 am
date modified: Monday, April 20th 2026, 12:44:55 pm
---

Shade offers a full-featured python SDK that enables you to access any part of your workspace including files, metadata, members, searches, and more.

### Installing the Shade Python SDK

Our SDK supports Python 3.8+. Once you have successfully installed Python on your machine, you can install below:

```
pip install shade-python-sdk
```

### Authenticating with the Python SDK

You can obtain an API key for the Shade Python SDK from your workspace and generating a new key.

Please keep in mind that this is a secret key and should not be shared publically or stored in a public repository.

![](https://academy.shade.inc/~gitbook/image?url=https%3A%2F%2F2149326901-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F78QKMeD8RCfROVEmgJMO%252Fuploads%252FjcCy3xf0wHIzeACc9Qc3%252FScreenshot%25202025-02-12%2520at%25203.52.23%25E2%2580%25AFPM.png%3Falt%3Dmedia%26token%3D3fb3bd6d-2ccb-4630-ae0e-12a934e27f36&width=768&dpr=3&quality=100&sign=568e4763&sv=2)

You can access your API Keys by going to Settings > API Keys

### Initializing Shade

You can easily initialize the Shade SDK by initializing a Shade object. This will authenticate and authorize as your user - whatever you have access to, the object will have access to.

```
API_KEY = 'sk....'
REMOTE_URL = 'https://api.shade.inc'
shade = Shade(remote_url=REMOTE_URL, api_key=API_KEY)
```

[NextCommon Patterns](https://academy.shade.inc/developers/common-patterns)

Last updated