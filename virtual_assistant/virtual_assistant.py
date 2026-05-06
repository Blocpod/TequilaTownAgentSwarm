from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import (
    WebSearchTool,
    PersistentShellTool,
    IPythonInterpreter,
)
from openai.types.shared import Reasoning
from dotenv import load_dotenv

from config import get_default_model, is_openai_provider
from shared_tools import CopyFile, ExecuteTool, FindTools, ManageConnections, SearchTools

load_dotenv()

# Class-level rename — idempotent, safe to run once at import time.
IPythonInterpreter.__name__ = "ProgrammaticToolCalling"


def create_virtual_assistant() -> Agent:
    return Agent(
        name="Guest Concierge",
        description="TequilaTown guest support, hospitality, FAQs, escalation, and external-system specialist.",
        instructions="./instructions.md",
        files_folder="./files",
        tools_folder="./tools",
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        tools=[
            WebSearchTool(),
            PersistentShellTool,
            IPythonInterpreter,
            CopyFile,
            ExecuteTool,
            FindTools,
            ManageConnections,
            SearchTools,
        ],
        conversation_starters=[
            "Answer a guest FAQ about TequilaTown.",
            "Draft a hospitality reply to a VIP guest.",
            "Summarize connected guest support systems.",
            "Create a staff escalation note for a guest issue.",
        ],
    )


if __name__ == "__main__":
    from agency_swarm import Agency
    Agency(create_virtual_assistant()).terminal_demo()
