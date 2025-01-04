from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import random
from datetime import datetime, timedelta

class LinkedInProfileInput(BaseModel):
    """Input schema for LinkedInProfileTool."""
    linkedin_url: str = Field(
        ..., 
        description="A placeholder URL - not used for actual profile generation"
    )

class LinkedInProfileTool(BaseTool):
    name: str = "Profile Generator"
    description: str = (
        "A tool for generating realistic professional profiles with detailed "
        "information about experience, education, and skills."
    )
    args_schema: Type[BaseModel] = LinkedInProfileInput

    # Sample data for random generation
    _first_names = ["Alex", "Jordan", "Taylor", "Morgan", "Casey", "Sam", "Jamie", "Robin", "Pat", "Drew", 
                   "Chris", "Avery", "Quinn", "Riley", "Sydney"]
    _last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", 
                  "Martinez", "Lee", "Wang", "Kim", "Singh", "Patel"]
    _companies = ["TechCorp Solutions", "DataFlow Systems", "Cloud Dynamics", "AI Innovations", 
                 "Digital Frontier", "Future Technologies", "Smart Systems", "Tech Giants",
                 "Data Dynamics", "Quantum Computing Inc"]
    _positions = ["Software Engineer", "Data Scientist", "Product Manager", "DevOps Engineer", 
                 "Full Stack Developer", "ML Engineer", "System Architect", "Cloud Engineer",
                 "Technical Lead", "Research Scientist"]
    _locations = ["San Francisco, CA", "New York, NY", "Seattle, WA", "Austin, TX", "Boston, MA",
                 "Chicago, IL", "Los Angeles, CA", "Denver, CO", "Portland, OR", "Atlanta, GA"]
    _skills = ["Python", "JavaScript", "React", "AWS", "Docker", "Kubernetes", "Machine Learning",
              "SQL", "Node.js", "Git", "CI/CD", "Java", "Go", "TypeScript", "MongoDB"]
    _universities = ["Stanford University", "MIT", "UC Berkeley", "Georgia Tech", "Carnegie Mellon",
                    "University of Washington", "UCLA", "University of Michigan", "Cornell", "CalTech"]
    _degrees = ["Bachelor of Science in Computer Science", "Master of Science in Software Engineering",
                "Bachelor of Engineering", "Master of Computer Science", "Ph.D. in Computer Science",
                "Master of Science in Data Science", "Bachelor of Science in Information Technology"]
    _certifications = ["AWS Certified Solutions Architect", "Google Cloud Professional", "Azure Solutions Expert",
                      "Certified Kubernetes Administrator", "CompTIA Security+", "Certified Scrum Master",
                      "TensorFlow Developer Certificate", "MongoDB Certified Developer"]

    def _generate_duration(self, start_year):
        end_year = min(start_year + random.randint(1, 4), datetime.now().year)
        if end_year == datetime.now().year:
            return f"{start_year} - Present"
        return f"{start_year} - {end_year}"

    def _generate_experience(self):
        experiences = []
        current_year = datetime.now().year
        start_year = current_year - random.randint(1, 8)
        
        for _ in range(random.randint(2, 3)):
            company = random.choice(self._companies)
            position = random.choice(self._positions)
            duration = self._generate_duration(start_year)
            experiences.append(f"- {position} at {company} ({duration})")
            start_year -= random.randint(2, 4)
        
        return experiences

    def _generate_education(self):
        education = []
        current_year = datetime.now().year
        start_year = current_year - random.randint(5, 10)
        
        for _ in range(random.randint(1, 2)):
            university = random.choice(self._universities)
            degree = random.choice(self._degrees)
            duration = f"{start_year - 4} - {start_year}"
            education.append(f"- {degree} from {university} ({duration})")
            start_year -= random.randint(2, 4)
        
        return education

    def _run(self, linkedin_url: str) -> str:
        # Generate random profile data
        full_name = f"{random.choice(self._first_names)} {random.choice(self._last_names)}"
        current_position = random.choice(self._positions)
        current_company = random.choice(self._companies)
        location = random.choice(self._locations)
        
        # Select random skills (5-8 skills)
        num_skills = random.randint(5, 8)
        skills = random.sample(self._skills, num_skills)
        
        # Generate experiences and education
        experiences = self._generate_experience()
        education = self._generate_education()
        
        # Select random certifications (2-3)
        num_certs = random.randint(2, 3)
        certifications = random.sample(self._certifications, num_certs)
        
        # Return formatted string that can be parsed by the task
        return f"""
Full Name: {full_name}
Current Position: {current_position}
Current Company: {current_company}
Location: {location}
Industry: Technology

Professional Skills:
{', '.join(skills)}

Work Experience:
{chr(10).join(experiences)}

Education:
{chr(10).join(education)}

Certifications:
{chr(10).join('- ' + cert for cert in certifications)}
""" 