Test Obsidian MCP wiring -- CODEX DESKTOP APP



IDAHO-VAULT ' main'



\---



> Obsidian is running locally with the MCP Tools community plugin. Please test it and ensure everything is wired up correctly!





Worked for 35m 16s

CODEX COMPLETE: \[\[Obsidian MCP]] is wired and smoke-tested.



I found and fixed the main break: \[\[Claude Desktop]]’s obsidian-mcp-tools entry had a stale OBSIDIAN\_API\_KEY. I updated it to match the current \[\[Obsidian]] \[\[Local REST API]] key, backed up the old config at C:\\Users\\loganf\\AppData\\Roaming\\Claude\\claude\_desktop\_config.json.bak-2026-05-17T08-12-26-293Z, and also registered the same MCP server in Codex’s global MCP config.



Verified green:



\[\[Obsidian Local REST API]] is listening on https://127.0.0.1:27124/.

mcp-tools is loaded as a REST API extension.

MCP server initializes as obsidian-mcp-tools and exposes 18 tools.

End-to-end MCP call get\_vault\_file successfully read CONSTITUTION.md.

Old stale mcp-server.exe helper processes were stopped so hosts will spawn fresh ones with the corrected key.

Only caveat: optional prompts/list returns 404 because there’s no Prompts/ vault path, and smart semantic search did not return a clean smoke result. Core vault file/search tooling is wired; semantic search may need Smart Connections/index attention separately.

