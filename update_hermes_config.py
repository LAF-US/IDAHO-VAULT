import yaml
import os

config_path = os.path.expanduser("~/.hermes/config.yaml")

with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Update model
config['model'] = {
    'provider': 'ollama-local',
    'default': 'mistral-large:latest',
    'api_key': 'ollama',
    'base_url': 'http://127.0.0.1:11434/v1',
    'api_mode': 'chat_completions'
}

# Update providers
new_providers = {
    'ollama-local': {
        'api': 'http://127.0.0.1:11434/v1',
        'api_key': 'ollama',
        'default_model': 'mistral-large:latest',
        'models': ['mistral-large:latest', 'devstral:latest', 'codestral:latest', 'qwen3.5:latest', 'phi3:mini', 'qwen2.5:3b'],
        'name': 'Ollama Local'
    },
    'ollama-devstral': {
        'api': 'http://127.0.0.1:11434/v1',
        'api_key': 'ollama',
        'default_model': 'devstral:latest',
        'name': 'Ollama Devstral'
    },
    'ollama-qwen': {
        'api': 'http://127.0.0.1:11434/v1',
        'api_key': 'ollama',
        'default_model': 'qwen3.5:latest',
        'name': 'Ollama Qwen'
    },
    'ollama-light': {
        'api': 'http://127.0.0.1:11434/v1',
        'api_key': 'ollama',
        'default_model': 'phi3:mini',
        'name': 'Ollama Light'
    },
    'openrouter-gpt4o': {
        'api': 'https://openrouter.ai/api/v1',
        'api_key': 'env:OPENROUTER_API_KEY',
        'default_model': 'openai/gpt-4o-mini',
        'name': 'OpenRouter GPT-4o Mini'
    },
    'openrouter-haiku': {
        'api': 'https://openrouter.ai/api/v1',
        'api_key': 'env:OPENROUTER_API_KEY',
        'default_model': 'anthropic/claude-3.5-haiku',
        'name': 'OpenRouter Claude Haiku'
    },
    'openrouter-mistral-large': {
        'api': 'https://openrouter.ai/api/v1',
        'api_key': 'env:OPENROUTER_API_KEY',
        'default_model': 'mistralai/mistral-large-2411',
        'name': 'OpenRouter Mistral Large'
    },
    'openrouter-mistral': {
        'api': 'https://openrouter.ai/api/v1',
        'api_key': 'env:OPENROUTER_API_KEY',
        'default_model': 'mistralai/mistral-small-2409',
        'name': 'OpenRouter Mistral Small'
    },
    'openrouter-free': {
        'api': 'https://openrouter.ai/api/v1',
        'api_key': 'env:OPENROUTER_API_KEY',
        'default_model': 'deepseek/deepseek-r1:free',
        'models': [
            'deepseek/deepseek-r1:free',
            'google/gemini-2.0-flash-exp:free',
            'meta-llama/llama-3.1-70b-instruct:free'
        ],
        'name': 'OpenRouter Free'
    }
}

config['providers'].update(new_providers)

# Update fallback_providers
config['fallback_providers'] = [
    'ollama-devstral',
    'ollama-qwen',
    'ollama-light',
    'openrouter-gpt4o',
    'openrouter-haiku',
    'openrouter-mistral-large',
    'openrouter-mistral'
]

with open(config_path, 'w') as f:
    yaml.dump(config, f, default_flow_style=False)

print("Hermes configuration updated successfully.")
