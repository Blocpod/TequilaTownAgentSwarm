from pathlib import Path

from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import WebSearchTool
from openai.types.shared import Reasoning

from config import get_default_model, is_openai_provider
from shared_tools import ExecuteTool, FindTools, ManageConnections, SearchTools

_INSTRUCTIONS_PATH = Path(__file__).parent / "instructions.md"


def create_vip_upsell_agent() -> Agent:
    return Agent(
        name="VIP Upsell Agent",
        description="Premium experience, reservation, and hosted-offer specialist for TequilaTown.",
        instructions=_INSTRUCTIONS_PATH.read_text(encoding="utf-8"),
        tools=[WebSearchTool(), ManageConnections, SearchTools, FindTools, ExecuteTool],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Create a VIP upgrade offer for a birthday group.",
            "Draft a premium reservation follow-up.",
            "Identify upsell moments in the guest journey.",
        ],
    )
