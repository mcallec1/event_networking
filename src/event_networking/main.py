#!/usr/bin/env python
# src/event_networking/main.py
import sys
import os
from dotenv import load_dotenv
from event_networking.crew import EventNetworkingCrew
from pathlib import Path

def run():
    """
    Run the crew.
    """
    # Get absolute path to .env file
    project_root = Path(__file__).parent.parent.parent
    env_path = project_root / '.env'
    
    # Verify .env file exists
    if not env_path.exists():
        print(f"Error: .env file not found at {env_path}")
        sys.exit(1)
        
    # Load environment variables
    load_dotenv(dotenv_path=env_path, override=True)
    
    # Debug information
    print(f".env file location: {env_path}")
    print(f"File exists: {env_path.exists()}")
    print(f"File contents readable: {env_path.is_file()}")
    
    api_key = os.getenv('OPENAI_API_KEY')
    model = os.getenv('MODEL')
    
    print(f"MODEL loaded: {'Yes' if model else 'No'} - Value: {model}")
    print(f"API KEY loaded: {'Yes' if api_key else 'No'} - Length: {len(api_key) if api_key else 0}")
    
    # Check if API key is set
    if not api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please add your OpenAI API key to the .env file")
        sys.exit(1)
        
    inputs = {
        'linkedInUrl': 'https://www.linkedin.com/in/swapnil-chhatre-221159162/'
    }
    
    try:
        EventNetworkingCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        print(f"Error running crew: {str(e)}")
        raise
    