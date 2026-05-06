import os
from agency_swarm import Agent, ModelSettings
from openai.types.shared.reasoning import Reasoning
from agency_swarm.tools import (
    WebSearchTool,
    PersistentShellTool,
    IPythonInterpreter,
    LoadFileAttachment,
)
from shared_tools import CopyFile, ExecuteTool, FindTools, ManageConnections, SearchTools

from config import get_default_model, is_openai_provider

current_dir = os.path.dirname(os.path.abspath(__file__))
instructions_path = os.path.join(current_dir, "instructions.md")

def create_data_analyst() -> Agent:
    return Agent(
        name="Analytics Agent",
        description="TequilaTown analytics specialist for KPIs, dashboards, guest behavior, revenue, flow, sentiment, and sponsor intelligence.",
        instructions=instructions_path,
        tools_folder=os.path.join(current_dir, "tools"),
        model=get_default_model(),
        tools=[
            WebSearchTool(),
            PersistentShellTool,
            IPythonInterpreter,
            LoadFileAttachment,
            CopyFile,
            ExecuteTool,
            FindTools,
            ManageConnections,
            SearchTools,
        ],
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
            truncation="auto",
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Analyze guest flow and conversion by room.",
            "Create a dashboard from ticket, check-in, and sales data.",
            "Summarize sponsor engagement KPIs.",
            "Find sentiment patterns in guest feedback.",
        ],
    )
