from pathlib import Path

from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import WebSearchTool
from openai.types.shared import Reasoning

from config import get_default_model, is_openai_provider

_INSTRUCTIONS_PATH = Path(__file__).parent / "instructions.md"


def create_tour_guide() -> Agent:
    return Agent(
        name="Tour Guide",
        description="Wayfinding, floor navigation, room/station info, accessibility, and timing specialist.",
        instructions=_INSTRUCTIONS_PATH.read_text(encoding="utf-8"),
        tools=[WebSearchTool()],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Build a 60-minute route for a first-time guest.",
            "Answer a venue navigation question.",
            "Plan an accessible route between themed rooms.",
        ],
    )
