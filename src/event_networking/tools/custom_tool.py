from typing import Type, Dict
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import os

class MarkdownWriterInput(BaseModel):
    content: str = Field(description="The content to write to the markdown file")
    filename: str = Field(description="The name of the markdown file (without .md extension)")
    my_profile: dict = Field(description="Your LinkedIn profile information")
    contact_profile: dict = Field(description="Contact's LinkedIn profile information")
    event_info: dict = Field(description="Event information")

class MessageFormatter:
    def __init__(self, my_profile: Dict, contact_profile: Dict, event_info: Dict):
        self.my_profile = my_profile
        self.contact_profile = contact_profile
        self.event_info = event_info

    def format_message(self) -> str:
        # Get the required information from the profiles
        contact_name = self.contact_profile.get('name', '')
        contact_position = self.contact_profile.get('current_position', '')
        contact_company = self.contact_profile.get('company', '')
        event_name = self.event_info.get('title', '')
        event_date = self.event_info.get('date', '')
        my_name = self.my_profile.get('name', '')
        my_position = self.my_profile.get('current_position', '')
        my_company = self.my_profile.get('company', '')
        my_linkedin = self.my_profile.get('profile_url', '')
        my_email = self.my_profile.get('email', '')

        # Format the message with actual information
        message = f"""# Connection Message for {contact_name} - {event_name}

## LinkedIn Connection Request

Hi {contact_name},

I noticed we'll both be attending {event_name} {f"on {event_date}" if event_date else ""}. As a fellow {contact_position} at {contact_company}, I'd love to connect and share insights about our industry.

Best regards,
{my_name}
{my_position} at {my_company}

## Follow-up Email Draft

Subject: Great connecting at {event_name}

Dear {contact_name},

I hope this email finds you well. I'm {my_name}, {my_position} at {my_company}, and we recently connected on LinkedIn regarding {event_name}.

I'd love to schedule some time to discuss our shared interests in the industry and explore potential collaboration opportunities.

Best regards,
{my_name}
{my_position}
{my_company}
{my_email}
LinkedIn: {my_linkedin}
"""
        return message

class MarkdownWriterTool(BaseTool):
    name: str = "Markdown Writer"
    description: str = "Writes formatted content to a markdown file in the project's messages directory"
    input_schema: Type[BaseModel] = MarkdownWriterInput

    def _run(self, content: str, filename: str, my_profile: dict, contact_profile: dict, event_info: dict) -> str:
        try:
            # Create message formatter and generate content
            formatter = MessageFormatter(my_profile, contact_profile, event_info)
            formatted_content = formatter.format_message()

            # Create messages directory if it doesn't exist
            messages_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "messages")
            os.makedirs(messages_dir, exist_ok=True)

            # Create the full file path
            file_path = os.path.join(messages_dir, f"{filename}.md")

            # Write the formatted content to the markdown file
            with open(file_path, 'w') as f:
                f.write(formatted_content)

            return f"Successfully wrote message to {file_path}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
