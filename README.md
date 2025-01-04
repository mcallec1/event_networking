# EventNetworking Crew

Welcome to the EventNetworking Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:

```bash
crewai install
```

### Additional Setup for LinkedIn Integration

The project includes LinkedIn profile scraping functionality. To set this up:

1. Install the required packages:

```bash
uv pip install playwright beautifulsoup4
```

2. Install Playwright's browser (only needs to be done once):

```bash
playwright install chromium
```

3. Configure your LinkedIn credentials in the `.env` file:

```
LINKEDIN_EMAIL=your-linkedin-email
LINKEDIN_PASSWORD=your-linkedin-password
```

Note: The LinkedIn scraping functionality works both locally and in cloud environments like Google IDX. No additional system dependencies are required.

### System Dependencies

This project requires certain system libraries for web automation features. Install them using your system's package manager:

On macOS (using Homebrew):

```bash
brew install glib nss nspr libxcb
```

On Ubuntu/Debian:

```bash
sudo apt-get install libglib2.0-0 libnss3 libnssutil3 libnspr4 libxcb1
```

On Fedora/RHEL:

```bash
sudo dnf install glib2 nss nspr libxcb
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/event_networking/config/agents.yaml` to define your agents
- Modify `src/event_networking/config/tasks.yaml` to define your tasks
- Modify `src/event_networking/crew.py` to add your own logic, tools and specific args
- Modify `src/event_networking/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the event_networking Crew, assembling the agents and assigning them tasks as defined in your configuration.

### Using the LinkedIn Integration

The LinkedIn tool allows you to fetch profile information from LinkedIn. Here's how it works:

1. Make sure you've completed the LinkedIn setup steps above
2. The tool will automatically handle browser automation and login
3. You can provide LinkedIn profile URLs to the tool for information extraction
4. The tool works in headless mode, so no browser window will be visible
5. Rate limiting is implemented to avoid being blocked by LinkedIn

Note: Please be mindful of LinkedIn's terms of service regarding data scraping.

## Understanding Your Crew

The event_networking Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the EventNetworking Crew or crewAI.

- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
