from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LinkedInProfileInput(BaseModel):
    """Input schema for LinkedInProfileTool."""
    linkedin_url: str = Field(
        ..., 
        description="The LinkedIn profile URL to scrape (e.g., 'https://www.linkedin.com/in/username')"
    )

class LinkedInProfileTool(BaseTool):
    name: str = "LinkedIn Profile Scraper"
    description: str = (
        "A tool for scraping LinkedIn profiles. Provide a LinkedIn profile URL "
        "to get information about the person's experience, education, and other "
        "public profile information."
    )
    args_schema: Type[BaseModel] = LinkedInProfileInput

    def _run(self, linkedin_url: str) -> str:
        try:
            # Get credentials from environment variables
            email = os.getenv("LINKEDIN_EMAIL")
            password = os.getenv("LINKEDIN_PASSWORD")

            # Set up Chrome options for headless browsing
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            # Initialize the driver
            driver = webdriver.Chrome(options=chrome_options)
            
            # Login to LinkedIn
            actions.login(driver, email, password)
            
            # Scrape the profile
            person = Person(linkedin_url, driver=driver)
            
            # Compile the profile information with safer attribute access
            profile_info = {
                "name": getattr(person, "name", "Name not available"),
                "experiences": [
                    {
                        "company": getattr(exp, "institution_name", "Unknown Company"),
                        "title": getattr(exp, "position_title", "Unknown Position"),
                        "duration": getattr(exp, "duration", "Duration not specified"),
                    }
                    for exp in getattr(person, "experiences", [])
                ],
                "education": [
                    {
                        "institution": getattr(edu, "institution_name", "Unknown Institution"),
                        "degree": getattr(edu, "degree", "Degree not specified"),
                    }
                    for edu in getattr(person, "educations", [])
                ]
            }
            
            # Close the browser
            driver.quit()
            
            # Return formatted information
            return f"""
Profile Information for {profile_info['name']}:

Experience:
{self._format_experiences(profile_info['experiences'])}

Education:
{self._format_education(profile_info['education'])}
"""
        except Exception as e:
            return f"Error scraping LinkedIn profile: {str(e)}"

    def _format_experiences(self, experiences):
        if not experiences:
            return "No experience information available"
        
        return "\n".join([
            f"- {exp['title']} at {exp['company']}" + 
            (f" ({exp['duration']})" if exp['duration'] else "")
            for exp in experiences
        ])

    def _format_education(self, education):
        if not education:
            return "No education information available"
        
        return "\n".join([
            f"- {edu['degree']} from {edu['institution']}"
            for edu in education
        ]) 