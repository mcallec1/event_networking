# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from event_networking.tools.linkedin_tool import LinkedInProfileTool
from event_networking.models.profile import UserProfile

@CrewBase
class EventNetworkingCrew():
  """Event Networking crew"""


  @agent
  def linkedin_scraper_my_profile(self) -> Agent:
    return Agent(
      config=self.agents_config['linkedin_scraper_my_profile'],
      verbose=True,
      tools=[LinkedInProfileTool()]
    )
  
  @agent
  def linkedin_scraper_contact_profile(self) -> Agent:
    return Agent(
      config=self.agents_config['linkedin_scraper_contact_profile'],
      verbose=True,
      tools=[LinkedInProfileTool()]
    )

  @task
  def get_my_profile(self) -> Task:
    return Task(
      config=self.tasks_config['get_my_profile'],
      output_pydantic=UserProfile
    )

  @task
  def get_contact_profile(self) -> Task:
    return Task(
      config=self.tasks_config['get_contact_profile'],
      output_pydantic=UserProfile
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
