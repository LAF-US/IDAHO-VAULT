---
title: "Running Mistral Vibe CLI with Local LLMs: A Complete Guide"
source: "https://dev.to/chung_duy_51a346946b27a3d/running-mistral-vibe-with-local-llms-a-complete-guide-1mde"
author:
  - "[[Chung Duy]]"
published: 2026-01-04
created: 2026-06-06
description: "Why run Mistral Vibe CLI with local LLM?   So, Mistral Vibe is this amazing CLI tool that..."
date created: Saturday, June 6th 2026, 2:51:04 pm
date modified: Saturday, June 6th 2026, 3:44:35 pm
---

## Why run Mistral Vibe CLI with local LLM?

So, Mistral Vibe is this amazing CLI tool that usually talks to Mistral's cloud. But honestly? Running it **locally** is a total game changer. It feels so much cooler when the "brain" is actually inside your own computer!

Here's why I'm loving the local setup:

- **Privacy Core**: My code stays right here on my machine. No "sending to the cloud" anxiety! 🔒
- **Free Forever**: Zero API bills. My wallet is so happy right now. 💸
- **Internet? Optional**: I can literally code in a cabin in the woods (if I had one). 🌲
- **Model Hopping**: I can try out whatever models I want just by pulling them from Ollama.

I'm using **Ollama** with the **devstral-small-2** model for this guide because it's super snappy for coding.

---

## Prerequisites

