from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import WebSearchTool, IPythonInterpreter
from openai.types.shared import Reasoning
from virtual_assistant.tools.ScholarSearch import ScholarSearch

from config import get_default_model, is_openai_provider


def create_deep_research() -> Agent:
    return Agent(
        name="Research Agent",
        description="Research specialist for trends, competitors, tequila culture, event benchmarks, and activation research.",
        instructions="./instructions.md",
        files_folder="./files",
        tools=[WebSearchTool(), ScholarSearch, IPythonInterpreter],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="high", summary="auto") if is_openai_provider() else None,
            response_include=["web_search_call.action.sources"] if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Research immersive nightlife and experiential event trends.",
            "Compare Miami experience competitors and sponsor opportunities.",
            "Find tequila category trends for sponsor storytelling.",
            "Research best practices for event gamification and check-ins.",
        ],
    )
