from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import yaml
import os

@CrewBase
class FiveWizardsCouncil():
	"""5Wizards Council Crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def who_wizard(self) -> Agent:
		return Agent(
			config=self.agents_config['who_wizard'],
			verbose=True
		)

	@agent
	def what_wizard(self) -> Agent:
		return Agent(
			config=self.agents_config['what_wizard'],
			verbose=True
		)

	@agent
	def when_wizard(self) -> Agent:
		return Agent(
			config=self.agents_config['when_wizard'],
			verbose=True
		)

	@agent
	def where_wizard(self) -> Agent:
		return Agent(
			config=self.agents_config['where_wizard'],
			verbose=True
		)

	@agent
	def why_wizard(self) -> Agent:
		return Agent(
			config=self.agents_config['why_wizard'],
			verbose=True
		)

	@agent
	def how_wizard(self) -> Agent:
		return Agent(
			config=self.agents_config['how_wizard'],
			verbose=True
		)

	@task
	def inquiry_task(self) -> Task:
		return Task(
			config=self.tasks_config['inquiry_task'],
		)

	@task
	def final_adjudication_task(self) -> Task:
		return Task(
			config=self.tasks_config['final_adjudication_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the 5Wizards Council crew"""
		return Crew(
			agents=[a for a in self.agents if a.role != self.how_wizard().role],
			tasks=self.tasks,
			process=Process.hierarchical,
			manager_agent=self.how_wizard(),
			verbose=True,
		)
