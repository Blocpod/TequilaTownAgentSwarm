from agency_swarm import Agent, ModelSettings
from openai.types.shared import Reasoning
from dotenv import load_dotenv

from config import get_default_model, is_openai_provider

load_dotenv()


def create_orchestrator() -> Agent:
    return Agent(
        name="Orchestrator",
        description=(
            "Master Orchestrator for TequilaTown Miami that routes guest experience, commerce, "
            "operations, insights, and creative workflows to the right specialist agents."
        ),
        instructions="./instructions.md",
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(effort="medium", summary="auto") if is_openai_provider() else None,
        ),
        conversation_starters=[
            "Plan today's TequilaTown guest experience and ops priorities.",
            "Create a sponsor recap with analytics, slides, docs, and creative assets.",
            "Build a VIP upsell campaign for this weekend's Miami guests.",
            "Summarize guest feedback and route fixes to the right teams.",
        ],
    )


if __name__ == "__main__":
    from agency_swarm import Agency
    Agency(create_orchestrator()).terminal_demo()
