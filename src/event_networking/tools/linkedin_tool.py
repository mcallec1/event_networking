from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import os
import time
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
    name: str = "LinkedIn Profile Tool"
    description: str = (
        "A tool for getting LinkedIn profile information. Provide a LinkedIn profile URL "
        "to get information about the person's experience, education, and other "
        "public profile information."
    )
    args_schema: Type[BaseModel] = LinkedInProfileInput

    def _run(self, linkedin_url: str) -> str:
        try:
            email = os.getenv("LINKEDIN_EMAIL")
            password = os.getenv("LINKEDIN_PASSWORD")

            if not all([email, password]):
                return "Error: LinkedIn credentials not found in environment variables"

            with sync_playwright() as p:
                # Launch browser with additional options
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-accelerated-2d-canvas',
                        '--disable-gpu'
                    ]
                )
                
                # Create a context with specific options
                context = browser.new_context(
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080},
                    java_script_enabled=True,
                )
                
                page = context.new_page()

                try:
                    # Login to LinkedIn with longer timeout
                    page.goto('https://www.linkedin.com/login', timeout=60000)
                    page.fill('input[id="username"]', email)
                    page.fill('input[id="password"]', password)
                    page.click('button[type="submit"]')
                    
                    # Wait for login to complete with longer timeout
                    page.wait_for_load_state('networkidle', timeout=60000)
                    time.sleep(3)  # Additional wait to ensure complete login

                    # Navigate to profile with longer timeout
                    page.goto(linkedin_url, timeout=60000)
                    
                    # Wait for key elements to load
                    page.wait_for_load_state('networkidle', timeout=60000)
                    
                    # Multiple attempts to find the main content
                    for _ in range(3):
                        try:
                            page.wait_for_selector('h1', timeout=20000)
                            break
                        except:
                            # Scroll and wait between attempts
                            page.evaluate('window.scrollTo(0, document.body.scrollHeight/2)')
                            time.sleep(2)
                    
                    # Scroll through the page to trigger lazy loading
                    for _ in range(3):
                        page.evaluate('window.scrollTo(0, document.body.scrollHeight * {})'.format(_ / 2))
                        time.sleep(1)
                    
                    # Get the page content
                    content = page.content()
                    soup = BeautifulSoup(content, 'html.parser')

                    # Extract profile information
                    profile_info = self._extract_profile_info(soup)

                except Exception as e:
                    print(f"Debug: Error during page navigation/loading: {str(e)}")
                    return f"Error during page loading: {str(e)}"
                finally:
                    # Always close the browser
                    browser.close()

                return self._format_profile_info(profile_info)

        except Exception as e:
            print(f"Debug: Error in browser setup: {str(e)}")
            return f"Error accessing LinkedIn profile: {str(e)}"

    def _extract_profile_info(self, soup):
        """Extract profile information from BeautifulSoup object."""
        try:
            # Basic profile information - trying multiple possible selectors
            name = (
                soup.find('h1', {'class': 'text-heading-xlarge'}) or
                soup.find('h1', {'class': 'top-card-layout__title'}) or
                soup.find('h1', {'class': 'inline t-24 t-black t-normal break-words'})
            )
            name = name.text.strip() if name else "Name not found"

            headline = (
                soup.find('div', {'class': 'text-body-medium'}) or
                soup.find('div', {'class': 'top-card-layout__headline'}) or
                soup.find('div', {'class': 'text-body-large'})
            )
            headline = headline.text.strip() if headline else "No headline available"

            # Experience section - trying multiple possible selectors
            exp_section = (
                soup.find('section', {'id': 'experience-section'}) or
                soup.find('div', {'id': 'experience'}) or
                soup.find('section', {'class': 'experience-section'})
            )
            experiences = []
            if exp_section:
                exp_items = (
                    exp_section.find_all('li', {'class': 'artdeco-list__item'}) or
                    exp_section.find_all('div', {'class': 'experience-item'}) or
                    exp_section.find_all('div', {'class': 'pv-entity__position-group'})
                )
                for item in exp_items:
                    title = (
                        item.find('span', {'class': 'mr1'}) or
                        item.find('h3', {'class': 't-16'}) or
                        item.find('h3', {'class': 'pv-entity__summary-info__title'})
                    )
                    company = (
                        item.find('span', {'class': 't-14'}) or
                        item.find('p', {'class': 'pv-entity__secondary-title'}) or
                        item.find('p', {'class': 'experience-item__subtitle'})
                    )
                    if title or company:
                        experiences.append({
                            'title': title.text.strip() if title else "Unknown Position",
                            'company': company.text.strip() if company else "Unknown Company"
                        })

            # Education section - trying multiple possible selectors
            edu_section = (
                soup.find('section', {'id': 'education-section'}) or
                soup.find('div', {'id': 'education'}) or
                soup.find('section', {'class': 'education-section'})
            )
            education = []
            if edu_section:
                edu_items = (
                    edu_section.find_all('li', {'class': 'artdeco-list__item'}) or
                    edu_section.find_all('div', {'class': 'education-item'}) or
                    edu_section.find_all('div', {'class': 'pv-education-entity'})
                )
                for item in edu_items:
                    school = (
                        item.find('span', {'class': 'mr1'}) or
                        item.find('h3', {'class': 'pv-entity__school-name'}) or
                        item.find('h3', {'class': 't-16'})
                    )
                    degree = (
                        item.find('span', {'class': 't-14'}) or
                        item.find('p', {'class': 'pv-entity__degree-name'}) or
                        item.find('p', {'class': 'education-item__subtitle'})
                    )
                    if school:
                        education.append({
                            'school': school.text.strip(),
                            'degree': degree.text.strip() if degree else "Degree not specified"
                        })

            # Add debug information
            if not experiences and not education:
                print("Debug: No experiences or education found. Available sections:")
                for section in soup.find_all('section'):
                    print(f"Section ID: {section.get('id', 'No ID')} - Class: {section.get('class', 'No Class')}")

            return {
                'name': name,
                'headline': headline,
                'experiences': experiences,
                'education': education
            }
        except Exception as e:
            print(f"Debug: Error in profile extraction: {str(e)}")
            return {
                'name': "Error extracting profile",
                'headline': str(e),
                'experiences': [],
                'education': []
            }

    def _format_profile_info(self, profile_info):
        """Format the profile information into a readable string."""
        output = f"""
Profile Information for {profile_info['name']}:
{profile_info['headline']}

Experience:
"""
        if profile_info['experiences']:
            for exp in profile_info['experiences']:
                output += f"- {exp['title']} at {exp['company']}\n"
        else:
            output += "No experience information available\n"

        output += "\nEducation:\n"
        if profile_info['education']:
            for edu in profile_info['education']:
                output += f"- {edu['degree']} from {edu['school']}\n"
        else:
            output += "No education information available"

        return output 