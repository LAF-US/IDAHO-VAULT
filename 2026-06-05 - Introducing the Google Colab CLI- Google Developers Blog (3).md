---
title: "Introducing the Google Colab CLI- Google Developers Blog"
source: "https://developers.googleblog.com/introducing-the-google-colab-cli/"
author:
  - "[[Spencer Shumway]]"
  - "[[Tyler Pirtle]]"
  - "[[Seth Troisi]]"
published: 2026-06-05
created: 2026-06-06
description: "Google announces the new Google Colab CLI, a lightweight tool bridging local terminals and remote runtimes for frictionless GPU/TPU offloading. Learn how developers and AI agents can execute remote scripts, download models, and automate ML pipelines."
date created: Saturday, June 6th 2026, 3:44:50 pm
date modified: Saturday, June 6th 2026, 3:45:27 pm
---

## Introducing the Google Colab CLI

[Spencer Shumway](https://developers.googleblog.com/search/?author=Spencer+Shumway) Product Manager

[Tyler Pirtle](https://developers.googleblog.com/search/?author=Tyler+Pirtle) Software Engineer

[Seth Troisi](https://developers.googleblog.com/search/?author=Seth+Troisi) Software Engineer

![Screenshot 2026-06-05 at 12.53.56 PM](https://storage.googleapis.com/gweb-developer-goog-blog-assets/images/Screenshot_2026-06-05_at_12.53.56PM.original.png)

Today we are announcing the [Google Colab Command-Line Interface](https://github.com/googlecolab/google-colab-cli) (CLI), which bridges the gap between your local terminal and remote Colab runtimes, providing a zero-friction execution platform for both developers and AI agents. The Colab CLI offers:

- **Zero-Friction Accelerator Provisioning:** Request high-powered GPUs or TPUs instantly (e.g., `colab --gpu A100` or `colab --gpu T4`).
- **Simple Remote Execution:** Run your local Python scripts and complex ML pipelines directly on Colab runtimes using `colab exec`.
- **Seamless Artifact Recovery:** Easily retrieve models, datasets, and replayable `.ipynb` logs via `colab download` and `colab log`.
- **Interactive Access:** Drop into an interactive environment on your remote Colab runtime with `colab repl` or `colab console`.

<video controls=""><source src="https://storage.googleapis.com/gweb-developer-goog-blog-assets/original_videos/ColabCLILarge.mp4" type="video/mp4"><p>Sorry, your browser doesn't support playback for this video</p></video>

### Agent-driven workflows in action

Because the Colab CLI integrates seamlessly into standard terminal environments, it can be used by any agent with terminal access. To ensure your AI assistants can hit the ground running, the CLI includes a prepackaged Colab [skill file](https://github.com/googlecolab/google-colab-cli/blob/main/COLAB_SKILL.md) that provides agents with instant, built-in context on exactly how to leverage the CLI. Let's look at a real life example of something a user or agent might try with the Colab CLI.

\*Note that while the example below highlights [Antigravity](https://antigravity.google/) agent using Colab CLI as a tool, Colab CLI can easily be used by Claude Code, Codex, and other agents.

Here is how an Agent can use the Colab CLI for a real-world ML workflow:

#### Fine-tuning Gemma 3-1B

The CLI can be used to run a real QLoRA pipeline that runs end-to-end with just a handful of commands. Offload heavy computational lifting to a GPU without typing a single cloud provisioning command by Instructing Antigravity (or your agent of choice) to build a remote fine-tuning job. In this scenario, we ask our agent to use the Colab CLI to fine-tune [google/gemma-3-1b-it](https://huggingface.co/google/gemma-3-1b-it) on a [Text-to-SQL dataset](https://huggingface.co/datasets/philschmid/gretel-synthetic-text-to-sql) to make the model better at writing SQL queries.

**The Antigravity prompt:**  
Use the Colab CLI (<https://github.com/googlecolab/google-colab-cli>) to fine-tune Gemma 3 1B using QLoRA. Provision a Colab T4 GPU instance, install the necessary ML packages (transformers, datasets, peft, trl, etc.), run my local ~ [finetune\_run](https://github.com/googlecolab/google-colab-cli/blob/main/examples/finetune_run.py)[.py](https://gist.github.com/spencersgoogle/05be7d5b8a86785284a72032d11e7214) script remotely, download the resulting safetensors adapter, save the notebook log, and cleanup.

**Antigravity executes:**

```shell
colab new --gpu T4
colab install transformers datasets peft trl bitsandbytes accelerate
colab exec -f finetune_run.py
colab log --output gemma_finetune_log.ipynb
colab stop
```

Antigravity also uses the "colab download" command to download the adapter model, adapter config, tokenizer config, and tokenizer, which can be used to load and run your fine-tuned model locally. Now you have a remotely fine-tuned model ready to serve from your local device!

### Try it out now

The Colab CLI makes powerful Colab compute accessible, programmable, and agent-ready. It is lightweight and easily accessible to any terminal-based AI agent. To start using the Colab CLI yourself, head over to the [Google Colab CLI GitHub repository](https://github.com/googlecolab/google-colab-cli) for setup instructions.

We are excited to see how this accelerates your development process and look forward to seeing what you and your agents build!
