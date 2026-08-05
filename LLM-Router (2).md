---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.4
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# LLM Router - IDAHO-VAULT

Tiered routing: light models for simple tasks, heavy models for complex tasks.
Local (Ollama) preferred, OpenRouter fallback.
Integrated with `swarm.json` agent registry.

Constitutional compliance: CONSTITUTION.md § I - Markdown = human, Python = machine

```python
import json
import requests
import subprocess
import os
from typing import Dict, List, Optional

# Load swarm.json for agent registry
with open('swarm.json', 'r') as f:
    swarm = json.load(f)

print(f"Vault authority: {swarm.get('vault_authority', 'unknown')}")
print(f"Agents: {[a['id'] for a in swarm.get('agents', [])]}")
```

```python
class LLMRouter:
    def __init__(self):
        self.ollama_url = "http://localhost:11434/api/generate"
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.openrouter_key = self._get_openrouter_key()
        self.models = {
            'light': {'ollama': 'gemma4:latest', 'openrouter': 'anthropic/claude-3-haiku'},
            'medium': {'ollama': 'llama3.2-vision:90b', 'openrouter': 'anthropic/claude-3-sonnet'},
            'heavy': {'ollama': 'llama3.2-vision:90b', 'openrouter': 'anthropic/claude-3-opus'}
        }
    
    def _get_openrouter_key(self) -> Optional[str]:
        try:
            result = subprocess.run(['op', 'read', 'op://Vault/OpenRouter API Key/credential'], 
                                capture_output=True, text=True, timeout=10)
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return os.environ.get('OPENROUTER_API_KEY')
    
    def route(self, prompt: str, complexity: str = 'light', use_local_first: bool = True) -> str:
        """Route LLM call based on complexity and availability."""
        if use_local_first:
            response = self._try_ollama(prompt, complexity)
            if response: return response
        return self._try_openrouter(prompt, complexity)
    
    def _try_ollama(self, prompt: str, complexity: str) -> Optional[str]:
        try:
            model = self.models[complexity]['ollama']
            response = requests.post(self.ollama_url, 
                json={'model': model, 'prompt': prompt, 'stream': False}, timeout=60)
            if response.status_code == 200:
                return response.json().get('response', '')
        except Exception as e:
            print(f"Ollama failed: {e}")
        return None
    
    def _try_openrouter(self, prompt: str, complexity: str) -> str:
        if not self.openrouter_key: return "Error: No OpenRouter API key"
        try:
            model = self.models[complexity]['openrouter']
            response = requests.post(self.openrouter_url,
                headers={'Authorization': f'Bearer {self.openrouter_key}',
                        'Content-Type': 'application/json'},
                json={'model': model, 'messages': [{'role': 'user', 'content': prompt}], 'max_tokens': 500},
                timeout=30)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return f"OpenRouter error: {response.status_code}"
        except Exception as e:
            return f"OpenRouter failed: {e}"

router = LLMRouter()
print("LLM Router initialized")
```

```python
# Test the router
test_prompt = "What is 2+2? Respond with just the number."
print(f"Testing: {test_prompt}")
response = router.route(test_prompt, complexity='light', use_local_first=True)
print(f"Response: {response}")
```
