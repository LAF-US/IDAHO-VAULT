from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class FiveWizardsCouncil:
    """A bounded six-lane inquiry crew with explicit human promotion boundaries."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def who_wizard(self) -> Agent:
        return Agent(config=self.agents_config["who_wizard"], verbose=True)

    @agent
    def what_wizard(self) -> Agent:
        return Agent(config=self.agents_config["what_wizard"], verbose=True)

    @agent
    def when_wizard(self) -> Agent:
        return Agent(config=self.agents_config["when_wizard"], verbose=True)

    @agent
    def where_wizard(self) -> Agent:
        return Agent(config=self.agents_config["where_wizard"], verbose=True)

    @agent
    def why_wizard(self) -> Agent:
        return Agent(config=self.agents_config["why_wizard"], verbose=True)

    @agent
    def how_wizard(self) -> Agent:
        return Agent(config=self.agents_config["how_wizard"], verbose=True)

    @task
    def who_inquiry_task(self) -> Task:
        return Task(config=self.tasks_config["who_inquiry_task"])

    @task
    def what_inquiry_task(self) -> Task:
        return Task(config=self.tasks_config["what_inquiry_task"])

    @task
    def when_inquiry_task(self) -> Task:
        return Task(config=self.tasks_config["when_inquiry_task"])

    @task
    def where_inquiry_task(self) -> Task:
        return Task(config=self.tasks_config["where_inquiry_task"])

    @task
    def why_inquiry_task(self) -> Task:
        return Task(config=self.tasks_config["why_inquiry_task"])

    @task
    def council_synthesis_task(self) -> Task:
        return Task(config=self.tasks_config["council_synthesis_task"])

    @crew
    def crew(self) -> Crew:
        """Create a finite inquiry run with direct, inspectable lane ownership."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
