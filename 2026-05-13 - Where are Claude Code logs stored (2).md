---
title: "Where are Claude Code logs stored?"
source: "https://claude-dev.tools/docs/log-locations"
author:
  - "[[matt1398]]"
published: 2026-05-13
created: 2026-06-11
description: "Claude Code writes JSONL session logs to ~/.claude/ — the hidden folder inside your home directory. The path is the same on macOS and Linux; on Windows it's %USERPROFILE%\.claude\."
---
Claude Code writes JSONL session logs to ~/.claude/ — the hidden folder inside your home directory. The path is the same on macOS and Linux; on Windows it's %USERPROFILE%\\.claude\\.

**Short answer.** Claude Code stores all of its logs and session transcripts in a hidden `.claude` folder inside your home directory. On macOS and Linux that is `~/.claude/`. On Windows that is `%USERPROFILE%\.claude\` — for example `C:\Users\<you>\.claude\`.

These logs exist whether or not you use claude-devtools. The app simply reads them.

## macOS — ~/.claude/ location

On macOS the Claude Code log file location is:

```
/Users/<you>/.claude/
```

Replace `<you>` with your account name. The folder is hidden by default in Finder; press `Cmd + Shift + .` to toggle hidden files, or open Terminal and run `open ~/.claude`.

## Linux — ~/.claude/ location

On Linux the Claude Code logs location is:

```
/home/<you>/.claude/
```

If you run Claude Code as a different user (e.g. inside a Docker container or under a system service), `HOME` resolves to that user's home directory. The `.claude` folder is hidden; `ls -la ~` shows it.

## Windows — %USERPROFILE%\\.claude\\ location

On Windows, Claude Code logs are stored in your user profile directory:

```
C:\Users\<you>\.claude\
```

Or with the environment variable:

```
%USERPROFILE%\.claude\
```

The folder is hidden — in File Explorer, enable **View → Show → Hidden items**, or paste the path directly into the address bar. Both PowerShell (`$env:USERPROFILE\.claude`) and CMD (`%USERPROFILE%\.claude`) resolve to the same location.

This applies to Claude Code installed via the CLI, the Claude Code VS Code / JetBrains extension, and the Claude Desktop app's coding integrations — all of them write to the same Windows location.

## What's inside ~/.claude/

The directory contains raw JSONL session transcripts — one file per session — along with project metadata, configuration, and cached state.

The `projects/` subdirectory contains one folder per Claude Code project; each folder holds the JSONL session transcripts for that project. Folder names are URL-encoded versions of the absolute project path on disk, so `/Users/you/code/my-app` becomes a directory like `-Users-you-code-my-app`.

For a field-by-field reference of the JSONL session format, see [the JSONL transcript anatomy guide](https://claude-dev.tools/docs/jsonl-format).

## Remote machines, Docker, and CI

If you're running Claude Code in Docker or on a remote machine, the logs live wherever `HOME` resolves inside that environment. claude-devtools' standalone mode supports overriding the path with the `CLAUDE_ROOT` environment variable, which is also useful when mounting `~/.claude` at a non-default path inside a container.

For inspecting sessions that ran on a CI machine, cloud instance, or team server, see [SSH remote sessions](https://claude-dev.tools/docs/ssh-remote).

## Related

- [Anatomy of a Claude Code JSONL transcript](https://claude-dev.tools/docs/jsonl-format)
- [Reading Claude Code session transcripts](https://claude-dev.tools/docs/transcripts)
- [Inspecting remote sessions over SSH](https://claude-dev.tools/docs/ssh-remote)

FAQ · 06

## Questions,answered.

Common questions about claude-devtools, session transcripts, and Claude Code logs on disk.

1. Claude Code logs are stored in the hidden ~/.claude/ folder inside your home directory. On macOS that is /Users/<you>/.claude/, on Linux /home/<you>/.claude/, and on Windows C:\\Users\\<you>\\.claude\\ (also reachable as %USERPROFILE%\\.claude\\).
2. On Windows, the Claude Code log file location is %USERPROFILE%\\.claude\\ — typically C:\\Users\\<you>\\.claude\\. The folder is hidden by default; enable 'Show hidden items' in File Explorer or paste the path directly into the address bar. The same location is used by the CLI, the VS Code extension, and the Claude Desktop coding integrations.
3. Claude Code session files are saved as JSONL transcripts under ~/.claude/projects/<encoded-project-path>/<session-id>.jsonl. Each project gets its own folder; each session is a separate JSONL file inside that folder.
4. On macOS, Claude Code sessions are stored at /Users/<you>/.claude/projects/. The folder is hidden in Finder by default — press Cmd+Shift+. to reveal hidden folders, or run \`open ~/.claude\` from Terminal.
5. The raw JSONL files in ~/.claude/ are readable in any text editor or with \`jq\`, but they are noisy — escaped JSON with system prompts and metadata. claude-devtools parses them into a structured conversation viewer with per-tool renderers, token attribution, and search.
6. Yes. The Claude Code CLI, the VS Code / JetBrains extensions, and the Claude Desktop app's coding features all write session logs to the same ~/.claude/ directory in the user's home folder.[Inspecting remote sessions over SSH](https://claude-dev.tools/docs/ssh-remote)

[

claude-devtools reads ~/.ssh/config for host aliases, opens SFTP to remote ~/.claude/, and isolates each host's state. Useful for CI machines, cloud instances, and team servers.

](https://claude-dev.tools/docs/ssh-remote)[

4 ways I cut Claude Code token usage after actually seeing my context

After watching my own Claude Code sessions in claude-devtools, I found four token-drain patterns I never would have caught from the terminal — heavy MCPs, lazy @-mentions, probabilistic skills, and monolithic CLAUDE.md files.

](https://claude-dev.tools/docs/token-saving-lessons)