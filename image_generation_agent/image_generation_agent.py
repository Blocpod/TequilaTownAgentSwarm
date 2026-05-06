from agency_swarm import Agent, ModelSettings
from agency_swarm.tools import LoadFileAttachment
from openai.types.shared.reasoning import Reasoning
from shared_tools import CopyFile

from config import get_default_model, is_openai_provider


def create_image_generation_agent() -> Agent:
    return Agent(
        name="Image Agent",
        description="TequilaTown image specialist for campaign visuals, lifestyle images, ad creative, and art assets.",
        instructions="instructions.md",
        tools_folder="./tools",
        tools=[LoadFileAttachment, CopyFile],
        model=get_default_model(),
        model_settings=ModelSettings(
            reasoning=Reasoning(summary="auto", effort="medium") if is_openai_provider() else None,
            truncation="auto",
        ),
        conversation_starters=[
            "Generate a premium TequilaTown campaign visual.",
            "Edit this event photo into a cinematic sponsor asset.",
            "Create social ad variants for a Miami tequila experience.",
            "Combine these references into a polished TequilaTown creative.",
        ],
    )


if __name__ == "__main__":
    from agency_swarm import Agency
    Agency(create_image_generation_agent()).terminal_demo()
