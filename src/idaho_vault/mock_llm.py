"""Minimal local LLM used for deployment validation without external secrets."""

from __future__ import annotations

from typing import Any

from crewai.llms.base_llm import BaseLLM


class StaticValidationLLM(BaseLLM):
    """Return a deterministic final answer in CrewAI's expected ReAct format."""

    def __init__(self) -> None:
        super().__init__(model="static-validation", provider="mock", temperature=0.0)

    def call(
        self,
        messages: str | list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        callbacks: list[Any] | None = None,
        available_functions: dict[str, Any] | None = None,
        from_task: Any | None = None,
        from_agent: Any | None = None,
        response_model: type[Any] | None = None,
    ) -> str:
        topic = "IDAHO-VAULT CrewAI bootstrap"
        if isinstance(messages, list):
            for message in reversed(messages):
                content = message.get("content")
                if isinstance(content, str) and content.strip():
                    topic = content.strip().splitlines()[0][:140]
                    break
        elif isinstance(messages, str) and messages.strip():
            topic = messages.strip().splitlines()[0][:140]

        task_hint = ""
        if from_task is not None and getattr(from_task, "description", None):
            task_hint = f" Task scope: {from_task.description}"

        return (
            "Thought: A deterministic local validation response is enough to verify "
            "that the CrewAI runtime, package entrypoints, and deployment contract are wired correctly.\n"
            "Final Answer: Bootstrap validation succeeded for "
            f"{topic}.{task_hint} "
            "The shard is using a local mock LLM on purpose, so no external model key is required for this validation run."
        )
