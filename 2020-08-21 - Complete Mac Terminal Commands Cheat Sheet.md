---
title: "Complete Mac Terminal Commands Cheat Sheet"
source: "https://www.geeksforgeeks.org/linux-unix/complete-mac-terminal-commands-cheat-sheet/"
author:
  - "[[GeeksforGeeks]]"
published: 2020-08-21
created: 2026-04-25
description: "Your All-in-One Learning Portal: GeeksforGeeks is a comprehensive educational platform that empowers learners across domains-spanning computer science and programming, school education, upskilling, commerce, software tools, competitive exams, and more."
---
The ****Mac Terminal**** is a powerful tool that allows you to interact with your macOS system through commands, giving you more control over your device than ever before. Whether you're a ****beginner exploring basic commands**** or an advanced user looking to streamline tasks, mastering ****Mac Terminal commands**** can significantly increase your productivity. From managing files and directories to troubleshooting your system or customizing settings, the Terminal opens up a world of possibilities beyond the standard macOS interface.

> Have you ever searched for ways to ****navigate macOS faster****, ****fix errors****, or ****automate tasks****? Knowing the right Terminal commands can help you perform these actions efficiently.

In this comprehensive ****Mac Terminal commands cheat sheet****, we’ve compiled essential commands for ****file management****, ****networking****, ****system diagnostics****, and more, tailored to meet your needs. Whether you're an IT professional, developer, or casual user, this cheat sheet will make using the Terminal simpler and more effective.

## Shortcuts Key For Mac Terminal

