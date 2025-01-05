#!/usr/bin/env python
# src/event_networking/main.py
import sys
import os
from dotenv import load_dotenv
from event_networking.crew import EventNetworkingCrew

def run():
    """
    Run the crew.
    """
    # Load environment variables
    load_dotenv()
    
    # Check if API key is set
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please add your OpenAI API key to the .env file")
        sys.exit(1)
        
    inputs = {
        'my_linkedin_url': 'https://www.linkedin.com/in/my-profile/',
        'contact_linkedin_url': 'https://www.linkedin.com/in/contact-profile/',  # Replace with actual contact URL
        'event_url': 'https://www.aicamp.ai/event/eventdetails/W2025010100/'  # Replace with actual event URL
    }
    
    try:
        EventNetworkingCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        print(f"Error running crew: {str(e)}")
        raise
    