---
title: "Shell Environment Loading | Knowledge Base"
source: "https://youtrack.jetbrains.com/articles/SUPPORT-A-1727/Shell-Environment-Loading"
author:
published:
created: 2026-06-18
description: "Shell Environment Loading"
---
On **macOS**, applications launched via a GUI (such as **Finder**, **Dock**, or **Spotlight**) inherit a relatively empty environment. Unfortunately, there’s no reliable or consistent way to modify this environment.

This has led to [complaints](https://youtrack.jetbrains.com/issue/IJPL-11674/On-Mac-OS-X-IDE-doesnt-pick-up-shell-environment-when-started-from-Dock-Spotlight) where tools that work fine in a terminal do **not** work when launched from the IDE. To address this, JetBrains IDEs attempt to **load the shell environment** on startup.

To do this, the IDE starts a background shell process and instructs it to run a helper script. Since version **2021.2**, the IDE shows a [notification](https://youtrack.jetbrains.com/issue/IDEA-263845) if this environment loading fails.

---

### Why Shell environment loading fails

The most common cause is that a **shell initialization script** (e.g., `.bashrc`, `.zshrc`) tries to **interact with a terminal**.

The IDE uses the `-i` flag to launch the shell in **interactive mode**, because most environment modifications are placed in user `*rc` files — which typically assume they’re running in a terminal.

However, the shell launched by the IDE **does not have access to a terminal**, which can result in:

- Errors
- Hanging or timeouts (IDE has 20 second timeout to get shell environment)  
	(For more detail, check the [IDE log](https://youtrack.jetbrains.com/articles/SUPPORT-A-1718) for the line: **"can't get shell environment"**)

---

### How to fix it

To avoid loading failures (and remove the notification), modify your shell script so it **skips terminal interactions** when launched by the IDE.

A common approach is to wrap such logic in a conditional block that checks for the IDE's environment variable:

```bash
if [ -z "$INTELLIJ_ENVIRONMENT_READER" ]; then
  # Launched by the IDE’s environment reader — skip interactive shell setup.
  return
fi
```

This ensures the script behaves correctly when run by the IDE’s background shell, while continuing to work normally in the terminal.

The IDE has a 20-second timeout for running the helper script that retrieves the shell environment, and this timeout cannot be changed.

If any of your script parts take longer than 20 seconds, wrap those calls in a conditional block as well.

---

### General Troubleshooting Steps:

1. Open a terminal and run `echo $SHELL`, or use any method to find your default shell.
2. Run `your_shell -i` (e.g., `/bin/zsh -i`, `/bin/bash -i`) in the terminal.
3. If it produces any errors or it takes too long to complete or waits for user input, check your shell initialization files and resolve these issues accordingly.

### Additional Troubleshooting Steps for macOS

1. In the IDE main menu, click `Help | Show Log in Finder`, then open idea.log in a text editor.
2. Search for `EnvironmentUtil - loading shell env` to locate a recent log entry similar to this:

> 2025-10-28 22:14:20,500 \[ 19\] INFO - #c.i.u.EnvironmentUtil - loading shell env: /path\_to\_your\_shell -l -c '/path/to/IDE\_Name.app/Contents/bin/printenv' > '/some\_temp\_path//ij-shell-env-data.tmp'

3. If you see an error message like “can’t get shell environment” near that log entry, try to fix it.
4. Copy the command part `/path_to_your_shell -l -c '/path/to/IDE_Name.app/Contents/bin/printenv'` from your log. Add a backslash (`\`) before each space inside your actual `'/path/to/IDE_Name.app/Contents/bin/printenv'` to escape the spaces.
5. Open the Terminal app and run that command. If it produces any errors or it takes too long to complete or waits for user input, check your shell initialization files and resolve these issues accordingly.

### Where to Find Shell Initialization Scripts

You can usually find your shell initialization script here:

- `~/.zshrc` or `~/.zshenv` — if you’re using the default macOS shell (Zsh)
- `~/.bash_profile` or `~/.bashrc` — if you’re using Bash
- Scripts under `~/.config/fish` — if you’re using the Fish shell

If you can’t find any of these files, check your home directory (~) for similar configuration files.