from pathlib import Path

from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import WebSearchTool
from openai.types.shared import Reasoning

from config import get_default_model, is_openai_provider
from shared_tools import ExecuteTool, FindTools, ManageConnections, SearchTools

_INSTRUCTIONS_PATH = Path(__file__).parent / "instructions.md"


def create_crm_lead_capture_agent() -> Agent:
    return Agent(
        name="CRM and Lead Capture",
        description="Guest profile, preference, consent, lead capture, and sponsor data specialist.",
        instructions=_INSTRUCTIONS_PATH.read_text(encoding="utf-8"),
        tools=[WebSearchTool(), ManageConnections, SearchTools, FindTools, ExecuteTool],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Design a consent-aware lead capture flow.",
            "Segment guests by tasting preferences.",
            "Prepare sponsor-safe lead fields.",
        ],
    )
