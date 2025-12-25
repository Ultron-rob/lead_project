import signal
from typing import List

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent


@CrewBase
class Leads:
    """Leads Crew for finding clients and generating emails"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Agents
    @agent
    def scout(self) -> Agent:
        return Agent(
            config=self.agents_config['scout'],
            verbose=True
        )

    @agent
    def analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['analyst'],
            verbose=True
        )

    @agent
    def closer(self) -> Agent:
        return Agent(
            config=self.agents_config['closer'],
            verbose=True
        )

    # Tasks
    @task
    def scout_task(self) -> Task:
        return Task(
            config=self.tasks_config['scout_task'],
        )

    @task
    def analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['analysis_task'],
        )

    @task
    def email_task(self) -> Task:
        return Task(
            config=self.tasks_config['email_task'],
            output_file='emails.md'
        )

    # Crew
    @crew
    def crew(self) -> Crew:
        """Creates the Leads crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
