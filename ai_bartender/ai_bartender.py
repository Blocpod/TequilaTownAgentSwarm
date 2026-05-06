from pathlib import Path

from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import WebSearchTool
from openai.types.shared import Reasoning

from config import get_default_model, is_openai_provider

_INSTRUCTIONS_PATH = Path(__file__).parent / "instructions.md"


def create_ai_bartender() -> Agent:
    return Agent(
        name="AI Bartender",
        description="TequilaTown beverage specialist for tequila, cocktail, tasting, and sponsor-brand recommendations.",
        instructions=_INSTRUCTIONS_PATH.read_text(encoding="utf-8"),
        tools=[WebSearchTool()],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Recommend a tasting path for a first-time tequila guest.",
            "Pair sponsor tequilas with guest flavor preferences.",
            "Create responsible cocktail talking points for tonight's bartenders.",
        ],
    )
