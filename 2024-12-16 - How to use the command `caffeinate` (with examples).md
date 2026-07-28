---
title: "How to use the command `caffeinate` (with examples)"
source: "https://commandmasters.com/commands/caffeinate-osx/"
author:
  - "[[CommandMasters]]"
published: 2024-12-16
created: 2026-05-04
description: "An awesome guide for the most useful CLI commands"
date created: Monday, May 4th 2026, 2:00:00 am
date modified: Monday, May 4th 2026, 2:01:28 am
---

![How to use the command `caffeinate` (with examples)](https://commandmasters.com/images/commands/general-9_hu05f28c6e3fa8017f6c313617b48b4862_9248_1110x0_resize_q90_h2_lanczos_2.webp)

The `caffeinate` command is a powerful utility available on macOS that prevents the system from sleeping. Whether it’s to ensure that a long-running process isn’t interrupted or to maintain system readiness for critical tasks, `caffeinate` provides flexible options to control when and how your Mac goes to sleep. This command can be especially useful for developers running scripts, professionals conducting presentations, or any user simply needing a nap-free Mac for a set period.

## Prevent from sleeping for 1 hour (3600 seconds)

Code:

```shell
caffeinate -u -t 3600
```

Motivation:  
Imagine you’re in the middle of downloading a large file or batch processing photos for an hour, and you need your Mac to stay awake without making any further adjustments. The `caffeinate` command allows you to keep your system active for a specified duration, making sure that your tasks are completed without any sleep interruptions.

Explanation:

- `-u`: This flag updates the last user activity time, preventing the system from sleeping due to inactivity.
- `-t 3600`: This sets a time limit, in seconds, for which `caffeinate` will run. Here, it’s set to 3600 seconds, equivalent to 1 hour.

Example Output:  
Upon running this command, your Mac will not enter sleep mode for the next hour. You won’t see any direct output on the terminal, but you can be assured that the system will remain active for the specified duration.

## Prevent from sleeping until a command completes

Code:

```shell
caffeinate -s "command"
```

Motivation:  
Running long scripts or computational tasks can be disrupted if your Mac goes to sleep. Using `caffeinate`, you can ensure that the system stays awake for the specific duration of a command, like a backup operation, a massive file transfer, or compiling large codebases, preventing interruptions.

Explanation:

- `-s`: This option tells `caffeinate` to prevent the system from sleeping while the specified command is running, ensuring that your work is uninterrupted until completion.
- `"command"`: Replace this placeholder with any command that you are interested in running without sleep interruptions.

Example Output:  
Executing this command will keep your Mac awake until the specified command finishes execution. There’s no visible output from `caffeinate` itself unless the enclosed command produces output.

## Prevent from sleeping until a process with the specified PID completes

Code:

```shell
caffeinate -w pid
```

Motivation:  
When you’ve launched a process and identified its process ID (PID), you may want to ensure your system stays awake till this process finishes. This is particularly useful in scenarios where you’re running a critical server update or a specific application process that cannot be interrupted.

Explanation:

- `-w`: This option instructs `caffeinate` to wait for a process with the specified PID (process identifier) to complete before allowing the system to sleep again.
- `pid`: The PID of the process you wish to track. It uniquely identifies the processes you want `caffeinate` to monitor.

Example Output:  
With this command, the Mac remains awake as long as the given PID is active. The command doesn’t return any information directly unless there is a status change in the specified process.

## Prevent from sleeping (use Ctrl + C to exit)

Code:

```shell
caffeinate -i
```

Motivation:  
There are times you need indefinite protection against sleep, such as during a presentation or an all-day coding session. Rather than setting a timer, you can manually control when your Mac can sleep by keeping it awake until you choose to stop the command.

Explanation:

- `-i`: This flag allows you to inhibit system inactivity sleep. As long as `caffeinate` is running, the system will not sleep because of inactivity.

Example Output:  
The system remains awake indefinitely, and you can manually terminate this mode when no longer needed by pressing `Ctrl + C` in the terminal, which stops the `caffeinate` process.

## Prevent disk from sleeping (use Ctrl + C to exit)

Code:

```shell
caffeinate -m
```

Motivation:  
In certain situations, you may require constant disk activity, such as when streaming large media files from your hard drive or running a database server. Preventing the disk from going into a low-power state can provide smoother performance and avoid errors related to disk inaccessibility.

Explanation:

- `-m`: This flag prevents the disk from going idle and subsequently sleeping, which ensures that active disk usage is maintained.

Example Output:  
The hard drive will stay awake as long as `caffeinate` is active with this option. Similarly, you can terminate the command using `Ctrl + C`, permitting the disk to resume its usual power-saving features.

## Conclusion

The `caffeinate` command on macOS offers flexibility and control over when your system should remain awake, making it an essential tool for users who need uninterrupted system performance. Whether it’s for a specific task duration or to keep the system constantly active during a task, `caffeinate` provides efficient options tailored to your needs.