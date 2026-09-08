---
title: "CLI Reference"
source: "https://docs.ollama.com/cli"
author:
published:
created: 2026-07-03
description:
---
### Run a model

```text
ollama run gemma4
```

### Launch integrations

```text
ollama launch
```

Configure and launch external applications to use Ollama models. This provides an interactive way to set up and start integrations with supported apps.

#### Supported integrations

- **OpenCode** - Open-source coding assistant
- **Claude Code** - Anthropic’s agentic coding tool
- **Codex** - OpenAI’s coding assistant
- **VS Code** - Microsoft’s IDE with built-in AI chat
- **Droid** - Factory’s AI coding agent

#### Examples

Launch an integration interactively:

```text
ollama launch
```

Launch a specific integration:

```text
ollama launch claude
```

Launch with a specific model:

```text
ollama launch claude --model qwen3.5
```

Configure without launching:

```text
ollama launch droid --config
```

#### Multiline input

For multiline input, you can wrap text with `"""`:

```text
>>> """Hello,
... world!
... """
I'm a basic program that prints the famous "Hello, world!" message to the console.
```

#### Multimodal models

```text
ollama run gemma4 "What's in this image? /Users/jmorgan/Desktop/smile.png"
```

### Generate embeddings

```text
ollama run embeddinggemma "Hello world"
```

Output is a JSON array:

```text
echo "Hello world" | ollama run nomic-embed-text
```

### Download a model

```text
ollama pull gemma4
```

### Remove a model

```text
ollama rm gemma4
```

### List models

```text
ollama ls
```

### Sign in to Ollama

```text
ollama signin
```

### Sign out of Ollama

```text
ollama signout
```

### Create a customized model

First, create a `Modelfile`

```text
FROM gemma4
SYSTEM """You are a happy cat."""
```

Then run `ollama create`:

```text
ollama create -f Modelfile
```

### List running models

```text
ollama ps
```

### Stop a running model

```text
ollama stop gemma4
```

### Start Ollama

```text
ollama serve
```

To view a list of environment variables that can be set run `ollama serve --help`