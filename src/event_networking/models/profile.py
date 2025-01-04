from typing import List
from pydantic import BaseModel

class WorkExperience(BaseModel):
    """Model for work experience information"""
    company: str
    title: str
    duration: str

class Education(BaseModel):
    """Model for education information"""
    institution: str
    degree: str
    years: str

class UserProfile(BaseModel):
    """Model for the complete user profile"""
    full_name: str
    current_position: str
    current_company: str
    location: str
    industry: str
    skills: List[str]
    experiences: List[WorkExperience]
    education: List[Education]
    certifications: List[str] 