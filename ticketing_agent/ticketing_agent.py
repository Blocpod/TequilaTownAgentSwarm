from pathlib import Path

from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import WebSearchTool
from openai.types.shared import Reasoning

from config import get_default_model, is_openai_provider
from shared_tools import CopyFile, ExecuteTool, FindTools, ManageConnections, SearchTools

_INSTRUCTIONS_PATH = Path(__file__).parent / "instructions.md"


def create_ticketing_agent() -> Agent:
    return Agent(
        name="Ticketing Agent",
        description="Admissions, upgrades, package, group sales, and Tixr support specialist.",
        instructions=_INSTRUCTIONS_PATH.read_text(encoding="utf-8"),
        tools=[WebSearchTool(), ManageConnections, SearchTools, FindTools, ExecuteTool, CopyFile],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Help a guest pick the right ticket package.",
            "Draft a group sales reply.",
            "Troubleshoot a Tixr ticketing question.",
        ],
    )
