from pathlib import Path

from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import WebSearchTool
from openai.types.shared import Reasoning

from config import get_default_model, is_openai_provider

_INSTRUCTIONS_PATH = Path(__file__).parent / "instructions.md"


def create_ai_chef() -> Agent:
    return Agent(
        name="AI Chef",
        description="Food pairing, flavor note, menu guidance, and dietary support specialist for TequilaTown.",
        instructions=_INSTRUCTIONS_PATH.read_text(encoding="utf-8"),
        tools=[WebSearchTool()],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Pair tonight's tasting room tequilas with small bites.",
            "Create dietary-safe menu language for guest concierge.",
            "Explain how agave flavor notes work with citrus, spice, and smoke.",
        ],
    )
