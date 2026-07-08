# Hermes OpenRouter + Local Plan (Coding)

Goal: integrate Codestral and Devstral into the local stack, leverage Ollama for fast local code tasks, and maintain OpenRouter as cloud fallback for heavy tasks.

Status: Draft plan - will update config and run doctor/tests.

Plan:
- Update Hermes config: add Codestral and Devstral as local models with correct default order
- Ensure `ollama-local` has those models listed
- Validate that OpenRouter remains as fallback after local models
- Prepare short smoke test: generate code with Codestral, then refactor with Devstral, then fallback to OpenRouter for edge cases
- Monitor after Mistral Large completes

Key risks:
- Model sizes and memory footprint; ensure sufficient RAM
- Download times; ensure users understand wait time

Next actions:
- Update config and run `hermes doctor` and `hermes setup` if needed
- Run test prompts to verify tool capabilities
