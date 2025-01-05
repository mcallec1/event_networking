# src/latest_ai_development/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from event_networking.tools.linkedin_tool import LinkedInProfileTool
from event_networking.tools.custom_tool import MarkdownWriterTool
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

  @agent
  def event_researcher(self) -> Agent:
    return Agent(
      config=self.agents_config['event_researcher'],
      verbose=True,
      tools=[ScrapeWebsiteTool()]
    )

  @agent
  def profile_analyzer(self) -> Agent:
    return Agent(
      config=self.agents_config['profile_analyzer'],
      verbose=True,
      tools=[]  # This agent will use built-in LLM capabilities for analysis
    )

  @agent
  def message_formatter(self) -> Agent:
    return Agent(
      config=self.agents_config['message_formatter'],
      verbose=True,
      tools=[MarkdownWriterTool()]
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

  @task
  def webscraping_event(self) -> Task:
    return Task(
      config=self.tasks_config['webscraping_event']
    )

  @task
  def analyze_and_create_messages(self) -> Task:
    return Task(
      config=self.tasks_config['analyze_and_create_messages']
    )

  @task
  def format_and_save_message(self) -> Task:
    return Task(
      config=self.tasks_config['format_and_save_message']
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
