# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from event_networking.tools.linkedin_tool import LinkedInProfileTool

@CrewBase
class EventNetworkingCrew():
  """Event Networking crew"""
  
  @agent
  def linkedin_scraper(self) -> Agent:
    return Agent(
      config=self.agents_config['linkedin_scraper'],
      verbose=True,
      tools=[LinkedInProfileTool()]
    )

  @task
  def linkedin_task(self) -> Task:
    return Task(
      config=self.tasks_config['linkedin_task'],
      #output_file='output/linkedin.md'
    )



  @crew
  def crew(self) -> Crew:
    """Creates the EventNetworking crew"""
    return Crew(
      agents=self.agents, # Automatically created by the @agent decorator
      tasks=self.tasks, # Automatically created by the @task decorator
      process=Process.sequential,
      verbose=True,
    )
