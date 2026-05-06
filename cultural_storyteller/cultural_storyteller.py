from pathlib import Path

from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import WebSearchTool
from openai.types.shared import Reasoning

from config import get_default_model, is_openai_provider

_INSTRUCTIONS_PATH = Path(__file__).parent / "instructions.md"


def create_cultural_storyteller() -> Agent:
    return Agent(
        name="Cultural Storyteller",
        description="Culturally respectful storytelling specialist for Mexico, agave, ritual, craft, art, and music.",
        instructions=_INSTRUCTIONS_PATH.read_text(encoding="utf-8"),
        tools=[WebSearchTool()],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="high", summary="auto") if is_openai_provider() else None,
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Write a respectful agave education moment for guests.",
            "Create room copy about tequila heritage and craft.",
            "Fact-check a cultural storytelling script.",
        ],
    )
