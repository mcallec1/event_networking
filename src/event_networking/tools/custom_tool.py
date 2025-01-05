from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import os

class MarkdownWriterInput(BaseModel):
    content: str = Field(description="The content to write to the markdown file")
    filename: str = Field(description="The name of the markdown file (without .md extension)")

class MarkdownWriterTool(BaseTool):
    name: str = "Markdown Writer"
    description: str = "Writes formatted content to a markdown file in the project's messages directory"
    input_schema: Type[BaseModel] = MarkdownWriterInput

    def _run(self, content: str, filename: str) -> str:
        # Create messages directory if it doesn't exist
        messages_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "messages")
        os.makedirs(messages_dir, exist_ok=True)

        # Create the full file path
        file_path = os.path.join(messages_dir, f"{filename}.md")

        # Write the content to the markdown file
        with open(file_path, 'w') as f:
            f.write(content)

        return f"Successfully wrote message to {file_path}"