Before moving toward the [Mac Terminal](https://www.geeksforgeeks.org/techtips/how-to-open-the-terminal-on-mac/) commands, let's know some shortcut keys to access the Mac Terminal. These key combinations help you to increase your work efficiency.

### Mac Terminal Keyboard Shortcuts

| ****Shortcut**** | ****Description**** |
| --- | --- |
| `Command + T` | Open a new Terminal tab. |
| `Command + N` | Open a new Terminal window. |
| `Command + W` | Close the current Terminal tab or window. |
| `Control + C` | Cancel the current command or process. |
| `Control + D` | Exit the current session or close the Terminal window. |
| `Control + Z` | Pause the current process and send it to the background. |
| `Command + K` | Clear the Terminal screen. |
| `Control + L` | Clear the screen (similar to `Command + K`). |
| `Command + Arrow Up` | Scroll up through previous commands in the history. |
| `Command + Arrow Down` | Scroll down through the command history. |
| `Control + A` | Move the cursor to the beginning of the line. |
| `Control + E` | Move the cursor to the end of the line. |
| `Control + U` | Delete everything from the cursor to the beginning of the line. |
| `Control + K` | Delete everything from the cursor to the end of the line. |
| `Control + W` | Delete the word before the cursor. |
| `Control + Y` | Paste the last deleted text. |
| `Control + R` | Search the command history. |
| `Control + S` | Resume a paused process (if it was paused using `Control + Z`). |
| `Control + C` | Interrupt a running process. |
| `Option + Left Arrow` | Move the cursor one word left. |
| `Option + Right Arrow` | Move the cursor one word right. |
| `Command + Shift + G` | Go to a specific directory by entering its path. |
| `Tab` | Auto-complete file or directory name. |

## Complete Mac Terminal Commands

In this section, you will get a complete table for Mac Terminal commands, we will start with the basics Mac terminal commands to advance Mac terminal commands like " ****Network,**** [****Homebrew****](https://www.geeksforgeeks.org/installation-guide/homebrew-installation-on-macos/)****, Environment Variable or Path,**** and more."

### Basics Mac Terminal Commands

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| **`**/**`** ****(Forward Slash)**** | Represents the root directory in the file system. | `/` |
| **`**.**`** ****(Single Period)**** | Refers to the current directory in which you're working. | `.` |
| **`**..**`** ****(Double Period)**** | Refers to the parent directory (one level up from the current directory). | `..` |
| **`**~**`** ****(Tilde)**** | Represents the home directory of the current user. | `~` |
| **`**sudo [command]**`** | Executes a command with elevated (super user) privileges. | `sudo rm -rf /path/to/folder` |
| **`**nano [file]**`** | Opens the ****Nano**** text editor to create or edit a file directly in the terminal. | `nano myfile.txt` |
| **`**open [file]**`** | Opens a specified file with the default application associated with its type. | `open myfile.txt` |

### Mac Terminal Command for Change Directory

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| **`**cd**`** | Navigate to the home directory | `cd` |
| **`**cd [folder]**`** | Change to a specific directory (e.g., `Documents`, `Downloads`) | `cd Documents` |
| **`**cd ~**`** | Go to the home directory (shortcut for the user's home directory) | `cd ~` |
| **`**cd /**`** | Navigate to the root directory of the file system | `cd /` |
| **`**cd -**`** | Go back to the previous directory you were last working in | `cd -` |
| **`**pwd**`** | Print the current working directory | `pwd` |
| **`**cd..**`** | Move up one level to the parent directory | `cd..` |
| **`**cd../..**`** | Move up two levels in the directory structure | `cd../..` |

### List Directory Contents Commands

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| **`**ls**`** | Lists all files and subdirectories in the current directory. | `ls` |
| `ls -C` | Displays the contents of the directory in a multi-column format. | `ls -C` |
| `ls -a` | Shows all entries in the directory, including hidden files (those starting with a period). | `ls -a` |
| `ls -1` | Lists files and directories, one entry per line. | `ls -1` |
| `ls -F` | Adds special symbols: a `/` after directories, a `*` after executable files, and an `@` after symlinks. | `ls -F` |
| `ls -S` | Sorts files and directories by size, with the largest listed first. | `ls -S` |
| `ls -l` | Lists files in long format, including file permissions, owner, group, size, and modification date. | `ls -l` |
| `ls -l /` | Displays a detailed list of files starting from the root directory, including symbolic links. | `ls -l /` |
| `ls -lt` | Lists files in long format, sorted by modification time (newest first). | `ls -lt` |
| `ls -lh` | Displays file sizes in human-readable format (KB, MB, GB, etc.) along with other detailed information. | `ls -lh` |
| `ls -lo` | Lists files with detailed information, including file size, owner, and flags. | `ls -lo` |
| `ls -la` | Shows a detailed list of all files, including hidden files (those starting with a period). | `ls -la` |

### Mac Terminal Commands for File Size and Disk Space

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| `du` | Displays the disk usage of each subdirectory and its contents | `du` |
| `du -sh [folder]` | Shows a human-readable output of the total size of all files in a specified directory | `du -sh /Documents` |
| `du -s` | Shows the total disk usage for the specified files or directories | `du -s /Users/YourUsername` |
| \`du -sk\* | sort -nr\` | Lists all files and folders with their sizes, including subfolders, sorted by size |
| `df -h` | Displays the available free disk space on your system in a human-readable format | `df -h` |
| `df -H` | Displays the free disk space in powers of 1,000 instead of 1,024 | `df -H` |

### File and Directory Management Commands

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| `mkdir <dir>` | Creates a new directory with the specified name. | `mkdir Projects` |
| `mkdir -p <dir>/<dir>` | Creates nested directories in a single command. | `mkdir -p Work/2023/Reports` |
| `mkdir <dir1> <dir2> <dir3>` | Creates multiple directories at once. | `mkdir Folder1 Folder2 Folder3` |
| `mkdir "<dir>"` | Creates a folder with spaces in its name. | `mkdir "My New Folder"` |
| `rmdir <dir>` | Deletes an empty directory. | `rmdir OldFolder` |
| `rm -R <dir>` | Removes a directory and all of its contents. | `rm -R ProjectFolder` |
| `touch <file>` | Creates a new, empty file without any extension. | `touch newfile.txt` |
| `cp <file> <dir>` | Copies a file to a specified directory. | `cp file.txt /Documents/` |
| `cp <file> <newfile>` | Copies a file to the current directory and renames it. | `cp file.txt newfile.txt` |
| `cp <file>~/<dir>/<newfile>` | Copies a file to a specified folder and renames it during the process. | `cp report.txt ~/Documents/Reports/summary.txt` |
| `cp -R <dir> <"new dir">` | Copies an entire directory, including its contents, to a new location. | `cp -R folder1 "New Folder"` |
| `cp -i <file><dir>` | Prompts you for confirmation before overwriting a file during copy. | `cp -i file1.txt /Backup/` |
| `cp <file1> <file2> <file3>/Users/<dir>` | Copies multiple files into a directory. | `cp file1.txt file2.txt /Users/username/Documents/` |
| `ditto -V [folder path][new folder]` | Copies the contents of one folder to another, with status updates. | `ditto -V /Folder1 /Folder2` |
| `rm <file>` | Deletes a specified file permanently. | `rm unwantedfile.txt` |
| `rm -i <file>` | Deletes a file with a prompt for confirmation. | `rm -i oldfile.txt` |
| `rm -f <file>` | Forces the deletion of a file without any confirmation. | `rm -f tempfile.txt` |
| `rm <file1> <file2> <file3>` | Deletes multiple files at once without confirmation. | `rm file1.txt file2.txt file3.txt` |
| `mv <file> <newfilename>` | Moves or renames a file to a new location or name. | `mv oldfile.txt newfile.txt` |
| `mv <file> <dir>` | Moves a file to a different directory. | `mv file.txt /Documents/Backup/` |
| `mv -i <file> <dir>` | Moves a file to a folder and asks for confirmation before overwriting. | `mv -i file1.txt /Documents/Backup/` |
| `mv *.png ~/<dir>` | Moves all PNG files from the current directory to another directory. | `mv *.png ~/Pictures/` |

### Mac Command History

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| `history n` | Shows the last `n` commands you’ve typed, allowing you to quickly review previous commands. | `history 5` |
| `![value]` | Executes the last command that starts with the given string or value. | `!ls` |
| `!!` | Runs the last command typed, saving you from having to retype it. | `!!` |

### Mac Terminal Permissions Commands

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| `ls -ld` | Displays the default permissions for a directory, such as a home directory. | `ls -ld ~` |
| `ls -ld <dir>` | Shows the read, write, and access permissions of a specific directory or folder. | `ls -ld /Documents/Work` |
| `chmod 755 <file>` | Modifies the permissions of a file, setting it to read, write, and execute for the owner, and read and execute for others. | `chmod 755 myscript.sh` |
| `chmod -R 600 <dir>` | Changes the permissions of a directory (and its contents) to read and write for the owner only, with no permissions for others. | `chmod -R 600 /Projects/` |
| `chown <user>:<group> <file>` | Changes the ownership of a file or directory to a specified user and group. Add `-R` to apply this to all files within a folder. | `chown user:admin myfile.txt` |

### Mac Network Commands for Terminal

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| `ping <host>` | Sends a network request to the specified host to check connectivity and displays the response time. | `ping google.com` |
| `whois <domain>` | Retrieves and displays information about the registered domain, including ownership and registration details. | `whois example.com` |
| `curl -O <url/to/file>` | Downloads a file from the specified URL using HTTP, HTTPS, or FTP protocols. | `curl -O http://example.com/file.zip` |
| `ssh <username>@<host>` | Connects to a remote system securely via SSH (Secure Shell) using the provided username and host. | `ssh user@192.168.1.1` |
| `scp <file> <user>@<host>:/remote/path` | Copies a local file to a remote host using SCP (Secure Copy Protocol). | `scp file.txt user@192.168.1.1:/home/user/` |
| `arp -a` | Displays a list of all devices currently on your local network, showing their IP and MAC addresses. | `arp -a` |
| `ifconfig en0` | Displays the network configuration details, including the IP and MAC address of your device. | `ifconfig en0` |
| `traceroute [hostname]` | Traces the route taken by data packets from your system to a destination address, showing each hop along the way. | `traceroute example.com` |

### Processes Commands

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| `ps -ax` | Displays a list of all currently running processes, including those from other users and background tasks. | `ps -ax` |
| `ps -aux` | Lists detailed information about running processes, including CPU usage, memory usage, PID, and the command being run. | `ps -aux` |
| `top` | Provides real-time information on running processes, displaying CPU and memory usage dynamically. | `top` |
| `top -ocpu -s 5` | Displays processes sorted by CPU usage, updating every 5 seconds. | `top -ocpu -s 5` |
| `top -o rsize` | Sorts the `top` command output by memory usage (resident memory size). | `top -o rsize` |
| `kill PID` | Terminates the process identified by its process ID (PID), which can be found in `ps` or `top` output. | `kill 12345` |

### Homebrew Commands

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| `brew doctor` | Check your Homebrew installation for potential issues. | `brew doctor` |
| `brew help` | Display a list of useful Homebrew formula and cask commands. | `brew help` |
| `brew list --formula` | List only the installed formulae (packages). | `brew list --formula` |
| `brew list --cask` | List only the installed casks (GUI applications). | `brew list --cask` |
| `brew outdated --formula` | List only outdated formulas (packages). | `brew outdated --formula` |
| `brew outdated --cask` | List only outdated casks (GUI applications). | `brew outdated --cask` |
| `brew pin [installed_formula]` | Pin a formula or cask to prevent it from being upgraded automatically. | `brew pin python` |
| `brew unpin [installed_formula]` | Unpin a formula or cask to allow it to be upgraded again. | `brew unpin python` |
| `brew cleanup` | Clean up stale lock files, outdated versions, and unnecessary files. | `brew cleanup` |

### Environment Variable or Path

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| `printenv` | Lists the current environment variables and shows information about your shell. | `printenv` |
| `$echo` | Prints a message or value to the Terminal. | `$echo "Hello, World!"` |
| `echo $PATH` | Displays the directories listed in the PATH variable, which are used to locate executable files. | `echo $PATH` |
| `echo $PATH > path.txt` | Saves the current PATH variable content to a text file. | `echo $PATH > path.txt` |
| `export PATH=$PATH:/new/path` | Adds a new directory to the current PATH for the session, allowing you to run programs from there. | `export PATH=$PATH:/usr/local/bin` |

### Search Commands for Mac Terminal

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| `find <dir> -name <"file">` | Search for all files named `<file>` within the specified directory `<dir>`. Use wildcards (`*`) to match partial filenames. | `find /Users/ -name "*.txt"` |
| `find <dir> -size +<size>` | Find files larger than a specified size in the given directory `<dir>`. | `find /Documents -size +10M` |
| `find <dir> -size -<size>` | Find files smaller than a specified size in the given directory `<dir>`. | `find /Downloads -size -5M` |
| `grep "<text>" <file>` | Search for and display all occurrences of `<text>` within a file `<file>`. Use `-i` to make the search case-insensitive. | `grep "error" logfile.txt` |
| `grep -rl "<text>" <dir>` | Recursively search for files within a directory `<dir>` that contain the specified `<text>`. | `grep -rl "TODO" /Projects/` |

### Output Commands

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| `cat <file>` | Displays the entire content of the specified file directly in the Terminal. | `cat myfile.txt` |
| `less <file>` | Displays the content of a file in a paginated view, allowing for easy scrolling. | `less myfile.txt` |
| `head <file>` | Displays the first 10 lines of a file. | `head myfile.txt` |
| `<cmd> < file` | Uses the content of a file as input for a command. | `sort < file.txt` |
| `<cmd> >> <file>` | Appends the output of a command to the specified file. | `echo "New text" >> myfile.txt` |
| `<cmd> > <file>` | Redirects the output of a command into the specified file, overwriting it. | `ls > directory_list.txt` |
| \`<cmd1> | <cmd2>\` | Sends the output of one command as input to another command (pipe). |

### HELP Commands

| ****Command**** | ****Description**** | ****Example**** |
| --- | --- | --- |
| `[command] -h` | Displays basic help information about a command | `ls -h` |
| `[command] --help` | Provides detailed help and options for a command | `mkdir --help` |
| `[command] help` | Displays help for the specified command | `cp help` |
| `reset` | Resets the Terminal display to its default state | `reset` |
| `man [command]` | Shows the manual page for a given command, with details | `man ls` |
| `whatis [command]` | Provides a brief, one-line description of a command | `whatis ls` |

## Conclusion

It is a bit hard to learn all the Mac Terminal commands mentioned above, but once you get used to it, it will help you control your system more easily. It might seem tricky at first, but once you learn the basic commands, it can make your work faster and more efficient. With the commands and shortcuts in this guide, you'll be able to navigate macOS, fix problems, and automate tasks like a pro.