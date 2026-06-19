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
                    topic = self._summarize_topic(content)
                    break
        elif isinstance(messages, str) and messages.strip():
            topic = self._summarize_topic(messages)

        return (
            "Thought: A deterministic local validation response is enough to verify "
            "that the CrewAI runtime, package entrypoints, and deployment contract are wired correctly.\n"
            "Final Answer: Bootstrap validation completed for "
            f"{topic}. "
            "The deterministic contract report is the authoritative assay for pass or fail. "
            "This shard uses a local mock LLM on purpose, so no external model key is required for bootstrap validation."
        )

    @staticmethod
    def _summarize_topic(content: str) -> str:
        """Keep the displayed topic concise even when the prompt carries a report."""
        first_line = content.strip().splitlines()[0]
        first_line = first_line.replace("Current Task:", "").strip()
        return first_line[:140]
