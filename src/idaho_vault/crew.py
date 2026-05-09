"""Minimal CrewAI validation crew for the first deployment pass."""

from __future__ import annotations

from crewai import Agent, Crew, Process, Task

from idaho_vault.bootstrap_contract import ContractReport
from idaho_vault.mock_llm import StaticValidationLLM


class IdahoVaultBootstrapCrew:
    """Build the smallest viable crew that proves deployment shape."""

    def __init__(self, report: ContractReport) -> None:
        self._llm = StaticValidationLLM()
        self._report = report

    def crew(self) -> Crew:
        validator = Agent(
            role="IDAHO-VAULT Bootstrap Validator",
            goal=(
                "Confirm that the repository exposes a valid CrewAI project shape "
                "without depending on external model credentials."
            ),
            backstory=(
                "You are the first disposable runtime shard for IDAHO-VAULT. "
                "Your job is to validate packaging and execution boundaries, "
                "not to write canon."
            ),
            llm=self._llm,
            allow_delegation=False,
            verbose=True,
            max_iter=1,
        )

        validation_task = Task(
            description=(
                "Validate the root CrewAI deployment contract for IDAHO-VAULT. "
                "Confirm the presence of the pyproject contract, the uv lockfile, "
                "the src/idaho_vault runtime package, and the doctrinal alignment "
                "between the live CrewAI manifest and training doctrine.\n\n"
                f"Deterministic contract report:\n{self._report.to_markdown()}"
            ),
            expected_output=(
                "A concise markdown validation note that agrees with the deterministic contract report."
            ),
            agent=validator,
        )

        return Crew(
            agents=[validator],
            tasks=[validation_task],
            process=Process.sequential,
            verbose=True,
        )
