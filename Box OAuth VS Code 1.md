---
updated: 2026-03-24
status: draft
source: commit
related:
- '127'
- '2026-03-24'
- URI
authority: LOGAN
---
# Box OAuth in VS Code (manual client registration)

Error seen in VS Code:
> “Dynamic Client Registration not supported. The authorization server ‘https://api.box.com/’ does not support automatic client registration. Do you want to proceed by manually providing a client registration (Client ID)? Note: When registering your OAuth application, make sure to include these redirect URIs: [...]”

Resolution: Box does not support Dynamic Client Registration, so VS Code must use a manually registered OAuth app.

Steps:
1. In the Box Developer Console, create an OAuth 2.0 “Custom App.”
2. Add the VS Code redirect URIs to the app:
   - `http://127.0.0.1:33418`
   - `https://vscode.dev/redirect`
3. Copy the issued Client ID (and Client Secret if prompted) from Box.
4. When VS Code shows the prompt, choose to provide the client registration and paste the Client ID (and Secret if required).

Notes:
- Keep the Client Secret out of the repo and out of version control.
- If the port changes in a future VS Code build, add that localhost URI to the Box app as well.