- MacOS at least 32GB, chip M4 (I never try with lower chip). Disk space should have at least 20GB since devstral-small-2 have size 15GB.
- Git
- Python 3.12 or higher
- pip or pipx
- ollama ([https://ollama.com/](https://ollama.com/))

I've not tried yet in Linux/Window but assume that should be same. If you are using Linux/Window ensure you have appropriate GPU hardware good enough to run Ollama devstral-small-2 24B.

---

## Installation Guide

### Step 1: Install Ollama

Ollama is a tool for running large language models locally with ease.

#### On macOS

```
# Download and install from official website
curl -fsSL https://ollama.com/install.sh | sh

# Or using Homebrew
brew install ollama
```

#### Verify Installation

```
ollama --version
```

### Step 2: Pull the Model

Download the `devstral-small-2` model (or any model you prefer):

```
# Pull the model (this may take a few minutes depending on your internet speed)
ollama pull devstral-small-2
```

Verify the model is downloaded:

```
ollama list
```

### Step 3: Start Ollama Server

```
# Start the Ollama server
ollama serve
```

**Note:** Keep this terminal window open. The server needs to run while you use Vibe.

**Default endpoint:** `http://localhost:11434`

To run Ollama in the background on macOS/Linux:

```
# Create a background service (optional)
ollama serve &
```

### Step 4: Install Mistral Vibe

Check out the repo: [https://github.com/mistralai/mistral-vibe](https://github.com/mistralai/mistral-vibe)

Using pipx

```
# Install pipx if you don't have it
brew install pipx  # macOS
# or
pip install pipx   # Linux/Windows

# Ensure pipx path is configured
pipx ensurepath

# Install Mistral Vibe from source
cd /path/to/mistral-vibe
pipx install -e .
```

#### Open new tab terminal and verify the installation

```
vibe --version
```

You should see: `vibe 1.3.3` (or your current version)

---

## Configuration

Mistral Vibe uses a TOML configuration file located at `~/.vibe/config.toml`.

### Step 1: Locate or Create Config File

When you first run `vibe`, it creates a default config file. However, we need to modify it to use Ollama.

### Step 2: Configure for Ollama

Create or edit `~/.vibe/config.toml` with the following configuration:

```
# ~/.vibe/config.toml

# Set Ollama model as default
active_model = "ollama-devstral-small-2"

# UI and behavior settings
textual_theme = "terminal"
vim_keybindings = false
disable_welcome_banner_animation = false
auto_compact_threshold = 200000
context_warnings = false
system_prompt_id = "cli"
include_commit_signature = true
include_model_info = true
include_project_context = true
enable_update_checks = true
api_timeout = 720.0

# Tool configurations (optional - customize as needed)
enabled_tools = []
disabled_tools = []

# ============================================
# PROVIDERS CONFIGURATION
# ============================================

# Ollama Provider (Local)
[[providers]]
name = "ollama"
api_base = "http://localhost:11434/v1"
api_key_env_var = ""  # No API key needed for local
api_style = "openai"
backend = "generic"
reasoning_field_name = "reasoning_content"

# Mistral Cloud Provider (Optional - keep for fallback)
[[providers]]
name = "mistral"
api_base = "https://api.mistral.ai/v1"
api_key_env_var = "MISTRAL_API_KEY"
api_style = "openai"
backend = "mistral"
reasoning_field_name = "reasoning_content"

# ============================================
# MODELS CONFIGURATION
# ============================================

# Ollama Models (Local)
[[models]]
name = "devstral-small-2"
provider = "ollama"
alias = "ollama-devstral-small-2"
temperature = 0.2
input_price = 0.0  # Free - local model
output_price = 0.0

[[models]]
name = "mistral"
provider = "ollama"
alias = "ollama-mistral"
temperature = 0.2
input_price = 0.0
output_price = 0.0

[[models]]
name = "devstral-2"
provider = "ollama"
alias = "ollama-devstral-2"
temperature = 0.2
input_price = 0.0
output_price = 0.0

# Cloud Models (Optional - for fallback)
[[models]]
name = "mistral-vibe-cli-latest"
provider = "mistral"
alias = "devstral-2-cloud"
temperature = 0.2
input_price = 0.4
output_price = 2.0

# ============================================
# PROJECT CONTEXT SETTINGS
# ============================================

[project_context]
max_chars = 40000
default_commit_count = 5
max_doc_bytes = 32768
truncation_buffer = 1000
max_depth = 3
max_files = 1000
max_dirs_per_level = 20
timeout_seconds = 2.0

# ============================================
# SESSION LOGGING
# ============================================

[session_logging]
save_dir = "~/.vibe/logs/session"
session_prefix = "session"
enabled = true

# ============================================
# TOOL PERMISSIONS
# ============================================

[tools.read_file]
permission = "always"
max_read_bytes = 64000

[tools.write_file]
permission = "ask"
max_write_bytes = 64000

[tools.search_replace]
permission = "ask"
max_content_size = 100000

[tools.bash]
permission = "ask"
max_output_bytes = 16000
default_timeout = 30

[tools.grep]
permission = "always"
max_output_bytes = 64000
default_max_matches = 100

[tools.todo]
permission = "always"
max_todos = 100
```

### Step 3: Understanding Key Configuration Options

#### Provider Configuration

```
[[providers]]
name = "ollama"                              # Provider identifier
api_base = "http://localhost:11434/v1"       # Ollama's OpenAI-compatible endpoint
api_key_env_var = ""                         # Empty = no API key required
api_style = "openai"                         # Use OpenAI-compatible API format
backend = "generic"                          # Use generic HTTP backend
```

#### Model Configuration

```
[[models]]
name = "devstral-small-2"                    # Exact model name in Ollama
provider = "ollama"                          # Links to provider above
alias = "ollama-devstral-small-2"            # Friendly name you'll use
temperature = 0.2                            # Lower = more deterministic
input_price = 0.0                            # Free for local
output_price = 0.0                           # Free for local
```

---

## Usage Examples

### Basic Usage

#### 1\. Start Vibe

```
# Navigate to your project
cd /path/to/your/project

# Start Vibe
vibe
```

You should see the Vibe interface and use it with local LLM. So any prompts will be processed by local LLM instead of cloud models and does not require any API key.

Happy coding!

[![Google article image](https://media2.dev.to/dynamic/image/width=775%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2F4xvesbdat735rxwhwvaw.png)](https://dev.to/googleai/gemini-35-flash-developer-guide-1i46?bb=263496)

## Gemini 3.5 Flash Developer Guide ⚡️

[Gemini 3.5 Flash](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/?bb=263496) is generally available (GA), stable, and ready for scaled production use. As our most intelligent Flash model, it delivers sustained frontier performance in agentic execution, coding, and long-horizon tasks at scale.

This guide contains an overview of improvements, API changes, and migration guidance for Gemini 3.5 Flash.